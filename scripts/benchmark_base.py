""" This module contains the base class for all benchmark workflows. """
import json
import os
import re
from datetime import datetime
from PIL import Image

from simple_ai_clients import AiApiClient

class Benchmark:
    """ Base class for all benchmark workflows. """

    def __init__(self, name, benchmark_dir, provider, model, api_key, role_description):
        """ Initialize the benchmark. """

        self.name = name
        self.benchmark_dir = benchmark_dir
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.role_description = role_description
        self.prompt = self.load_prompt()
        self.client = AiApiClient(api=self.provider,
                                  api_key=self.api_key,
                                  gpt_role_description=self.role_description)

    def load_prompt(self):
        """ Load the prompt from the benchmark directory. """
        prompt_path = os.path.join(self.benchmark_dir, 'prompt.txt')
        with open(prompt_path, 'r') as f:
            return f.read()

    @staticmethod
    def resize_image(image_path, max_size=(1024, 1024)):
        img = Image.open(image_path)
        img.thumbnail(max_size)

        # Correctly build resized filename
        directory, filename = os.path.split(image_path)
        name, ext = os.path.splitext(filename)
        resized_filename = f"{name}_small{ext}"
        resized_path = os.path.join(directory, resized_filename)

        # Save resized image
        img.save(resized_path, optimize=True, quality=85)
        return resized_path

    def ask_llm(self, image_paths):
        self.client.clear_image_resources()

        if self.resize_images():
            image_paths = [self.resize_image(image_path) for image_path in image_paths]

        for image_path in image_paths:
            self.client.add_image_resource(image_path)

        return self.client.prompt(model=self.model,
                                  prompt=self.prompt)

    def save_answer(self, image_name, answer):
        date_str = datetime.now().strftime('%Y-%m-%d')
        save_path = os.path.join(self.benchmark_dir, 'answers', date_str)
        os.makedirs(save_path, exist_ok=True)

        test_id = f"{self.provider}_{self.model}".replace('-', '_')
        file_name = f"{self.get_image_base_name(image_name)}_{test_id}.{self.get_output_format()}"

        with open(os.path.join(save_path, file_name), 'w', encoding='utf-8') as f:
            json.dump(answer, f)

    def prepare_scoring_data(self, image_name, answer):
        if "response_text" in answer:
            response_text = answer["response_text"]
            if self.convert_result_to_json() and response_text.startswith("```json"):
               json_text = response_text[6:3]
               try:
                    return json.loads(json_text)
               except json.JSONDecodeError:
                    return {}
        return {}

    def score_answer(self, image_name, answer):
        return {"total": 0}

    def create_render(self, image_name, result):
        image_base_name = self.get_image_base_name(image_name)
        return f"| {image_base_name} |\n"

    def update_result_table(self, rendered_results):
        table_path = os.path.join(self.benchmark_dir, 'result_table.md')
        with open(table_path, 'w', encoding='utf-8') as f:
            f.write("| Image | Truth | Answer | Score |\n")
            f.write("|-------|-------|--------|-------|\n")
            f.writelines(rendered_results)

    def run(self):
        """Run the benchmark, supporting multi-image prompts."""
        images_dir = os.path.join(self.benchmark_dir, 'images')
        image_files = sorted(os.listdir(images_dir))

        rendered_results = []
        processed_images = set()

        # Group images by request
        image_groups = {}

        for image_file in image_files:
            if image_file in processed_images:
                continue

            match = re.match(self.get_page_part_regex(), image_file, re.IGNORECASE)
            if match:
                base_name = match.group(1)
                grouped_images = sorted([
                    img for img in image_files if img.startswith(base_name + '_p')
                ])
                image_groups[base_name] = grouped_images
                processed_images.update(grouped_images)
            else:
                image_name, _ = os.path.splitext(image_file)
                image_groups[image_name] = [image_file]
                processed_images.add(image_file)

        # Process each image group
        for request_id, img_files in image_groups.items():
            image_paths = [os.path.join(images_dir, img) for img in img_files]

            answer = self.ask_llm(image_paths)
            self.save_answer(request_id, answer)
            result = self.score_answer(request_id, answer)
            render = self.create_render(request_id, result)
            rendered_results.append(render)

        self.update_result_table(rendered_results)

    @staticmethod
    def convert_result_to_json():
        return True

    @staticmethod
    def resize_images():
        return True

    @staticmethod
    def get_page_part_regex():
        return r'(.+)_p\d+\.(jpg|jpeg|png)$'

    @staticmethod
    def get_output_format():
        return "json"

    @staticmethod
    def get_image_base_name(image_name):
        return os.path.splitext(image_name)[0]

    @property
    def title(self):
        return f"{self.name} ({self.provider}/{self.model})"

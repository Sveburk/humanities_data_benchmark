""" This module contains the base class for all benchmark workflows. """
import importlib
import json
import os
import re
import tempfile
from datetime import datetime
from PIL import Image

from scoring_helper import remove_none
from simple_ai_clients import AiApiClient

class Benchmark:
    """ Base class for all benchmark workflows. """

    def __init__(self, config, api_key, benchmark_directory):
        """ Initialize the benchmark. """

        self.id = config.get('id', None)
        self.name = config['name']
        self.benchmark_dir = benchmark_directory
        self.provider = config['provider']
        self.model = config['model']
        self.api_key = api_key
        self.role_description = config['role_description']
        self.prompt_file = config['prompt_file']
        self.prompt = self.load_prompt()
        self.request_render = ""
        self.dataclass_name = config['dataclass']
        self.dataclass = self.load_dataclass()

        kwargs = {
            "api": self.provider,
            "api_key": self.api_key,
            "gpt_role_description": self.role_description,
        }
        if self.dataclass:
            kwargs["dataclass"] = self.dataclass

        self.client = AiApiClient(**kwargs)

    def load_prompt(self) -> str:
        """ Load the prompt from the benchmark directory. """
        prompt_path = os.path.join(self.benchmark_dir, "prompts", self.prompt_file)
        with open(prompt_path, 'r') as f:
            prompt = f.read()
            if False:
                try:
                    kwargs = {}
                    prompt = prompt.format(**kwargs)
                except KeyError as e:
                    return prompt
            return prompt

    def load_dataclass(self) -> None | type:
        """ Dynamically load a dataclass from dataclass.py """
        class_name = self.dataclass_name
        if class_name is None or class_name == "default" or class_name == "":
            return None

        try:
            dataclass_module = importlib.import_module(f"benchmarks.{self.name}.dataclass")
            return getattr(dataclass_module, class_name)
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Could not load dataclass {class_name}: {e}")

    def load_ground_truth(self,
                          image_name: str) -> dict:
        """ Load the ground truth from the benchmark directory. """
        ground_truth_path = os.path.join(self.benchmark_dir, "ground_truths", f"{image_name}.json")
        try:
            with open(ground_truth_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    return {"error": "Ground truth file is empty."}
                return json.loads(content)
        except FileNotFoundError:
            return {"error": f"Ground truth not found: {image_name}"}
        except json.JSONDecodeError as e:
            return {"error": "Invalid JSON format."}

    @staticmethod
    def resize_image(image_path: str,
                     temp_dir: str,
                     max_size: tuple = (1024, 1024)) -> str:
        """ Resize an image to fit within the max size. """
        img = Image.open(image_path)
        img.thumbnail(max_size)

        filename = os.path.basename(image_path)
        resized_path = os.path.join(temp_dir, filename)

        img.save(resized_path, optimize=True, quality=85)
        return resized_path

    def ask_llm(self,
                image_paths: list[str]) -> dict:
        """ Ask the language model a question. """
        self.client.clear_image_resources()

        if self.resize_images:
            with tempfile.TemporaryDirectory() as temp_dir:
                resized_images = [
                    self.resize_image(image_path, temp_dir)
                    for image_path in image_paths
                ]

                for resized_image_path in resized_images:
                    self.client.add_image_resource(resized_image_path)

                return self.client.prompt(model=self.model, prompt=self.prompt)
        else:
            for image_path in image_paths:
                self.client.add_image_resource(image_path)

            return self.client.prompt(model=self.model, prompt=self.prompt)

    def save_answer(self,
                    image_name: str,
                    answer: dict) -> None:
        """ Save the answer to a file. """
        date_str = datetime.now().strftime('%Y-%m-%d')
        save_path = os.path.join(self.benchmark_dir, 'results', date_str)
        os.makedirs(save_path, exist_ok=True)

        file_name = f"{self.get_request_name(image_name)}.{self.get_output_format}"

        with open(os.path.join(save_path, file_name), 'w', encoding='utf-8') as f:
            json.dump(answer, f)

    def prepare_scoring_data(self,
                             answer: dict) -> dict:
        """ Prepare the data for scoring. """
        if "response_text" in answer:
            response_text = answer["response_text"]
            json_text = None
            if self.convert_result_to_json and "```json" in response_text:
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(1)

            if json_text is None:
                json_text = response_text

            if isinstance(json_text, dict):
                return json_text

            try:
                json_dict = json.loads(json_text)
                if self.remove_none_values:
                    return remove_none(json_dict)
                return json_dict
            except json.JSONDecodeError as e:
                return {"error": "Invalid JSON format."}

        return {"error": "No response text found."}

    def create_request_render(self,
                              image_name: str,
                              result: dict,
                              score: dict,
                              truth) -> str:
        return ""

    def save_render(self,
                    image_name: str,
                    render: str) -> None:
        self.request_render = render
        date_str = datetime.now().strftime('%Y-%m-%d')
        filename = f"{self.get_request_name(image_name)}.md"
        save_path = os.path.join(self.benchmark_dir, date_str, 'renders')
        os.makedirs(save_path, exist_ok=True)
        with open(os.path.join(save_path, filename), 'w', encoding='utf-8') as f:
            f.write(render)

    def run(self) -> dict:
        """Run the benchmark."""
        images_dir = os.path.join(self.benchmark_dir, 'images')
        image_files = sorted(os.listdir(images_dir))
        processed_images = set()

        # Update ground truth

        if self.update_required:
            self.update_ground_truth()

        # Group images by request
        image_groups = {}

        for image_file in image_files:
            if image_file in processed_images:
                continue

            match = re.match(self.get_page_part_regex, image_file, re.IGNORECASE)
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
        all_results = {}
        for request_id, img_files in image_groups.items():
            image_paths = [os.path.join(images_dir, img) for img in img_files]

            answer = self.ask_llm(image_paths)
            self.save_answer(request_id, answer)
            ground_truth = self.load_ground_truth(request_id)
            score = self.score_answer(request_id, answer, ground_truth)
            all_results[self.get_request_name(request_id)] = score
            render = self.create_request_render(request_id, answer, score, ground_truth)
            self.save_render(request_id, render)

        return all_results

    @staticmethod
    def get_image_base_name(image_name: str) -> str:
        return os.path.splitext(image_name)[0]

    def get_request_name(self,
                         image_name: str) -> str:
        if self.id is not None:
            return f"request_{self.id}"
        else:
            name = self.get_image_base_name(image_name) + f"_{self.provider}_{self.model}_{self.prompt_file}"
            name = name.replace(" ", "_").replace("-", "_").replace(".", "_")
        return name

    def score_answer(self,
                     image_name: str,
                     response: dict,
                     ground_truth: dict) -> dict:
        return {"total": 0}

    @property
    def remove_none_values(self) -> bool:
        """If True, remove None values from the response before scoring."""
        return True

    @property
    def convert_result_to_json(self) -> bool:
        """If the result is a JSON string, convert it to a JSON object."""
        return True

    @property
    def resize_images(self) -> bool:
        """If images are too large, resize them before sending to the model."""
        return False

    @property
    def get_page_part_regex(self) -> str:
        """If multiple images are part of a single request, this regex will match the base name."""
        return r'(.+)_p\d+\.(jpg|jpeg|png)$'

    @property
    def get_output_format(self) -> str:
        """Files saved in <benchmark>/results/ will be saved in this format."""
        return "json"

    @property
    def title(self) -> str:
        """Title of the benchmark. Used in the result table."""
        return f"{self.name} ({self.provider}/{self.model})"

    @property
    def update_required(self) -> bool:

        """ If an update of the ground truth is required before running the benchmark. """

        return False

    @staticmethod
    def update_ground_truth() -> None:

        """ Update the ground truth. """

        return None

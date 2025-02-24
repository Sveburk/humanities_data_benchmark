import os
from simple_ai_clients import AiApiClient

class Benchmark:
    def __init__(self, name, benchmark_dir, provider, model, api_key, role_description):
        self.name = name
        self.benchmark_dir = benchmark_dir
        self.provider = provider
        self.model = model
        self.api_key = api_key
        self.prompt = self.load_prompt()
        self.client = AiApiClient(api=self.provider,
                                  api_key=self.model,
                                  gpt_role_description=)

    def load_prompt(self):
        prompt_path = os.path.join(self.benchmark_dir, 'prompt.txt')
        with open(prompt_path, 'r') as f:
            return f.read()

    def ask_llm(self, image):
        # Generic implementation
        response = self.client.ask(image=image, prompt=self.prompt)
        return response

    def save_answer(self, image_name, answer):
        save_path = os.path.join(self.benchmark_dir, 'answers')
        os.makedirs(save_path, exist_ok=True)
        with open(os.path.join(save_path, f"{image_name}.txt"), 'w') as f:
            f.write(answer)

    def score_answer(self, image_name, answer):
        # Generic scoring logic
        truth_path = os.path.join(self.benchmark_dir, 'truths', f"{image_name}.txt")
        with open(truth_path, 'r') as f:
            truth = f.read().strip()
        return {"score": answer.strip() == truth, "truth": truth, "answer": answer.strip()}

    def create_render(self, image_name, result):
        # Generic render creation
        return f"| {image_name} | {result['truth']} | {result['answer']} | {result['score']} |\n"

    def update_result_table(self, rendered_results):
        table_path = os.path.join(self.benchmark_dir, 'result_table.md')
        with open(table_path, 'w') as f:
            f.write("| Image | Truth | Answer | Score |\n")
            f.write("|-------|-------|--------|-------|\n")
            f.writelines(rendered_results)

    def run(self):
        images_dir = os.path.join(self.benchmark_dir, 'images')
        rendered_results = []

        for image_file in os.listdir(images_dir):
            image_path = os.path.join(images_dir, image_file)
            answer = self.ask_llm(image_path)
            self.save_answer(image_file, answer)
            result = self.score_answer(image_file, answer)
            render = self.create_render(image_file, result)
            rendered_results.append(render)

        self.update_result_table(rendered_results)

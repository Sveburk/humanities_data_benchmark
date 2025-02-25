from scripts.benchmark_base import Benchmark

class BibliographicData(Benchmark):

    def score_answer(self, image_name, response, ground_truth):
        data = self.prepare_scoring_data(response)
        return {"score": 66}

    def create_request_render(self, image_name, result, score, truth):
        render = f"""
## Result for image: {image_name}

### Prompt:
{self.load_prompt()}

### Response:
{result['response_text']}

### Ground Truth:
{truth}"""

        return render
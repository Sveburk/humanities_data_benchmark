from scripts.benchmark_base import Benchmark

class TestBenchmark2(Benchmark):

    def score_answer(self, image_name, response, ground_truth):
        data = self.prepare_scoring_data(response)
        print(data)
        print("-------------------------------")
        print(ground_truth)
        return {"score": 66}
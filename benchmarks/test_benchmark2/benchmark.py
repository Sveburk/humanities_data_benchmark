import os

from scripts.benchmark_base import Benchmark


class TestBenchmark2(Benchmark):

    def score_answer(self, image_name, answer):
        data = self.prepare_scoring_data(image_name, answer)
        print(data)
        return {"score": 66}
from scripts.benchmark_base import Benchmark
from scripts.scoring_helper import get_all_keys, get_nested_value, calculate_fuzzy_score


class BibliographicData(Benchmark):

    def score_benchmark(self, all_scores):
        total_score = 0
        for score in all_scores:
            print(">>>>", score['fuzzy'])
            total_score += score['fuzzy']

        #return {"fuzzy": total_score / len(all_scores)}
        return {"fuzzy": total_score / len(all_scores)}

    def score_request_answer(self, image_name, response, ground_truth):
        data = self.prepare_scoring_data(response)

        my_keys = get_all_keys(ground_truth)

        avg_score = 0
        for k in my_keys:
            test_value = get_nested_value(data, k)
            gold_value = get_nested_value(ground_truth, k)
            score = calculate_fuzzy_score(test_value, gold_value)
            avg_score += score
        avg_score /= len(my_keys)
        return {"fuzzy": avg_score}

    def create_request_render(self, image_name, result, score, truth):
        data = self.prepare_scoring_data(result)
        my_keys = get_all_keys(truth)
        avg_score = 0
        md_table_body = ""
        for k in my_keys:
            test_value = get_nested_value(data, k)
            gold_value = get_nested_value(truth, k)
            score = calculate_fuzzy_score(test_value, gold_value)
            avg_score += score
            md_table_body += f"\n| {k} | {test_value} | {gold_value} | {score} |"
        avg_score /= len(my_keys)

        render = (
            f"### Result for image: {image_name}\n"
            f"Average Fuzzy Score: **{avg_score}**\n"
            "<small>\n\n"
            f"| Key | Value | Ground Truth | Score |\n"
            f"| --- | --- | --- | --- |"
            f"{md_table_body}\n\n"
            "</small>\n"
        )

        return render
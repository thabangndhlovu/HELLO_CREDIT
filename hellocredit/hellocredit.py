class CreditRatingCalculator:
    def __init__(self, metrics):
        self.metrics = metrics

    def _calculate_metric_score(self, metric, thresholds, inverse):
        for score, (lower, upper) in enumerate(thresholds, start=1):
            if (inverse and metric <= upper) or (not inverse and metric >= lower):
                return score
        return len(thresholds) // 2  # else return the middle score

    def _calculate_category_score(self, category_metrics, ratios):
        total_weighted_score = 0
        for metric_name, metric_data in category_metrics["metrics"].items():
            value = ratios[metric_name]
            score = self._calculate_metric_score(
                value, metric_data.thresholds, metric_data.lower_is_better
            )
            weight = category_metrics["metric_weights"][metric_name]
            total_weighted_score += score * weight
        return total_weighted_score

    def _calculate_scores(self, ratios):
        scores = {}
        for category, category_data in self.metrics.items():
            category_score = self._calculate_category_score(category_data, ratios[category])
            scores[category] = category_score
        return scores

    def _calculate_weighted_score(self, scores):
        weights = {
            category: category_data["class_weight"]
            for category, category_data in self.metrics.items()
        }
        return sum(scores[category] * weight for category, weight in weights.items())

    def _determine_credit_rating(self, weighted_score):
        credit_ratings = {
            "Aaa": 2.5,
            "Aa": 3.5,
            "A": 4.5,
            "Baa": 5.5,
            "Ba": 6.5,
            "B": 7.5,
            "Caa": 8.5,
            "Ca": 9.5,
            "C": float("inf")
        }
        return next(rating for rating, threshold in credit_ratings.items() if weighted_score <= threshold)

    def calculate_credit_rating(self, ratios):
        self.scores = self._calculate_scores(ratios)
        self.credit_score = self._calculate_weighted_score(self.scores)
        self.credit_rating = self._determine_credit_rating(self.credit_score)
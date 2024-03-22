from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class CreditRatingCalculator:
    def __init__(self, metrics):
        self.metrics = metrics

    def _calculate_metric_score(self, metric, thresholds, inverse):
        for score, (lower, upper) in enumerate(thresholds, start=1):
            if (inverse and metric <= upper) or (not inverse and metric >= lower):
                return score
        return len(thresholds) // 2 # else return the middle score

    def _calculate_category_score(self, category_metrics, ratios):
        total_weighted_score = 0

        for metric, weight in zip(
            category_metrics["metrics"].items(), category_metrics["weights"]
        ):
            metric_name, metric_data = metric
            value = ratios[metric_name]
            score = self._calculate_metric_score(
                value, metric_data["thresholds"], metric_data["lower_is_better"]
            )
            total_weighted_score += score * weight

        return total_weighted_score

    def _calculate_scores(self, ratios):
        scores = {}
        for category, category_data in self.metrics.items():
            category_score = self._calculate_category_score(category_data, ratios)
            scores[category] = category_score
        return scores

    def _calculate_weighted_score(self, scores):
        weights = {
            category: category_data["class_weight"]
            for category, category_data in self.metrics.items()
        }
        return sum(scores[category] * weight for category, weight in weights.items())

    def _determine_credit_rating(self, weighted_score):
        credit_ratings = [
            (1.5, "Aaa"),
            (2.5, "Aa"),
            (3.5, "A"),
            (4.5, "Baa"),
            (5.5, "Ba"),
            (6.5, "B"),
            (7.5, "Caa"),
            (8.5, "Ca"),
            (float("inf"), "C"),
        ]

        for threshold, rating in credit_ratings:
            if weighted_score < threshold:
                return rating

    def calculate_credit_rating(self, ratios):
        self.scores = self._calculate_scores(ratios)
        self.weighted_score = self._calculate_weighted_score(self.scores)
        self.credit_rating = self._determine_credit_rating(self.weighted_score)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate", response_class=HTMLResponse)
async def calculate(request: Request):
    form_data = await request.form()
    ratios = {
        'oper_margin': float(form_data['oper_margin']),
        'debt_to_equity': float(form_data['debt_to_equity']),
        'tot_debt_to_ebitda': float(form_data['tot_debt_to_ebitda']),
        'ebitda_to_tot_int_exp': float(form_data['ebitda_to_tot_int_exp']),
    }

    model = CreditRatingCalculator(metrics)
    model.calculate_credit_rating(ratios)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "scores": model.scores,
        "weighted_score": model.weighted_score,
        "credit_rating": model.credit_rating
    })

import os
import json
from functools import partial
from dataclasses import field, dataclass

import numpy as np
import pandas as pd

from hellocredit.utils import get_rating_meta
from hellocredit.helpers import MAPPED_RATINGS



@dataclass
class HelloCredit:
    input_dict: dict = field(default_factory=dict)
    
    def __post_init__(self):
        self.nested_dict = get_nested_dict(self.input_dict["file_path"])
        self.company_period_metrics = get_period_metrics(self.nested_dict)
        self.company_expected_metrics = get_expected_metrics(self.nested_dict)
        self.compute_rating = partial(calculate_credit_rating, metrics=self.input_dict["configuration"])
        self.work_dir = self.input_dict["work_directory"]
            
    def update_input_dict(self, input_dict: dict) -> dict:  
        def deep_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = deep_update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        self.input_dict = deep_update(self.input_dict, input_dict)
    
    
    def run_function(self) -> bool:
        
        # Expected and Single Period Calcs
        calculator_output = self.compute_rating(ratios=self.company_expected_metrics)
        rating_meta = get_rating_meta("Rating", calculator_output["credit_rating"])
        
        calculator_periods_output = {
            period: self.compute_rating(ratios=self.company_period_metrics[period])
            for period in self.company_period_metrics
        }
            
        # Bayesian Model
        model_output = bayesian_ridge_model(self.nested_dict, **self.input_dict["probabilistic_model"])
        model_output_transform = bayesian_ridge_transform(model_output)
        model_output_computed_rating = {
            period: self.compute_rating(ratios=model_output_transform[period]) 
            for period, metrics in enumerate(model_output_transform)
        }
        
        bayesian_model_output = {
            "model_output": model_output,
            "model_output_transform": model_output_transform,
            "computed_rating": model_output_computed_rating,
        }
        
        self.output_dict = {
            "rating_meta": rating_meta,
            "company_expected_metrics": self.company_expected_metrics,
            "company_period_metrics": self.company_period_metrics,
            "calculator_output": calculator_output,
            "calculator_periods_output": calculator_periods_output,
            "bayesian_model_output": bayesian_model_output,
        }
        
        files_to_dump = {
            "output_dict.json": self.output_dict,
            "input_dict.json": self.input_dict
        }

        for filename, data in files_to_dump.items():
            file_path = os.path.join(self.work_dir, filename)
            with open(file_path, "w") as f:
                json.dump(data, f)
                            
        return self.output_dict

   






def calculate_credit_rating(metrics, ratios):
    calculation_details = {"metrics": {}}

    def determine_credit_rating(score):
        for rating, threshold in MAPPED_RATINGS:
            if score <= threshold:
                return rating
        return len(MAPPED_RATINGS) // 2  # Return the middile rating if no threshold is met

    def calculate_metric_score(value, thresholds, lower_is_better):
        for score, (lower, upper) in enumerate(thresholds, start=1):
            if lower_is_better and value <= upper or not lower_is_better and value >= lower:
                return score
        return len(thresholds) // 2

    def calculate_category_score(category, category_data):
        category_ratios = ratios[category]
        metric_weights = category_data["metric_weights"]
        total_weighted_score = 0

        for metric_name, metric_data in category_data["metrics"].items():
            value = category_ratios[metric_name]
            score = calculate_metric_score(value, metric_data["thresholds"], metric_data["lower_is_better"])
            
            weight = metric_weights[metric_name]
            weighted_score = score * weight
            
            rating = determine_credit_rating(score)
            total_weighted_score += weighted_score
            calculation_details["metrics"][metric_name] = {
                "category": category,
                "value": value,
                "score": score,
                "weight": weight,
                "weighted_score": weighted_score,
                "rating": rating,
            }
        return total_weighted_score

    scores = {category: calculate_category_score(category, category_data)
              for category, category_data in metrics.items()}

    total_weighted_score = sum(
        scores[category] * category_data["class_weight"]
        for category, category_data in metrics.items()
    )
    total_weight = sum(category_data["class_weight"] for category_data in metrics.values())
    credit_score = total_weighted_score / total_weight
    credit_rating = determine_credit_rating(credit_score)

    calculation_details.update({
        "scores": scores,
        "credit_score": credit_score,
        "credit_rating": credit_rating,
    })
    
    return calculation_details


def get_expected_metrics(data, n=100):
    return {
        category: {metric: sum(values[-n:]) / min(len(values), n) 
                   for metric, values in metrics.items()}
        for category, metrics in data.items()
    }


def get_nested_dict(data):
    nested_dict = {}

    for (category, metric), values in data.iterrows():
        if category not in nested_dict:
            nested_dict[category] = {}
        nested_dict[category][metric] = values.tolist()

    return nested_dict


def get_nested_dict(file_path):
    
    data = pd.read_excel(file_path, index_col=[0, 1])
    nested_dict = {}

    for (category, metric), values in data.iterrows():
        if category not in nested_dict:
            nested_dict[category] = {}
        nested_dict[category][metric] = values.tolist()

    return nested_dict


def get_period_metrics(data):
    n = len(data['leverage_coverage_metrics']['debt_to_equity'])
    return {
        i: {
            category: {metric: values[i] 
            for metric, values in metrics.items()}
            for category, metrics in data.items()
        }
        for i in range(n)
    }


def bayesian_ridge_transform(data):
    list_length = len(next(iter(next(iter(data.values())).values())))
    return [
        {
            category: {
                metric: values[i] for metric, values in metrics.items()
            } for category, metrics in data.items()
        } for i in range(list_length)
    ]


def bayesian_ridge_model(metrics, periods=1, look_back_periods=5, max_iter=300, tol=1e-3):
    import numpy as np
    from sklearn.linear_model import BayesianRidge
    
    predictions = {}
    periods, look_back_periods, max_iter = abs(periods), abs(look_back_periods), abs(max_iter)
    
    for metric_group, values_dict in metrics.items():
        predictions[metric_group] = {}
        for metric, values in values_dict.items():
            
            recent_values = values[-look_back_periods:]
            X = np.arange(len(recent_values)).reshape(-1, 1)
            
            model = BayesianRidge(max_iter=max_iter, tol=tol).fit(X, recent_values)
            
            next_periods = np.arange(look_back_periods, look_back_periods + periods).reshape(-1, 1)
            predictions[metric_group][metric] = model.predict(next_periods).tolist() if periods > 0 else list(recent_values)
    return predictions
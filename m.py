@dataclass
class CreditModel:
    file_path: str = None
    metrics_path: str = None
    
    def __post_init__(self):
        self.load_model()
    
    def load_model(self):
        
        self.file_path = self.file_path or "data.xlsx"
        self.metrics_path = self.metrics_path or "financial_metrics.json"
        
        with open(self.metrics_path, "r") as f:
            self.metrics = json.load(f)
        
        self.class_weights = {m: self.metrics[m]["class_weight"] for m in self.metrics}
        
        self.df = pd.read_excel(self.file_path)
        self.nested_dict = get_nested_dict(self.df)
        self.company_period_metrics = get_period_metrics(self.nested_dict)
        self.company_expected_metrics = get_expected_metrics(self.nested_dict)
    
    
    def update_input_dict(self, input_dict: dict) -> dict:
        default_input = {
            "company_name": None,
            "calculator_model": {"sector": "Corporates", "size": "Small"},
            "factor_weights_model": self.class_weights,
            "probabilistic_model": {"periods": 1, "max_iter": 300, "tol": 1e-3}

        }

        def deep_update(d, u):
            for k, v in u.items():
                if isinstance(v, dict):
                    d[k] = deep_update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        updated_input_dict = deep_update(default_input, input_dict)
        return updated_input_dict
    
    
    def update_output_dict(self):
        calculator = CreditRatingCalculator(self.metrics)
        calculator.calculate_credit_rating(self.company_expected_metrics)
        calculator_output = calculator.calculation_details

        # Single Period Calcs
        calculator_periods_output = {}
        for period in self.company_period_metrics:
            calculator = CreditRatingCalculator(self.metrics)
            calculator.calculate_credit_rating(self.company_period_metrics[period])
            calculator_periods_output[period] = calculator.calculation_details

        # Bayesian Model
        bayesian_model_output = bayesian_ridge_model(nested_dict, **input_dict["probabilistic_model"])

        # Rating Description
        rating_description = rating_description_dict[calculator_output["credit_rating"]]

        output_dict = {
            "company_name": input_dict["company_name"],
            "rating_description": rating_description,
            "company_expected_metrics": company_expected_metrics,
            "company_period_metrics": self.company_period_metrics,
            "calculator_output": calculator_output,
            "calculator_periods_output": calculator_periods_output,
            "bayesian_model_output": bayesian_model_output,
            "metrics": metrics
        }
        return output_dict
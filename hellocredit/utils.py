import pandas as pd
import pandera as pa

from .helpers import MAPPED_RATINGS, RATING_META

def get_credit_rating(score):
    for rating, threshold in MAPPED_RATINGS:
        if score <= threshold:
            return rating


def get_rating_meta(key, val):
    index = RATING_META[key].index(val)
    result = {}
    for key, value in RATING_META.items():
        formatted_key = key.lower().replace(' ', '_')
        
        if key == "Probability of Default":
            result[formatted_key] = float(value[index].rstrip('%'))
        elif key == "Score Range":
            score_str = value[index].replace('≤', '').replace('>', '').strip()
            result[formatted_key] = float(score_str)
        else:
            result[formatted_key] = value[index]
    return result



def validate_dataframe(df: pd.DataFrame, company_size: str) -> pd.DataFrame:
    expected_metrics = {
        "Small": [
            "debt_to_equity", "debt_to_ebitda", "ebitda_to_interest_expense",
            "debt_to_tangible_assets", "asset_turnover", "inventory_to_cost_of_sales",
            "cash_to_assets", "ebitda_margin", "total_assets", "sales_growth",
            "return_on_assets"
        ],
        "Medium": [
            "debt_to_equity", "debt_to_ebitda", "ebitda_to_interest_expense",
            "debt_to_tangible_assets", "asset_turnover", "inventory_to_cost_of_sales",
            "cash_to_assets", "ebitda_margin", "total_assets", "sales_growth",
            "return_on_assets"
        ],
        "Large": [
            "debt_to_equity", "debt_to_ebitda", "ebitda_to_interest_expense",
            "asset_turnover", "ebitda_margin", "return_on_assets"
        ]
    }
    
    column_schema = {col: pa.Column(float) for col in df.columns}
    schema = pa.DataFrameSchema(
        columns=column_schema,
        index=pa.MultiIndex([
            pa.Index(str, name="Metric Category"),
            pa.Index(str, name="Metric Name", checks=[
                pa.Check.isin(expected_metrics[company_size]),
                pa.Check(lambda x: set(x) == set(expected_metrics[company_size]), 
                error="DataFrame contains unexpected or missing metrics")
            ])
        ]),
        strict=True
    )
    return schema.validate(df)


def percentage_to_rating(percentage):
    if percentage <= -100:
        return ('C', 10)
    
    scale = 10 - (percentage + 100) / 200 * 7.5
    return next((rating, round(scale, 2)) for rating, threshold in MAPPED_RATINGS if scale <= threshold)



def get_buckets(min_val, max_val, lower_is_better=False, num_buckets=9):
    """
    Generates optimized buckets based on min, max values, desired number of buckets, and whether lower values are better.

    Args:
        min_val (float): The minimum value.
        max_val (float): The maximum value.
        num_buckets (int, optional): Number of buckets. Defaults to 9.
        lower_is_better (bool, optional): True if lower values are better, else False. Defaults to False.

    Returns:
        list: List of tuples (start, end) representing each bucket's range.
    """
    min_val, max_val = (max_val, min_val) if lower_is_better else (min_val, max_val)
    interval = (max_val - min_val) / (num_buckets - 1)
    buckets = [(round(min_val + i * interval, 2), round(min_val + (i + 1) * interval, 2)) for i in range(num_buckets - 1)]
    buckets.append((round(max_val - interval, 2), max_val))
    return list(reversed(buckets)) if lower_is_better else buckets


# Redefine the values and number of buckets for clarity
min_val = 1
median_val = 3
max_val = 5
num_buckets = 3

# Generate the optimized buckets
buckets_list = get_buckets(min_val, median_val, max_val, num_buckets)
print(buckets_list)
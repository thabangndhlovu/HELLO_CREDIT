
The `model_name` (model) is designed to assess the creditworthiness of private small-to-medium sized companies based on their financial metrics. The model considers a range of financial ratios categorised into three main classes: Profitability, Leverage & Coverage, and Efficiency. By analysing these metrics, the model derives a probability of default and assigns a credit score and corresponding credit rating.


- [Model Overview](#model-overview)
  - [Financial Categories and Metrics](#financial-categories-and-metrics)
  - [Metric Weight](#metric-weight)
  - [Credit Score \& Ratings](#credit-score--ratings)
  - [Model Training](#model-training)
- [Model Limitations](#model-limitations)
###



# Model Overview

The model follows a multi-step process to determine the credit score and rating for a given company. It relies on a set of predefined financial metrics, their respective weighting, and threshold values. The key components of the model are as follows:

## Financial Categories and Metrics

The model considers three main categories of financial metrics:

- **Profitability**: Includes ratios that assess the company's ability to generate profit and its overall financial performance i.e. EBITDA Margin, Total Assets, and Sales Growth.
- **Leverage & Coverage**: Includes ratios that evaluate the company's debt levels and its ability to cover its financial obligations i.e. Debt to Equity, Debt to EBITDA, EBITDA to Interest Expense, and Debt to Tangible Assets.
- **Efficiency**: Includes ratios that measure how effectively the company utilises its assets/resources to generate revenue i.e. Asset Turnover, Inventory to Cost of Sales, and Cash to Assets.

## Metric Weight

Each financial category and metric is assigned a specific weight that reflects its relative importance in the overall credit assessment. The weights are determined based on the significance of each metric and ratio in evaluating the company's financial health and creditworthiness. The weights are derived from JSE All Share Index constituents by industry classification, which serves as company classification.

The model calculates quantile buckets for each ratio based on market data. For example, Banks' Debt/Equity 10th percentile is 8.3, 50th percentile is 163, and 90th percentile is 303.1. These quantile buckets are used to assign appropriate weights to the metrics, ensuring that the model's assessment aligns with industry and market norms.

*[Tables omitted due to formatting limitations in this text-based format]*

## Credit Score & Ratings

For each metric within a category, the model assigns a score based on the metric's value and its corresponding quantile position as per the industry. The model credit score ranges from 1.5 (highest rating) to 8.5 (lowest rating) in increments of 1.0.

For example, if the Debt/Equity falls between the 10th and 15th percentiles, it might be assigned a score of 1.5 based on the predefined quantiles. The model then maps the calculated credit score of the metric to a corresponding credit rating ranging from "Aaa" (highest rating) to "C" (lowest rating).

The overall credit score for a company is calculated using the following formula:

```
Overall Credit Score = Σ (Category Weight * Σ (Metric Weight * Metric Score))
```

The final credit rating is determined by mapping the overall credit score to the corresponding rating in the table above.

## Model Training

The model undergoes a training process to optimise the category and metric weights used in the calculation. The training process aims to minimise the difference between the predicted credit rating and the actual credit rating from Moody's, Fitch, and S&P (if available).

The training process involves the following steps:

1. Category and metric weights are initialised using industry norms.
2. Gradient descent, category and metric weights are iteratively adjusted to minimise the loss function, which quantifies the difference between the predicted credit rating and the credit rating from rating agencies. The loss function used is the Mean Absolute Percentage Error (MAPE), calculated as:

```
MAPE = (1/n) * Σ |Actual - Predicted| / |Actual| * 100
```

Where n is the number of observations in the dataset.


# Model Limitations

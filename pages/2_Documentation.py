import streamlit as st


st.set_page_config(
    page_title="Documentation", layout="centered", initial_sidebar_state="collapsed"
)

st.markdown("""
# Model Overview
The `model_name` (model) is designed to assess the creditworthiness of private small-to-medium sized companies based on their financial metrics. The model considers a range of financial ratios categorised into three main classes: Profitability, Leverage & Coverage, and Efficiency. By analysing these metrics, the model derives a probability of default and assigns a credit score and corresponding credit rating.

- [Model Overview](#model-overview)
  - [Financial Categories and Metrics](#financial-categories-and-metrics)
  - [Metric Weight](#metric-weight)
  - [Credit Score \& Ratings](#credit-score--ratings)
  - [Model Training](#model-training)
- [Model Limitations](#model-limitations)
#

The model follows a multi-step process to determine the credit score and rating for a given company. It relies on a set of predefined financial metrics, their respective weighting, and threshold values. The key components of the model are as follows:

## Financial Categories and Metrics

The model considers three main categories of financial metrics:

- **Profitability**: Includes ratios that assess the company's ability to generate profit and its overall financial performance i.e. EBITDA Margin, Total Assets, and Sales Growth.
- **Leverage & Coverage**: Includes ratios that evaluate the company's debt levels and its ability to cover its financial obligations i.e. Debt to Equity, Debt to EBITDA, EBITDA to Interest Expense, and Debt to Tangible Assets.
- **Efficiency**: Includes ratios that measure how effectively the company utilises its assets/resources to generate revenue i.e. Asset Turnover, Inventory to Cost of Sales, and Cash to Assets.

## Metric Weight

Each financial category and metric is assigned a specific weight that reflects its relative importance in the overall credit assessment. The weights are determined based on the significance of each metric and ratio in evaluating the company's financial health and creditworthiness. The weights are derived from JSE All Share Index constituents by industry classification, which serves as company classification. 

The model calculates quantile buckets for each ratio based on market data. For example, Banks' Debt/Equity 10th percentile is 8.3, 50th percentile is 163, and 90th percentile is 303.1. These quantile buckets are used to assign appropriate weights to the metrics, ensuring that the model's assessment aligns with industry and market norms.

Table 1: Metric industry percentiles
| Ratio                       | 10th Percentile | 25th Percentile | 50th Percentile (Median) | 75th Percentile | 90th Percentile |
|-----------------------------|-----------------|-----------------|--------------------------|-----------------|-----------------|
| Debt to Equity              | 0.25            | 0.50            | 1.00                     | 2.00            | 5.00            |
| Debt to EBITDA              | 0.50            | 1.00            | 2.00                     | 4.50            | 9.00            |
| Debt to Tangible Assets     | 0.20            | 0.40            | 0.60                     | 1.00            | 2.00            |
| Inventory to Cost of Sales  | 0.10            | 0.20            | 0.40                     | 0.60            | 1.00            |
| EBITDA to Interest Expense  | 25.00           | 15.00           | 6.00                     | 1.00            | 0.00            |
| EBITDA Margin               | 40.00%          | 30.00%          | 20.00%                   | 10.00%          | 5.00%           |
| Total Assets (millions)     | 500.00          | 50.00           | 5.00                     | 0.50            | 0.10            |
| Sales Growth                | 40.00%          | 25.00%          | 15.00%                   | 5.00%           | 0.00%           |
| Asset Turnover              | 5.00            | 3.00            | 2.00                     | 1.00            | 0.50            |
| Cash to Assets              | 0.50            | 0.30            | 0.20                     | 0.10            | 0.05            |

*Source: JSE All Share as of 01 April 2024, Bloomberg*  

By leveraging these distributions, the model provides a standardised, data-driven approach to assessing and classifying companies based on their financial health. 
However, it's important to note that this approach initially only provides a distribution of market norms; subsequently, the model undergoes training to align its assessments with those of rating agencies.

Table 2: Aligning percentile with credit rating and score

| Metric        | 10th Percentile | 25th Percentile | 50th Percentile (Median) | 75th Percentile | 90th Percentile |
|---------------|-----------------|-----------------|--------------------------|-----------------|-----------------|
| Credit Rating | Aaa, Aa         | A, Baa          | Ba, B                    | Caa, Ca         | C               |


## Credit Score & Ratings

For each metric within a category, the model assigns a score based on the metric's value and its corresponding quantile position as per the industry. The model credit score ranges from 1.5 (highest rating) to 8.5 (lowest rating) in increments of 1.0.

For example, if the Debt/Equity falls between the 10th and 15th percentiles, it might be assigned a score of 1.5 based on the predefined quantiles. The model then maps the calculated credit score of the metric to a corresponding credit rating ranging from "Aaa" (highest rating) to "C" (lowest rating).

The overall credit score for a company is calculated using the following formula:

```
Overall Credit Score = Σ (Category Weight * Σ (Metric Weight * Metric Score))
```

The specific metrics, their corresponding weights, and the category weights used in the model are as follows:

| Category                    | Category Weight | Metric                     | Metric Weight |
|-----------------------------|-----------------|----------------------------|---------------|
| Profitability Metrics       | 35%             | EBITDA Margin              | 40%           |
|                             |                 | Total Assets               | 30%           |
|                             |                 | Sales Growth               | 30%           |
| Leverage & Coverage Metrics | 40%             | Debt to Equity             | 20%           |
|                             |                 | Debt to EBITDA             | 20%           |
|                             |                 | EBITDA to Interest Expense | 20%           |
|                             |                 | Debt to Tangible Assets    | 40%           |
| Efficiency Metrics          | 25%             | Asset Turnover             | 40%           |
|                             |                 | Inventory to Cost of Sales | 30%           |
|                             |                 | Cash to Assets             | 30%           |

*This is subject to iterative adjustment*


The final credit rating is determined by mapping the overall credit score to the corresponding rating in the table above.

| Credit Rating | Score Threshold |
|---------------|-----------------|
| Aaa           | 1.5             |
| Aa            | 2.5             |
| A             | 3.5             |
| Baa           | 4.5             |
| Ba            | 5.5             |
| B             | 6.5             |
| Caa           | 7.5             |
| Ca            | 8.5             |
| C             | > 8.5           |

## Model Training (Machine Learning)

The model undergoes a training process to optimise the category and metric weights used in the calculation. 
The training process aims to minimise the difference between the predicted credit rating and the actual credit rating from rating agencies such as Moody's, Fitch, and S&P by adjusting the weights.

The training process involves the following steps:

1. Category and metric weights are initialised using industry norms.
2. Gradient descent, category and metric weights are iteratively adjusted to minimise the loss function, which quantifies the difference between the predicted credit rating and the credit rating from rating agencies. 

The loss function used is the Mean Absolute Percentage Error (MAPE), calculated as:

```
MAPE = (1/n) * Σ |Actual - Predicted| / |Actual| * 100
```

Where n is the number of observations in the dataset.

Here's the content formatted as markdown:

## Model Limitations

While the `model_name` provides valuable insights into the credit rating of private small-to-medium sized and large companies, it's important to acknowledge its limitations:

1. **Data Dependency**: The model relies heavily on financial metrics, which may not always be up-to-date or accurately reported, especially for private companies. The quality and timeliness of input data directly affect the model's accuracy.

2. **Industry Specificity**: While the model uses industry-specific percentiles, it may not fully capture the nuances of all industries. Some sectors may have unique financial structures that are not adequately represented in the model.

3. **Size Bias**: The model's training data is based on JSE All Share Index constituents, which may not perfectly represent the financial characteristics of small-to-medium sized companies.

4. **Qualitative Factors**: The model focuses on quantitative financial metrics and does not account for qualitative factors such as management quality, market position, or regulatory environment, which can significantly impact a company's creditworthiness.

5. **Economic Cycle Sensitivity**: The model may not fully capture the impact of economic cycles on a company's financial health, potentially leading to over-optimistic ratings during economic booms or overly pessimistic ratings during downturns.

6. **Limited Historical Data**: For newer companies or those with limited financial history, the model may not provide as accurate an assessment due to insufficient data points.

7. **Geographical Limitations**: The model's training data is primarily based on South African companies, which may limit its applicability to companies in other regions with different economic conditions or accounting standards.

8. **Rapid Changes**: The model may not immediately reflect sudden changes in a company's financial situation or market conditions, as it relies on periodic financial reports.

9. **Complex Financial Structures**: For companies with complex financial structures or those involved in significant M&A activities, the model may not fully capture the intricacies of their financial position.

10. **Model Drift**: Over time, the model's accuracy may decrease if not regularly updated to reflect changing market conditions and industry norms.

Users of this model should be aware of these limitations and use the model's output as one of several tools in a comprehensive credit assessment process, rather than as a sole determinant of creditworthiness.
""")


if st.button("Back", type="primary", use_container_width=True):
    st.switch_page("main.py")

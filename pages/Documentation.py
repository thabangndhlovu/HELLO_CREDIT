import streamlit as st

st.markdown("""
Aurthor: Thabang Ndhlovu

# Introduction
The `model_name` (model) is designed to assess the creditworthiness of private small-to-medium sized companies based on their financial metrics. The model takes into account various financial ratios categorised into three main classes: Profitability, Leverage & Coverage, and Efficiency. By analysing these metrics, the model assigns a credit score and a corresponding credit rating to each company, as well as the probability of default. 


# Model Overview
The model follows a multi-step process to determine the credit score and rating for a given company. It relies on a set of predefined financial metrics, their respective weights, and threshold values. The key components of the model are as follows:


## Financial Categories & Metrics
The model considers three main categories of financial metrics:

- **Profitability Metrics:**  This category includes ratios such as EBITDA Margin, Total Assets, and Sales Growth, which assess the company's ability to generate profit and its overall financial performance.
- **Leverage & Coverage Metrics:** Ratios in this category, such as Debt to Equity, Debt to EBITDA, EBITDA to Interest Expense, and Debt to Tangible Assets, evaluate the company's debt levels and its ability to cover its financial obligations.
- **Efficiency Metrics:** This category comprises ratios like Asset Turnover, Inventory to Cost of Sales, and Cash to Assets, which measure how effectively the company utilises its assets/resources to generate revenue.

## Metric Weight
Each financial category and metric is assigned a specific weight that reflects its relative importance in the overall credit assessment. The weights are determined based on the significance of each metric and ratio in evaluating the company's financial health and creditworthiness. The weights are derived from JSE All Share Index constituents by industry classification, which serves as company classification. 

The model calculates quantile buckets for each ratio based on market data. For example, Banks' Debt/Equity 10th percentile is 8.3, 50th percentile is 163, and 90th percentile is 303.1. These quantile buckets are used to assign appropriate weights to the metrics, ensuring that the model's assessment aligns with industry and market norms.

Table 1: (metric industry percentiles)

| Ratio                      | 10th Percentile | 25th Percentile | 50th Percentile (Median)  | 75th Percentile | 90th Percentile |
|----------------------------|-----------------|-----------------|---------------------------|-----------------|-----------------|
| Debt to Equity             | 0.25            | 0.50            | 1.00                      | 2.00            | 5.00            |
| Debt to EBITDA             | 0.50            | 1.00            | 2.00                      | 4.50            | 9.00            |
| Debt to Tangible Assets    | 0.20            | 0.40            | 0.60                      | 1.00            | 2.00            |
| Inventory to Cost of Sales | 0.10            | 0.20            | 0.40                      | 0.60            | 1.00            |
| EBITDA to Interest Expense | 25.00           | 15.00           | 6.00                      | 1.00            | 0.00            |
| EBITDA Margin              | 40.00%          | 30.00%          | 20.00%                    | 10.00%          | 5.00%           |
| Total Assets (millions)    | 500.00          | 50.00           | 5.00                      | 0.50            | 0.10            |
| Sales Growth               | 40.00%          | 25.00%          | 15.00%                    | 5.00%           | 0.00%           |
| Asset Turnover             | 5.00            | 3.00            | 2.00                      | 1.00            | 0.50            |
| Cash to Assets             | 0.50            | 0.30            | 0.20                      | 0.10            | 0.05            |

Table 2 (aligning percentile with credit rating and score) 

| Metric         | 10th Percentile | 25th Percentile | 50th Percentile (Median)  | 75th Percentile | 90th Percentile |
|----------------|-----------------|-----------------|---------------------------|-----------------|-----------------|
| Credit Score   | 1.5             | 2.5             | 4.5                       | 6.5             | 8.5             |
| Credit Rating  | Aaa             | Aa              | A                         | Baa             | Ba, B, Caa, C   |

The specific metrics, their corresponding weights, and the category weights used in the model model are as follows:

| Category                 | Category Weight | Metric                     | Metric Weight |
|--------------------------|-----------------|----------------------------|---------------|
| Profitability Metrics    | 25              | EBITDA Margin              | 0.4           |
|                          |                 | Total Assets               | 0.3           |
|                          |                 | Sales Growth               | 0.3           |
| Leverage & Coverage Metrics | 20           | Debt to Equity             | 0.2           |
|                          |                 | Debt to EBITDA             | 0.2           |
|                          |                 | EBITDA to Interest Expense | 0.2           |
|                          |                 | Debt to Tangible Assets    | 0.4           |
| Efficiency Metrics       | 15              | Asset Turnover             | 0.4           |
|                          |                 | Inventory to Cost of Sales | 0.3           |
|                          |                 | Cash to Assets             | 0.3           |

*Model training changes the weight on the table above*
**Credit Score & Ratings**
For each metric within a category, the model assigns a score based on the metric's value and its corresponding quantile position as per the industry. The model credit score ranges from 1.5 (highest rating) to 8.5 (lowest rating) in increments of 1.0. 

For example, if the Debt/Equity falls between the 10th and 15th percentiles, it might be assigned a score of 1.5 based on the predefined quantiles. The model then maps the calculated credit score of the metric to a corresponding credit rating ranging from "Aaa" (highest rating) to "C" (lowest rating), as shown in the following table:

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

The overall credit score for a company is calculated using the following formula:

$CreditScore = \frac{\sum_{j=1}^{m} (CategoryScore_j \times CategoryWeight_j)}{\sum_{j=1}^{m} CategoryWeight_j}$

where:
- $m$ is the total number of categories
- $CategoryScore_j$ is the weighted average score of the metrics within the $j$-th category, calculated as:

  $CategoryScore_j = \frac{\sum_{i=1}^{n_j} (MetricScore_{i,j} \times MetricWeight_{i,j})}{\sum_{i=1}^{n_j} MetricWeight_{i,j}}$

  - $n_j$ is the number of metrics in the $j$-th category
  - $MetricScore_{i,j}$ is the score assigned to the $i$-th metric in the $j$-th category based on its quantile position
  - $MetricWeight_{i,j}$ is the weight assigned to the $i$-th metric in the $j$-th category

- $CategoryWeight_j$ is the weight assigned to the $j$-th category

The final credit rating is determined by mapping the overall credit score to the corresponding rating in the table above.

**Model Training**
The model undergoes a training process to optimise the category and metric weights used in the calculation. The training process aims to minimise the difference between the predicted credit rating and the actual credit rating from Moody's, Fitch, and S&P (if available). The training process involves the following steps:

1. Category and metric weights are initialised using industry norms.
2. Using gradient descent, class and metric weights are iteratively adjusted to minimise the loss function, which quantifies the difference between the predicted credit rating and the credit rating from rating agencies. The loss function used is the Mean Absolute Percentage Error (MAPE), calculated as:

   $MAPE = \frac{1}{n} \sum_{i=1}^{n} \left| \frac{Actual_i - Predicted_i}{Actual_i} \right| \times 100$

   where:
   - $n$ is the total number of companies in the training dataset
   - $Actual_i$ is the actual credit rating from rating agencies for the $i$-th company
   - $Predicted_i$ is the predicted credit rating by the model model for the $i$-th company

3. The process repeats for a specified number of iterations or until convergence.

Through this training process, the model learns to assign appropriate class and metric weights, generating credit scores that closely approximate the actual credit ratings from rating agencies.

**Conclusion**
The Credit Rating Calculator provides a systematic approach to assess the creditworthiness of companies based on their financial metrics. By considering various ratios across three main categories - Profitability, Leverage & Coverage, and Efficiency - and applying a weighted scoring system, the model generates credit scores and ratings that align with industry standards and market data.

The training process, which utilises gradient descent to minimise the difference between predicted and actual credit ratings, ensures that the model's outputs are reliable and closely approximate the assessments provided by established rating agencies such as Moody's, Fitch, and S&P.

""")
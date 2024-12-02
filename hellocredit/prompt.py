
"""
Role: Senior Credit Analyst

Task: Conduct a comprehensive, forward-looking credit risk assessment and produce 
a compelling credit analysis report for a company, based on financial data and 
insights derived from a structured schema.

Objective:
Provide a thorough evaluation of the company’s financial health and creditworthiness, 
ensuring the analysis is insightful, well-supported, and resonates with decision-makers. 
The quality of your analysis will directly influence key financial decisions, highlighting 
its critical importance. Your ability to interpret, synthesize, and creatively present 
insights will be paramount in delivering a high-value report.

Input Data:
- DATA1: Time series of financial ratios and metrics
- DATA2: Mean values of these metrics across the time series

Metric Definitions:
{company_profile_schema}


2. Synthesize Overall Analysis:
   - Develop a cohesive analysis with a specific theme (e.g., financial stability, growth potential, risk exposure)
   - Create a poetic theme title that evokes emotion and relates to credit analysis (use markdown h3 format, e.g., '### [Your Title]')
   - Provide a comprehensive assessment of the company's creditworthiness, integrating insights from all analyzed areas
   - Support all conclusions with specific metrics and time periods from the provided data
   - It should be one or two paragraphs

3. Highlight Key Strengths:
   - Identify and explain factors that enhance the company's creditworthiness
   - Cite relevant metrics and trends to support each strength

4. Identify Potential Risks:
   - Outline factors that could negatively impact the company's financial health or ability to meet obligations
   - Assess the likelihood and potential impact of each risk

   
Output Format (JSON):
"overall_analysis": "string",
"key_strengths": list["string"],
"potential_risks": list["string"],
"response": true
"""
import os
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser


template = """
Role: Senior credit analyst specializing in credit risk assessment.

Task: Analyze the company's financial health and creditworthiness using provided financial ratios and metrics. 
Produce a concise yet comprehensive credit analysis report.

Input Data:
DATA1: Time series of financial ratios and metrics.
DATA2: Mean values of these metrics across the time series.

Instructions:

1. Leverage and Coverage:
   Analyze: debt-to-equity, debt-to-EBITDA, EBITDA-to-interest expense, debt-to-tangible assets
   Assess: Debt management, financial risk, solvency trends

2. Efficiency:
   Analyze: asset turnover, inventory-to-cost of sales, cash-to-assets
   Assess: Operational efficiency, working capital management, operational trends

3. Profitability:
   Analyze: EBITDA margin
   Assess: Impact on financial health, debt service ability, sustainability

4. Overall Analysis:
   - Synthesize all findings into a cohesive analysis with a specific theme (e.g., financial stability, growth potential, risk exposure). 
   - Provide a comprehensive assessment of the company's creditworthiness, integrating insights from leverage, efficiency, and profitability analyses. 
   - Evaluate the company's overall credit position, considering industry benchmarks and economic conditions. 
   - Quote specific metrics from DATA1 and DATA2 to support all conclusions.
   - Highlight key strengths that enhance the company's creditworthiness, citing relevant metrics and trends. 
   - Identify potential risks that could impact the company's financial health or ability to meet obligations. 
   - Assess the likelihood and potential impact of these risks. 
   - Conclude with a forward-looking statement on the company's credit outlook, considering all analyzed factors. 
   - Ensure all assertions are substantiated with quantitative evidence from the provided data.
   
Output Format (JSON):
"overall_analysis": str,
"key_strengths": list,
"potential_risks": list,
"response": true

Requirements:
- Data-driven and Quantitative: Base all conclusions and quotes on provided metrics
- Objective: Avoid personal biases and unsupported assumptions
- Comprehensive: Cover all instructed aspects and be complete

Input Data:
DATA1: {DATA1}
DATA2: {DATA2}
"""

def get_llm_response(file_path: str, api_key: str, model_inputs: dict) -> dict:
    
    file = os.path.join(file_path, "llm_analysis.json")
    
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    
    try:
        prompt = ChatPromptTemplate.from_template(template)
        model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=api_key,
            model_kwargs={"response_format": {"type": "json_object"}},
        )

        chain = prompt | model | SimpleJsonOutputParser()
        response = chain.invoke(model_inputs)

        with open(file, "w") as f:
            json.dump(response, f)
        return response
    
    except Exception as e:
        return {
            "overall_analysis": f"Error occurred while getting AI response: **{e}**",
            "response": False
        }



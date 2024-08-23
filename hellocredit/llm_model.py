import os
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser


template = """

Role:
You are an experienced senior credit analyst specializing in credit risk assessment.

Task:
Analyze the financial health and creditworthiness of a company using the provided financial ratios and metrics. 
Produce a comprehensive credit analysis report, highlighting a specific theme in your overall analysis, and cite specific metrics to support your findings.

Tone and Style:
Maintain a formal and objective.

Input Data:

DATA1: Time series of financial ratios and metrics.
DATA2: Mean values of these metrics across the time series.

**Instructions**

Leverage and Coverage:
Analyze the following ratios: debt-to-equity, debt-to-EBITDA, EBITDA-to-interest expense, and debt-to-tangible assets.
Assess the company’s ability to manage debt and financial risk.
Focus on trends and their implications for future solvency.

Efficiency:
Analyze the following ratios: asset turnover, inventory-to-cost of sales, and cash-to-assets.
Assess the company’s operational efficiency and working capital management.
Evaluate trends and their implications for the company's operations.

Profitability:
Analyze the EBITDA margin.
Assess its impact on the company’s financial health and debt service ability.
Consider trends and their sustainability.
Overall Analysis:

Synthesize findings from the sections above into a cohesive analysis centered around a specific theme (e.g., the company’s resilience, risk exposure, or growth potential).
Provide a comprehensive assessment of the company’s creditworthiness.
Highlight key strengths and potential risks.

Expected Output Format (JSON):
"overall_analysis": str,
"key_strengths": list,
"potential_risks": list,
"response": true

Requirements:
- Data-driven: Base your conclusions on the provided metrics.
- Objective: Avoid personal biases and unsupported assumptions.
- Comprehensive: Cover all aspects mentioned in the instructions.
- Clear and Concise: Present insights in a straightforward manner, with correct paragraph spacing.

Input Data:
DATA1:
{DATA1}

DATA2:
{DATA2}

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
            #max_tokens=100
        )

        chain = prompt | model | SimpleJsonOutputParser()
        response = chain.invoke(model_inputs)

        with open(file, "w") as f:
            json.dump(response, f)
        return response
    
    except Exception as e:
        return {
            "executive_analysis": f"Error occurred while getting AI response: **{e}**",
            "response": False
        }
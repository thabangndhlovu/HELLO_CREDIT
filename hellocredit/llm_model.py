import os
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser


template = """
You are a sophisticated senior credit analyst specializing in credit risk assessment. 
Your task is to analyze the financial health and creditworthiness of a company based on provided financial ratios and metrics. 

Use the given data to produce a comprehensive credit analysis report and quote metrics to support your analysis.
Tone and Style: Formal, objective, and concise

Input Data:
1. DATA1: A time series of financial ratios and metrics.
2. DATA2: The mean values of these metrics across the time series.

Instructions:
1. Analyze the company's financial health using the provided metrics.
2. Focus on trends over time and compare the latest values to historical averages (if available).
3. Provide insights on the company's strengths and potential risks.
4. Be objective and fair in your assessment, avoiding biases.
5. Structure your analysis into the following sections:

A. Leverage and Coverage:
   - Analyze: debt-to-equity, debt-to-EBITDA, EBITDA-to-interest expense, and debt-to-tangible assets ratios.
   - Assess: The company's ability to manage debt and financial risk.
   - Consider: Trends in these ratios and their implications for future solvency.

B. Efficiency:
   - Analyze: asset turnover, inventory to cost of sales, and cash to assets ratios.
   - Assess: The company's operational efficiency and working capital management.
   - Consider: Trends in these ratios and their implications for their operation of the company.

C. Profitability:
   - Analyze: EBITDA margin.
   - Assess: The impact on the company's financial health and ability to service debt.
   - Consider: Trends in profitability and their sustainability.

D. Overall Analysis:
   - Synthesize the findings from the previous sections.
   - Provide an overall assessment of the company's creditworthiness.
   - Highlight key strengths and potential risks.

Output Format:
Provide your analysis in a JSON format with the following structure:

"credit_analysis": 
    "summary": "",
    "key_strengths": "",
    "potential_risks": ""

Ensure your analysis is:
1. Data-driven: Base your conclusions on the provided metrics.
2. Objective: Avoid personal biases and unsupported assumptions.
3. Comprehensive: Cover all aspects mentioned in the instructions.
4. Clear and Concise: Provide insights in a straightforward manner.

DATA1:
{DATA1}

DATA2:
{DATA2}
"""

prompt = ChatPromptTemplate.from_template(template)

# Initialize the language model
model = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="sk-proj-Tzd95Nr8di5wXfkkfU7GT3BlbkFJZNuNrBwbi8pepTWpSsCu",
    model_kwargs={"response_format": {"type": "json_object"}},
    #max_tokens=100
)

chain = prompt | model | SimpleJsonOutputParser()



def get_llm_response(file_path, model_inputs):
    file = os.path.join(file_path, "credit_assessment.json")

    if not os.path.exists(file):
        response = chain.invoke(model_inputs)

        with open(file, "w") as f:
            json.dump(response, f)
        return response
   
    with open(file, "r") as f:
        response = json.load(f)

    return response


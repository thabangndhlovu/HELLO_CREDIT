import os
import json

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser

MODEL = "gemini-1.5-pro-exp-0801"
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]


template = """
Role: Senior Credit Analyst

Task: Conduct a comprehensive credit risk assessment and produce a detailed credit analysis report for a company based on provided financial data.

Input Data:
- DATA1: Time series of financial ratios and metrics
- DATA2: Mean values of these metrics across the time series

Instructions:

1. Analyze Key Financial Areas:

   a) Leverage and Coverage:
      - Examine: debt-to-equity, debt-to-EBITDA, EBITDA-to-interest expense, debt-to-tangible assets
      - Evaluate: Debt management, financial risk, and solvency trends

   b) Efficiency:
      - Examine: asset turnover, inventory-to-cost of sales, cash-to-assets
      - Evaluate: Operational efficiency, working capital management, and operational trends

   c) Profitability:
      - Examine: EBITDA margin
      - Evaluate: Impact on financial health, debt service ability, and sustainability

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

5. Conclude with Credit Outlook:
   - Provide a forward-looking statement on the company's credit outlook, considering all analyzed factors

6. Formatting Guidelines:
   - Use markdown to separate sections and improve readability
   - Ensure all assertions are supported by quantitative evidence from the provided data

Output Format (JSON):
"overall_analysis": "string",
"key_strengths": ["string"],
"potential_risks": ["string"],
"response": true

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
        model = ChatGoogleGenerativeAI(
            model=MODEL,
            model_kwargs={"response_format": {"type": "json_object"}},
        )

        chain = prompt | model | SimpleJsonOutputParser()
        response = chain.invoke(model_inputs)

        with open(file, "w") as f:
            json.dump(response, f)
        return response

    except Exception as e:
        return {
            "overall_analysis": f"Error occurred while getting AI response: \n**{e}**",
            "response": False,
        }

import os
import json

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers.json import SimpleJsonOutputParser


from openai import OpenAI
import google.generativeai as genai
import os
from openai import OpenAI
from typing import Literal

# TEMPLATE = """
# Role: Senior Credit Analyst

# Task: Conduct a comprehensive credit risk assessment and produce a detailed
# credit analysis report for a company based on provided financial data. Consider
# the MODEL_PROFILE and how the metrics and descriptions relate to each other
# think through the parameters provide an analysis. The analysis should be complete
# and comprehensive.

# Input Data:
# - DATA1: Time series of financial ratios and metrics
# - DATA2: Mean values of these metrics across the time series

# MODEL_PROFILE:
# - {METRICS_SCHEMA}

# 2. Synthesize Overall Analysis:
#    - Develop a cohesive analysis with a specific theme (e.g., financial stability, growth potential, risk exposure)
#    - Create a poetic theme title that evokes emotion and relates to credit analysis (use markdown h3 format, e.g., '### [Your Title]')
#    - Provide a comprehensive assessment of the company's creditworthiness, integrating insights from all analyzed areas
#    - Support all conclusions with specific metrics and time periods from the provided data
#    - It should be one or two paragraphs

# 3. Highlight Key Strengths:
#    - Identify and explain factors that enhance the company's creditworthiness
#    - Cite relevant metrics and trends to support each strength

# 4. Identify Potential Risks:
#    - Outline factors that could negatively impact the company's financial health or ability to meet obligations
#    - Assess the likelihood and potential impact of each risk

# 5. Conclude with Credit Outlook:
#    - Provide a forward-looking statement on the company's credit outlook, considering all analyzed factors

# 6. Formatting Guidelines:
#    - Use markdown to separate sections and improve readability
#    - Ensure all assertions are supported by quantitative evidence from the provided data

# Output Format (JSON):
# "overall_analysis": "string",
# "key_strengths": list["string"],
# "potential_risks": list["string"],
# "response": true

# Input Data:
# DATA1: {DATA1}
# DATA2: {DATA2}

# """





TEMPLATE = """
**Role:** Senior Credit Analyst

**Task:** Conduct an in-depth credit risk assessment and produce a detailed credit analysis 
report for a company based on the provided financial data. Your analysis should be complete, 
comprehensive, and creative, considering all relevant aspects given the data provided. 
Focus on how the metrics and descriptions in the **MODEL_PROFILE** relate to each other, 
and think critically through the parameters to provide a high-quality analysis.

**Instructions:**

1. **Analyze the Data:**
   - **Examine DATA1 and DATA2 thoroughly:**
     - **DATA1:** Time series of financial ratios and metrics.
     - **DATA2:** Mean values of these metrics across the time series.
   - For each metric in the **MODEL_PROFILE**, assess the company's performance over time and in comparison to the provided thresholds and ratings.
   - Consider the **interrelationships** between different metrics and how they collectively impact the company's credit risk profile.
   - Think deeply about the implications of each metric's trend and level, and how they reflect the company's financial health and creditworthiness.
   - **Support all conclusions with specific metrics and time periods** from the provided data.

2. **Synthesize Overall Analysis:**
   - **Develop a cohesive analysis with a specific theme** that encapsulates your findings (e.g., financial resilience, strategic growth, emerging risks).
   - **Create a poetic theme title** that evokes emotion and relates to credit analysis (use markdown h3 format, e.g., `### The Beacon of Financial Fortitude`).
   - Provide a **comprehensive assessment** of the company's creditworthiness, **integrating insights from all analyzed areas** (profitability, capital adequacy and leverage, asset quality).
   - Discuss **trends, patterns, and significant changes** in the company's financial metrics over time.
   - Highlight how the company's performance in different metrics compares to industry averages or benchmarks if relevant.
   - The analysis should be **detailed and expansive**, comprised of multiple paragraphs that delve into the nuances of the company's financial situation.

3. **Highlight Key Strengths:**
   - **Identify and explain in detail** all factors that enhance the company's creditworthiness.
   - Cite relevant metrics, positive trends, and comparisons to thresholds to support each strength.
   - Explain how these strengths contribute to the company's ability to meet its financial obligations and sustain operations.

4. **Identify Potential Risks:**
   - **Outline all factors** that could negatively impact the company's financial health or ability to meet obligations.
   - Assess the **likelihood and potential impact** of each risk, backed by data.
   - Discuss any adverse trends, metric levels approaching critical thresholds, or negative comparatives.

5. **Conclude with Credit Outlook:**
   - Provide a **forward-looking statement** on the company's credit outlook, considering all analyzed factors.
   - Include potential future developments, and how the company's current position may evolve.
   - Offer strategic recommendations or considerations based on your analysis.

6. **Formatting Guidelines:**
   - Use **markdown** to separate sections and improve readability (e.g., headings, subheadings, bullet points).
   - **Ensure all assertions are supported by quantitative evidence** from the provided data.
   - Maintain a professional and analytical tone, suitable for a senior-level credit analysis report.
   - The final output should be structured and presented clearly, facilitating easy understanding of your key points and conclusions.

7. **Output Format (JSON):**
   ```json
     "overall_analysis": "string",
     "key_strengths": ["string", "string", "..."],
     "potential_risks": ["string", "string", "..."],
     "response": true
   ```

**MODEL_PROFILE:**
{METRICS_SCHEMA}

**Input Data:**

- **DATA1:** {DATA1}
- **DATA2:** {DATA2}

"""


def get_llm_response(
   file_path: str, model_inputs: dict,
   llm_provider: Literal["chatgpt", "gemini"] = "chatgpt", cache: bool = True,
   ) -> dict:
   
   cache_file = os.path.join(file_path, "llm_analysis.json")
   content = TEMPLATE.format(**model_inputs).replace("\n", "").strip(" ")

   # Return cached response if exists and cache is enabled
   if cache and os.path.exists(cache_file):
      with open(cache_file, "r") as f:
         return json.load(f)
   try:
      if llm_provider == "chatgpt":
         response = _get_openai_response(content)
      else:
         response = _get_gemini_response(content)

      if cache:
         with open(cache_file, "w") as f:
            json.dump(response, f)

      return response

   except Exception as e:
      return {
         "overall_analysis": f"Error occurred while getting {llm_provider.upper()} response: \n{str(e)}",
         "response": False,
      }


def _get_openai_response(content: str) -> dict:
   client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

   completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
         {
               "role": "system",
               "content": "You are a helpful senior credit analyst. Guide the user through the solution step by step.",
         },
         {"role": "user", "content": content},
      ],
      response_format={"type": "json_object"},
   )

   return json.loads(completion.choices[0].message.content) #eval(completion.choices[0].message.content)


def _get_gemini_response(content: str) -> dict:
   genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

   generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 64,
      "max_output_tokens": 8192,
      "response_mime_type": "application/json",
   }

   model = genai.GenerativeModel(
      model_name="gemini-1.5-flash", #"gemini-exp-1121", #"gemini-1.5-flash", 
      generation_config=generation_config,
   )

   response = model.generate_content(content)

   return json.loads(response.text)



def parse_company_profile_schema(schema: dict) -> str:
    MAPPED_RATINGS = ["Aaa", "Aa", "A", "Baa", "Ba", "B", "Caa", "Ca", "C"]

    result = []
    for category, details in schema.items():
        result.append(f"\n{category.replace('_', ' ').upper()}:\n  Description: {details['description']}\n  Class Weight: {details['class_weight']}%")
        for metric, metric_desc in details['metric_description'].items():
            result.append(f"  Metric: {metric.replace('_', ' ').title()}\n    Description: {metric_desc}\n    Weight: {details['metric_weights'][metric] * 100:.2f}%")
            
            thresholds = details['metrics'][metric]['thresholds']
            order = "Increasing" if not details['metrics'][metric]['lower_is_better'] else "Decreasing"
            thresholds_text = ", ".join([f"{thr[0]} to {thr[1]}" for thr in thresholds])
            
            # Reverse ratings if order is Increasing (lower_is_better=False)
            ratings = MAPPED_RATINGS[::-1] if details['metrics'][metric]['lower_is_better'] else MAPPED_RATINGS
            
            result.append(f"    Rating: {', '.join(ratings)}")
            result.append(f"    Thresholds: {thresholds_text}")
            result.append(f"    Order Preference: {order} order preferred")
    return "\n".join(result)
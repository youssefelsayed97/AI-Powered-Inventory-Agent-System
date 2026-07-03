import os
import json
from google import genai
from google.genai.errors import APIError
from dotenv import load_dotenv
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("genai_api"))
ai_models = ["gemini-2.5-flash-lite", "gemini-2.5-flash"]


def ai_decide(user_input):
    prompt = f"""
    You are a tool-calling AI Agent.

    Your task is to choose exactly ONE tool.

    Available tools:

    [
        {{
            "name":"search_stock",
            "description":"Search inventory",
            "parameters":{{
                "semantic_query":"string",
                        "filters":{{
                        "Code":null,
                        "LowPrice":null,
                        "HighPrice":null,
                        "Source":null
                        }}
            }}
        }},
        {{
            "name":"delete_stock",
            "description":"Delete inventory item",
            "parameters":{{
                "Code":"Integer"
            }}
        }}
    ]
    
    
    For search requests:
    
    - Put the product description or natural language search into "semantic_query".
    - Extract structured conditions into "filters".
    - Do not include structured fields inside semantic_query.
    - If Indoor or Outdoor put them en the source field
    - If the user's search contains only filter conditions (such as Source, Code, LowPrice, HighPrice) and no product description, return an empty semantic_query.
    
    example 1:
            {{
            "tool":"search_stock",
                "args":{{
                    "semantic_query":"iphone",
                    "filters":{{}}
                }}
            }}
            
    example 2:
            {{
            "tool":"search_stock",
                "args":{{
                    "semantic_query":"iphone",
                    "filters":{{
                        "HighPrice":{{
                            "lte":500
                        }}
                    }}
                }}
            }}            
    
    Rules:

    - Choose only one tool.
    - Extract parameters from user input.
    - Never guess missing information.
    - Return valid JSON only.
    - Never explain.
    - Never use markdown.
    - Never output anything except JSON.

    JSON format:

    {{
        "tool":"tool_name",
        "args":{{
            ...
        }}
    }}

    If information is missing:

    {{
        "tool":None,
        "args":None
    }}

    User:
    {user_input}
    """
    for model in ai_models:
        print(f"Trying model {model}")

        for i in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                try:
                    data = json.loads(response.text)

                    if isinstance(data, dict):
                        return data

                    else:
                        print("Response is not dict → retrying...")
                        continue

                except json.JSONDecodeError:
                    print("Invalid JSON → retrying...")
                    continue

            except APIError as e:
                wait = 2 ** i
                print(f"Attempt {i + 1}/5 failed: {e}")
                print(f"Retrying in {wait} seconds...")
                time.sleep(wait)

        print(f"Model {model} failed after 3 attempts. Switching to next model...")

    return {"tool": None, "args": {}}


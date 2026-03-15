import os
import json
from groq import Groq
import dotenv
from .tools import (
    search_employees, flag_attrition_risk,
    summarize_department, find_low_satisfaction, find_high_earners
)

dotenv.load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """You are an HR AI assistant. Help HR professionals get insights from their employee data.

When you need information, use the provided tools. 
If the user mentions a specific department, pass it to the tool if possible.

CRITICAL (Tool Use): If you decide to use a tool, you MUST output ONLY the tool call. 
Do NOT provide any conversational preamble, introduction, or reasoning text before or after the tool call.

CRITICAL (Final Response): Once you have the data from a tool, your goal is to ANALYZE and SYNTHESIZE it.
- **Data Presentation**: ALWAYS use a Markdown Table (standard pipe format: | Col 1 | Col 2 |) for ANY list of employees, statistics, or structured records. 
- **Narrative Analysis**: Provide a clear, narrative summary of what the data shows (e.g., "I've identified a trend where employees in Sales have the lowest satisfaction scores").
- **Structure**: Typically, present the data table first for clarity, then follow up with your narrative analysis and recommendations.
- **Synthesis**: Connect different data points (e.g., matching low satisfaction with attrition). Do NOT just dump the table without context.

Be analytical, professional, and insight-driven."""

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_employees",
            "description": "Semantically search employee records for any natural language query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Natural language search query"},
                    "top_k": {"type": "string", "description": "Number of results to return (default 5)"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "flag_attrition_risk",
            "description": "Find employees who have left or are at high attrition risk",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {"type": "string", "description": "Optional department filter"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "summarize_department",
            "description": "Get all employee profiles from a specific department. If looking for all employees, use 'all'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "department": {"type": "string", "description": "Department name e.g. Sales, HR, Engineering, or 'all'"}
                },
                "required": ["department"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_low_satisfaction",
            "description": "Find employees with low job satisfaction scores",
            "parameters": {
                "type": "object",
                "properties": {
                    "top_k": {"type": "string", "description": "Number of results to return (default 10)"},
                    "department": {"type": "string", "description": "Optional: Filter by department name"}
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_high_earners",
            "description": "Find the highest paid employees in the dataset",
            "parameters": {
                "type": "object",
                "properties": {
                    "top_k": {"type": "string", "description": "Number of results to return (default 10)"},
                    "department": {"type": "string", "description": "Optional: Filter by department name"}
                },
                "required": []
            }
        }
    }
]

TOOL_MAP = {
    "search_employees": search_employees,
    "flag_attrition_risk": flag_attrition_risk,
    "summarize_department": summarize_department,
    "find_low_satisfaction": find_low_satisfaction,
    "find_high_earners": find_high_earners
}

def run_agent(user_query: str, history: list = []) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Include conversation history
    for turn in history:
        messages.append({"role": "user", "content": turn["user"]})
        messages.append({"role": "assistant", "content": turn["assistant"]})

    messages.append({"role": "user", "content": user_query})

    while True:
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=1024
            )
        except Exception as e:
            return f"Error connecting to AI service: {str(e)}"

        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content or "I couldn't generate a response."

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                }
                for tc in msg.tool_calls
            ]
        })

        for tc in msg.tool_calls:
            fn_name = tc.function.name
            try:
                # Clean up potential truncated or malformed JSON from model
                args_str = tc.function.arguments
                if not args_str.strip().endswith('}'):
                    args_str = args_str.strip() + '}'
                
                fn_args = json.loads(args_str) if args_str else {}
                
                # Robust integer conversion for top_k
                if "top_k" in fn_args:
                    try:
                        fn_args["top_k"] = int(str(fn_args["top_k"]))
                    except (ValueError, TypeError):
                        fn_args["top_k"] = 10
                
                # Ensure it's a dict before calling
                if not isinstance(fn_args, dict):
                    fn_args = {}

                result = TOOL_MAP[fn_name](**fn_args)
            except Exception as e:
                result = f"Error executing {fn_name}: {str(e)}"

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": str(result)
            })

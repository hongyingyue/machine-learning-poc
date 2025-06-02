import os
import warnings
from datetime import datetime
from litellm import completion
from duckduckgo_search import DDGS
import json
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

api_key = "sk-proj-xxxx"
os.environ["OPENAI_API_KEY"] = api_key
warnings.filterwarnings("ignore", category=UserWarning)
console = Console()

# Tool 1: DuckDuckGo Search
def duckduckgo_search(query, max_results=5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append(f"{r['title']}: {r['href']}")
    return "\n".join(results)

# Tool 2: Character Counter
def count_character_count(text):
    return f"The input has {len(text)} characters."

# Tool3: Character count in word
def count_character_occurrence(word, character):
    if len(character) != 1:
        return "Error: Please provide a single character."
    count = word.count(character)
    return f"The character '{character}' appears {count} time(s) in '{word}'."

# Tool 3: Current Datetime
def get_current_datetime():
    return f"The current date and time is: {datetime.now().isoformat()}"


tool_functions = {}

def register_tool(func):
    tool_functions[func.__name__] = func
    return func

# Register tools
register_tool(duckduckgo_search)
register_tool(count_character_count)
register_tool(count_character_occurrence)
register_tool(get_current_datetime)


# Tool registry
tools = [
    {
        "type": "function",
        "function": {
            "name": "duckduckgo_search",
            "description": "Searches the web for the latest info using DuckDuckGo",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    }
                },
                "required": ["query"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_character_count",
            "description": "Counts the number of characters in a string",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The string to count characters in",
                    }
                },
                "required": ["text"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_character_occurrence",
            "description": "Counts how many times a given character appears in a word",
            "parameters": {
                "type": "object",
                "properties": {
                    "word": {
                        "type": "string",
                        "description": "The word in which to count the character",
                    },
                    "character": {
                        "type": "string",
                        "description": "The single character to count",
                    },
                },
                "required": ["word", "character"],
            },
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Returns the current date and time",
            "parameters": {
                "type": "object",
                "properties": {}
            },
        }
    }
]

def run_agent(question):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]

    for step in range(3):
        console.rule(f"[bold green]Step {step}")
        console.print(Syntax(str(messages), "python", theme="monokai", word_wrap=True))

        response = completion(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        msg = response['choices'][0]['message']

        if msg.get("tool_calls"):
            tool_call = msg["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            arguments = json.loads(tool_call["function"]["arguments"])

            console.print(Panel.fit(
                f"[bold yellow]🔧 Tool requested[/bold yellow]: [cyan]{function_name}[/cyan]([magenta]{arguments}[/magenta])",
                title="Tool Call", style="yellow"))

            if function_name in tool_functions:
                try:
                    result = tool_functions[function_name](**arguments)
                except Exception as e:
                    result = f"Error running tool '{function_name}': {e}"
            else:
                result = f"❌ Unknown tool: {function_name}"

            messages.append(msg)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": result,
            })

            console.print(Panel.fit(result, title="Tool Result", style="cyan"))
        else:
            final_answer = msg["content"]
            console.print(Panel.fit(
                f"[bold green]🤖 Final Answer:[/bold green]\n{final_answer}",
                style="green", title="Answer"
            ))
            break


if __name__ == "__main__":
    while True:
        user_question = input("\nAsk something (or type 'q' to quit): ")
        if user_question.strip().lower() in {"exit", "q"}:
            print("Goodbye!")
            break
        run_agent(user_question)

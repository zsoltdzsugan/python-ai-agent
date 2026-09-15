import sys
import os
import argparse
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_functions import available_functions, call_function

def generate_content(client, messages):
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )


def main():
    print("Hello from aiagent!")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key is None:
        raise RuntimeError("Api unreachable!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages=[
        { "role": "system", "content": system_prompt },
        { "role": "user", "content": args.user_prompt }
    ]

    for _ in range(20):
        response = generate_content(client, messages)    
        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result = call_function(tool_call, args.verbose)

                if not result['content']:
                    raise Exception("No content")

                if args.verbose:
                    print(f"-> {result['content']}")

                messages.append(result)
        else:
            print(f"Final response: {message.content}")

            if args.verbose:
                print(f"Prompt tokens: {response.usage.prompt_tokens}")
                print(f"Response tokens: {response.usage.completion_tokens}")

            break

    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

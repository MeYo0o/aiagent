import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    import time
    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0,
                    tools=[available_functions],
                ),
            )
        except Exception as e:
            if "429" in str(e):
                time.sleep(15)
                continue
            raise e

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("Failed to retrieve usage metadata from the Gemini API.")

        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count} Response tokens: {response.usage_metadata.candidates_token_count}")

        if response.function_calls:
            function_results = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose=args.verbose)
                
                if not function_call_result.parts:
                    raise Exception("Function call result has no parts.")
                
                if getattr(function_call_result.parts[0], "function_response", None) is None:
                    raise Exception("Function response is None.")
                    
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Function response data is None.")
                    
                function_results.append(function_call_result.parts[0])
                
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                    
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            return
            
    print("Error: Agent reached maximum number of iterations without producing a final response.")
    exit(1)
if __name__ == "__main__":
    main()


import os
import sys
from dotenv import load_dotenv
from google.genai import types
from google import genai
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    #if len(sys.argv) == 1:
        #print("Prompt not provided")
        #sys.exit(1)

    #print("Hello from project-3-ai!")

    if verbose:
        print(f"'User prompt: {user_prompt}\n'")

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):
    """
    Implemented function flow:
    1. Send user message to LLM
    2. LLM responds (either with text OR function calls)
    3. If function calls: Execute them, add results to conversation, go back to step 2
    4. If text response: Return it to user
    """
    for _ in range(20):
        try:
            response = client.models.generate_content(
            model = "gemini-2.0-flash-001",
            contents = messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                ),
            )


            if verbose:
                print(f"'Prompt tokens: {response.usage_metadata.prompt_token_count}'")
                print(f"'Response tokens: {response.usage_metadata.candidates_token_count}'")

            if not response.function_calls:
                return response.text

            function_responses = []
            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(function_call_part, verbose)
                    func_call_response = function_call_result.parts[0].function_response.response

                    if not function_call_result or not func_call_response:
                        raise Exception("empty function call result")
                    if verbose:
                        print(f"-> {func_call_response}")
                    tool_message = types.Content(
                        role="user",
                        parts = [
                            types.Part.from_function_response(
                                name=function_call_part.name,
                                response=func_call_response,
                            )
                        ],
                    ) 
                    messages.append(tool_message)
            if not tool_message:
                raise Exception("no function responses generated, exiting.")
            
        except Exception as e:
            print(f"Error : {e}")
            break
if __name__ == "__main__":
    main()

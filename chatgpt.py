
import torch
from openai import OpenAI

class Model():

    def __init__(self, file_upload_dir='uploads') -> None:
        
        print(f"GPU Capability: {torch.cuda.get_device_capability(0)[0]}")

        self.file_upload_dir = file_upload_dir

        self.api_key = self.get_param("chatgpt_api_key")

        self.chat_gpt_client = OpenAI(api_key=self.api_key)
        
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

        print(f"Starting RagModel on device {self.device}")


    def get_param(self, param_name):

        apikey = ""

        with open('config.txt') as apifile:
            for line in apifile:
                if param_name in line:
                    idx = line.find(":")
                    apikey = line[idx+1:].strip()

        if(len(apikey) == 0):
            raise Exception(f"Unable to load {param_name} API key")
        
        return apikey



    def split_list(self, input_list: list[str], slice_size: int=10) -> list[list[str]]:
        return [input_list[i:i+slice_size] for i in range(0, len(input_list), slice_size)]


    def text_formatter(self, text: str) -> str:
        """Performs text formatting"""
        cleaned_text = text.replace("\n", " ").strip()
        return cleaned_text

    def ask(self,
            tests: str,
            goal: str,
            last_generated_code: str = "None",
            error: str = "None",            
            temperature: float = 0.7,
            max_new_tokens: int = 256) -> str:
        """
        Takes a query, finds relevant resources/context, and generates an answer to the query based on the relevant resources.
        """

        # Format the prompt.
        prompt = self.prompt_formatter(tests=tests,
                                       goal=goal,
                                       last_generated_code=last_generated_code,
                                       error=error)

        # Use OpenAI's API to generate a response

        response = self.chat_gpt_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}",
                }
            ],
            model="gpt-4o",
        )

        print(f"[INFO] Raw response {response}")

        output_text = response.choices[0].message.content

        output_text = output_text.strip()

        return output_text
    

    def prompt_formatter(self, goal: str,
                         tests: str,
                         last_generated_code: str,
                         error: str):

        base_prompt = """
            Please take the attached unit tests and goal, and provide code written in python that will pass the tests. 
            You are being used as part of a fully automated system. The answer you provide will be directly written to a .py file to be executed. 
            Absolutely do not return the python executable or quotes around the code. Just return the raw code. 
            Please don't include any filler text, just the code. Don't include the tests themselves in your response.  
            If the original code provided failed, this prompt might include an error along with the unit test. Please keep that error in mind.  
            Tests to pass:
            {tests}
            Goal: {goal}
            Previous Code: {last_generated_code}
            Error: {error}
            Answer: 
        """
        prompt = base_prompt.format(goal=goal, 
                                    tests=tests, 
                                    last_generated_code=last_generated_code,
                                    error=error)

        return prompt
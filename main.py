from chatgpt import Model
import pytest
from run_tests import *

model = Model()

with open("test.py") as file:
    tests = file.read()

with open("output/test.py", "w") as file:
    file.write(tests)
 

last_generated_code = "None"
error = "None"

max_iterations = 10

for i in range(max_iterations):

    response = model.ask(tests=tests, 
                         goal="A simple math class", 
                         last_generated_code=last_generated_code, 
                         error=error)

    with open("output/app.py", "w") as file:
        file.write(response)
        # print("Model response: ", response)
   
    result, error = run_pytest()

    if result == 0:
        print("Completed code generation. All tests passed")
        break
    else:
        print(error)
        print("Failed tests. Regenerating code..")

    last_generated_code = response
     
import os
import openai
from decouple import config

openai.api_key = config('OPENAI_API_KEY')

def get_GPT3_davinci_response (command:str):

    response = openai.Completion.create(model="text-davinci-003", prompt=command, temperature=0)
    
    fl = open('temp_response.json', 'w')
    fl.write(str(response))
    fl.close()
    return response
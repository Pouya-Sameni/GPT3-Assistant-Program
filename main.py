import sms_platform as SP
import parsers
import openAI_connect as gpt
import time
from decouple import config


while True:
    command = parsers.get_text_body(SP.recieve_sms_via_email()).strip()
    
    if len(command) != 0:
        print ("Command: " + command)
        response = gpt.get_GPT3_davinci_response(command)
        response = parsers.parse_gpt_resonse(str(response))
        SP.send_sms_via_email(number=config('phone_number'), message=response, provider="Koodo")

    time.sleep(5)


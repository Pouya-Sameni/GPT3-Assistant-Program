import sms_platform as SP
import parsers
import openAI_connect as gpt
import time
from decouple import config
import google_cal

while True:
    command = parsers.get_text_body(SP.recieve_sms_via_email()).strip()
    
    firstCommand = command[0:command.find("\n")].strip()
    if len(command) != 0 and firstCommand == "?schedule":
        command = command[command.find("\n"):]
        givenList = google_cal.get_event_list()
        command = command + " in format yyyy-mm-dd hh:mm\n"
        for event in givenList:
            command = command + "\n" + event
        
        print(command)
        response = gpt.get_GPT3_davinci_response(command, maxToks=250)
        response = parsers.parse_gpt_resonse()
        print(response)
        SP.send_sms_via_email(number=config('phone_number'), message=response, provider="Telus")

    elif len(command) != 0:
        print ("Command: " + command)
        response = gpt.get_GPT3_davinci_response(command)
        response = parsers.parse_gpt_resonse()
        SP.send_sms_via_email(number=config('phone_number'), message=response, provider="Telus")

    time.sleep(5)


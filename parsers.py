import xml.etree.ElementTree as ET
import json

def get_text_body(message:str):

    if message != "":
        message = message[message.find("<pre>") +5 :message.find("</pre>")]
        return message

    return ""


def parse_gpt_resonse():
    f = open('temp_response.json')
    data = json.load(f)

    str = data['choices'][0]['text'].strip()
    
    # Closing file
    f.close()
    return str
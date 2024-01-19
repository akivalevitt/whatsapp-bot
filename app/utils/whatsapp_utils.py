import logging
from flask import current_app, jsonify
import json
import requests
import aiohttp
import asyncio
from dotenv import load_dotenv
from dotenv import set_key

import os
# from app.services.openai_service import generate_response
import re
from app.utils import automateFirst
from app.utils import aiPart
# Global dictionary to manage conversation state for each user
user_states = {}
# Example conversation steps
conversation_steps = {
    1: "Please enter your Username:",
    2: "Please enter your Password.",
    3: "Please enter amount to pay R: \nEg *150*",
    4: 'Please confirm the below details by sending the word *Confirm*'
}

inputs = {
    "Account Info":{},
    "Username":"",
    "Password":"",
    "Amount":"",
    "Confirm":"",
    "Name":""
}

stepsDone = {
    1: False,
    2: False,
    3: False,
    4: False,
    5: False,
    6: False
}
message_array=[]
user_convo={}
# Function to get the next step in the conversation
def get_next_step(user_id, account_details):
    current_step = user_states.get(user_id, 0)
    next_step = current_step + 1
    user_states[user_id] = next_step
    output=""
    if(next_step==1):
        output=conversation_steps.get(next_step, None)+account_details
    else:
        output=conversation_steps.get(next_step, None)

    return output


def log_http_response(response):
    logging.info(f"Status: {response.status_code}")
    logging.info(f"Content-type: {response.headers.get('content-type')}")
    logging.info(f"Body: {response.text}")


def get_text_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )


def get_button_message_input(recipient, text):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "template",
            "template": {"name": "template", "language": {"code": "en_US"},}
        }
    )


def generate_response(response):
    # Return text in uppercase
    return response.upper()


def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
    }

    url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"

    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=100
        )  # 10 seconds timeout as an example
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        logging.error("Timeout occurred while sending message")
        return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (
        requests.RequestException
    ) as e:  # This will catch any general request exception
        logging.error(f"Request failed due to: {e}")
        return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        log_http_response(response)
        return response
    



# async def send_message(data):
#     headers = {
#         "Content-type": "application/json",
#         "Authorization": f"Bearer {current_app.config['ACCESS_TOKEN']}",
#     }

#     async with aiohttp.ClientSession() as session:
#         url = f"https://graph.facebook.com/{current_app.config['VERSION']}/{current_app.config['PHONE_NUMBER_ID']}/messages"
#         try:
#             async with session.post(url, data=data, headers=headers) as response:
#                 if response.status == 200:
#                     print("Status:", response.status)
#                     print("Content-type:", response.headers["content-type"])

#                     html = await response.text()
#                     print("Body:", html)
#                 else:
#                     print(response.status)
#                     print(response)
#         except aiohttp.ClientConnectorError as e:
#             print("Connection Error", str(e))



def process_text_for_whatsapp(text):
    # Remove brackets
    pattern = r"\【.*?\】"
    # Substitute the pattern with an empty string
    text = re.sub(pattern, "", text).strip()

    # Pattern to find double asterisks including the word(s) in between
    pattern = r"\*\*(.*?)\*\*"

    # Replacement pattern with single asterisks
    replacement = r"*\1*"

    # Substitute occurrences of the pattern with the replacement
    whatsapp_style_text = re.sub(pattern, replacement, text)

    return whatsapp_style_text

    #Entry Point
def process_whatsapp_message(body):
    wa_id = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
    name = body["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_body = message["text"]["body"]

    if(wa_id not in user_convo):
         user_convo[wa_id]=[]

    user_convo[wa_id].append(message_body)


    if((message_body!=user_convo[wa_id][len(user_convo[wa_id])-2] or len(user_convo[wa_id])==1) and (message_body=="Restart")):
        
                user_states[wa_id]=0
                # data = get_text_message_input(current_app.config["RECIPIENT_WAID"], "Process Canceled, Send your Recipient Details again...")
                data = get_text_message_input(wa_id, "Process canceled. \nSend your recipient details again.")
                send_message(data)
                
    
    elif(message_body!=user_convo[wa_id][len(user_convo[wa_id])-2] or len(user_convo[wa_id])==1 ):


        current_step = user_states.get(wa_id, 0)
        next_step = current_step + 1
        user_states[wa_id] = next_step
        response=""
        
        if(next_step==1):
            inputs["Account Info"] = eval(aiPart.dictOfBankDetails(message_body))
            inputs["Name"]=name
            response=conversation_steps.get(next_step, None) # enter username
            stepsDone[1]=True
            data = get_text_message_input(wa_id, response)

        if(next_step==2 and stepsDone[1]):
            inputs["Username"]=message_body
            response=conversation_steps.get(next_step, None) # enter password
            stepsDone[2]=True
            data = get_text_message_input(wa_id, response)
            

        if(next_step==3 and stepsDone[2]):
            os.environ["PASSWORD"]=message_body
            response=conversation_steps.get(next_step, None) # enter amount
            stepsDone[3]=True
            data = get_text_message_input(wa_id, response)

        if(next_step==4 and stepsDone[3]):
            inputs["Amount"]=message_body
            amount=message_body

            response=conversation_steps.get(next_step, None)+"\n\n"\
            +"\nBenificiery: "+inputs["Account Info"]["name"]\
            +"\nAccount Number: "+inputs["Account Info"]["account number"]\
            +"\nBranch Code: "+inputs["Account Info"]["branch code"]\
            +"\nAmount to Pay: R"+amount\
            +"\nFNB Username: "+inputs["Username"]\
            +"\nFNB Password: "+os.getenv("PASSWORD")

            stepsDone[4]=True
            data = get_text_message_input(wa_id, response)
            
            
        
        if(next_step==5 and message_body=="Confirm" and stepsDone[4]):
            # run the bot
            #print(account_details)
            # data = get_text_message_input(current_app.config["RECIPIENT_WAID"], "Bot Working For You")
            data = get_text_message_input(wa_id, "Bot Working For You")
            send_message(data)
            automateFirst.runBot(inputs)
            response = "Proccessing Payment."
            user_states[wa_id]=0
            data = get_text_message_input(wa_id, response)
        
        


        # Check user's current state and get the next step
        # response = get_next_step(wa_id,account_details)

        # If there's no next step, it means the conversation has ended
        # if not response:
        #     response = "Thank you for providing all the details."
            

        #data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
        
        send_message(data)
        # asyncio.run(send_message(data))

        # loop = asyncio.new_event_loop()
        # # asyncio.set_event_loop(loop)
        # loop.run_until_complete(send_message(data))
        # loop.close()


        # TODO: implement custom function here
        # response = generate_response("Payment Processing")
        # response= "Loading Please Wait"
        # data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
        # send_message(data)

        # automateFirst.runBot(message_body)

        # OpenAI Integration
        # response = generate_response(message_body, wa_id, name)
        # response = process_text_for_whatsapp(response)

        # data = get_text_message_input(current_app.config["RECIPIENT_WAID"], response)
        # send_message(data)

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(send_message(data))
        # loop.close()



def is_valid_whatsapp_message(body):
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )

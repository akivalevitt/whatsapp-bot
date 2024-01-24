import openai
import pandas as pd
from dotenv import load_dotenv
import os

def dictOfBankDetails(message):

    openai.api_key=os.getenv("SECRETKEY")
    #message="Bank: FNB/RMB Account Holder: Akiva Levitt Account Type: FNB Aspire Current Account Account Number: 62461084370 branch code: 250655"
    stream = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Given the following banking details, provide me with a dictionary giving me the: name, account number and branch code. If they are empty populate them with an empty string:"+message}],
        
    )
    accountDetails = stream.choices[0].message.content

    #for debugging
    # accountDetails =str({
    #     "name": "John Do",
    #     "account number": "373974324",
    #     "branch code": "123456"
    #     })
    return accountDetails





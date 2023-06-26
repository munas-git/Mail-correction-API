from fastapi import FastAPI
from mail_corrector import *

app = FastAPI()
mail_fixer = mailCorrection()

@app.post("/basic-correction")
def basic_correction(email:str):

    adjusted_email = mail_fixer.basic_correction(email)
    if email == adjusted_email:
        mail_adjusted = False
    else:
        mail_adjusted = True


    return(
        {
            "oriinal_email": email,
            "mail_adjusted": mail_adjusted,
            "adjusted_email": adjusted_email,
            "mail_active": "True/False.",
        }
    )


@app.post("/advanced-correction")
def advanced_correction(emil:str):
    return(
        {"hello": "world"}
    )
import smtplib
from config import setting
from email.message import EmailMessage
from email.utils import formataddr # Used to specify senders name


sender_email = setting.sender
password = setting.password
mail = EmailMessage()

def send_mail(
        senders_name:str,
        senders_email:str,
        receivers_email: str,
        mail_subject:str,
        mail_content:str
    ) -> bool:
    '''
    Function to send email to individuals.
        Inputs: 
            senders_name (str) : The name of the emails sender i.e individual or organization name.
            senders_email (str) : The email of the sender i.e individual or organizations email.
            receivers_email (str) : The email of the receiver.
            mail_subject:str,
            mail_content:str

        Output
    '''

    # Setting email parameters
    mail["Subject"] = mail_subject
    mail["From"] = formataddr((f"{senders_name}", f"{senders_email}"))
    mail["To"] = receivers_email
    mail["BCC"] = senders_email
    mail.set_content(mail_content)

    # Sending mail
    with smtplib.SMTP() as server:
        print()


if __name__ == "__main__":
    send_mail()
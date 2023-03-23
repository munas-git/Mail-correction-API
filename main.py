import ssl
import smtplib
from config import setting
from email.message import EmailMessage
from email.utils import formataddr


sender_email = setting.sender
password = setting.password


class Mail():
    
    def __init__(self,
                senders_name:str,
                senders_email:str,
                senders_password:str,
                receivers_email: str,
                mail_subject:str,
                mail_content:str,
                senders_email_domain:str
            ) -> None:
        
        '''
        Class to send email to individuals.
            Inputs: 
                senders_name (str) : The name of the emails sender i.e individual or organization name.
                senders_email (str) : The email of the sender i.e individual or organizations email.
                senders_password (str) : The password of the email sender.
                receivers_email (str) : The email of the receiver.
                mail_subject (str) : The subject/title of the email.
                mail_content (str) : The content of the email.
                senders_email_domain (str) : This usually falls after the @ symbol i.e: google, outlook, e.t.c
        '''

        self.senders_name = senders_name
        self.senders_email = senders_email
        self.senders_password = senders_password
        self.receivers_email = receivers_email
        self.mail_subject = mail_subject
        self.mail_content = mail_content
        self.senders_email_domain = senders_email_domain


    def define_mail(self) -> bool:
        '''
        This function takes in all the necessary email parameters and structures them appropriately for the email.
            Input
                self: Everything from class.
            Output
                email_status (Bool) : True/False status mail sending status
        '''

        # Instantiate mail class
        self.mail_cont = EmailMessage()
        # Setting email parameters
        self.mail_cont["Subject"] = self.mail_subject
        self.mail_cont["From"] = formataddr((f"{self.senders_name}", f"{self.senders_email}"))
        self.mail_cont["To"] = self.receivers_email
        self.mail_cont["BCC"] = self.senders_email
        self.mail_cont.set_content(self.mail_content)

        message = 'Mail definition status: True'
        return(message)


    def send_mail(self):

        # Security
        self.context = ssl.create_default_context()

        # Confirm email server
        if self.senders_email_domain == 'google':
            server = 'smtp.gmail.com'
            port = 465
        elif self.senders_email_domain == 'outlook':
            server = 'smtp-mail.outlook.com'
            port = 587
        # Sending mail
        elif self.senders_email_domain == 'icloud':
            server = 'smtp.mail.me.com'
            port = 587


        with smtplib.SMTP_SSL(server, port, context= self.context) as smtp:
            # Attempt to login.
            try:
                smtp.login(self.senders_email, self.senders_password)
                message = "login complete: True"
                # Attempt to send email.
                try:
                    smtp.sendmail(self.senders_email, self.receivers_email, self.mail_cont.as_string())
                    message = "mail sent: True"   
                except Exception:
                    message = "mail sent: False"
            except Exception:
                message = "login complete: False"
        
        return(message)

if __name__ == "__main__":
    content = "Hello Abramam, how are you doing today?\n This is a test for AutoBatch system."
    mail = Mail("AutoBatch", "einsteinmunachiso@gmail.com", "abrahamogudu@gmail.com", "AutoBatch Test", content, 'google')
    mail.define_mail()
    mail.send_mail()
import ssl
import string
import smtplib
from config import setting # Comment this out before production.
from email.message import EmailMessage
from email.utils import formataddr
from difflib import SequenceMatcher


# Comment these out before production.
sender_email = setting.sender 
password = setting.password
tlds = ['net', 'com', 'org', 'io', 'co', 'uk', 'ca', 'dev', 'me']
mail_servers = [
    'outlook', 'gmail', 'icloud', 'yahoo', 'hotmail',
    'aim', 'titan', 'protonmail', 'pm', 'zoho', 'yandex',
    'gmx', 'hubspot', 'mail', 'tutanota', 'geeksforgeeks'
    ]

class Mail():
    
    '''
        Class to send email to individuals.
            Inputs: 
                senders_name (str) : The name of the emails sender i.e individual or organization name.
                senders_email (str) : The email of the sender i.e individual or organizations email.
                senders_password (str) : The password of the email sender.
                mail_subject (str) : The subject/title of the email.
                senders_email_domain (str) : This usually falls after the @ symbol i.e: google, outlook, e.t.c
        '''
    
    def __init__(self,
                senders_name:str,
                senders_email:str,
                senders_password:str,
                mail_subject:str,
                senders_email_domain:str
            ) -> None:
        

        self.senders_name = senders_name
        self.senders_email = senders_email
        self.senders_password = senders_password
        self.mail_subject = mail_subject
        self.senders_email_domain = senders_email_domain


    def define_mail(self) -> str:
        '''
        This function takes in all the necessary email parameters and structures them appropriately for the email.
            Input
                self: Everything from class.
            Output
                email_status (String-Bool) : statement with True/False mail sending status i.e Mail definition status: True
        '''

        # Instantiate mail class
        self.mail_cont = EmailMessage()
        # Setting email parameters
        self.mail_cont["Subject"] = self.mail_subject
        self.mail_cont["From"] = formataddr((f"{self.senders_name}", f"{self.senders_email}"))
        # self.mail_cont["BCC"] = self.senders_email

        message = 'Mail definition status: True'
        return(message)
    

    def send_same_mail(self, receivers_emails: list, mail_content:str):
        '''
        Same mail to all recipients sending function.
            Input:
                receivers_emails (list) : List containing emails of all the receiver.
                mail_content (str) : The content of the email.
                with_analytics (bool), default = False : This is used to tell the function if it should return information about how many mails were sent succesfully or not.
            Output: login/mail status.
        '''
        # Adding receivers email and mail content to mail content build.
        self.mail_cont["BCC"] = ", ".join(receivers_emails)
        self.mail_cont.set_content(mail_content)

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

        # if with_analytics == True
        with smtplib.SMTP_SSL(server, port, context= self.context) as smtp:
            # Attempt to login.
            try:
                smtp.login(self.senders_email, self.senders_password)
                # Attempt to send email.
                message = "login complete: True"
                try:
                    smtp.sendmail(self.senders_email, receivers_emails, self.mail_cont.as_string())
                    message = "mail sent: True"   
                except Exception:
                    message = "mail sent: False"
            except Exception:
                message = "login complete: False"
            
            # Clearing 'to' in order to avoid - ValueError: There may be at most 1 To headers in a message
            # del self.mail_cont['To']
        
        return(message)


    def send_custom_mail(self, receivers_email: str, mail_content:str):
        '''
        Mail sending function.
            Input:
                receivers_email (str) : The email of the receiver.
                mail_content (str) : The content of the email.
                with_analytics (bool), default = False : This is used to tell the function if it should return information about how many mails were sent succesfully or not.
            Output: login/mail status.


        '''
        # Adding receivers email and mail content to mail content build.
        self.mail_cont["To"] = receivers_email
        self.mail_cont.set_content(mail_content)

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

        # if with_analytics == True
        with smtplib.SMTP_SSL(server, port, context= self.context) as smtp:
            # smtp.ehlo()  # send the extended hello to our server
            # smtp.starttls()  # tell server we want to communicate with TLS encryption
            # Attempt to login.
            try:
                smtp.login(self.senders_email, self.senders_password)
                # Attempt to send email.
                message = "login complete: True"
                try:
                    smtp.sendmail(self.senders_email, receivers_email, self.mail_cont.as_string())
                    message = "mail sent: True"   
                except Exception:
                    message = "mail sent: False"
            except Exception:
                message = "login complete: False"
            
            # Clearing 'to' in order to avoid - ValueError: There may be at most 1 To headers in a message
            del self.mail_cont['To']
        
        return(message)
    

class mailCorrection():

    """
    This class handles all activities related to mail correction attempts.
    From basic attempts with simple rules to more advanced attempts with
    attempts that consider a much broader size of rules as compared to the basic attempt.

    Inputs
        tlds (list) : List of all valid mail top-level-domains ie. co, com, uk, e.t.c.
        mail_servers (list) : List of all valid mail servers ie. gmail, outlook, e.t.c
    """
    
    def __init__(self, tlds: list, mail_servers: list):

        self.tlds = tlds
        self.mail_servers = mail_servers
        self.max_tld_score = 0
        self.max_server_score = 0
        self.correct_tld = ''
        self.correct_server = ''
        self.punctuations = string.punctuation.replace(".", "").replace('@', '')
        self.new_mail_list = []

    
    def basic_attempt(self, wrong_mail: str) -> str:
        """
        This function handles basic attempts to correct invalid/wrong email addresses,
        it consideres only basic email validation rules and makes necessary adjustments.
        """

        # Handlig punctuations in wrong positions.
        wrong_mail_post_at = wrong_mail.split('@')[1]

        for punctuation in self.punctuations:
            if punctuation in wrong_mail_post_at:
                wrong_mail_post_at = wrong_mail_post_at.replace(punctuation, ".").strip('.')

        for mail_part in wrong_mail_post_at.split('.'):
            if mail_part != '':
                self.new_mail_list.append(mail_part)
        mail = "@"+".".join(self.new_mail_list)
        wrong_mail = wrong_mail.split('@')[0]+mail

        # Handling top level domains.
        for tld in self.tlds:
            tld_score = SequenceMatcher(a=wrong_mail.split('.')[-1], b=tld).quick_ratio() # Checking scores for input TLDs and list of correct TLDs
            if tld_score > self.max_tld_score:
                self.max_tld_score, self.correct_tld = tld_score, tld # Updating scores and correct TLD

        # Handling mail servers.
        for mail_server in self.mail_servers:
            server_score = SequenceMatcher(a=wrong_mail.split('@')[1], b=mail_server).quick_ratio() # Checking scores for input server and list of correct servers
            if server_score > self.max_server_score:
                self.max_server_score, self.correct_server = server_score, mail_server

        correct_mail = wrong_mail.replace(wrong_mail.split('@')[1], self.correct_server)+"."+self.correct_tld
        return(correct_mail)
    

    def advanced_attempt(self, wrong_mail: str) -> str:
        """
        This function handles advanced attempts to correct invalid/wrong email addresses,
        it consideres basic and advanced email validation rules in order to find out what
        is wrong with an email address then makes necessary adjustments in attempt to fix it.
        """
        for tld in self.tlds:
            tld_score = SequenceMatcher(a=wrong_mail.split('.')[-1], b=tld).quick_ratio() # Checking scores for input TLDs and list of correct TLDs
            if tld_score > self.max_tld_score:
                self.max_tld_score, self.correct_tld = tld_score, tld # Updating scores and correct TLD

        for mail_server in self.mail_servers:
            server_score = SequenceMatcher(a=wrong_mail.split('@')[1], b=tld).quick_ratio() # Checking scores for input server and list of correct servers
            if server_score > self.max_server_score:
                self.max_server_score, self.correct_server = server_score, mail_server

        correct_mail = wrong_mail.replace(wrong_mail.split('@')[1], self.correct_server)+"."+self.correct_tld
        return(correct_mail)





if __name__ == "__main__":
    
    # wrong_mail = Mail("AutoBatch No Reply", "einsteinmunachiso@gmail.com", password, "AutoBatch Test", "google")
    # mail_define = wrong_mail.define_mail()
    # print(mail_define)
    # wrong_mail.send_same_mail(["einsteinmunachiso@gmail.com"], "This should work well, do you see other emails?")

    # emails, names = ["kinfe9870@gmail.com", "abrahamogudu@gmail.com", "mosope48@gmail.com", "einsteinmunachiso@gmail.com", "ein", "dat"], ["Kinfe", "Abraham", "Mosope", "einstein", "ein", "dat"]
    # analytics = input("Display analytics? Y/n: ")
    # print("Alright, sending mails to the following individuals email\n")

    # sent = 0
    # not_sent = 0

    # for email, name in zip(emails, names):
    #     print(name, ":", email)
    #     content = f"""Hey {name}, - 2nd test. NO BLOCK ABEG
    #     \n\nI trust this email finds you well. As you are aware, the payroll window is here, and we are thrilled that you get to use our latest version - Bento V3. We are confident that Bento V3 represents our best work yet and we are excited for you to experience its awesomeness.
    #     \n\nAs with all major deployments, there are bound to be some hitches - and there will always be risk of data corruption during a migration but we are working to fix any issues and are confident that the product is stable and will perform optimally during this payroll window.
    #     \n\nWe moved from a 3 bedroom duplex into a waterfront mansion. A few things like our bar stools have not been delivered and we don’t know the best restaurants in the new neighborhood just yet. But we are so proud of this build and are confident that you will love it.
    #     \n\nDig in and experience it. We’ll love to hear your thoughts. And we do ask for some patience. This was a big build - a few things were removed, some added. Happy to discuss our reasoning.
    #     \n\nThe best products of course are an ongoing conversation between the users and builders.
    #     \n\nBest regards,
    #     \nEinstein from AutoBatch Team.

        # """
        # mail.send_same_mail(["kinfe9870@gmail.com", "einsteinmunachiso@gmail.com"], "Hello, just another test")

        # send_mail = mail.send_mail(email, content)
        # if analytics.lower() == 'y':
        #     if send_mail == "mail sent: True":
        #         sent += 1
        #     else:
        #         not_sent += 1
        #     print("Number of sent mails:", sent)
        #     print("Number of unsent mails:", not_sent)
        #     import matplotlib.pyplot as plt
        #     plt.pie([7,4,], explode=[0.02, 0.02], wedgeprops=dict(width=.55), labels=["Sent", "Unsent"], autopct='%1.1f%%');
        #     plt.savefig("Mail Status.jpeg")
        #     print("Complete, you can now view pie chart")
        # else:
        #     print("Complete")

    import time

    wrong_mail = input("Enter incorrect email address: ")
    print("Attempting to correct email....")
    time.sleep(2)
    mailc = mailCorrection(tlds, mail_servers)
    correct_mail = mailc.basic_attempt(wrong_mail)
    print(f"The right email should be: '{correct_mail}'")
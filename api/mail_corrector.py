import string
from difflib import SequenceMatcher
punctuations = string.punctuation.replace(".", "")


tlds = ['net', 'com', 'org', 'io', 'co', 'uk', 'ca', 'dev', 'me']
mail_servers = [
    'outlook', 'gmail', 'icloud', 'yahoo', 'hotmail','aim',
    'titan', 'pm', 'zoho', 'yandex', 'gmx', 'hubspot', 'mail',
    'tutanota', 'geeksforgeeks'
    ]


class mailCorrection():

    """
    This class handles all activities related to mail correction attempts.
    From basic attempts with simple rules to more advanced attempts with
    attempts that consider a much broader size of rules as compared to the basic attempt.

    Inputs
        tlds (list) : List of all valid mail top-level-domains ie. co, com, uk, e.t.c.
        mail_servers (list) : List of all valid mail servers ie. gmail, outlook, e.t.c
    """
    
    def __init__(self):

        self.tlds = tlds
        self.mail_servers = mail_servers
        self.max_tld_score = 0
        self.max_server_score = 0
        self.correct_tld = ''
        self.correct_server = ''
        self.punctuations = string.punctuation.replace(".", "").replace('@', '')
        self.new_mail_list = []
        self.must_be_com = ["gmail", "outlook", "yahoo", "icloud", "protonmail"] # List of mail servers that must always end with .com

    
    def basic_correction(self, wrong_mail: str) -> str:
        """
        This function handles basic attempts to correct invalid/wrong email addresses,
        it consideres only basic email validation rules and makes necessary adjustments.
        """

        # Handlig punctuations in wrong positions.
        wrong_mail_post_at_symbol = wrong_mail.split('@')[1]

        for punctuation in self.punctuations:
            if punctuation in wrong_mail_post_at_symbol:
                wrong_mail_post_at_symbol = wrong_mail_post_at_symbol.replace(punctuation, ".").strip('.')

        for mail_part in wrong_mail_post_at_symbol.split('.'):
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
        # Ensuring that gmail, outlook, icloud and yahoo mail always ends up with .com toplevel domain.
        after_at_symbol = correct_mail.split('@')[1]
        server = after_at_symbol.split('.')[0]
        if server in self.must_be_com:
            correct_mail = correct_mail.split('@')[0]+'@'+server+'.com'
        return(correct_mail)
    

    def advanced_correction(self, wrong_mail: str) -> str:
        """
        This function handles advanced attempts to correct invalid/wrong email addresses,
        it consideres basic and advanced email validation rules in order to find out what
        is wrong with an email address then makes necessary adjustments in attempt to fix it.
        """

        email_post_at_symbol = wrong_mail.split("@")[1]
        for punctuation in punctuations:
            if punctuation in email_post_at_symbol: # replacing any symbol that is not a "." after the @ symbol
                email_post_at_symbol = email_post_at_symbol.replace(punctuation, ".").strip('.')
        # List of everything after the @ symbol without extra characters or spaces.
        clean_post_at_symbol = [output for output in email_post_at_symbol.split(".") if output != '']

        if len(clean_post_at_symbol) == 2:
            print(clean_post_at_symbol)
        if len(clean_post_at_symbol) == 3:
            print(clean_post_at_symbol)  
        # for tld in self.tlds:
        #     tld_score = SequenceMatcher(a=wrong_mail.split('.')[-1], b=tld).quick_ratio() # Checking scores for input TLDs and list of correct TLDs
        #     if tld_score > self.max_tld_score:
        #         self.max_tld_score, self.correct_tld = tld_score, tld # Updating scores and correct TLD

        # for mail_server in self.mail_servers:
        #     server_score = SequenceMatcher(a=wrong_mail.split('@')[1], b=tld).quick_ratio() # Checking scores for input server and list of correct servers
        #     if server_score > self.max_server_score:
        #         self.max_server_score, self.correct_server = server_score, mail_server

        # correct_mail = wrong_mail.replace(wrong_mail.split('@')[1], self.correct_server)+"."+self.correct_tld
        # return(correct_mail)
    

def mail_active(mail: str) -> bool:
    """
    This function performs mail active status check by pinging the email address and returning true if it is active and false if it isn't.
    
    INPUT
        mail(str): email address to verify.   
    OUTPUT
        active(bool): The email addresses activity status.
    """

m = mailCorrection()
print(m.advanced_correction("spinalchord@hub..ng&co."))


# For advanced email correction attempts, consider the following
# The position of server and tld. i.e tdl can never come before server
# E.g einstein@gmail.com is valid, einstein@com.gmail is not.
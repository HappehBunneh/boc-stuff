import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import yaml

class Mail():
    def __init__(self, sender_email, sender_password, recipients, f):
        self.email = sender_email
        self.pwd = sender_password
        self.recipients = recipients
        self.file = f

    def sendMail(self):
        for recipient in self.recipients:
            self.msg = MIMEMultipart()
            self.msg['From'] = self.email
            self.msg['To'] = recipient
            self.msg['Subject'] = self.file
            self.attachment = open(self.file, 'rb')
            p = MIMEBase('application', 'octet-stream')
            p.set_payload((self.attachment).read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % self.file)
            self.msg.attach(p)
            self.s = smtplib.SMTP('smtp.gmail.com', 587)
            self.s.starttls()
            self.s.login(self.email, self.pwd)
            self.s.sendmail(self.email, recipient, self.msg.as_string())
            self.s.quit()
    
if __name__ == '__main__':
    with open('config.yaml', 'r') as f:
        config = yaml.load(f)  
        pwd = config['emailpwd']
        fromaddr = config['emailusr']
        toaddr = config['recipients']
    sender = Mail(fromaddr, pwd, toaddr, 'buffer.txt')
    sender.sendMail()

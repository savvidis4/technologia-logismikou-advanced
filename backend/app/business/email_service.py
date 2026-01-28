from email.message import EmailMessage
import smtplib


class EmailService:

    def __init__(self):
        self.user = None
        self.sender = "uniwabanking@gmail.com"
        self.password = "xwyfttknmpngfhwx"
        self.recipient = None
        self.message = None
        self.theme = None
        self.ver = False
        self.new = False

    def set_email_data(self, user, theme, mess, ver, new):
        self.user = user
        self.theme = theme
        self.message = mess
        self.recipient = [user]
        self.ver = ver
        self.new = new

    def send_email(self):

        email = EmailMessage()
        email["From"] = self.sender
        email["To"] = self.recipient
        email["Subject"] = self.theme
        email.set_content(message)

        if self.ver and not self.new:
            message = {"title":"Verify Email","message":"Please check the inbox of the email you used"}
        elif self.ver and self.new:
            message = {"title":"Verify New Email","message":"Please check the inbox of the new email you used"}

        smtp = smtplib.SMTP("smtp.gmail.com", port=587)
        smtp.starttls()
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.recipient, email.as_string())
        smtp.quit()

        print('SENT')
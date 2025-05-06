# Import smtplib for the actual sending function
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


def send_email(subject="No subject", content="I am boring"):
    mail_host = "smtp.163.com"
    mail_user = "yuetan@163.com"
    mail_pw = "********"  # 授权码
    sender = "yuetan@163.com"
    receiver = "yuetan@163.com"

    # Create the container (outer) email message.
    msg = MIMEText(content, "plain", "utf-8")
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        smtp = smtplib.SMTP_SSL(mail_host, 994)  # 实例化smtp服务器
        smtp.login(mail_user, mail_pw)  # 登录
        smtp.sendmail(sender, receiver, msg.as_string())
        print("Email send successfully")
    except smtplib.SMTPException:
        print("Error: email send failed")


if __name__ == '__main__':
    send_email(subject="Training finished", content="I am boring")

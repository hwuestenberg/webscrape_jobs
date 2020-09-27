import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def tst_msg():
    text = """\
    Subject: Peter's update


    Hello there,
    Peter is interested into your feelings about the world. Please, share any thoughts!


    This message is sent from P. Pandaslowski.
    """

    html = """\
    <html>
      <body>
        <p>Hello there,<br>
           it is Peter. Shall we?<br>
           <a href="http://www.youtube.com">Youtube</a> 
           Some more random text.
        </p>
      </body>
    </html>
    """

    return text, html


def send_peters_update(text, html):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ppandaslowski@gmail.com"  # Enter your address
    receiver_email = "ppandaslowski@gmail.com"  # Enter receiver address
    password = input("Type your password and press enter: ")


    # Define MIME message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Peter's update"
    message["From"] = sender_email
    message["To"] = receiver_email


    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")


    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)  # HTML must be LAST


    # Begin safe connection, login and send message
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        # server.sendmail(sender_email, receiver_email, message)  # Only plain text
        server.sendmail(sender_email, receiver_email, message.as_string())  # MIME
        print(f"Message sent to {receiver_email}")


    return 1


if __name__ == '__main__':

    txt, ht = tst_msg()
    send_peters_update(txt, ht)


# port = 587  # For starttls
# smtp_server = "smtp.gmail.com"
# sender_email = "ppandaslowski@gmail.com"
# receiver_email = "ppandaslowski@gmail.com"
#
#
# password = input("Type your password and press enter:")
#
#
# message = """\
# Subject: Test message
#
# This message is sent from P. Pandaslowski."""
#
#
# context = ssl.create_default_context()
# with smtplib.SMTP(smtp_server, port) as server:
#     server.ehlo()  # Can be omitted
#     server.starttls(context=context)
#     server.ehlo()  # Can be omitted
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)
#

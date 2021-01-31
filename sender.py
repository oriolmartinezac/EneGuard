import os
import smtplib

def send_email(option, price, url):

    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = 'EneGuard'
        body = 'Option: '+str(option)+' is in a good discount.\nLink: '+url+'\nThe price is: '+str(price)+' euros'
        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

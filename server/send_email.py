import protonmail
import os
from dotenv import load_dotenv


async def send_email(token, email):
    load_dotenv()
    password = os.getenv('PROTON_PW')
    client = protonmail.core.ProtonmailClient()
    client.login("commons-team@proton.me", password)

    # send mails
    client.send_mail(
        [email],
        "Your Commons verification token",
        f"Your verification token is {token}"
    )

    client.destroy()

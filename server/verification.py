import random
import asyncio
import protonmail
import os
import datetime
from dotenv import load_dotenv

verification_token = {}

# methods here only tested visually because this relies on a web scraper


async def start_verify(email):
    token = random.randint(100000, 999999)
    now = datetime.datetime.now()
    if email in verification_token:
        _, last_request = verification_token[email]
        if now - datetime.timedelta(seconds=120) > last_request:
            verification_token[email] = (token, now)
        else:
            print('[INFO] Send email request rejected; still waiting for time out.')
            return False
    else:
        verification_token[email] = (token, now)
    asyncio.create_task(send_email(token, email))
    return True


def check_token(email, token):
    return verification_token[email][0] == int(token)


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

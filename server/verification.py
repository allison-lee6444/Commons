import random
import asyncio
import protonmail
import os
from dotenv import load_dotenv

verification_token = {}

# methods here only tested visually because this relies on a web scraper


async def start_verify(email):
    token = random.randint(100000, 999999)
    verification_token[email] = token
    asyncio.create_task(send_email(token, email))


def check_token(email, token):
    return verification_token[email] == token


# usage: asyncio.run(start_verify(email))

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

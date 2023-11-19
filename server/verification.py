from send_email import send_email
import random
import asyncio

verification_token = {}


async def start_verify(email):
    token = random.randint(100000, 999999)
    verification_token[email] = token
    asyncio.create_task(send_email(token, email))


def check_token(email, token):
    return verification_token[email] == token

# usage: asyncio.run(start_verify(email))

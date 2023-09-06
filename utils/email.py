import asyncio


async def send_welcome_email(email: str) -> None:
    await asyncio.sleep(5)      # simulate email sending...
    print(f'Welcome email sent to: {email}')

import asyncio

from utils.logger import log_email_activity


async def send_welcome_email(email: str) -> None:
    await asyncio.sleep(5)      # simulate email sending service processing...
    log_email_activity(email, 'welcome email sent')


async def send_farewell_email(email: str) -> None:
    await asyncio.sleep(5)      # simulate email sending service processing...
    log_email_activity(email, 'farewell email sent')


async def send_book_order_email(email: str) -> None:
    await asyncio.sleep(5)      # simulate email sending service processing...
    log_email_activity(email, 'book order email sent')

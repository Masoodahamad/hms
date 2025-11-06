from concurrent.futures import ThreadPoolExecutor
from flask import current_app
import logging
import time

_executor = ThreadPoolExecutor(max_workers=2)

def _send(email_to: str, subject: str, body: str):
    # Simulated email send
    logging.getLogger(__name__).info("Sending email to %s: %s", email_to, subject)
    time.sleep(0.5)  # simulate latency
    return {"to": email_to, "subject": subject, "ok": True}

def send_email(email_to: str, subject: str, body: str, background: bool = True):
    if background:
        return _executor.submit(_send, email_to, subject, body)
    return _send(email_to, subject, body)

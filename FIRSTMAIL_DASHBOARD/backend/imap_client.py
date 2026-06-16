# backend/imap_client.py

import email
import imaplib

from concurrent.futures import ThreadPoolExecutor

from mail_parser import parse_message
from services import get_sender_mails


IMAP_HOST = "imap.firstmail.ltd"
IMAP_PORT = 993


class IMAPClient:

    def __init__(
        self,
        email_address,
        password
    ):

        self.email_address = email_address
        self.password = password

        self.mail = None

    def connect(self):

        self.mail = imaplib.IMAP4_SSL(
            IMAP_HOST,
            IMAP_PORT
        )

        self.mail.login(
            self.email_address,
            self.password
        )

    def disconnect(self):

        if self.mail:

            try:
                self.mail.logout()
            except:
                pass

    def get_latest_messages(
        self,
        limit=20
    ):

        self.mail.select("INBOX")

        status, data = self.mail.search(
            None,
            "ALL"
        )

        if status != "OK":
            return []

        message_ids = data[0].split()

        message_ids = message_ids[-limit:]

        messages = []

        for msg_id in reversed(
            message_ids
        ):

            status, msg_data = self.mail.fetch(
                msg_id,
                "(RFC822)"
            )

            if status != "OK":
                continue

            raw_email = msg_data[0][1]

            msg = email.message_from_bytes(
                raw_email
            )

            messages.append(
                msg
            )

        return messages


def check_account(
    email_address,
    password,
    service_id
):

    client = IMAPClient(
        email_address,
        password
    )

    try:

        client.connect()

        messages = client.get_latest_messages(
            limit=30
        )

        allowed_senders = (
            get_sender_mails(
                service_id
            )
        )

        for message in messages:

            parsed = parse_message(
                message
            )

            sender = (
                parsed["sender"]
                .lower()
            )

            if allowed_senders:

                if not any(
                    s.lower() in sender
                    for s in allowed_senders
                ):
                    continue

            if parsed["code"]:

                return {
                    "email": email_address,
                    "status": "success",
                    "sender": parsed["sender"],
                    "subject": parsed["subject"],
                    "date": parsed["date"],
                    "code": parsed["code"]
                }

        return {
            "email": email_address,
            "status": "not_found",
            "code": None
        }

    except Exception as e:

        return {
            "email": email_address,
            "status": "error",
            "error": str(e)
        }

    finally:

        client.disconnect()


def check_accounts(
    accounts,
    service_id,
    max_workers=20
):
    """
    accounts = [
        {
            "email": "...",
            "password": "..."
        }
    ]
    """

    results = []

    with ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:

        futures = []

        for account in accounts:

            futures.append(
                executor.submit(
                    check_account,
                    account["email"],
                    account["password"],
                    service_id
                )
            )

        for future in futures:

            results.append(
                future.result()
            )

    return results
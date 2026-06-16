# backend/mail_parser.py

import re
from email.message import Message
from email.utils import parsedate_to_datetime


CODE_PATTERNS = [
    r"\b\d{4}\b",
    r"\b\d{5}\b",
    r"\b\d{6}\b",
    r"\b\d{7}\b",
    r"\b\d{8}\b"
]


def get_email_body(message: Message) -> str:

    body = ""

    if message.is_multipart():

        for part in message.walk():

            content_type = part.get_content_type()

            if content_type == "text/plain":

                try:

                    body = part.get_payload(
                        decode=True
                    ).decode(
                        errors="ignore"
                    )

                    break

                except Exception:
                    pass

    else:

        try:

            body = message.get_payload(
                decode=True
            ).decode(
                errors="ignore"
            )

        except Exception:
            pass

    return body


def extract_code(text: str):

    for pattern in CODE_PATTERNS:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group()

    return None


def extract_sender(message: Message):

    return message.get(
        "From",
        ""
    )


def extract_subject(message: Message):

    return message.get(
        "Subject",
        ""
    )


def extract_date(message: Message):

    raw_date = message.get(
        "Date"
    )

    if not raw_date:
        return None

    try:

        return parsedate_to_datetime(
            raw_date
        )

    except Exception:

        return None


def parse_message(message: Message):

    body = get_email_body(
        message
    )

    return {
        "sender": extract_sender(
            message
        ),

        "subject": extract_subject(
            message
        ),

        "date": extract_date(
            message
        ),

        "code": extract_code(
            body
        ),

        "body": body
    }
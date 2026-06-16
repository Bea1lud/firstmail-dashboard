# backend/services.py

SERVICES = {
    "telegram": {
        "name": "Telegram",
        "sender_mail": [
            "telegram.org"
        ]
    },

    "tiktok": {
        "name": "TikTok",
        "sender_mail": [
            "tiktok.com"
        ]
    },

    "twitch": {
        "name": "Twitch",
        "sender_mail": [
            "twitch.tv"
        ]
    },

    "discord": {
        "name": "Discord",
        "sender_mail": [
            "discord.com"
        ]
    },

    "steam": {
        "name": "Steam",
        "sender_mail": [
            "steampowered.com",
            "steam"
        ]
    },

    "epic": {
        "name": "Epic Games",
        "sender_mail": [
            "epicgames.com"
        ]
    }
}


def get_services():
    return SERVICES


def get_service(service_id):
    return SERVICES.get(service_id)


def get_sender_mails(service_id):

    service = get_service(service_id)

    if not service:
        return []

    return service["sender_mail"]
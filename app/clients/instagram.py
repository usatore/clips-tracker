from instagrapi import Client
from app.config import settings

def login_to_instagram():
    instagram = Client()
    instagram.login(
        username=settings.INSTAGRAM_USERNAME,
        password=settings.INSTAGRAM_PASSWORD
    )
    return instagram
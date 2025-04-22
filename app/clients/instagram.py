from instagrapi import Client
from app.config import settings


instagram = Client()

instagram.login(
    username=settings.INSTAGRAM_USERNAME,
    password=settings.INSTAGRAM_PASSWORD
)
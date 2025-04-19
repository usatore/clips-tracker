from googleapiclient.discovery import build
from app.config import settings


youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)




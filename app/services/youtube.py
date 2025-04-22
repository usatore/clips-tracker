from datetime import datetime
import isodate
from app.clients.youtube import youtube
from app.services.utils import is_before_date, save_to_csv


def get_uploads_playlist_id(handle: str) -> str:
    request = youtube.channels().list(part='contentDetails', forHandle=handle)
    response = request.execute()
    return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def fetch_videos_chunk(video_ids: list[str]) -> list[dict]:
    request = youtube.videos().list(
        part='snippet,statistics,contentDetails',
        id=','.join(video_ids)
    )
    return request.execute().get('items', [])


def is_shorts(video: dict) -> bool:
    """Проверяет, является ли видео шортсом (меньше 62 секунд)."""
    try:
        duration = video['contentDetails']['duration']
        seconds = isodate.parse_duration(duration).total_seconds()
        return seconds < 62
    except Exception:
        return False


def collect_clips_to_csv(handle: str, user_date_str: str, batch_size: int = 10):
    uploads_playlist_id = get_uploads_playlist_id(handle)
    filename = f"{handle}_youtube_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    next_page_token = None
    shorts_batch = []
    headers = ['Ссылка', 'Просмотры', 'Лайки', 'Дата публикации', 'Длительность']

    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids = [
            item['snippet']['resourceId']['videoId']
            for item in response['items']
        ]

        videos = fetch_videos_chunk(video_ids)

        for video in videos:
            if is_shorts(video) and is_before_date(video.get('snippet', {}).get('publishedAt'), user_date_str):
                video_id = video['id']
                url = f"https://youtube.com/shorts/{video_id}"
                stats = video.get('statistics', {})
                views = stats.get('viewCount', '0')
                likes = stats.get('likeCount', '0')
                published = video.get('snippet', {}).get('publishedAt', '')[:10]
                duration = video.get('contentDetails', {}).get('duration', '')

                shorts_batch.append([url, views, likes, published, duration])

            if len(shorts_batch) == batch_size:
                save_to_csv(filename, shorts_batch, headers, append=True)
                shorts_batch.clear()

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    if shorts_batch:
        save_to_csv(filename, shorts_batch, headers, append=True)
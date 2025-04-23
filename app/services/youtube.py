from datetime import datetime
import isodate
from app.clients.youtube import youtube
from app.services.utils import is_before_date, init_csv_file, append_csv_chunk


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


def collect_yt_clips(handle: str, user_date_str: str, batch_size: int = 10):
    uploads_playlist_id = get_uploads_playlist_id(handle)
    filename = f"{handle}_youtube_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    headers = ['Ссылка', 'Просмотры', 'Лайки', 'Дата публикации']

    init_csv_file(filename, headers)

    next_page_token = None
    batch = []


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
                views = stats.get('viewCount', 'No info')
                likes = stats.get('likeCount', 'No info')
                published = video.get('snippet', {}).get('publishedAt', '')[:10]

                batch.append([url, views, likes, published])

            if len(batch) == batch_size:
                append_csv_chunk(filename, batch)
                batch.clear()

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    if batch:
        append_csv_chunk(filename, batch)
from datetime import datetime
import csv
import isodate
from app.clients.youtube import youtube

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


def save_to_csv(filename: str, video_response: dict, append: bool = False):
    mode = 'a' if append else 'w'
    file_empty = False

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_empty = f.readline() == ''
    except FileNotFoundError:
        file_empty = True

    with open(filename, mode=mode, encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Пишем заголовки только если файл пустой или открываем заново
        if not append or file_empty:
            writer.writerow(['Ссылка', 'Просмотры', 'Лайки', 'Дата публикации', 'Длительность'])

        for item in video_response['items']:
            video_id = item['id']
            url = f"https://youtube.com/shorts/{video_id}"
            stats = item.get('statistics', {})
            snippet = item.get('snippet', {})
            content_details = item.get('contentDetails', {})

            views = stats.get('viewCount', '0')
            likes = stats.get('likeCount', '0')
            published = snippet.get('publishedAt', '')[:10]
            duration = content_details.get('duration', '')

            writer.writerow([url, views, likes, published, duration])

    print(f"CSV файл обновлён: {filename}")



def is_shorts(video: dict) -> bool:
    """Проверяет, является ли видео шортсом (меньше 62 секунд)."""
    try:
        duration = video['contentDetails']['duration']
        seconds = isodate.parse_duration(duration).total_seconds()
        return seconds < 62
    except Exception:
        return False


def is_before_date(item: dict, user_date_str: str) -> bool:
    """
    Проверяет, было ли видео опубликовано до указанной даты.

    :param item: элемент из video_response['items']
    :param user_date_str: дата в формате 'ДД.ММ.ГГГГ'
    :return: True, если видео было опубликовано до user_date_str
    """
    try:
        if not user_date_str:
            return True  # Если дата не передана, считаем, что все видео подходящие

        user_date = datetime.strptime(user_date_str, '%d.%m.%Y').date()
        published_at = item.get('snippet', {}).get('publishedAt')
        if not published_at:
            return False

        published_date = datetime.strptime(published_at[:10], '%Y-%m-%d').date()
        return published_date < user_date

    except Exception as e:
        print(f"Ошибка в is_before_date: {e}")
        return False


def collect_shorts_to_csv(handle: str, user_date_str: str, batch_size: int = 10):
    uploads_playlist_id = get_uploads_playlist_id(handle)
    filename = f"{handle}_youtube_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    next_page_token = None
    shorts_batch = []

    while True:
        # Получаем пачку из playlistItems
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

        # Получаем данные по видео
        videos = fetch_videos_chunk(video_ids)

        # Фильтруем только шортсы
        for video in videos:
            if is_shorts(video) and is_before_date(video, user_date_str):
                shorts_batch.append(video)

            if len(shorts_batch) == batch_size:
                save_to_csv(filename, video_response={'items': shorts_batch}, append=True)
                shorts_batch.clear()

        # Следующая страница
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    # Сохраняем оставшиеся видео
    if shorts_batch:
        save_to_csv(filename, video_response={'items': shorts_batch}, append=True)









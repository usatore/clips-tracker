from datetime import datetime
from app.services.utils import save_to_csv, is_before_date
from app.clients.instagram import instagram


def collect_ig_clips(username: str, user_date_str: str):
    user_id = instagram.user_id_from_username(username)
    medias = instagram.user_clips(user_id)  # Получаем Reels
    filename = f"{username}_instagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    headers = ['Ссылка', 'Просмотры', 'Лайки', 'Дата публикации']

    rows_to_save = []

    for media in medias:
        published_at_ts = media.taken_at.timestamp()
        date_str = datetime.fromtimestamp(published_at_ts).strftime("%d.%m.%Y")
        url = f"https://www.instagram.com/reel/{media.code}/"
        views = media.view_count or 0
        likes = media.like_count or 0

        if is_before_date(published_at_ts, user_date_str, is_timestamp=True):
            rows_to_save.append([url, views, likes, date_str])


    save_to_csv(filename, rows_to_save, headers)





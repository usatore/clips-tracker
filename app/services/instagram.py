from datetime import datetime
from app.services.utils import save_to_csv, is_before_date
from app.clients.instagram import instagram


def fetch_and_save_instagram_reels(username: str, user_date_str: str):
    try:
        user_id = instagram.user_id_from_username(username)
        medias = instagram.user_clips(user_id)  # Получаем Reels

        rows_to_save = []

        for media in medias:
            published_at_ts = media.taken_at.timestamp()
            date_str = datetime.fromtimestamp(published_at_ts).strftime("%d.%m.%Y")
            url = f"https://www.instagram.com/reel/{media.code}/"
            views = media.view_count or 0
            likes = media.like_count or 0

            if is_before_date(published_at_ts, user_date_str, is_timestamp=True):
                rows_to_save.append([url, views, likes, date_str])

        headers = ['Ссылка', 'Просмотры', 'Лайки', 'Дата публикации']
        filename = f"{username}_instagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        save_to_csv(filename, rows_to_save, headers)

    except Exception as e:
        print(f"Ошибка при получении или сохранении рилзов: {e}")


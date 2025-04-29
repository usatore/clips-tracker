from app.services.utils import init_csv_file, append_csv_chunk, is_before_date
from datetime import datetime
from app.clients.instagram import login_to_instagram


def collect_ig_clips(username: str, user_date_str: str, batch_size: int = 10):

    instagram = login_to_instagram()

    user = instagram.user_info_by_username_v1(username)
    user_id = user.pk
    medias = instagram.user_medias_v1(user_id)
    medias = [media for media in medias if media.media_type == 2 and media.product_type == 'clips']
    filename = f"{username}_instagram_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    headers = ['Ссылка', 'Просмотры', 'Лайки', 'Дата публикации']

    init_csv_file(filename, headers)

    batch = []

    for media in medias:
        published_at_ts = media.taken_at.timestamp()
        if is_before_date(published_at_ts, user_date_str, is_timestamp=True):
            date_str = datetime.fromtimestamp(published_at_ts).strftime("%d.%m.%Y")
            url = f"https://www.instagram.com/reel/{media.code}"
            views = media.view_count or 'No info'
            likes = media.like_count or 'No info'

            batch.append([url, views, likes, date_str])

            if len(batch) == batch_size:
                append_csv_chunk(filename, batch)
                batch.clear()

    if batch:
        append_csv_chunk(filename, batch)

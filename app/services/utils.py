from datetime import datetime
import csv


def is_before_date(published_at, user_date_str: str, is_timestamp: bool = False) -> bool:
    """
    Проверяет, было ли видео опубликовано до указанной даты.

    :param published_at: дата публикации (строка ISO 8601 или timestamp)
    :param user_date_str: дата в формате 'ДД.ММ.ГГГГ'
    :param is_timestamp: если True, published_at — это Unix timestamp
    :return: True, если видео было опубликовано до user_date_str
    """
    try:
        if not user_date_str:
            return True

        user_date = datetime.strptime(user_date_str, '%d.%m.%Y').date()
        if not published_at:
            return False

        if is_timestamp:
            published_date = datetime.fromtimestamp(published_at).date()
        else:
            published_date = datetime.strptime(published_at[:10], '%Y-%m-%d').date()

        return published_date < user_date

    except Exception as e:
        print(f"Ошибка в is_before_date: {e}")
        return False


def init_csv_file(filename: str, headers: list[str]):
    """Создаёт CSV-файл с заголовками."""
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)


def append_csv_chunk(filename: str, rows: list[list]):
    """Добавляет строки в существующий CSV без заголовков."""
    with open(filename, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
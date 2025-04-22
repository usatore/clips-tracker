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


def save_to_csv(filename: str, rows: list[list], headers: list[str], append: bool = False):
    """
    Сохраняет данные в CSV.

    :param filename: имя CSV-файла
    :param rows: список строк для записи (каждая строка — список значений)
    :param headers: список заголовков
    :param append: добавлять в файл (True) или перезаписать (False)
    """
    mode = 'a' if append else 'w'
    file_empty = False

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            file_empty = f.readline() == ''
    except FileNotFoundError:
        file_empty = True

    with open(filename, mode=mode, encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)

        if not append or file_empty:
            writer.writerow(headers)

        for row in rows:
            writer.writerow(row)

    print(f"CSV файл обновлён: {filename}")
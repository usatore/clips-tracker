from app.services.youtube import collect_shorts_to_csv


def extract_youtube_handle(link: str) -> str | None:
    """Проверяет, является ли ссылка на YouTube и извлекает handle."""
    if "youtube.com" not in link:
        return None
    if '@' in link:
        return '@' + link.split('@')[-1].split('/')[0]
    return link if link.startswith('@') else None


def extract_tiktok_handle(link: str) -> str | None:
    """Заглушка для TikTok — пока не реализована."""
    # Пример: https://www.tiktok.com/@username
    if "tiktok.com" not in link:
        return None
    if '@' in link:
        return '@' + link.split('@')[-1].split('/')[0]
    return None


def extract_instagram_handle(link: str) -> str | None:
    """Заглушка для Instagram — пока не реализована."""
    # Пример: https://www.instagram.com/username/
    if "instagram.com" not in link:
        return None
    parts = link.strip('/').split('/')
    if len(parts) >= 4:
        return parts[3]
    elif len(parts) == 2:
        return parts[-1]
    return None


def process_youtube():
    while True:
        try:
            link = input("Введите ссылку на YouTube-канал или handle (например, https://youtube.com/@имя): ").strip()
            handle = extract_youtube_handle(link)

            if not handle:
                print("Похоже, это невалидная ссылка на YouTube. Попробуйте снова.\n")
                continue

            date_str = input("Введите дату в формате ДД.ММ.ГГГГ (или оставьте пустым): ").strip()
            collect_shorts_to_csv(handle, user_date_str=date_str)
            print("Готово!\n")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C.")
            break
        except Exception as e:
            print(f"Ошибка: {e}\n")


def process_tiktok():
    print("Обработка TikTok пока не реализована.")


def process_instagram():
    print("Обработка Instagram пока не реализована.")


def main():
    print("Добро пожаловать!\n")

    while True:
        try:
            platform = input("Выберите платформу (youtube / tiktok / instagram) или 'exit': ").strip().lower()

            if platform == 'exit':
                print("Выход.")
                break
            elif platform == 'youtube':
                process_youtube()
            elif platform == 'tiktok':
                process_tiktok()
            elif platform == 'instagram':
                process_instagram()
            else:
                print("Неизвестная платформа. Попробуйте снова.\n")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C.")
            break


if __name__ == "__main__":
    main()

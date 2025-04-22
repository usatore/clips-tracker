from app.services.youtube import collect_clips_to_csv as collect_yt_clips
from app.services.instagram import fetch_and_save_instagram_reels as collect_ig_clips


def process_youtube():
    while True:
        try:
            handle = input("Введите handle YouTube-канала: ").strip()

            date_str = input("Введите дату в формате ДД.ММ.ГГГГ (или оставьте пустым): ").strip()
            collect_yt_clips(handle, user_date_str=date_str)
            print("Готово!\n")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C.")
            break
        except Exception as e:
            print(f"Ошибка: {e}\n")



def process_instagram():
    while True:
        try:
            handle = input("Введите handle Instagram-профиля: ").strip()

            date_str = input("Введите дату в формате ДД.ММ.ГГГГ (или оставьте пустым): ").strip()
            collect_ig_clips(handle, user_date_str=date_str, csv_filename='kekus.csv')
            print("Готово!\n")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C.")
            break
        except Exception as e:
            print(f"Ошибка: {e}\n")


def process_youtube():
    while True:
        try:
            handle = input("Введите handle YouTube-канала: ").strip()

            date_str = input("Введите дату в формате ДД.ММ.ГГГГ (или оставьте пустым): ").strip()
            collect_yt_clips(handle, user_date_str=date_str)
            print("Готово!\n")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C.")
            break
        except Exception as e:
            print(f"Ошибка: {e}\n")


def process_instagram():
    while True:
        try:
            handle = input("Введите handle Instagram-профиля: ").strip()

            date_str = input("Введите дату в формате ДД.ММ.ГГГГ (или оставьте пустым): ").strip()
            collect_ig_clips(handle, user_date_str=date_str)
            print("Готово!\n")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C.")
            break
        except Exception as e:
            print(f"Ошибка: {e}\n")



def run_cli():
    print("Добро пожаловать в ClipTracker!\n")

    while True:
        try:
            platform = input("Выберите платформу (youtube / instagram) или 'exit': ").strip().lower()

            if platform == 'exit':
                print("Выход.")
                break
            elif platform == 'youtube':
                process_youtube()
            elif platform == 'instagram':
                process_instagram()
            else:
                print("Неизвестная платформа. Попробуйте снова.\n")

        except KeyboardInterrupt:
            print("\nВыход по Ctrl+C.")
            break



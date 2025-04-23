from app.services.youtube import collect_yt_clips
from app.services.instagram import collect_ig_clips

def process_platform(platform_name: str, collect_func):
    while True:
        try:
            handle = input(f"Введите handle {platform_name}-профиля: ").strip()
            date_str = input("Введите дату в формате ДД.ММ.ГГГГ (или оставьте пустым): ").strip()
            collect_func(handle, user_date_str=date_str)
            print("Готово!\n")
        except Exception as e:
            print(f"Ошибка: {e}\n")


def run_cli():
    print("Добро пожаловать в ClipsTracker!\n")

    while True:
        platform = input("Выберите платформу (youtube / instagram) или 'exit': ").strip().lower()
        if platform == 'exit':
            print("Выход.")
            break
        elif platform == 'youtube':
            process_platform("YouTube", collect_yt_clips)
        elif platform == 'instagram':
            process_platform("Instagram", collect_ig_clips)
        else:
            print("Неизвестная платформа. Попробуйте снова.\n")




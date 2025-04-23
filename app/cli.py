from app.services.youtube import collect_yt_clips
from app.services.instagram import collect_ig_clips

PLATFORMS = {
    "youtube": {
        "name": "YouTube",
        "collector": collect_yt_clips
    },
    "instagram": {
        "name": "Instagram",
        "collector": collect_ig_clips
    }
}

def process_platform(platform_name: str, collect_func):
    while True:
        try:
            handle = input(f"Введите username/handle {platform_name}-профиля (или 'back'): ").strip()
            if handle.lower() == 'back':
                break
            date_str = input("Введите дату в формате ДД.ММ.ГГГГ (или оставьте пустым): ").strip()
            collect_func(handle, user_date_str=date_str)
            print("Готово!\n")
        except Exception as e:
            print(f"Ошибка: {e}\n")

def run_cli():
    print("Добро пожаловать в ClipsTracker!\n")

    while True:
        print("Доступные платформы:")
        for key in PLATFORMS:
            print(f" - {key}")
        platform = input("\nВыберите платформу или 'exit': ").strip().lower()

        if platform == 'exit':
            print("Выход.")
            break
        elif platform in PLATFORMS:
            platform_data = PLATFORMS[platform]
            process_platform(platform_data["name"], platform_data["collector"])
        else:
            print("Неизвестная платформа. Попробуйте снова.\n")



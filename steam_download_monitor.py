import os
import time
import winreg
import re


# -------------------------------
# 1. Найти путь установки Steam через реестр
# -------------------------------
def get_steam_path():
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Valve\Steam"
        )
        steam_path, _ = winreg.QueryValueEx(key, "SteamPath")
        return steam_path
    except Exception:
        return None


# -------------------------------
# 2. Найти лог загрузок Steam
# -------------------------------
def get_content_log_path(steam_path):
    return os.path.join(steam_path, "logs", "content_log.txt")


# -------------------------------
# 3. Получить последнюю скачиваемую игру из логов
# -------------------------------
def get_current_game(log_path):
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # ищем строки типа "Downloading app XXXX"
        for line in reversed(lines):
            match = re.search(r"Downloading\s+app\s+(\d+)", line)
            if match:
                return f"AppID {match.group(1)}"

        return "Не удалось определить игру"

    except Exception:
        return "Лог недоступен"


# -------------------------------
# 4. Получить скорость загрузки (примерно)
# -------------------------------
def get_download_speed(log_path):
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        # ищем строки со скоростью (Steam пишет bytes/sec)
        for line in reversed(lines):
            match = re.search(r"DownloadSpeed:\s+([\d\.]+)", line)
            if match:
                speed = float(match.group(1))
                return speed / (1024 * 1024)  # MB/s

        return 0.0

    except Exception:
        return 0.0


# -------------------------------
# 5. Проверка: загрузка на паузе или нет
# -------------------------------
def is_paused(log_path):
    try:
        with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for line in reversed(lines):
            if "Pausing download" in line:
                return True
            if "Resuming download" in line:
                return False

        return False

    except Exception:
        return False


# -------------------------------
# MAIN
# -------------------------------
def main():
    steam_path = get_steam_path()

    if not steam_path:
        print("❌ Steam не найден в реестре")
        return

    log_path = get_content_log_path(steam_path)

    if not os.path.exists(log_path):
        print("❌ Лог загрузок Steam не найден:", log_path)
        return

    print("✅ Steam найден:", steam_path)
    print("📄 Лог загрузок:", log_path)

    print("\n=== Мониторинг загрузки (5 минут) ===\n")

    for minute in range(1, 6):
        game = get_current_game(log_path)
        paused = is_paused(log_path)
        speed = get_download_speed(log_path)

        print(f"⏱ Минутa {minute}/5")
        print(f"🎮 Игра: {game}")

        if paused or speed == 0:
            print("⏸ Загрузка на паузе или нет активных загрузок")
        else:
            print(f"⬇ Скорость загрузки: {speed:.2f} MB/s")

        print("-" * 40)

        time.sleep(60)


if __name__ == "__main__":
    main()

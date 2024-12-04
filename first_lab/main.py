import subprocess

import psutil


def display_system_temperatures():
    """
    Функция для отображения текущих температур всех доступных датчиков.
    """
    try:
        # Проверка наличия сенсоров температуры
        if not hasattr(psutil, "sensors_temperatures"):
            print(
                "Температурные датчики не" "поддерживаются на этом устройстве."
            )
            return

        # Получение и вывод данных о температуре
        temps = psutil.sensors_temperatures()

        if not temps:
            print("Нет доступных датчиков температуры.")
            return

        print("Температуры датчиков:")
        for sensor, entries in temps.items():
            print(f"\nДатчик: {sensor}")
            for entry in entries:
                print(f"  {entry.label or 'N/A'}: {entry.current}°C")
    except Exception as e:
        print(f"Ошибка при чтении температуры: {e}")


def display_fan_speeds():
    """
    Функция для отображения скорости
    вращения вентиляторов с использованием утилиты sensors.
    """
    try:
        # Запуск команды sensors и считывание данных о вентиляторах
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        output = result.stdout

        print("\nСкорость вращения вентиляторов:")
        print(output)
    except FileNotFoundError:
        print(
            "Утилита 'sensors' не установлена."
            "Установите её с помощью: sudo apt install lm-sensors"
        )
    except Exception as e:
        print(f"Ошибка при чтении скорости вентиляторов: {e}")


if __name__ == "__main__":
    print("Измерение физических величин")
    display_system_temperatures()
    display_fan_speeds()

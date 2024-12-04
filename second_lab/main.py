import json
import time

import psutil


def get_temperature_data():
    """
    Функция для получения текущей температуры с датчиков.
    Возвращает словарь {название датчика: температура}.
    """
    temps = psutil.sensors_temperatures()  # Получаем данные о температуре
    results = {}

    if not temps:
        print("Нет доступных датчиков температуры.")
        return results

    for sensor, entries in temps.items():
        for entry in entries:
            label = (
                entry.label or sensor
            )  # Если метка пустая, используй название сенсора
            results[label] = entry.current  # Фиксируем текущую температуру

    return results


def collect_measurements(interval, count):
    """
    Проводит серию измерений температуры с заданным интервалом.
    :param interval: интервал времени между измерениями (в секундах).
    :param count: количество измерений.
    :return: список замеров, где каждый элемент -
    это данные одного измерения (словарь).
    """
    measurements = []  # Список для хранения результатов

    print(
        f"Начинаем серию замеров: {count} измерений"
        f"с интервалом {interval} секунд."
    )
    for i in range(count):
        print(f"\nЗамер {i + 1}...")
        data = get_temperature_data()  # Собираем текущие данные о температуре
        measurements.append(data)  # Добавляем данные в список
        print(data)  # Выводим текущие данные в консоль

        if (
            i < count - 1
        ):  # Ждём перед следующим замером (кроме последнего замера)
            time.sleep(interval)

    print("\nСерия измерений завершена.")
    return measurements


def save_to_json(data, filename="measurements.json"):
    """
    Сохраняет данные в JSON файл.
    :param data: данные для сохранения.
    :param filename: имя файла для сохранения
    (по умолчанию 'measurements.json').
    """
    try:
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Результаты измерений сохранены в файл {filename}")
    except Exception as e:
        print(f"Ошибка сохранения данных в файл {filename}: {e}")


if __name__ == "__main__":
    # Параметры измерений
    # Интервал времени между измерениями (в секундах)
    interval_between_measurements = 2
    # Количество замеров
    number_of_measurements = 10

    # Запуск серии измерений
    results = collect_measurements(
        interval_between_measurements, number_of_measurements
    )

    # Сохранение результатов в JSON файл
    save_to_json(results, "measurements.json")

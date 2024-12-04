import subprocess
import time

import matplotlib.pyplot as plt


def get_fan_speeds():
    """
    Функция для получения текущей скорости вращения вентиляторов.
    Использует команду `sensors` для доступа к данным.
    Возвращает словарь {название вентилятора: скорость RPM}.
    """
    fan_data = {}
    try:
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        output = result.stdout.splitlines()

        for line in output:
            if "RPM" in line:  # Ищем строки со скоростями вентиляторов
                parts = line.split()
                fan_name = parts[0].strip(":")  # Название вентилятора
                rpm = int(parts[1])  # Значение RPM
                fan_data[fan_name] = rpm
    except Exception as e:
        print(f"Ошибка при получении данных RPM: {e}")

    return fan_data


def collect_measurements_rpm(interval, count, target_fan=None):
    """
    Проводит серию измерений скорости вращения
    вентиляторов с заданным интервалом.
    :param interval: Интервал времени между измерениями (в секундах).
    :param count: Количество измерений.
    :param target_fan: Название интересующего вентилятора.
    Если None, берётся первый доступный.
    :return: Список кортежей (время, значение RPM).
    """
    measurements = []  # Храним список (время, значение RPM)
    time_elapsed = 0  # Время от начала измерений

    print(
        f"Собираем значения скорости вращения вентиляторов с интервалом"
        f"{interval} секунд ({count} измерений)."
    )
    for i in range(count):
        print(f"\nИзмерение {i + 1}...")
        data = get_fan_speeds()

        if not data:
            print("Скорость вентиляторов недоступна. Пропускаем измерение.")
            continue

        # Если вентилятор не указан, берём первый
        if not target_fan:
            target_fan = next(
                iter(data)
            )  # Берём имя первого найденного вентилятора

        if target_fan in data:
            measurements.append(
                (time_elapsed, data[target_fan])
            )  # Сохраняем время и RPM
            print(
                f"Время: {time_elapsed}s, {target_fan}: {data[target_fan]} RPM"
            )
        else:
            print(f"Вентилятор {target_fan} не найден. Пропускаем измерение.")

        time_elapsed += interval  # Увеличиваем прошедшее время
        if i < count - 1:  # Ждём между измерениями (кроме последнего)
            time.sleep(interval)

    print("\nСерия измерений завершена.")
    return measurements


def plot_measurements(measurements, fan_name):
    """
    Построение графика измерений.
    :param measurements: Список кортежей (время, значение RPM).
    :param fan_name: Название вентилятора.
    """
    if not measurements:
        print("Нет данных для построения графика.")
        return

    # Разбиваем измерения на две оси: Время (ось Y) и скорость (ось X)
    times = [item[0] for item in measurements]
    values = [item[1] for item in measurements]

    plt.figure(figsize=(10, 6))  # Размер графика
    plt.plot(
        values, times, marker="o", linestyle="-", color="g", label=fan_name
    )
    plt.xlabel("Скорость вращения (RPM)")  # Подпись оси X
    plt.ylabel("Время (s)")  # Подпись оси Y

    # Название графика
    plt.title(f"График изменений скорости {fan_name} с течением времени")
    plt.legend()
    plt.grid(True)
    plt.gca().invert_yaxis()  # Инверсия оси Y, чтобы время шло сверху вниз
    plt.savefig("graph.png")
    print("График сохранён в файл graph.png")


if __name__ == "__main__":
    # Параметры измерений
    # Интервал времени между измерениями (в секундах)
    interval_between_measurements = 2
    # Количество измерений
    number_of_measurements = 10
    fan_to_track = 'fan1'

    # Сбор данных о вентиляторах
    results = collect_measurements_rpm(
        interval_between_measurements, number_of_measurements, fan_to_track
    )

    # Построение графика распределения
    if results:
        plot_measurements(results, fan_to_track or "Заданный вентилятор")

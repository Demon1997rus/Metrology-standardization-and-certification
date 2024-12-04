import time
import subprocess
import matplotlib.pyplot as plt
import numpy as np


def get_fan_speeds():
    """
    Функция для получения текущей скорости вращения вентиляторов.
    Использует команду `sensors` для доступа к данным.
    Возвращает словарь {название вентилятора: скорость RPM}.
    """
    fan_data = {}
    try:
        # Запускаем команду sensors и получаем её вывод
        result = subprocess.run(["sensors"], capture_output=True, text=True)
        output = result.stdout.splitlines()

        # Парсим вывод: ищем строки со значениями RPM
        for line in output:
            if "RPM" in line:
                parts = line.split()
                fan_name = parts[0].strip(":")  # Название вентилятора
                rpm = int(parts[1])  # Значение RPM
                fan_data[fan_name] = rpm
    except Exception as e:
        print(f"Ошибка при получении данных RPM: {e}")

    return fan_data


def collect_measurements_rpm(interval, count, target_fan=None):
    """
    Проводит серию измерений скорости
    вращения вентиляторов с заданным интервалом.
    :param interval: Интервал времени между измерениями (в секундах).
    :param count: Количество измерений.
    :param target_fan: Название интересующего вентилятора.
    Если None, берётся первый доступный.
    :return: Список кортежей (время, значение RPM).
    """
    measurements = []  # Хранит список измерений в формате (время, RPM)
    time_elapsed = 0  # Прошедшее время от начала измерений

    print(
        f"Собираем значения скорости вращения вентиляторов"
        f"с интервалом {interval} секунд ({count} измерений)."
    )
    for i in range(count):
        print(f"\nИзмерение {i + 1}...")
        fan_speeds = get_fan_speeds()

        if not fan_speeds:
            print(
                "Не удалось получить данные о скорости вентилей. Пропускаем измерение."
            )
            continue

        # Если вентилятор не указан, выбираем первый
        if not target_fan:
            target_fan = next(
                iter(fan_speeds)
            )  # Берём первый доступный вентилятор

        if target_fan in fan_speeds:
            measurements.append(
                (time_elapsed, fan_speeds[target_fan])
            )  # Сохраняем время и RPM
            print(
                f"Время: {time_elapsed}s, {target_fan}: {fan_speeds[target_fan]} RPM"
            )
        else:
            print(f"Вентилятор {target_fan} не найден. Пропускаем измерение.")

        time_elapsed += interval  # Увеличиваем прошедшее время
        if i < count - 1:  # Ждём между измерениями (кроме последнего)
            time.sleep(interval)

    print("\nСерия измерений завершена.")
    return measurements


def calculate_statistics(measurements):
    """
    Вычисляет математическое ожидание и среднеквадратичное отклонение для RPM.
    :param measurements: Список кортежей (время, RPM).
    :return: Tuple (математическое ожидание, стандартное отклонение).
    """
    values = [value for _, value in measurements]  # Берём только значения RPM
    mean = np.mean(values)  # Математическое ожидание (среднее)
    std_dev = np.std(values)  # Среднеквадратичное отклонение

    return mean, std_dev


def plot_graph_and_save(measurements, fan_name):
    """
    Построение графиков RPM и распределения значений, сохранение в PNG.
    :param measurements: Список кортежей (время, значение RPM).
    :param fan_name: Название вентилятора.
    """
    # Разделяем данные на ось времени и RPM
    times = [time for time, _ in measurements]
    values = [value for _, value in measurements]

    # График изменения RPM по времени
    plt.figure(figsize=(10, 6))
    plt.plot(
        times, values, marker="o", linestyle="-", color="r", label=fan_name
    )
    plt.xlabel("Время (s)")
    plt.ylabel("Скорость вращения (RPM)")
    plt.title(f"Изменение скорости {fan_name} по времени")
    plt.legend()
    plt.grid(True)
    file1 = "rpm_graph.png"
    plt.savefig(file1)  # Сохраняем график
    print(f"График RPM сохранён в файл {file1}")
    plt.close()

    # Гистограмма распределения значений RPM
    plt.figure(figsize=(10, 6))
    plt.hist(
        values, bins=10, color="orange", edgecolor="black", label=fan_name
    )
    plt.xlabel("Скорость вращения (RPM)")
    plt.ylabel("Частота")
    plt.title(f"Распределение скорости {fan_name} (RPM)")
    plt.legend()
    file2 = "rpm_distribution.png"
    plt.savefig(file2)  # Сохраняем в файл
    print(f"Гистограмма сохранена в файл {file2}")
    plt.close()


if __name__ == "__main__":
    # Параметры измерений
    interval_between_measurements = (
        2  # Интервал между измерениями (в секундах)
    )
    number_of_measurements = 10  # Количество измерений
    fan_to_track = (
        "fan1"  # Название вентилятора ("fan1" или другой, если известно)
    )

    # Сбор данных
    measurements = collect_measurements_rpm(
        interval_between_measurements, number_of_measurements, fan_to_track
    )

    # Вычисление статистики
    if measurements:
        mean, std_dev = calculate_statistics(measurements)
        print(f"\nМатематическое ожидание: {mean:.2f} RPM")
        print(f"Среднеквадратичное отклонение: {std_dev:.2f} RPM")

        # Построение и сохранение графиков
        plot_graph_and_save(
            measurements, fan_to_track or "Неизвестный вентилятор"
        )

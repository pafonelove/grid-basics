#region Import.
import os
import subprocess
import time
#endregion


def read_best_result(file_path: str) -> tuple:
    """
    Читать все файлы с результатами переборов.
    :param file_path: путь к файлу.
    :return: лучший результат переборов из всех результирующих файлов в формате кортежа.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    value = float(lines[0])
    weight = float(lines[1])
    items = [line.strip() for line in lines[2:]]
    return value, weight, items


if __name__ == "__main__":
    # Запуск 4 параллельных процессов для вычислений.
    total_tasks = 4
    processes: list = [] # список для процессов

    for i in range(total_tasks):
        # Запуск процессов через Popen.
        p = subprocess.Popen(["python", "task6-worker.py", str(i), str(total_tasks)])
        processes.append(p)

    for p in processes:
        p.wait()

    # Инициализация кортежа для получения лучшей выборки из переборов.
    best_overall: tuple = (0, 0, [])
    for i in range(total_tasks):
        result_file: str = f"result{i}.txt" # путь до файла с результатом выборки из процесса
        while not os.path.exists(result_file):
            time.sleep(0.1)

        value, weight, items = read_best_result(result_file)
        # Перезапись лучшего результата при наличии наилучшего.
        if value > best_overall[0]:
            best_overall = (value, weight, items)

    print("ЛУЧШЕЕ РЕШЕНИЕ:")
    print(f"Общая стоимость: {best_overall[0]}")
    print(f"Общий вес: {best_overall[1]}")
    print("Предметы:")
    for line in best_overall[2]:
        print(f"  {line}")

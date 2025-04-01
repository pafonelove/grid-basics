#region Import.
import sys
from itertools import product
from math import prod
#endregion


def parse_items(file_path: str) -> tuple:
    """
    Читать исходный файл с данными.
    :param file_path: путь к файлу.
    :return: распаковка максимального веса рюкзака и списка вещей.
    """
    with open(file_path, "r") as f:
        lines = f.readlines()
    # Парсинг максимального веса рюкзака.
    max_weight = float(lines[0].strip().split("=")[1])
    items = []
    for line in lines[1:]:
        # Парсинг названия, веса, стоимости и количества каждой вещи в исходном файле.
        name, weight, value, quantity = line.strip().split()
        items.append({
            "name": name,
            "weight": float(weight),
            "value": float(value),
            "quantity": int(quantity)
        })
    return max_weight, items


def generate_combinations(items: list, start_index: int, end_index: int):
    """
    Сформировать все возможные переборы комбинаций вещей.
    :param items: список вещей.
    :param start_index: начальный индекс создания комбинации.
    :param end_index: конечный индекс создания комбинации.
    :return: индекс и перебор комбинации.
    """
    ranges = [range(i["quantity"] + 1) for i in items]
    # Создание всех возможных комбинаций для текущего интервала индексов.
    for idx, combo in enumerate(product(*ranges)):
        if start_index <= idx < end_index:
            yield idx, combo


def evaluate_combo(combo, items, max_weight):
    """
    Сформировать комбинацию для вывода в файл.
    :param combo: комбинация выбранных вещей.
    :param items:
    :param max_weight:
    :return:
    """
    total_weight = 0
    total_value = 0
    selection = []
    for count, item in zip(combo, items):
        total_weight += count * item["weight"]
        total_value += count * item["value"]
        selection.append((item["name"], count))
    if total_weight <= max_weight:
        return total_value, total_weight, selection
    return None


if __name__ == "__main__":
    # task_id и total_tasks передаются в subprocess.Popen().
    task_id = int(sys.argv[1])
    total_tasks = int(sys.argv[2])
    max_weight, items = parse_items("./items.txt")

    total_combos = prod(i["quantity"] + 1 for i in items)   # количество всех возможных комбинаций
    chunk_size = total_combos // total_tasks                # размер буффера перебора
                                                            # (количество комбинаций поделить на количество нод (потоков)
    start_index: int = task_id * chunk_size                 # начальный индекс вычисления для каждой из нод
    end_index = total_combos if task_id == total_tasks - 1 else (task_id + 1) * chunk_size

    # Инициализация кортежа для лучшей комбинации.
    best = (0, 0, [])

    # Запись/перезапись файла переборов всех комбинаций для текущей ноды.
    with open(f"out{task_id}.txt", "w") as f:
        for idx, combo in generate_combinations(items, start_index, end_index):
            result = evaluate_combo(combo, items, max_weight)
            combo_str: str = ", ".join([f"{item['name']}:{count}" for item, count in zip(items, combo)])
            if result:
                f.write(f"[!!! УСПЕХ !!!] Перебор {idx}: {combo_str} | Вес вещей: {result[1]}, Стоимость: {result[0]}\n")
                if result[0] > best[0]:
                    best = result
            else:
                f.write(f"[ПРОПУСК ] Перебор {idx}: {combo_str} | Превышен допустимый вес\n")


    # Отдельный файл с результатом для task6-grid.py.
    with open(f"result{task_id}.txt", "w") as f:
        f.write(f"{best[0]}\n")     # стоимость вещей
        f.write(f"{best[1]}\n")     # вес вещей
        for name, count in best[2]: # комбинация вещей
            if count > 0:
                f.write(f"{name}:{count}\n")

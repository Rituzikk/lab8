"""Программа запрашивает критерии и их попарные сравнения, строит матрицу
парных сравнений и вычисляет весовые коэффициенты критериев.
"""
from fractions import Fraction

MIN_CRITERIA = 2   # с одним критерием сравнивать нечего
MAX_CRITERIA = 10  # больше 10 критериев - это 45+ вопросов, пользователь собьётся

# Допустимые суждения по шкале Саати: 1..9 и обратные 1/2..1/9.
# Fraction используется, чтобы "1/3" не превращалось в неточное 0.333...
ALLOWED = {Fraction(k) for k in range(1, 10)} | {Fraction(1, k) for k in range(2, 10)}


def ask(prompt):
    """Единая точка ввода: в одном месте обрезаем пробелы у всех ответов."""
    return input(prompt).strip()


def parse_judgement(text):
    """Разбирает ответ вида '3' или '1/3'. Возвращает Fraction или None.

    Возвращаем None вместо исключения, чтобы вызывающий код мог просто
    переспросить пользователя, а не падать на опечатке.
    """
    text = text.replace(" ", "")
    try:
        if "/" in text:
            numerator, denominator = text.split("/")
            value = Fraction(int(numerator), int(denominator))
        else:
            value = Fraction(int(text))
    except (ValueError, ZeroDivisionError):
        return None
    return value if value in ALLOWED else None


def read_count():
    """Запрашивает число критериев, пока не будет введено допустимое."""
    while True:
        text = ask(f"Количество критериев ({MIN_CRITERIA}-{MAX_CRITERIA}): ")
        try:
            count = int(text)
        except ValueError:
            print("Ошибка: нужно ввести целое число, например 3.")
            continue
        if MIN_CRITERIA <= count <= MAX_CRITERIA:
            return count
        print(f"Ошибка: число критериев должно быть от {MIN_CRITERIA} до {MAX_CRITERIA}.")


def read_names(count):
    """Запрашивает названия критериев, чтобы вопросы были понятнее номеров."""
    names = []
    for i in range(1, count + 1):
        while True:
            name = ask(f"Название критерия {i} (Enter - 'Критерий {i}'): ")
            name = name or f"Критерий {i}"
            # Одинаковые названия сделали бы вопросы неразличимыми.
            if name in names:
                print("Ошибка: такое название уже есть, введите другое.")
                continue
            names.append(name)
            break
    return names


def read_pairwise(names):
    """Запрашивает сравнения только для пар i < j.

    Нижний треугольник матрицы вычисляется как обратные величины,
    поэтому пользователю не нужно вводить каждое сравнение дважды.
    """
    count = len(names)
    matrix = [[Fraction(1)] * count for _ in range(count)]
    print("\nШкала: 1 - равны, 3 - умеренное превосходство, 5 - существенное,")
    print("7 - значительное, 9 - очень сильное (2, 4, 6, 8 - промежуточные).")
    print("Если важнее второй критерий, введите дробь: 1/3, 1/5 и т.д.\n")
    for i in range(count):
        for j in range(i + 1, count):
            while True:
                text = ask(f"«{names[i]}» по сравнению с «{names[j]}» (1-9 или 1/2..1/9): ")
                value = parse_judgement(text)
                if value is None:
                    print("Ошибка: введите число от 1 до 9 или дробь от 1/2 до 1/9.")
                    continue
                matrix[i][j] = value
                matrix[j][i] = 1 / value
                break
    return matrix


def calc_weights(matrix):
    """Весовые коэффициенты: сумма строки / сумма всех элементов матрицы.

    Нормировка на общую сумму гарантирует, что веса в сумме дают 1.
    """
    row_sums = [sum(row) for row in matrix]
    total = sum(row_sums)
    return [float(s / total) for s in row_sums]


def print_matrix(names, matrix):
    """Показывает матрицу, чтобы пользователь мог проверить свои ответы."""
    print("\nМатрица попарных сравнений:")
    for name, row in zip(names, matrix):
        cells = "  ".join(f"{float(v):5.2f}" for v in row)
        print(f"  {name[:15]:<15} {cells}")


def main():
    print("Метод анализа иерархий (Т. Саати)\n")
    try:
        count = read_count()
        names = read_names(count)
        matrix = read_pairwise(names)
    except (EOFError, KeyboardInterrupt):
        # Прерывание - не ошибка программы, поэтому выходим без трассировки.
        print("\nВвод прерван. Выход.")
        return 1

    print_matrix(names, matrix)
    weights = calc_weights(matrix)
    print("\nВесовые коэффициенты:")
    for name, w in zip(names, weights):
        print(f"  {name}: {w:.2f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from fractions import Fraction

MIN_N = 2
MAX_N = 10

# допустимые значения по шкале Саати: 1..9 и обратные 1/2..1/9
# Fraction, чтобы 1/3 не терялась в округлении
ALLOWED = {Fraction(k) for k in range(1, 10)} | {Fraction(1, k) for k in range(2, 10)}


def parse_value(text):
    # возвращает None при ошибке, чтобы можно было просто переспросить
    text = text.replace(" ", "")
    try:
        if "/" in text:
            a, b = text.split("/")
            value = Fraction(int(a), int(b))
        else:
            value = Fraction(int(text))
    except (ValueError, ZeroDivisionError):
        return None
    return value if value in ALLOWED else None


def read_count():
    while True:
        text = input(f"Количество критериев ({MIN_N}-{MAX_N}): ").strip()
        try:
            n = int(text)
        except ValueError:
            print("Ошибка: нужно ввести целое число, например 3.")
            continue
        if MIN_N <= n <= MAX_N:
            return n
        print(f"Ошибка: число должно быть от {MIN_N} до {MAX_N}.")


def read_names(n):
    names = []
    for i in range(1, n + 1):
        while True:
            name = input(f"Название критерия {i} (Enter - 'Критерий {i}'): ").strip()
            name = name or f"Критерий {i}"
            # одинаковые названия сделают вопросы неразличимыми
            if name in names:
                print("Ошибка: такое название уже есть.")
                continue
            names.append(name)
            break
    return names


def read_matrix(names):
    n = len(names)
    matrix = [[Fraction(1)] * n for _ in range(n)]
    print("\nШкала: 1 - равны, 3 - умеренное превосходство, 5 - существенное,")
    print("7 - значительное, 9 - очень сильное (2, 4, 6, 8 - промежуточные).")
    print("Если важнее второй критерий, вводите дробь: 1/3, 1/5 и т.д.\n")
    for i in range(n):
        for j in range(i + 1, n):
            while True:
                text = input(f"«{names[i]}» по сравнению с «{names[j]}»: ").strip()
                value = parse_value(text)
                if value is None:
                    print("Ошибка: введите число от 1 до 9 или дробь от 1/2 до 1/9.")
                    continue
                matrix[i][j] = value
                # обратное значение считаем сами, чтобы не спрашивать пару дважды
                matrix[j][i] = 1 / value
                break
    return matrix


def calc_weights(matrix):
    # сумма строки / сумма всех элементов, тогда веса в сумме дают 1
    row_sums = [sum(row) for row in matrix]
    total = sum(row_sums)
    return [float(s / total) for s in row_sums]


def main():
    print("Метод анализа иерархий (Т. Саати)\n")
    try:
        n = read_count()
        names = read_names(n)
        matrix = read_matrix(names)
    except (EOFError, KeyboardInterrupt):
        # прерывание не считаем ошибкой, выходим без трассировки
        print("\nВвод прерван. Выход.")
        return

    print("\nМатрица попарных сравнений:")
    for name, row in zip(names, matrix):
        print(f"  {name[:15]:<15}", "  ".join(f"{float(v):5.2f}" for v in row))

    print("\nВесовые коэффициенты:")
    for name, w in zip(names, calc_weights(matrix)):
        print(f"  {name}: {w:.2f}")


main()
import subprocess
import math
from scipy import special as sc


def read_bits(filename):
    """
    Читает бинарную последовательность из файла

    Параметры:
        filename (str): имя файла

    Возвращает:
        str: строка из 0 и 1
    """
    with open(filename, "r") as file:
        return file.read().strip()


def frequency_test(bits):
    """
    Частотный побитовый тест NIST

    Считает сумму битов (1 -> +1, 0 -> -1) и проверяет,
    насколько она близка к нулю

    Параметры:
        bits (str): бинарная последовательность

    Возвращает:
        float: p-value
    """
    n = len(bits)

    s = 0
    for b in bits:
        if b == "1":
            s += 1
        else:
            s -= 1

    s_obs = abs(s) / math.sqrt(n)
    return sc.erfc(s_obs / math.sqrt(2))


def runs_test(bits):
    """
    Тест на одинаковые подряд идущие биты (Runs Test)

    Считает количество серий (runs) и сравнивает с ожидаемым
    для случайной последовательности

    Параметры:
        bits (str): бинарная последовательность

    Возвращает:
        tuple (float, bool): (p-value, успех/неуспех) если тест применим
        bool: False если тест неприменим (слишком сильный перекос)
    """
    n = len(bits)
    pi = bits.count("1") / n

    # условие применимости из методички
    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return False

    # считаем количество серий
    v = 0
    for i in range(n - 1):
        if bits[i] != bits[i + 1]:
            v += 1

    numerator = abs(v - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    if denominator == 0:
        return False

    p_value = sc.erfc(numerator / denominator)
    return p_value, p_value >= 0.01


def longest_run_test(bits):
    """
    Тест на самую длинную последовательность единиц в блоке

    Разбивает последовательность на блоки по 8 бит, в каждом
    ищет максимальную серию единиц, считает статистику и
    проверяет через хи-квадрат

    Параметры:
        bits (str): бинарная последовательность (ровно 128 бит)

    Возвращает:
        float: p-value
    """
    block_size = 8
    n_blocks = len(bits) // block_size
    blocks = [bits[i * block_size:(i + 1) * block_size] for i in range(n_blocks)]

    counts = [0, 0, 0, 0]  # для длин: <=1, 2, 3, >=4

    for block in blocks:
        max_run = 0
        current = 0

        for b in block:
            if b == "1":
                current += 1
                max_run = max(max_run, current)
            else:
                current = 0

        if max_run <= 1:
            counts[0] += 1
        elif max_run == 2:
            counts[1] += 1
        elif max_run == 3:
            counts[2] += 1
        else:
            counts[3] += 1

    # теоретические вероятности из методички (для M=8)
    pi = [0.2148, 0.3672, 0.2305, 0.1875]
    n = len(blocks)
    chi2 = 0

    for i in range(4):
        expected = n * pi[i]
        if expected > 0:
            chi2 += ((counts[i] - expected) ** 2) / expected

    return sc.gammaincc(3 / 2, chi2 / 2)


def run_generators():
    """Запускает генераторы C++ и Java, сохраняет битовые строки в файлы"""
    subprocess.run(["generator.exe"])
    subprocess.run(["javac", "generators/generator.java"])
    subprocess.run(["java", "-cp", "generators", "generator"])


def analyze(name, filename, result_file):
    """
    Прогоняет все три теста и пишет результат в файл

    Параметры:
        name (str): имя генератора (C++ / Java)
        filename (str): путь к файлу с битовой строкой
        result_file (file): открытый файл для записи
    """
    bits = read_bits(filename)

    p1 = frequency_test(bits)
    result2 = runs_test(bits)
    p3 = longest_run_test(bits)

    result_file.write(f"Generator {name}\n\n")
    result_file.write(f"Test1 P = {p1:.5f} - {'success' if p1 >= 0.01 else 'fail'}\n")

    if result2 is False:
        result_file.write(f"Test2 P = N/A - test not applicable\n")
    else:
        p2, success = result2
        result_file.write(f"Test2 P = {p2:.5f} - {'success' if success else 'fail'}\n")

    result_file.write(f"Test3 P = {p3:.5f} - {'success' if p3 >= 0.01 else 'fail'}\n\n")


def main():
    """Основная функция: запускает генераторы, тесты, сохраняет результат"""
    run_generators()

    with open("result.txt", "w") as result:
        analyze("C++", "gen_bits/cpp_gen.txt", result)
        analyze("Java", "gen_bits/java_gen.txt", result)


if __name__ == "__main__":
    main()
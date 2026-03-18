import subprocess
import math
from scipy import special as sc


def read_bits(filename):
    """
    Чтение бинарной последовательности из файла.

    Параметры
   
    filename : str
        Имя файла с бинарной последовательностью.

    Возвращает
    
    str
        Строка, содержащая последовательность из символов 0 и 1.
    """
    with open(filename, "r") as file:
        return file.read().strip()


def frequency_test(bits):
    """
    Частотный побитовый тест.

    Проверяет равномерность распределения нулей и единиц
    в бинарной последовательности.

    Параметры
  
    bits : str
        Бинарная последовательность.

    Возвращает
   
    float
        Значение p-value.
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
    Тест на одинаковые подряд идущие биты.

    Проверяет количество серий нулей и единиц
    в последовательности.

    Параметры

    bits : str
        Бинарная последовательность.

    Возвращает
    
    float
        Значение p-value или None, если тест неприменим.
    """
    n = len(bits)

    pi = bits.count("1") / n

    # Проверка применимости теста (по NIST)
    tau = 2 / math.sqrt(n)
    if abs(pi - 0.5) >= tau:
        return None  # тест неприменим

    v = 1
    for i in range(1, n):
        if bits[i] != bits[i - 1]:
            v += 1

    numerator = abs(v - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)

    return sc.erfc(numerator / denominator)

def longest_run_test(bits):
    """
    Тест на самую длинную последовательность единиц в блоке.

    Последовательность разбивается на блоки фиксированной длины.
    В каждом блоке определяется максимальная длина серии единиц.

    Параметры
   
    bits : str
        Бинарная последовательность.

    Возвращает
   
    float
        Значение p-value.
    """
    block_size = 8
    blocks = [bits[i:i + block_size] for i in range(0, len(bits), block_size)]

    counts = [0, 0, 0, 0]

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

    pi = [0.2148, 0.3672, 0.2305, 0.1875]

    n = len(blocks)
    chi2 = 0

    for i in range(4):
        expected = n * pi[i]
        chi2 += ((counts[i] - expected) ** 2) / expected

    return sc.gammaincc(3 / 2, chi2 / 2)


def run_generators():
    """
    Запуск генераторов C++ и Java.
    """
    subprocess.run(["generator.exe"])

    subprocess.run(["javac", "generators/generator.java"])
    subprocess.run(["java", "-cp", "generators", "generator"])


def analyze(name, filename, result_file):
    """
    Запуск всех тестов NIST для заданной последовательности.

    Параметры
  
    name : str
        Название генератора.
    filename : str
        Файл с последовательностью.
    result_file : file
        Файл для записи результатов.
    """
    bits = read_bits(filename)

    p1 = frequency_test(bits)
    p2 = runs_test(bits)
    p3 = longest_run_test(bits)

    result_file.write(f"Generator {name}\n\n")

    result_file.write(f"Test1 P = {p1:.5f} - {'success' if p1 >= 0.01 else 'fail'}\n")
    result_file.write(f"Test2 P = {p2:.5f} - {'success' if p2 >= 0.01 else 'fail'}\n")
    result_file.write(f"Test3 P = {p3:.5f} - {'success' if p3 >= 0.01 else 'fail'}\n\n")


def main():
    """
    Основная функция программы.

    Запускает генераторы случайных последовательностей,
    выполняет три статистических теста NIST и сохраняет
    результаты в файл result.txt.
    """
    run_generators()

    with open("result.txt", "w") as result:
        analyze("C++", "gen_bits/cpp_gen.txt", result)
        analyze("Java", "gen_bits/java_gen.txt", result)


if __name__ == "__main__":
    main()
#include <iostream>
#include <fstream>
#include <random>

/*
Генератор псевдослучайной бинарной последовательности.

Программа генерирует последовательность из 0 и 1
длиной 128 бит и сохраняет её в файл gen_bits/cpp_gen.txt.
Используется стандартный генератор случайных чисел
библиотеки C++.
*/

int main() {

    const int COUNT = 128;

    std::ofstream file("gen_bits/cpp_gen.txt");

    if (!file.is_open()) {
        std::cerr << "Ошибка открытия файла\n";
        return 1;
    }

    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dist(0, 1);

    for (int i = 0; i < COUNT; i++) {
        file << dist(gen);
    }

    file.close();

    return 0;
}
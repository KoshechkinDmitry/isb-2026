import java.io.FileWriter;
import java.io.IOException;
import java.util.Random;

/*
Генератор псевдослучайной бинарной последовательности.

Программа генерирует последовательность из 0 и 1
длиной 128 бит и сохраняет её в файл gen_bits/java_gen.txt.
Используется стандартный генератор Random.
*/

public class generator {

    public static void main(String[] args) {

        int COUNT = 128;

        Random random = new Random();

        try {

            FileWriter writer = new FileWriter("gen_bits/java_gen.txt");

            for (int i = 0; i < COUNT; i++) {
                writer.write(Integer.toString(random.nextInt(2)));
            }

            writer.close();

        } catch (IOException e) {
            System.out.println("Ошибка записи файла");
        }
    }
}
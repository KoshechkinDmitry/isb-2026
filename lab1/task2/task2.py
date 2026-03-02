from collections import Counter
from constants import TASK2_INPUT, TASK2_OUTPUT, TASK2_FREQ
from cod13_key import KEY


def load_text(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def save_text(filename: str, data: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)


def calculate_frequencies(text: str) -> str:
    total = len(text)
    counter = Counter(text)

    freq_dict = {char: count / total for char, count in counter.items()}
    sorted_freq = dict(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))

    return str(sorted_freq)


def decrypt(text: str, key: dict) -> str:
    return "".join(key.get(char, char) for char in text)


def main():
    text = load_text(TASK2_INPUT)

    # подсчет частот
    frequencies = calculate_frequencies(text)
    save_text(TASK2_FREQ, frequencies)

    # дешифр
    decrypted_text = decrypt(text, KEY)
    save_text(TASK2_OUTPUT, decrypted_text)

    print("Готово.")


if __name__ == "__main__":
    main()
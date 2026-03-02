from constants import *

def encrypt(text, alphabet, key):
    result = ""
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            result += key[index]
        else:
            result += char
    return result


def decrypt(text, alphabet, key):
    result = ""
    for char in text:
        if char in key:
            index = key.index(char)
            result += alphabet[index]
        else:
            result += char
    return result


def main():
    # Чтение исходного
    with open(TASK1_INPUT, "r", encoding="utf-8") as f:
        text = f.read()

    # Шифровка
    encrypted_text = encrypt(text, ALPHABET, FIXED_KEY)

    # сейв шифр текста
    with open(TASK1_ENC_OUTPUT, "w", encoding="utf-8") as f:
        f.write(encrypted_text)

    # Дешифро
    decrypted_text = decrypt(encrypted_text, ALPHABET, FIXED_KEY)

    # сейв дешифр текста
    with open(TASK1_DEC_OUTPUT, "w", encoding="utf-8") as f:
        f.write(decrypted_text)

    # сейв ключ
    with open(TASK1_KEY_OUTPUT, "w", encoding="utf-8") as f:
        f.write(FIXED_KEY)

    # Проверка корректности
    if text == decrypted_text:
        print("Дешифрование выполнено корректно.")
    else:
        print("Ошибка при дешифровании.")


if __name__ == "__main__":
    main()
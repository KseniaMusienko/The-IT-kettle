# -*- coding: utf-8 -*-
"""Test 7.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BAi4PPHBgWgSnXQ0fVV5pYlx6UAdKC9f
"""

import cv2
from matplotlib import pyplot as plt

def load_image(path):
    # Загрузка изображения
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if image is None:
        return None, False

    # Проверяем наличие альфа-канала
    has_alpha_channel = image.shape[-1] == 4

    # Преобразуем изображение в RGB
    if has_alpha_channel:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]

        # Убираем прозрачность
        result = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        result[alpha == 0] = (255, 255, 255)  # Делаем прозрачные пиксели белыми
    else:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return result, has_alpha_channel


# Основной цикл программы
while True:
    path = input("Введите путь к изображению: ")

    try:
        # Попытка загрузки изображения
        image, has_alpha_channel = load_image(path)

        if image is not None:
            # Сообщение об успешной загрузке
            print(f"Изображение успешно загружено! Формат: {'PNG' if has_alpha_channel else 'JPG'}")

            if has_alpha_channel:
                print("Обнаружены прозрачные пиксели. Они были заменены на белые.")

            # Сохранение исправленного изображения
            cv2.imwrite('output.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

            # Отображаем изображение с использованием Matplotlib
            plt.figure(figsize=(10, 10))
            plt.imshow(image)
            plt.show()
            break
        else:
            raise ValueError("Невозможно загрузить изображение")
    except Exception as e:
        print(f"Произошла ошибка при загрузке изображения: {e}. Попробуйте еще раз.")

import cv2
from PIL import Image, ImageFilter
from matplotlib import pyplot as plt

def load_image(path):
    # Загрузка изображения
    image = cv2.imread(path, cv2.IMREAD_UNCHANGED)

    if image is None:
        return None, False

    # Проверяем наличие альфа-канала
    has_alpha_channel = image.shape[-1] == 4

    # Преобразуем изображение в RGB
    if has_alpha_channel:
        bgr = image[:, :, :3]
        alpha = image[:, :, 3]

        # Убираем прозрачность
        result = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        result[alpha == 0] = (255, 255, 255)  # Делаем прозрачные пиксели белыми
    else:
        result = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return result, has_alpha_channel

def resize_image(image, width=None, height=None):
    if width is None or height is None:
        return image

    # Рассчитываем новые размеры
    h, w = image.shape[:2]
    if width is None:
        ratio = height / h
        width = int(w * ratio)
    elif height is None:
        ratio = width / w
        height = int(h * ratio)

    resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized

def convert_to_grayscale(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray

def apply_gaussian_blur(image, radius=1):
    pil_img = Image.fromarray(image)
    blurred = pil_img.filter(ImageFilter.GaussianBlur(radius=radius))
    return np.array(blurred)

def show_and_save_image(image):
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.show()
    cv2.imwrite('output.png', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def get_user_choice():
    choice = input("\nВыберите действие:\n"
                   "1. Изменить размер\n"
                   "2. Конвертировать в черно-белое\n"
                   "3. Применить размытие\n"
                   "4. Завершить изменения и сохранить\n"
                   "Ваш выбор: ")
    return choice

def validate_input(user_input, valid_choices):
    while user_input not in valid_choices:
        print("Некорректный ввод. Повторите попытку.")
        user_input = input("Ваш выбор: ")
    return user_input

def main():
    path = input("Введите путь к изображению: ")

    try:
        # Попытка загрузки изображения
        image, has_alpha_channel = load_image(path)

        if image is not None:
            # Сообщение об успешной загрузке
            print(f"Изображение успешно загружено! Формат: {'PNG' if has_alpha_channel else 'JPG'}")

            if has_alpha_channel:
                print("Обнаружены прозрачные пиксели. Они были заменены на белые.")

            continue_changes = True
            while continue_changes:
                choice = get_user_choice()
                choice = validate_input(choice, ['1', '2', '3', '4'])

                if choice == '1':
                    width = input("Введите новую ширину (оставьте пустым для сохранения пропорций): ")
                    height = input("Введите новую высоту (оставьте пустым для сохранения пропорций): ")

                    if width.isdigit():
                        width = int(width)
                    else:
                        width = None

                    if height.isdigit():
                        height = int(height)
                    else:
                        height = None

                    image = resize_image(image, width, height)
                    print("Размер изменен!")

                elif choice == '2':
                    image = convert_to_grayscale(image)
                    print("Конвертация в черно-белое выполнена!")

                elif choice == '3':
                    radius = input("Введите радиус размытия (целое число от 1 до 100): ")
                    while not radius.isdigit() or not (1 <= int(radius) <= 100):
                        print("Некорректный ввод. Радиус должен быть целым числом от 1 до 100.")
                        radius = input("Попробуйте снова: ")
                    radius = int(radius)
                    image = apply_gaussian_blur(image, radius)
                    print("Размытие применено!")

                elif choice == '4':
                    show_and_save_image(image)
                    print("Изменения сохранены!")
                    continue_changes = False

        else:
            raise ValueError("Невозможно загрузить изображение")
    except Exception as e:
        print(f"Произошла ошибка при загрузке изображения: {e}. Попробуйте еще раз.")

if __name__ == "__main__":
    main()
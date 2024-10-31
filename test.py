# import os

# def is_cyrillic(text):
#     return any('а' <= char <= 'я' or 'А' <= char <= 'Я' for char in text)

# def write_cyrillic_filenames(directory):
#     with open('names.txt', 'w', encoding='utf-8') as file:
#         for filename in os.listdir(directory):
#             if is_cyrillic(filename):
#                 file.write(filename + '\n')

# # Change 'your_directory_path' to the path of your directory
# write_cyrillic_filenames(r"C:\Users\karim\Downloads\Video_New\Video_New\Name\Women's_names")


names = """Агафья.mp4
Аглая.mp4
Агния.mp4
Азалия.mp4
Акулина.mp4
Алевтина.mp4
Александра.mp4
Алина.mp4
Алла.mp4
Анастасия.mp4
Ангелина.mp4
Анжела.mp4
Анжелика.mp4
Анна.mp4
Антонина.mp4
Анфиса.mp4
Валентина.mp4
Валерия.mp4
Варвара.mp4
Василиса.mp4
Вера.mp4
Вероника.mp4
Виктория.mp4
Виолетта.mp4
Галина.mp4
Глафира.mp4
Дана.mp4
Дарья.mp4
Евгения.mp4
Евдокия.mp4
Евлалия.mp4
Евпраксия.mp4
Евфросиния.mp4
Екатерина.mp4
Елена.mp4
Елизавета.mp4
Жанна.mp4
Зинаида.mp4
Злата.mp4
Зоя.mp4
Инга.mp4
Инесса.mp4
Инна.mp4
Иоанна.mp4
Ираида.mp4
Ирина.mp4
Ия.mp4
Карина.mp4
Каролина.mp4
Кира.mp4
Клавдия.mp4
Ксения.mp4
Лада.mp4
Лариса.mp4
Лидия.mp4
Лилия.mp4
Любовь.mp4
Людмила.mp4
Маргарита.mp4
Марина.mp4
Мария.mp4
Марфа.mp4
Матрёна.mp4
Мирослава.mp4
Надежда.mp4
Наталья.mp4
Нина.mp4
Нонна.mp4
Оксана.mp4
Октябрина.mp4
Олимпиада.mp4
Ольга.mp4
Павлина.mp4
Пелагея.mp4
Полина.mp4
Прасковья.mp4
Рада.mp4
Раиса.mp4
Регина.mp4
Римма.mp4
Руслана.mp4
Светлана.mp4
Серафима.mp4
Снежана.mp4
София.mp4
Таисия.mp4
Тамара.mp4
Татьяна.mp4
Ульяна.mp4
Фёкла.mp4
Фаина.mp4
Юлия.mp4
Яна.mp4
Ярослава.mp4
"""

names_list = names.splitlines()
d = {}

for name in names_list:
    key = name.split('.')[0]
    d[key] = name

print(d)

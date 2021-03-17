import requests
import random

message_ghost = "Я вот что хочу сказать - даже если я мёртв, это не значит, что я не буду сюда писать! Так и знайте."
i = random.randint(0, 100)
j = 0
while (i > j):
    rand_sign = random.randint(0, len(message_ghost)-1)
    alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    rand_alphabet = random.randint(1, len(alphabet)-1)
    message_ghost = message_ghost[:rand_sign] + alphabet[rand_alphabet] + message_ghost[rand_sign+1:]
    j += 1
print(message_ghost)
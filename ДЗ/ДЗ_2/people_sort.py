# people_sort.py

def person_lister(f):
    def inner(people):
        # Сортируем список людей по возрасту (индекс 2)
        sorted_people = sorted(people, key=lambda x: int(x[2]))
        # Применяем функцию оформления к каждому человеку
        return [f(person) for person in sorted_people]

    return inner


@person_lister
def name_format(person):
    first, last, age, sex = person
    # Выбираем обращение в зависимости от пола
    prefix = "Mr." if sex == 'M' else "Ms."
    return f"{prefix} {first} {last}"


if __name__ == '__main__':
    # Сначала вводим количество людей
    n = int(input("Введите количество людей: "))

    people = []
    for i in range(n):
        # Вводим данные каждого человека
        person_input = input(f"Введите данные человека {i + 1} (имя фамилия возраст пол): ")
        # Разбиваем строку на части
        person_data = person_input.split()
        people.append(person_data)

    # Получаем и выводим результат
    result = name_format(people)
    print("\nРезультат:")
    for name in result:
        print(name)
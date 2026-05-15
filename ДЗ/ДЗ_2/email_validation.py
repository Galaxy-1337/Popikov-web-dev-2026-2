import re


def fun(s):
    # Формат: username@websitename.extension
    # username: буквы, цифры, тире (-), подчеркивание (_)
    # websitename: только буквы и цифры
    # extension: только буквы, максимальная длина 3
    pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$'
    return bool(re.match(pattern, s))


def filter_mail(emails):
    return list(filter(fun, emails))


if __name__ == '__main__':
    # Пример входных данных
    n = int(input().strip())
    emails = []
    for _ in range(n):
        emails.append(input().strip())

    filtered_emails = filter_mail(emails)
    print(sorted(filtered_emails))
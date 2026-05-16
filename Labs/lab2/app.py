import random
import re
from functools import lru_cache
from flask import Flask, render_template, abort, request, make_response

from faker import Faker

fake = Faker()

app = Flask(__name__)

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']


# ====================
# Существующие функции
# ====================

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = {'author': fake.name(), 'text': fake.text()}
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments


def generate_post(i):
    return {
        'title': fake.sentence(nb_words=6)[:-1],
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }


@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)


# ========
# Маршруты
# ========

# Главная страница ЛР №2
@app.route('/index')
def index():
    return render_template('index.html', title='Главная')


# Страница со всеми постами
@app.route('/')
@app.route('/posts')
def posts():
    return render_template('posts.html', title='Блог', posts=posts_list())


@app.route('/posts/<int:index>')
def post(index):
    try:
        p = posts_list()[index]
    except IndexError:
        abort(404)
    return render_template('post.html', title=p['title'], post=p)


@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')


# ================
# НОВЫЙ ФУНКЦИОНАЛ
# ================

# 1. Параметры URL
@app.route('/request-params/')
def request_params():
    """Отображает все параметры URL (GET-параметры)"""
    params = dict(request.args)
    return render_template('url_params.html', title='Параметры URL', params=params)


# 2. Заголовки запроса
@app.route('/request-headers/')
def request_headers():
    """Отображает все заголовки HTTP-запроса"""
    headers = dict(request.headers)
    return render_template('headers.html', title='Заголовки запроса', headers=headers)


# 3. Cookie (установка/удаление)
@app.route('/request-cookies/')
def request_cookies():
    """Отображает cookies, позволяет установить или удалить определённый cookie"""
    cookie_value = request.cookies.get('user_preference')
    action = request.args.get('action')

    response = make_response(render_template('cookies.html',
                                              title='Cookie',
                                              cookie_value=cookie_value))

    if action == 'set':
        response.set_cookie('user_preference', 'dark_mode', max_age=60 * 60 * 24 * 30)
        cookie_value = 'dark_mode'
        return make_response(render_template('cookies.html',
                                             title='Cookie',
                                             cookie_value=cookie_value))
    elif action == 'delete':
        response.delete_cookie('user_preference')
        cookie_value = None
        return make_response(render_template('cookies.html',
                                             title='Cookie',
                                             cookie_value=cookie_value))

    return response


# 4. Параметры формы (POST)
@app.route('/request-form/', methods=['GET', 'POST'])
def request_form():
    """Отображает отправленные данные формы"""
    form_data = None
    if request.method == 'POST':
        form_data = dict(request.form)
    return render_template('form_params.html', title='Параметры формы', form_data=form_data)


# 5. Валидация номера телефона
def clean_phone_number(phone: str) -> str:
    """Очищает номер телефона от всех символов, кроме цифр"""
    return re.sub(r'\D', '', phone)


def validate_phone_number(phone: str) -> tuple:
    """
    Проверяет номер телефона на соответствие формату.
    Возвращает: (is_valid, error_message, formatted_number)
    """
    phone_stripped = phone.strip()

    # Проверка: номер не должен начинаться с недопустимого символа
    first_char = phone_stripped[0] if phone_stripped else ''
    if first_char not in ('+', '8') and not first_char.isdigit():
        return False, "Недопустимый ввод. В номере телефона встречаются недопустимые символы.", None

    # Разрешённые символы: цифры, + (только в начале), пробелы, скобки, дефисы, точки
    allowed_chars_pattern = re.compile(r'^[\d+\s\(\)\-\.]+$')
    if not allowed_chars_pattern.match(phone_stripped):
        return False, "Недопустимый ввод. В номере телефона встречаются недопустимые символы.", None

    # Извлекаем только цифры
    digits = clean_phone_number(phone_stripped)
    digit_count = len(digits)

    if digit_count == 0:
        return False, "Недопустимый ввод. Неверное количество цифр.", None

    # Определяем ожидаемое количество цифр по первому символу
    if phone_stripped.startswith('+7') or phone_stripped.startswith('8'):
        expected_count = 11
    else:
        expected_count = 10

    if digit_count != expected_count:
        return False, "Недопустимый ввод. Неверное количество цифр.", None

    # Дополнительная проверка: для номера с +7, после +7 должна идти цифра
    if phone_stripped.startswith('+7'):
        rest = phone_stripped[2:].lstrip()
        if not rest or not rest[0].isdigit():
            return False, "Недопустимый ввод. В номере телефона встречаются недопустимые символы.", None

    # Форматирование номера — в формате 8-***-***-**-**
    if expected_count == 11:
        # Для 11 цифр: если начинался с +7, заменяем первую цифру на 8
        if phone_stripped.startswith('+7'):
            digits = '8' + digits[1:]
        # Если начинался с 8, оставляем как есть
    else:
        # Для 10 цифр: добавляем 8 в начало
        digits = '8' + digits

    # Форматируем как 8-***-***-**-**
    formatted = f"{digits[:1]}-{digits[1:4]}-{digits[4:7]}-{digits[7:9]}-{digits[9:]}"

    return True, None, formatted


@app.route('/phone-validator/', methods=['GET', 'POST'])
def phone_validator():
    """Страница с формой валидации номера телефона"""
    error_message = None
    formatted_phone = None
    phone_input = ""

    if request.method == 'POST':
        phone_input = request.form.get('phone', '')
        is_valid, error, formatted = validate_phone_number(phone_input)

        if is_valid:
            formatted_phone = formatted
        else:
            error_message = error

    return render_template('phone.html',
                           title='Валидация номера телефона',
                           error_message=error_message,
                           formatted_phone=formatted_phone,
                           phone_input=phone_input)


if __name__ == '__main__':
    app.run(debug=True)
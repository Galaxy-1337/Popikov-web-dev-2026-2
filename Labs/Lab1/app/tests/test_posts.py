import pytest
from flask import template_rendered
from contextlib import contextmanager

# 1. Тест: Главная страница доступна (статус 200)
def test_index_status(client):
    response = client.get('/')
    assert response.status_code == 200

# 2. Тест: На главной странице есть название блога и приветствие
def test_index_content(client):
    response = client.get('/')
    assert "PolyBlog" in response.text
    assert "Любые статьи на ваш вкус!" in response.text

# 3. Тест: Страница со всеми постами доступна
def test_posts_status(client):
    response = client.get('/posts')
    assert response.status_code == 200

# 4. Тест: Для страницы постов используется шаблон 'posts.html'
def test_posts_template_used(client, captured_templates, mocker, posts_list):
    # Подменяем функцию posts_list() на тестовые данные
    mocker.patch("app.posts_list", return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts')
        assert len(templates) > 0
        template, _ = templates[0]
        assert template.name == 'posts.html'

# 5. Тест: В контекст шаблона передаётся правильный заголовок
def test_posts_context_title(client, captured_templates, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts')
        _, context = templates[0]
        assert context['title'] == 'Блог'  # заголовок страницы постов

# 6. Тест: В контекст передаётся список постов ожидаемой длины
def test_posts_context_list(client, captured_templates, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts')
        _, context = templates[0]
        assert len(context['posts']) == 1  # в фикстуре 1 пост

# 7. Тест: Страница существующего поста (id=0) доступна
def test_post_status_valid(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert response.status_code == 200

# 8. Тест: Для страницы поста используется шаблон 'post.html'
def test_post_template_used(client, captured_templates, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        assert len(templates) > 0
        template, _ = templates[0]
        assert template.name == 'post.html'

# 9. Тест: Заголовок страницы совпадает с заголовком поста
def test_post_context_title(client, captured_templates, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        _, context = templates[0]
        assert context['title'] == posts_list[0]['title']

# 10. Тест: В контекст передан правильный объект поста
def test_post_context_object(client, captured_templates, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        _, context = templates[0]
        assert context['post'] == posts_list[0]

# 11. Тест: На странице поста отображается его заголовок
def test_post_content_title(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert posts_list[0]['title'] in response.text

# 12. Тест: На странице поста отображается имя автора
def test_post_content_author(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert posts_list[0]['author'] in response.text

# 13. Тест: На странице поста отображается дата в формате ГГГГ-ММ-ДД
def test_post_content_date(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert "2025-03-10" in response.text

# 14. Тест: На странице поста отображается текст поста
def test_post_content_text(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert posts_list[0]['text'] in response.text

# 15. Тест: На странице поста отображается изображение
def test_post_content_image(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert "123.jpg" in response.text

# 16. Тест: На странице поста есть форма для комментариев
def test_post_content_form(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert "Оставьте комментарий" in response.text
    assert "<form" in response.text

# 17. Тест: В подвале страницы указаны ФИО и номер группы
def test_post_content_footer(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/0')
    assert "Попиков Иван Алексеевич" in response.text
    assert "241-372" in response.text

# 18. Тест: Запрос несуществующего поста возвращает ошибку 404
def test_post_404(client, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    response = client.get('/posts/1')  # в фикстуре только пост с индексом 0
    assert response.status_code == 404

# 19. Тест: В контекст шаблона передаётся правильный автор поста
def test_post_template_data(client, captured_templates, mocker, posts_list):
    mocker.patch("app.posts_list", return_value=posts_list)
    with captured_templates as templates:
        client.get('/posts/0')
        _, context = templates[0]
        assert context['post']['author'] == 'Иванов Иван Иванович'
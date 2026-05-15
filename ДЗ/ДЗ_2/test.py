import pytest
import sys
import os
import math
from io import StringIO
import datetime

# Импорт функций из файлов решений
from fact import fact_rec, fact_it
from show_employee import show_employee
from sum_and_sub import sum_and_sub
from process_list import process_list_comp, process_list_gen
from my_sum import my_sum
from my_sum_argv import my_sum_argv
from files_sort import sort_files
from file_search import search_file
from email_validation import fun, filter_mail
from fibonacci import fibonacci, cube
from average_scores import compute_average_scores
from plane_angle import Point, plane_angle
from phone_number import sort_phone
from people_sort import name_format
from complex_numbers import Complex
from circle_square_mk import circle_square_mk
from log_decorator import function_logger


class TestFact:
    """Тесты для файла fact.py (Факториал)"""

    @pytest.mark.parametrize("n,expected", [
        (0, 1), (1, 1), (2, 2), (3, 6), (4, 24), (5, 120)
    ])
    def test_fact_rec(self, n, expected):
        assert fact_rec(n) == expected

    @pytest.mark.parametrize("n,expected", [
        (0, 1), (1, 1), (2, 2), (3, 6), (4, 24), (5, 120)
    ])
    def test_fact_it(self, n, expected):
        assert fact_it(n) == expected


class TestShowEmployee:
    """Тесты для show_employee.py"""

    @pytest.mark.parametrize("name,salary,expected", [
        ("John", 0, "John: 0 ₽"),
        ("Maria", 100000, "Maria: 100000 ₽"),
        ("Peter", 75000, "Peter: 75000 ₽")
    ])
    def test_employee(self, name, salary, expected):
        assert show_employee(name, salary) == expected


class TestSumAndSub:
    """Тесты для sum_and_sub.py"""

    @pytest.mark.parametrize("a,b,expected_sum,expected_sub", [
        (10, 5, 15, 5),
        (20, 7, 27, 13),
        (15, 15, 30, 0),
        (-5, -3, -8, -2)
    ])
    def test_sum_and_sub(self, a, b, expected_sum, expected_sub):
        s, d = sum_and_sub(a, b)
        assert s == expected_sum and d == expected_sub


class TestProcessList:
    """Тесты для process_list.py"""

    @pytest.mark.parametrize("input_list,expected", [
        ([1, 3, 5, 7], []),
        ([2, 4, 6, 8], [4, 16, 36, 64]),
        ([1, 2, 3, 4, 5, 6], [4, 16, 36])
    ])
    def test_comp(self, input_list, expected):
        assert process_list_comp(input_list) == expected

    @pytest.mark.parametrize("input_list,expected", [
        ([1, 2, 3, 4], [4, 16]),
        ([1, 3, 5, 7], []),
        ([2, 4, 6, 8], [4, 16, 36, 64]),
        ([], [])
    ])
    def test_gen(self, input_list, expected):
        assert list(process_list_gen(input_list)) == expected


class TestMySum:
    """Тесты для my_sum.py"""

    @pytest.mark.parametrize("args,expected", [
        ((1, 2, 3), 6),
        ((10, 20), 30),
        ((5, 5, 5, 5), 20)
    ])
    def test_sum(self, args, expected):
        assert my_sum(*args) == expected


class TestMySumArgv:
    """Тесты для my_sum_argv.py"""

    @pytest.mark.parametrize("args,expected", [
        (['1', '2', '3'], "6"),
        (['10', '20'], "30"),
        (['5', '5', '5', '5'], "20")
    ])
    def test_output(self, capsys, args, expected):
        sys.argv = ['script'] + args
        my_sum_argv()
        assert capsys.readouterr().out.strip() == expected


class TestSortFiles:
    """Тесты для files_sort.py"""

    def test_sort(self, capsys, tmp_path):
        p = tmp_path
        (p / "b.txt").write_text("c")
        (p / "a.py").write_text("c")
        (p / "c.jpg").write_text("c")
        sort_files(str(p))
        out = capsys.readouterr().out
        assert "a.py" in out and "b.txt" in out


class TestFileSearch:
    """Тесты для file_search.py"""

    def test_found(self, capsys, tmp_path):
        (tmp_path / "t.txt").write_text("content")
        search_file("t.txt", str(tmp_path))
        assert "Found in" in capsys.readouterr().out


class TestEmailValidation:
    """Тесты для email_validation.py"""

    @pytest.mark.parametrize("email,expected", [
        ("a@b.c", True),
        ("user@domain.com", True),
        ("user-name@domain.com", True),
        ("invalid", False),
        ("@domain.com", False)
    ])
    def test_email(self, email, expected):
        assert fun(email) is expected


class TestFibonacci:
    """Тесты для fibonacci.py"""

    @pytest.mark.parametrize("n,expected", [
        (0, []),
        (1, [0]),
        (2, [0, 1]),
        (3, [0, 1, 1]),
        (4, [0, 1, 1, 2])
    ])
    def test_fib(self, n, expected):
        assert fibonacci(n) == expected

    @pytest.mark.parametrize("x,expected", [
        (0, 0), (1, 1), (2, 8), (3, 27)
    ])
    def test_cube(self, x, expected):
        assert cube(x) == expected


class TestAverageScores:
    """Тесты для average_scores.py"""

    @pytest.mark.parametrize("scores,expected", [
        ([(10, 20), (20, 30)], (15.0, 25.0)),
        ([(5, 5, 5), (10, 10, 10)], (7.5, 7.5, 7.5)),
        ([(100,), (200,)], (150.0,)),
        ([(0, 0), (0, 0)], (0.0, 0.0))
    ])
    def test_avg(self, scores, expected):
        assert compute_average_scores(scores) == expected


class TestPlaneAngle:
    """Тесты для plane_angle.py"""

    def test_90_degrees(self):
        angle = plane_angle(Point(0, 0, 0), Point(1, 0, 0), Point(1, -1, 0), Point(1, -1, 1))
        assert abs(angle - 90.0) < 1e-5

    def test_0_degrees(self):
        # Исправлено: используем векторы, дающие угол 0 градусов без нулевых векторов
        # Первая плоскость: точки A(0,0,0), B(1,0,0), C(1,1,0)
        # Вторая плоскость: точки C(1,1,0), D(2,1,0) - параллельна первой
        angle = plane_angle(Point(0, 0, 0), Point(1, 0, 0), Point(1, 1, 0), Point(2, 1, 0))
        # Угол между плоскостями может быть 0 или 180 градусов
        assert abs(angle - 0.0) < 1e-5 or abs(angle - 180.0) < 1e-5


class TestPhoneNumber:
    """Тесты для phone_number.py"""

    @pytest.mark.parametrize("phone,expected", [
        (["81234567890"], "+7 (123) 456-78-90"),
        (["89211234567"], "+7 (921) 123-45-67"),
        (["+79001234567"], "+7 (900) 123-45-67")
    ])
    def test_sort(self, phone, expected):
        res = sort_phone(phone)
        assert res[0] == expected


class TestPeopleSort:
    """Тесты для people_sort.py"""

    @pytest.mark.parametrize("people,expected_first,expected_second", [
        ([["A", "B", "20", "M"], ["C", "D", "10", "F"]], "Ms. C D", "Mr. A B"),
        ([["John", "Doe", "30", "M"], ["Jane", "Smith", "25", "F"]], "Ms. Jane Smith", "Mr. John Doe")
    ])
    def test_sort(self, people, expected_first, expected_second):
        res = list(name_format(people))
        assert res[0] == expected_first
        assert res[1] == expected_second


class TestComplexNumbers:
    """Тесты для complex_numbers.py"""

    @pytest.mark.parametrize("c1,c2,expected", [
        ((1, 1), (2, 2), "3.00+3.00i"),
        ((2, 3), (4, 5), "6.00+8.00i")
    ])
    def test_add(self, c1, c2, expected):
        assert str(Complex(*c1) + Complex(*c2)) == expected

    @pytest.mark.parametrize("c1,c2,expected", [
        ((1, 1), (2, 2), "-1.00-1.00i"),
        ((5, 5), (2, 3), "3.00+2.00i")
    ])
    def test_sub(self, c1, c2, expected):
        assert str(Complex(*c1) - Complex(*c2)) == expected


class TestCircleSquareMK:
    """Тесты для circle_square_mk.py"""

    @pytest.mark.parametrize("r,n", [
        (1, 10000), (2, 10000), (5, 10000)
    ])
    def test_area(self, r, n):
        exact = math.pi * r ** 2
        approx = circle_square_mk(r, n)
        assert abs(approx - exact) < 0.5 * r


class TestLogDecorator:
    """Тесты для log_decorator.py"""

    def test_log(self, tmp_path):
        f = tmp_path / "log.txt"

        @function_logger(str(f))
        def foo(): pass

        foo()
        assert "foo" in f.read_text("utf-8")

    def test_log_with_args(self, tmp_path):
        f = tmp_path / "log.txt"

        @function_logger(str(f))
        def bar(x): return x * 2

        bar(5)
        content = f.read_text("utf-8")
        assert "bar" in content and "10" in content


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", "test.py"]))
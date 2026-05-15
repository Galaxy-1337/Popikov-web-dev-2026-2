import subprocess
import pytest
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

INTERPRETER = sys.executable


def run_script(filename, input_data=None):
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'

    input_str = '\n'.join(input_data if input_data else [])
    if input_str:
        input_str += '\n'

    proc = subprocess.run(
        [INTERPRETER, filename],
        input=input_str,
        capture_output=True,
        text=True,
        check=False,
        encoding='utf-8',
        env=env
    )
    if proc.returncode != 0 and proc.stderr:
        sys.stderr.write(f"Error running {filename}: {proc.stderr}\n")
    output = proc.stdout.strip()
    return [line for line in output.split('\n') if line] if output else []


# ========== Тесты ==========

def test_hello_world():
    assert run_script('1.hello.py') == ['Hello, World!']


@pytest.mark.parametrize("input_data, expected", [
    ('1', ['Weird']),
    ('4', ['Not Weird']),
    ('22', ['Not Weird'])
])
def test_python_if_else_1(input_data, expected):
    assert run_script('2.python_if_else.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", [
    ('3', ['Weird']),
    ('6', ['Weird']),
    ('20', ['Weird'])
])
def test_python_if_else_2(input_data, expected):
    assert run_script('2.python_if_else.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", [
    ('2', ['Not Weird']),
    ('4', ['Not Weird']),  # чётное, 2<=n<=5 -> Not Weird
    ('8', ['Weird'])       # чётное, 6<=n<=20 -> Weird
])
def test_python_if_else_3(input_data, expected):
    result = run_script('2.python_if_else.py', [input_data])
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [
    (['1', '2'], ['3', '-1', '2']),
    (['10', '5'], ['15', '5', '50']),
    (['-1', '-1'], ['-2', '0', '1'])
])
def test_arithmetic_operators(input_data, expected):
    assert run_script('3.arithmetic_operators.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", [
    (['3', '5'], ['0', '0.6']),
    (['10', '2'], ['5', '5.0']),
    (['7', '0'], ['Error: Division by zero'])
])
def test_division(input_data, expected):
    assert run_script('4.division.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", [
    ('3', ['0', '1', '4']),
    ('5', ['0', '1', '4', '9', '16']),
    ('1', ['0'])
])
def test_loops(input_data, expected):
    assert run_script('5.loops.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", [
    ('5', ['12345']),
    ('3', ['123']),
    ('1', ['1'])
])
def test_print_function(input_data, expected):
    assert run_script('6.print_function.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", [
    (['5', '2 3 6 6 5'], ['5']),
    (['4', '1 2 3 4'], ['3']),
    (['6', '10 9 8 7 6 5'], ['9'])
])
def test_second_score(input_data, expected):
    assert run_script('7.second_score.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", [
    (['5', 'Гарри', '37.21', 'Берри', '37.21', 'Тина', '37.2', 'Акрити', '41', 'Харш', '39'], ['Берри', 'Гарри']),
    (['4', 'Eve', '40', 'Anna', '50', 'Charlie', '50', 'Bob', '60'], ['Anna', 'Charlie']),
    (['4', 'Alice', '70', 'Zoe', '80', 'John', '85', 'Jane', '80'], ['Jane', 'Zoe'])
])
def test_nested_list(input_data, expected):
    result = run_script('8.nested_list.py', input_data)
    assert sorted(result) == sorted(expected)


@pytest.mark.parametrize("input_data, expected", [
    (['12', 'insert 0 5', 'insert 1 10', 'insert 0 6', 'print', 'remove 6', 'append 9', 'append 1', 'sort', 'print', 'pop', 'reverse', 'print'],
    ['[6, 5, 10]', '[1, 5, 9, 10]', '[9, 5, 1]']),
    (['8', 'append 1', 'append 2', 'append 3', 'print', 'pop', 'print', 'append 4', 'print'],
    ['[1, 2, 3]', '[1, 2]', '[1, 2, 4]']),
    (['6', 'insert 0 100', 'insert 1 200', 'print', 'reverse', 'print', 'print'],
    ['[100, 200]', '[200, 100]', '[200, 100]'])
])
def test_lists(input_data, expected):
    result = run_script('9.lists.py', input_data)
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [
    ('Www.MosPolytech.ru', ['wWW.mOSpOLYTECH.RU']),
    ('Hello World', ['hELLO wORLD']),
    ('123abc!', ['123ABC!'])
])
def test_swap_case(input_data, expected):
    assert run_script('10.swap_case.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", [
    ('this is a string', ['this-is-a-string']),
    ('hello world', ['hello-world']),
    ('one two three', ['one-two-three'])
])
def test_split_and_join(input_data, expected):
    assert run_script('11.split_and_join.py', [input_data]) == expected


def test_max_word_1():
    output = run_script('12.max_word.py')
    assert all(len(w) >= 10 for w in output if w)


def test_max_word_2():
    output = run_script('12.max_word.py')
    assert isinstance(output, list)


def test_price_sum_1():
    output = run_script('13.price_sum.py')
    assert len(output) == 1
    parts = output[0].split()
    assert len(parts) == 3


def test_price_sum_2():
    output = run_script('13.price_sum.py')
    assert len(output) == 1
    assert output[0].count('.') == 3


def test_price_sum_3():
    output = run_script('13.price_sum.py')
    parts = output[0].split()
    assert all(p.replace('.', '').replace('-', '').isdigit() for p in parts)


@pytest.mark.parametrize("input_data, expected", [
    (['abc', 'cba'], ['YES']),
    (['hello', 'olleh'], ['YES']),
    (['test', 'tset'], ['YES']),
    (['abc', 'def'], ['NO'])
])
def test_anagram(input_data, expected):
    assert run_script('14.anagram.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected", [
    (['3', '1 5', '3 7', '6 9', '4'], ['2']),  # 4 попадает в [1,5] и [3,7] → 2
    (['2', '1 2', '3 4', '2'], ['1']),         # 2 попадает в [1,2] → 1
    (['3', '0 10', '5 15', '20 25', '7'], ['2'])
])
def test_metro(input_data, expected):
    result = run_script('15.metro.py', input_data)
    assert result == expected


@pytest.mark.parametrize("input_data, expected", [
    ('BANANA', ['Стюарт 12']),
    ('ANA', ['Кевин 4']),
    ('AAA', ['Кевин 6'])
])
def test_minion_game(input_data, expected):
    result = run_script('16.minion_game.py', [input_data])
    result_clean = [' '.join(r.split()) for r in result]
    expected_clean = [' '.join(e.split()) for e in expected]
    assert result_clean == expected_clean


@pytest.mark.parametrize("input_data, expected", [
    ('2000', ['True']),
    ('1990', ['False']),
    ('1900', ['False']),
    ('2004', ['True'])
])
def test_is_leap(input_data, expected):
    assert run_script('17.is_leap.py', [input_data]) == expected


@pytest.mark.parametrize("input_data, expected", [
    (['3 2', '1 5 3', '3 1', '5 7'], ['1']),
    (['4 2', '1 2 3 4', '1 2', '3 4'], ['0']),
    (['5 2', '1 2 3 4 5', '1 3 5', '2 4'], ['1'])
])
def test_happiness(input_data, expected):
    assert run_script('18.happiness.py', input_data) == expected


@pytest.mark.parametrize("input_data, expected_lines", [
    (['10 3', 'gold 4 100', 'silver 3 60', 'copper 5 50'], 3),
    (['5 2', 'gold 3 90', 'silver 4 40'], 2),
    (['0 1', 'gold 5 100'], 0),
])
def test_pirate_ship_count(input_data, expected_lines):
    result = run_script('19.pirate_ship.py', input_data)
    assert len(result) == expected_lines


def test_pirate_ship_format():
    input_data = ['5 2', 'A 3 90', 'B 4 40']
    result = run_script('19.pirate_ship.py', input_data)
    for line in result:
        parts = line.split()
        assert len(parts) == 3
        assert '.' in parts[1] and '.' in parts[2]


@pytest.mark.parametrize("input_data, expected", [
    (['2', '1 2', '3 4', '5 6', '7 8'], ['19 22', '43 50']),
    (['1', '5', '6'], ['30']),
    (['2', '0 0', '0 0', '1 2', '3 4'], ['0 0', '0 0'])
])
def test_matrix_mult(input_data, expected):
    result = run_script('20.matrix_mult.py', input_data)
    assert result == expected
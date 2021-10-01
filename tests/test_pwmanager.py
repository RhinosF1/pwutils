from pwutil import (compare_pw, hash_pw, validate_password,
                                 validate_username)


def test_password_compare_success():
    password = 'test'
    hashedpw = hash_pw(password)
    assert compare_pw(hashedpw, password)


def test_password_compare_fail():
    password = 'test'
    hashedpw = hash_pw('test2')
    assert compare_pw(hashedpw, password) is False


def test_password_reject_short():
    failed = False
    try:
        validate_password('test')
    except ValueError:
        failed = True
    assert failed


def test_password_reject_common():
    failed = False
    try:
        validate_password('password')
    except ValueError:
        failed = True
    assert failed


def test_password_reject_both():
    failed = False
    try:
        validate_password('qwerty')
    except ValueError:
        failed = True
    assert failed


def test_password_valid():
    password = 'mygoodpassword'
    assert validate_password(password) == password


def test_username_space():
    username = 'My username'
    assert validate_username(username) == 'My_username'


def test_username_lowerfirst():
    username = 'testuser'
    assert validate_username(username) == 'Testuser'


def test_username_multispace():
    username = 'A user name'
    assert validate_username(username) == 'A_user_name'


def test_username_spacelower():
    username = 'test user'
    assert validate_username(username) == 'Test_user'


def test_username_three_changes():
    username = 'a test user'
    assert validate_username(username) == 'A_test_user'


def test_username_sqli():
    assert validate_username('";') == ';'

import pytest
import sys
sys.path.append('..')
sys.path.append('.')
from message_match import mmatch  # noqa: E402


# not nested
def test_simplest_possible():
    assert mmatch({'a': 'b'}, {'a': 'b'})


def test_extra_stuff():
    assert mmatch({'a': 'b', 'c': 'd'}, {'a': 'b'})


def test_simplest_miss():
    assert not mmatch({'a': 'b'}, {'c': 'd'})


def test_simplest_multi_match():
    assert mmatch({'a': 'b', 'c': 'd'}, {'a': 'b', 'c': 'd'})


# nested
def test_simplest_nested():
    assert mmatch({'x': {'y': 'z'}}, {'x': {'y': 'z'}})


def test_simplest_nested_extra_stuff():
    assert mmatch({'a': 'b', 'x': {'y': 'z'}}, {'x': {'y': 'z'}})


def test_multiple_matches_nested():
    assert mmatch({'a': 'b', 'x': {'y': 'z'}},
                  {'a': 'b', 'x': {'y': 'z'}})


# array in message, scalar in match: checks membership
@pytest.mark.xfail(strict=True)
def test_array_contains():
    assert mmatch({'a': [1, 2, 3]}, {'a': 2})


@pytest.mark.xfail(strict=True)
def test_array_does_not_contain():
    assert mmatch({'a': [1, 2, 3]}, {'a': 5})


# array on both sides: full recursion
@pytest.mark.xfail(strict=True)
def test_array_full_match():
    assert mmatch({'a': [1, 2, 3]}, {'a': [1, 2, 3]})


@pytest.mark.xfail(strict=True)
def test_nested_array_full_match():
    assert mmatch({'a': [{'a': 'b'}, 2, 3]}, {'a': [{'a': 'b'}, 2, 3]})


# regex
@pytest.mark.xfail(strict=True)
def test_simplest_regex():
    assert mmatch({'a': 'forefoot'}, {'a': ' special/foo/'})


@pytest.mark.xfail
def test_simplest_regex_failure():
    assert not mmatch({'a': 'forefoot'}, {'a': ' special/smurf/'})


@pytest.mark.xfail
def test_regex_failure_for_case_sensitivity():
    assert not mmatch({'a': 'forefoot'}, {'a': ' special/FOO/'})


@pytest.mark.xfail(strict=True)
def test_regex_pass_for_case_sensitivity():
    assert mmatch({'a': 'forefoot'}, {'a': ' special/FOO/i'})


# special forms
def test_always_pass_with_match_as_an_empty_dict():
    assert mmatch({'a': 'b'}, {})


def test_always_pass_with_both_as_empty_dict():
    assert mmatch({}, {})


def test_validate_the_always_pass_works_nested():
    assert mmatch({'a': {'b': 'c'}}, {'a': {}})


def test_validate_always_pass_if_nested_does_not_override_failure_elsewhere():
    assert not mmatch({'a': {'b': 'c'}}, {'a': {}, 'x': 'y'})


def test_always_pass_should_pass_even_against_a_deeper_structure():
    assert mmatch({'a': {'b': 'c'}}, {})


# strangeness
def test_pass_empty_strings():
    assert mmatch({'a': ''}, {'a': ''})


def test_fail_two_things_that_are_both_false_but_different():
    assert not mmatch({'a': ''}, {'a': 0})


def test_fail_invalid_special():
    assert not mmatch({'a': 'forefoot'}, {'a': ' specialhuhFOO/i'})

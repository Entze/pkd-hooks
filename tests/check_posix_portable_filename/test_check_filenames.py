from typing import Collection, Mapping

from check_posix_portable_filename import check_filenames


def test_valid_filename() -> None:
    expected: Mapping[str, Collection[str]] = {}
    actual = check_filenames(["foo", "bar/baz"])
    assert actual == expected


def test_illegal_filename_umlaut() -> None:
    expected: Mapping[str, Collection[str]] = {"föö": {"ö"}}
    actual = check_filenames(["föö"])
    assert actual == expected


def test_illegal_filename_space() -> None:
    expected: Mapping[str, Collection[str]] = {"foo/bar baz": {" "}}
    actual = check_filenames(["foo/bar baz"])
    assert actual == expected


def test_illegal_filename_uses_common_reason() -> None:
    expected: Mapping[str, Collection[str]] = {"föö/bar": {"ö"}, "föö/baz": {"ö"}}
    actual = check_filenames(["föö/bar", "föö/baz"])
    assert actual == expected


def test_illegal_filename_multiple_chars() -> None:
    expected: Mapping[str, Collection[str]] = {"föö/bär": {"ö", "ä"}}
    actual = check_filenames(["föö/bär"])
    assert actual == expected

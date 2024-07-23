import io
import unittest.mock as mock

from check_posix_portable_filename import args_files_to_filenames


def test_empty_to_stdin() -> None:
    expected = ["foo", "bar", "baz"]

    with mock.patch("sys.stdin", io.StringIO("foo\nbar\nbaz\n")):
        actual = args_files_to_filenames([])
    assert actual == expected


def test_minus_to_stdin() -> None:
    expected = ["foo", "bar", "baz"]
    with mock.patch("sys.stdin", io.StringIO("foo\nbar\nbaz\n")):
        actual = args_files_to_filenames(["-"])
    assert actual == expected


def test_list_to_list() -> None:
    expected = ["foo", "bar", "baz"]
    actual = args_files_to_filenames(["foo", "bar", "baz"])
    assert actual == expected


def test_list_with_minus() -> None:
    expected = ["foo", "bar", "baz"]
    with mock.patch("sys.stdin", io.StringIO("bar\nbaz\n")):
        actual = args_files_to_filenames(["foo", "-"])
    assert actual == expected

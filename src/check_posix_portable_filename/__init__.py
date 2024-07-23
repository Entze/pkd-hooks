import argparse
import functools
import pathlib
import re
import sys
from typing import Collection, Mapping, MutableMapping, MutableSet, Sequence, Set

POSIX_PORTABLE_FILENAMES_STR: str = r"[^A-Za-z0-9._-]"
POSIX_PORTABLE_FILENAMES_PATTERN: re.Pattern = re.compile(POSIX_PORTABLE_FILENAMES_STR)


@functools.cache
def check_part(part: str) -> Set[str]:
    match_: Sequence[str] = re.findall(POSIX_PORTABLE_FILENAMES_PATTERN, part)
    return set(match_)


def check_filenames(filenames: Sequence[str]) -> Mapping[str, Collection[str]]:
    filename_to_illegal_characters: MutableMapping[str, MutableSet[str]] = {}

    for filename in filenames:
        path: pathlib.Path = pathlib.Path(filename)
        for part in path.parts:
            illegal_characters = check_part(part)
            if illegal_characters:
                if filename not in filename_to_illegal_characters:
                    filename_to_illegal_characters[filename] = set()
                filename_to_illegal_characters[filename] |= illegal_characters

    return filename_to_illegal_characters


def args_files_to_filenames(files: Sequence[str]) -> Sequence[str]:
    if files and "-" not in files:
        return files
    assert not files or "-" in files

    stdin_lines = [line.strip() for line in sys.stdin]

    return [file for file in files if file != "-"] + stdin_lines


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check if a name contains characters outside of the POSIX portable filenames set"
    )
    parser.add_argument("files", metavar="FILE", nargs="*", help="Filenames to check, stdin per default")

    args = parser.parse_args()

    filenames = args_files_to_filenames(args.files)
    filename_to_illegal_characters = check_filenames(filenames)

    retval = 0
    for filename, illegal_characters in filename_to_illegal_characters.items():
        print(f'"{filename}" contains illegal characters:', sorted(illegal_characters), file=sys.stderr)
        retval = 1

    return retval

import re
import typing as t
from pathlib import Path


class DocString(t.NamedTuple):
    content: str
    function_name: str

    def example_block(self) -> t.Union[t.Iterable[str], None]:
        expression_re = re.compile(r"Examples?:\n+((?:\s{8}.+?\n)+)")

        match = expression_re.search(self.content)
        if not match:
            return None

        example = match.group(1)

        return (line.strip() for line in example.strip().splitlines())


def docstrings(path: Path) -> t.Iterable[DocString]:
    docstring_re = re.compile(r"def (.+?)\((?:.|\n)+?:[\s\n]+?\"\"\"((?:.|\s|\n)+?)\"\"\"")

    with open(path) as f:
        text = f.read()
        docstrings = docstring_re.finditer(text)

    return map(
        lambda match: DocString(function_name=match.group(1), content=match.group(2)), docstrings
    )


def generate_test_function(docstring: DocString) -> str:
    if not (example_block := docstring.example_block()):
        return ""

    built_function = ""

    built_function += "@pytest.mark.mypy_testing\n"
    built_function += f"def test_mypy_{docstring.function_name}() -> None:\n"

    for line in map(lambda l: l.strip(), example_block):
        if not line:
            continue

        to_be_revealed = line.replace(">>> ", "")
        if line.startswith(">>> "):
            to_be_revealed = f"_.{to_be_revealed}"

        built_function += f"    reveal_type({to_be_revealed})  # R:\n"

    return built_function


def main(path: Path) -> str:
    imports = "import pytest\n\n"
    imports += f"import pydash as _\n\n\n"

    return imports + "\n\n".join(map(generate_test_function, docstrings(path)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="path to python file", type=Path)
    args = parser.parse_args()

    if not args.filename.exists():
        print(f"`{args.filename}` does not exist")
        exit(1)

    print(main(args.filename))

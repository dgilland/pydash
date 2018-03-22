"""
Conversion code generation for fp variants

Code generation is a prepackaging build step
You should not need to run this to use pydash.fp
"""

import os
from ._sig import arrays


def generate_modules():
    output_dir = os.path.dirname(__file__)
    for module in (arrays,):
        name = module_name(module)
        filepath = os.path.join(output_dir, name + ".py")
        with open(filepath, "w") as f:
            f.write("\n".join(module_code(name, module.__signatures__)))
            f.write("\n")


def module_name(module):
    return module.__name__.split('.')[-1]


def module_code(name, signatures):
    yield '"fp variant of {} functions"'.format(name)
    yield "import pydash as pyd"
    yield "from .convert import convert"
    yield "__all__ = ("
    for sig in signatures:
        yield '    "{}",'.format(sig[0])
    yield ")"
    yield ""
    yield ""
    templates = {
        1: "{0} = pyd.{0}",
        2: "{0} = convert({1!r}, pyd.{0})",
        3: "{0} = convert({1!r}, pyd.{0}, **{2!r})",
    }
    for sig in signatures:
        yield templates[len(sig)].format(*sig)


if __name__ == "__main__":
    generate_modules()

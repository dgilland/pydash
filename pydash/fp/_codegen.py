"""
Conversion code generation for fp variants

Code generation is a prepackaging build step
You should not need to run this to use pydash.fp
"""

import os
import pydash as pyd
from . import _docstr
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
    yield "docstrings = {"
    for sig in signatures:
        yield ""
        yield "    # {}".format(sig[0])
        if len(sig) == 1:
            continue
        yield '    "{}": """'.format(sig[0])
        yield function_docstr(*sig)
        yield '""",'
    yield "}"
    yield ""
    yield ""
    yield "def _convert(order, func, **kwargs):"
    yield "    fp_func = convert(order, func, **kwargs)"
    yield "    fp_func.__doc__ = docstrings.get(func.__name__, func.__doc__)"
    yield "    return fp_func"
    yield ""
    yield ""
    templates = {
        1: "{0} = pyd.{0}",
        2: "{0} = _convert({1!r}, pyd.{0})",
        3: "{0} = _convert({1!r}, pyd.{0}, **{2!r})",
    }
    for sig in signatures:
        yield templates[len(sig)].format(*sig)


def function_docstr(name, order, options=None):
    original_func = getattr(pyd, name)
    cap = (options or {}).get('cap', False)
    return _docstr.convert(name, order, cap, original_func.__doc__)


if __name__ == "__main__":
    generate_modules()

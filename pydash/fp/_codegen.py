"""
Conversion code generation for fp variants

Code generation is a prepackaging build step
You should not need to run this to use pydash.fp
"""

import os
import textwrap

import pydash as pyd
from . import _docstr
from ._sig import arrays


def generate_modules():
    output_dir = os.path.dirname(__file__)
    for module in (arrays,):
        name = module_name(module)
        functions = list(all_function_data(module))
        filepath = os.path.join(output_dir, name + ".py")
        with open(filepath, "w") as f:
            f.write("\n".join(module_code(name, functions)))
            f.write("\n")


def module_name(module):
    return module.__name__.split('.')[-1]


def all_function_data(module):
    for sig in module.signatures:
        docstr = module.docstr_overrides.get(sig[0], '')
        yield function_data(sig, docstr)


def function_data(sig, docstr):
    return {
        "target_name": sig[0],
        "conversion": function_conversion(sig),
        "docstr": docstr.rstrip(' ') or function_docstr(*sig),
    }


templates = {
    2: "{0} = pyd.{1}",
    3: "{0} = _convert({2!r}, pyd.{1})",
    4: "{0} = _convert({2!r}, pyd.{1}, **{3!r})",
}


def function_conversion(sig):
    return templates[len(sig)].format(*sig)


def function_docstr(target_name, source_name, order=None, options=None):
    if order is None:
        return None
    original_func = getattr(pyd, source_name)
    cap = (options or {}).get('cap', False)
    return _docstr.convert(
        target_name=target_name,
        source_name=source_name,
        order=order,
        cap=cap,
        docstr=original_func.__doc__
    )


def module_code(name, functions):
    yield '"fp variant of {} functions"'.format(name)
    yield "import pydash as pyd"
    yield "from .convert import convert"
    yield "__all__ = ("
    for func_data in functions:
        yield '    "{}",'.format(func_data["target_name"])
    yield ")"
    yield ""
    yield ""
    yield "docstrings = {"
    for func_data in functions:
        yield ""
        yield "    # {}".format(func_data["target_name"])
        if func_data["docstr"] is None:
            continue
        yield '    "{}": """'.format(func_data["target_name"])
        yield textwrap.dedent(func_data["docstr"])
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
    for func_data in functions:
        yield func_data["conversion"]


if __name__ == "__main__":
    generate_modules()

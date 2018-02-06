# -*- coding: utf-8 -*-
import functools
import inspect
import operator
import re

import pydash as pyd

from . import _code

"""
Naïve docstring manipulation for documenting fp variants
"""

# section titles
ARGS = 'Args:'
KWARGS = 'Keyword Args:'
EXAMPLE = 'Example:'


def convert(func_name, order, docstr):
    inverse = [p[1] for p in sorted(zip(order, range(len(order))))]
    sections = docstr_sections(docstr)
    args = arguments(sections)
    new_args = [ARGS] + pyd.flatten(rearg(inverse, args)) + ['']
    new_example = convert_example(func_name, args, inverse, sections)
    lines = []
    for section in sections:
        if section[0] == ARGS:
            lines.extend(new_args)
        elif section[0] == EXAMPLE:
            lines.extend(new_example)
        elif section[0] != KWARGS:
            lines.extend(section)
    return '\n'.join(lines)


def docstr_sections(docstr):
    is_title = re.compile(r'^[\w ]+:$').match
    lines = inspect.cleandoc(docstr).splitlines()
    # ah, just do it imperatively
    sections = [[]]
    for line in lines:
        if is_title(line):
            sections.append([])
        sections[-1].append(line)
    return sections


def get_section(title, sections):
    return pyd.find(sections, lambda s: s[0] == title)


def arguments(sections):
    args = []
    arg_re = re.compile(r'^    \*?\w+ +\([\w,| ]+\):')
    for title in [ARGS, KWARGS]:
        section = get_section(title, sections) or []
        for line in section[1:]:
            if arg_re.match(line):
                args.append([])
            if line:
                args[-1].append(line)
    return args


def rearg(order, args):
    if len(args) < 2 or len(args) <= max(order):
        return args
    count = len(order)
    base = operator.itemgetter(*order)(args)
    return [required(a) for a in base] + args[count:]


def convert_example(func_name, args, inverse, sections):
    example = get_section(EXAMPLE, sections)
    if example is None:
        return []
    arg_re = re.compile(r'\w+')
    arg_names = [arg_re.search(a[0]).group() for a in args]
    code_rearg = functools.partial(_code.rearg, func_name, arg_names, inverse)
    return [convert_code(code_rearg, line) for line in example]


def convert_code(code_rearg, line):
    code_prefix = '    >>> '
    if line.startswith(code_prefix):
        pos = len(code_prefix)
        return code_prefix + code_rearg(line[pos:])
    return line


opt_re = re.compile(r'(^    \*?\w+ +\([\w,| ]+), optional(\):)')
required = lambda arg: [opt_re.sub(r'\1\2', arg[0])] + arg[1:]

# -*- coding: utf-8 -*-
"""
Naïve docstring manipulation for documenting fp variants

TODO:
    * handle star args better
    * handle errors better
    * remove default doc for required args(?)
    * tests for docstring and code conversion
"""
import inspect
import operator
import re

import pydash as pyd

from . import _code


# section titles
ARGS = 'Args:'
KWARGS = 'Keyword Args:'
EXAMPLE = 'Example:'
WARNING = 'Warning:'
RETURNS = 'Returns:'
code_prefix = '    >>> '


def convert(target_name, source_name, order, cap, docstr):
    sections = docstr_sections(docstr)
    context = {
        'target_name': target_name,
        'source_name': source_name,
        'order': order,
        'inverse': [p[1] for p in sorted(zip(order, range(len(order))))],
        'args': arguments(sections),
        'cap': cap,
    }
    lines = []
    for section in sections:
        if section[0] == WARNING and 'modif' in section[1]:
            continue
        elif section[0] == ARGS:
            lines.extend(arity(**context))
            lines.extend(new_args(**context))
        elif section[0] == KWARGS:
            continue
        elif section[0] == RETURNS:
            lines.extend(convert_returns(section))
            lines.extend(cap_note(**context))
        elif section[0] == EXAMPLE:
            example = list(convert_example(section, context))
            if example[1:]:
                lines.extend(example)
            else:
                print("WARNING: no example for {}".format(target_name))
        else:
            lines.extend(section)
    return '\n'.join(lines)


def docstr_sections(docstr):
    is_title = re.compile(r'^([\w ]+:|\.\. \w+::.*)$').match
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


def arity(order, **_):
    return ['Arity: {}'.format(len(order)), '']


def new_args(**context):
    return [ARGS] + pyd.flatten(rearg(**context)) + ['']


def rearg(inverse, args, cap, **_):
    if len(args) < 2 or len(args) <= max(inverse):
        return args
    count = len(inverse)
    base = operator.itemgetter(*inverse)(args)
    extra = [] if cap else args[count:]
    return [required(a) for a in base] + extra


def convert_returns(section):
    return_re = re.compile('modified', re.I)
    return [
        section[0],
    ] + [return_re.sub('Resulting', ''.join(line)) for line in section[1:]]


def cap_note(cap, target_name, order, **_):
    if not cap:
        return []
    return [
        'Note:',
        '    The fp variant of {} takes'.format(target_name),
        '    exactly {} arguments'.format(len(order)),
        '',
    ]


def convert_example(section, context):
    if not _code.astor:
        return []
    arg_re = re.compile(r'\w+')
    arg_names = [arg_re.search(a[0]).group() for a in context["args"]]
    pos = len(code_prefix)

    def code_rearg(line):
        if not line.startswith(code_prefix):
            return line
        try:
            code = _code.rewrite(arg_names=arg_names, **context)(line[pos:])
            return code_prefix + code
        except TypeError:
            return 'invalid'

    return filter_invalid_code(code_rearg(line) for line in section)


def filter_invalid_code(seq):
    for line in seq:
        if line == 'invalid':
            swallow_invalid(seq)
        elif line.strip():
            yield line


def swallow_invalid(i):
    for line in i:
        if not line.startswith(code_prefix):
            break


opt_re = re.compile(r'(^    \*?\w+ +\([\w,| ]+), optional(\):)')


def required(arg):
    return [opt_re.sub(r'\1\2', arg[0])] + arg[1:]

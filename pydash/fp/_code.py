# -*- coding: utf-8 -*-
"""
Source code manipulation for rearranging fp variant examples
"""
import ast
import operator

try:
    import astor
except ImportError:
    astor = None


def rearg(func_name, arg_names, order, cap):
    transformer = Reorder(func_name, arg_names, order, cap)
    return lambda expr: transform(transformer, expr)


def transform(transformer, expr):
    tree = ast.parse(expr.strip())
    newtree = transformer.visit(tree)
    return astor.to_source(newtree).strip()


class Reorder(ast.NodeTransformer):
    def __init__(self, func_name, arg_names, order, cap):
        self.func_name = func_name
        self.arg_names = arg_names
        self.order = order
        self.cap = cap
        super(Reorder, self).__init__()

    def visit_Call(self, node):  # noqa
        if node.func.id != self.func_name:
            return self.generic_visit(node)
        required_count = len(self.order)
        found_count = len(node.args) + len(node.keywords)
        if found_count < required_count:
            raise TypeError('too few arguments')
        if found_count > required_count and self.cap:
            raise TypeError('too many arguments')
        args_dict = dict(zip(self.arg_names, node.args))
        args_dict.update({k.arg: k.value for k in node.keywords})
        if len(args_dict) < 2:
            return node
        args = [args_dict.get(name) for name in self.arg_names]
        new_args = list(operator.itemgetter(*self.order)(args))
        if required_count < len(node.args):
            if not (self.cap or node.keywords):
                new_args.extend(node.args[required_count:])
        node.args = tuple(new_args)
        node.keywords = []
        return node

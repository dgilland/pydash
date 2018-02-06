import ast
import operator

try:
    import astor
except ImportError:
    astor = None

"""
Source code manipulation for rearranging fp variant examples
"""


def rearg(func_name, arg_names, order, expr):
    transformer = Reorder(func_name, arg_names, order)
    return transform(transformer, expr)


def transform(transformer, expr):
    tree = ast.parse(expr.strip())
    newtree = transformer.visit(tree)
    return astor.to_source(newtree).strip()


class Reorder(ast.NodeTransformer):
    def __init__(self, func_name, arg_names, order):
        self.func_name = func_name
        self.arg_names = arg_names
        self.order = order
        super(Reorder, self).__init__()

    def visit_Call(self, node):
        if node.func.id != self.func_name:
            return self.generic_visit(node)
        args_dict = dict(zip(self.arg_names, node.args))
        args_dict.update({k.arg: k.value for k in node.keywords})
        if len(args_dict) < 2:
            return node
        if len(args_dict) < len(self.order):
            raise TypeError('too few arguments')
        args = [args_dict.get(name) for name in self.arg_names]
        node.args = operator.itemgetter(*self.order)(args)
        node.keywords = []
        return node

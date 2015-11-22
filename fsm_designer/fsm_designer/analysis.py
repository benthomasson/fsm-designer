
import ast


class AnalysisVisitor(ast.NodeVisitor):

    def visit_ClassDef(self, node):
        print "class", node.name
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        print "   def", node.name
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        # print type(node), dir(node)
        # print type(node.func), dir(node.func)
        # print node.func, node.lineno, node.col_offset
        # print node.func.id
        print "func", self.visit(node.func)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        # print type(node), dir(node)
        return self.visit(node.id)

    def visit_Attribute(self, node):
        # print type(node), dir(node)
        return self.visit(node.value)

    def visit_str(self, node):
        return node

    def visit_identifier(self, node):
        return node

    def generic_visit(self, node):
        # print node
        ast.NodeVisitor.generic_visit(self, node)

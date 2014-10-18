"""LEXOR to LATEX NodeConverter

"""

import re
from lexor.core.converter import NodeConverter, get_converter_namespace
from lexor.core.elements import ProcessingInstruction


class LatexNC(NodeConverter):
    """Perform macro substitutions. """

    def start(self, node):
        node.data = self.converter['MacroNC'].eval_text(node.data)
        return node


class LatexEnvironNC(NodeConverter):
    """Adjust the enviroments. """

    def __init__(self, converter):
        NodeConverter.__init__(self, converter)
        namespace = get_converter_namespace()
        self.re_label = re.compile(r'\\label\{(.*?)\}')
        if 'latex_labels' not in namespace:
            namespace['latex_labels'] = list()
        self.handle = {
            'equation': self.handle_equation,
            'align': self.handle_align,
            'subequations': self.handle_subequations,
        }

    def end(self, node):
        new_node = self.handle[node.name](node)
        environ = self.converter.document.namespace['math_environ']
        environ.append([new_node, node.get('par', '')])
        return new_node

    def handle_label(self, node):
        """Collect labels. """
        latex_labels = get_converter_namespace()['latex_labels']
        if 'id' in node:
            if node['id'] in latex_labels:
                self.msg('E001', node, [node['id']])
            else:
                latex_labels.append(node['id'])
        match = self.re_label.findall(node[0].data)
        for item in match:
            if item in latex_labels:
                self.msg('E001', node, [node['id']])
            else:
                latex_labels.append(item)

    def handle_equation(self, node):
        """Transform an equation. """
        name = node.name
        cdata = self.converter['MacroNC'].eval_text(node[0].data)
        if 'id' in node:
            self.handle_label(node)
            data = '\\begin{%s}\\label{%s}%s\\end{%s}'
            data = data % (name, node['id'], cdata, name)
        else:
            data = '\\begin{%s*}%s\\end{%s*}'
            data = data % (name, cdata, name)
        newnode = ProcessingInstruction('?latex', data)
        node.parent.insert_before(node.index, newnode)
        del node.parent[node.index]
        return newnode

    def handle_subequations(self, node):
        """Check for id. """
        if 'id' in node:
            self.handle_label(node)
        return node

    @staticmethod
    def label(node):
        """Check if we need to label. """
        if '\\label' in node[0].data:
            return True
        if 'class' in node:
            if 'label' in node['class']:
                return True
            if 'nolabel' in node['class']:
                return False
        if 'id' in node and node['id'] != '':
            return True
        return False

    @staticmethod
    def wrap(node):
        """Check if we need to surround the align enviroment. """
        if 'class' in node:
            if 'subeq' in node['class']:
                return 'subequations'
        return False

    def handle_align(self, node):
        """Translate align enviroment. """
        cdata = self.converter['MacroNC'].eval_text(node[0].data)
        label = self.label(node)
        if 'at' in node:
            if label:
                data = '\\begin{alignat}{%s}' % node['at']
            else:
                data = '\\begin{alignat*}{%s}' % node['at']
            if 'id' in node and '\\label' not in cdata:
                data += '\\label{%s}' % node['id']
            data += cdata
            if label:
                data += '\\end{alignat}'
            else:
                data += '\\end{alignat*}'
        else:
            if label:
                data = '\\begin{align}'
            else:
                data = '\\begin{align*}'
            if 'id' in node and '\\label' not in cdata:
                data += '\\label{%s}' % node['id']
            data += cdata
            if label:
                data += '\\end{align}'
            else:
                data += '\\end{align*}'
        if self.wrap(node):
            data = "\\begin{subequations}%s\end{subequations}" % data
        self.handle_label(node)
        newnode = ProcessingInstruction('?latex', data)
        node.parent.insert_before(node.index, newnode)
        del node.parent[node.index]
        return newnode

    def convert(self):
        """Iterate through the items in the `math_environ` list
        and adjust them in the paragraph. """
        environ = self.converter.document.namespace['math_environ']
        for item, info in environ:
            prev_ele = item.previous_element
            next_ele = item.next_element
            if 'begin' in info:
                if 'end' in info:
                    pass
                elif next_ele is not None and next_ele.name == 'p':
                    next_ele.insert_before(0, item)
            elif prev_ele is not None and prev_ele.name == 'p':
                prev_ele.append_child_node(item)
                if 'end' in info:
                    pass
                elif next_ele is not None and next_ele.name == 'p':
                    prev_ele.extend_children(next_ele)
                    del next_ele.parent[next_ele.index]


MSG = {
    'E001': 'LaTeX label `{0}` already defined',
}
MSG_EXPLANATION = [
    """
    - Address references can only be defined once. 'E001' tells you
      the location of where it was first defined and the location
      where you are trying to redefine it.

    Okay:
        [1]: http://google.com
        [2]: http://daringfireball.net/projects/markdown/

    E001:
        [1]: http://google.com
        [1]: http://daringfireball.net/projects/markdown/

""",
]

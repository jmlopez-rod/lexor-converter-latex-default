"""LEXOR to HTML FIGURE NodeConverter

Node writer description.

"""

from lexor.core.converter import NodeConverter, get_converter_namespace
import lexor.core.elements as core


class FigureNC(NodeConverter):
    """Adjust a figure. """

    def end(self, node):
        center = core.Element('center')
        caption = core.Element('caption')
        caption['_void'] = 'true'
        if 'id' in node:
            latex_labels = get_converter_namespace()['latex_labels']
            if node['id'] in latex_labels:
                self.converter['LatexNC'].msg('E001', node, [node['id']])
            else:
                latex_labels.append(node['id'])
            caption['id'] = node['id']
            del node['id']
        caption.extend_children(node)
        if 'src' in node:
            if '.tex' in node['src']:
                image = core.Void('input')
                image['args'] = node['src']
            else:
                image = core.Void('includegraphics')
                image['args'] = node['src']
                if 'width' in node:
                    image['width'] = node['width']
                    del node['width']
                else:
                    image['width'] = '5.97in'
            del node['src']
            center.append_child(image)
        node.append_child(center)
        node.append_child(caption)
        if node.attlen == 0:
            node['!htb'] = ""
        return node

from sphinx.builders.latex import LaTeXBuilder
from sphinx.transforms.post_transforms import SphinxPostTransform
from docutils import nodes


class HiddenNode(nodes.Element):
    """A node that will not be rendered."""

    def __init__(self, rawsource="", *children, **attributes):
        super().__init__("", **attributes)

    @classmethod
    def add_node(cls, app):
        app.add_node(
            cls,
            override=True,
            html=(visit_HiddenNode, None),
            latex=(visit_HiddenNode, None),
            textinfo=(visit_HiddenNode, None),
            text=(visit_HiddenNode, None),
            man=(visit_HiddenNode, None),
        )


def visit_HiddenNode(self, node):
    raise nodes.SkipNode


class HideDropdownsTransform(SphinxPostTransform):
    """Replaces nodes with dropdowns with a node that is ignored when rendering."""

    default_priority = 400

    def apply(self, **kwargs):
        for node in self.document.traverse(nodes.Element):
            if set(node["classes"]) & {"dropdown", "toggle"}:
                node.replace_self([HiddenNode()])


def setup(app):
    app.connect("builder-inited", setup_transforms)


def setup_transforms(app):
    if not isinstance(app.builder, LaTeXBuilder):
        return

    app.add_post_transform(HideDropdownsTransform)
    HiddenNode.add_node(app)
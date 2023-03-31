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


class HideNodesTransform(SphinxPostTransform):
    """Hides nodes with the given classes during rendering."""

    default_priority = 400

    def apply(self, **kwargs):
        builder_ignore_classes = self.app.config['builder_ignore_classes']
        ignore_classes = builder_ignore_classes.get(
            self.app.builder.name, set()
        )
        print(f"Ignoring {ignore_classes} for {self.app.builder.name} builder")
        for node in self.document.traverse(nodes.Element):
            node_classes = set(node['classes'])
            if node_classes & ignore_classes:
                print(f"Ignoring {node} due to {node_classes & ignore_classes}")
                node.replace_self([HiddenNode()])


DEFAULT_BUILDER_IGNORE_CLASSES = {
    "latex": [
        "dropdown", "toggle", "margin",
    ]
}


def setup(app):
    app.connect("builder-inited", setup_transforms)
    app.connect('config-inited', setup_ignore_classes)
    app.add_config_value("builder_ignore_classes", DEFAULT_BUILDER_IGNORE_CLASSES, "env", [dict])



def setup_ignore_classes(app, config):
    config['builder_ignore_classes'] = {
        k: set(v) for k, v in config['builder_ignore_classes'].items()
    }


def setup_transforms(app):
    app.add_post_transform(HideNodesTransform)
    HiddenNode.add_node(app)

import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive, directives
import codecs
from sphinxcontrib.mermaid import (
    align_spec, 
    search_image_for_language,
    mermaid,
    html_visit_mermaid,
    latex_visit_mermaid,
    texinfo_visit_mermaid,
    text_visit_mermaid,
    man_visit_mermaid,
    Mermaid,
    MermaidClassDiagram,
    figure_wrapper,
)

class Mermaid(Directive):
    """
    Directive to insert arbitrary Mermaid markup.
    """
    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'alt': directives.unchanged,
        'align': align_spec,
        'caption': directives.unchanged,
        'name': directives.unchanged,
    }

    def get_mm_code(self):
        if self.arguments:
            # try to load mermaid code from an external file
            document = self.state.document
            if self.content:
                return [document.reporter.warning(
                    'Mermaid directive cannot have both content and '
                    'a filename argument', line=self.lineno)]
            env = self.state.document.settings.env
            argument = search_image_for_language(self.arguments[0], env)
            rel_filename, filename = env.relfn2path(argument)
            env.note_dependency(rel_filename)
            try:
                with codecs.open(filename, 'r', 'utf-8') as fp:
                    mmcode = fp.read()
            except (IOError, OSError):
                return [document.reporter.warning(
                    'External Mermaid file %r not found or reading '
                    'it failed' % filename, line=self.lineno)]
        else:
            # inline mermaid code
            mmcode = '\n'.join(self.content)
            if not mmcode.strip():
                return [self.state_machine.reporter.warning(
                    'Ignoring "mermaid" directive without content.',
                    line=self.lineno)]
        return mmcode

    def run(self):

        node = mermaid()
        node['code'] = self.get_mm_code()
        node['options'] = {}
        if 'alt' in self.options:
            node['alt'] = self.options['alt']
        if 'align' in self.options:
            node['align'] = self.options['align']
        if 'inline' in self.options:
            node['inline'] = True

        caption = self.options.get('caption')
        if caption:
            node = figure_wrapper(self, node, caption)

        self.add_name(node)
        return [node]


def install_js(app, *args):
    # add required javascript
    if not app.config.mermaid_version:
        _mermaid_js_url = None     # asummed is local
    elif app.config.mermaid_version == "latest":
        _mermaid_js_url = "https://unpkg.com/mermaid/dist/mermaid.min.js"
    else:
        _mermaid_js_url = f"https://unpkg.com/mermaid@{app.config.mermaid_version}/dist/mermaid.min.js"
    if _mermaid_js_url:
        app.add_js_file(_mermaid_js_url, priority=app.config.mermaid_js_priority)

    if app.config.mermaid_init_js:
        # If mermaid is local the init-call must be placed after `html_js_files` which has a priority of 800.
        priority = 500 if _mermaid_js_url is not None else 801
        app.add_js_file(None, body=app.config.mermaid_init_js, priority=priority)


def setup(app):
    app.add_node(
        mermaid,
        html=(html_visit_mermaid, None),
        latex=(latex_visit_mermaid, None),
        texinfo=(texinfo_visit_mermaid, None),
        text=(text_visit_mermaid, None),
        man=(man_visit_mermaid, None),
    )
    app.add_directive("mermaid", Mermaid)
    app.add_directive("autoclasstree", MermaidClassDiagram)

    app.add_config_value("mermaid_cmd", "mmdc", "html")
    app.add_config_value("mermaid_cmd_shell", "False", "html")
    app.add_config_value("mermaid_pdfcrop", "", "html")
    app.add_config_value("mermaid_output_format", "raw", "html")
    app.add_config_value("mermaid_params", list(), "html")
    app.add_config_value("mermaid_js_priority", 500, "html")
    app.add_config_value("mermaid_verbose", False, "html")
    app.add_config_value("mermaid_sequence_config", False, "html")
    app.add_config_value("mermaid_version", "latest", "html")
    app.add_config_value(
        "mermaid_init_js", "mermaid.initialize({startOnLoad:true});", "html"
    )
    app.connect("html-page-context", install_js)

    return {"version": sphinx.__display_version__, "parallel_read_safe": True}

import contextlib
from IPython.utils.capture import capture_output
from IPython.display import display

import base64
import subprocess


@contextlib.contextmanager
def captured_as_mimebundle():
    mimebundle = {}
    with capture_output() as c:
        yield mimebundle

    for output in c.outputs:
        mimebundle.update(output.data)


@contextlib.contextmanager
def displayed_as_mimebundle():
    with captured_as_mimebundle() as mimebundle:
        yield
    display(mimebundle, raw=True)


def format_dot(src, dpi):
    mime = {}
    result = subprocess.run(
        ["dot", "-T", "svg"], capture_output=True, input=src.encode("utf-8")
    )
    if result.returncode:
        mime["text/plain"] = result.stderr.decode()
    else:
        mime["image/svg+xml"] = result.stdout.decode()

        result = subprocess.run(
            ["dot", "-T", "png", f"-Gdpi={dpi:d}"],
            capture_output=True,
            input=src.encode("utf-8"),
        )
        mime["image/png"] = base64.b64encode(result.stdout).decode() + "\n"

    return mime


class DOT:
    def __init__(self, source, dpi=300):
        self.source = source
        self.dpi = dpi

    def _repr_mimebundle_(self, include=None, exclude=None):
        return format_dot(self.source, self.dpi)
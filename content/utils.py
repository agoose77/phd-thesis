import contextlib
from IPython.utils.capture import capture_output
from IPython.display import display


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

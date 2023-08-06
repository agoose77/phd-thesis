import pathlib


THIS_FILE = pathlib.Path(__file__).resolve()


def setup(app):
    app.config.templates_path.append(
        str(THIS_FILE.parent / "_templates")
    )
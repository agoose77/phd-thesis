def setup_assets_policy(app, config):
    print(f"Setting HTML policy to {app.config.html_assets_policy}")
    app.set_html_assets_policy(app.config.html_assets_policy)


def setup(app):
    app.add_config_value("html_assets_policy", "per_page", "html")
    app.connect('config-inited', setup_assets_policy)

    print(app.builder)
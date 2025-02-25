def define_env(env):
    # get mkdocstrings' Python handler
    python_handler = env.conf["plugins"]["mkdocstrings"].get_handler("python")
 
    # get the `update_env` method of the Python handler
    update_env = python_handler.update_env

    # override the `update_env` method of the Python handler
    def patched_update_env(config):
        update_env(config=config)

        # get the `convert_markdown` filter of the env
        convert_markdown = python_handler.env.filters["convert_markdown"]

        # build a chimera made of macros+mkdocstrings
        def render_convert(markdown: str, *args, **kwargs):
            return convert_markdown(env.render(markdown), *args, **kwargs)

        # patch the filter
        python_handler.env.filters["convert_markdown"] = render_convert
    
    # patch the method
    python_handler.update_env = patched_update_env
import json
import typing

import pygments.lexers
import pygments.styles
from pygments.formatters.terminal256 import Terminal256Formatter

from adz import CFG


class Echo:
    def __init__(self, config: CFG):
        self.config = config

    def __call__(self, obj: typing.Any = None, ext: str = "text"):
        if isinstance(obj, bytes):
            try:
                obj = json.loads(obj)
            except json.decoder.JSONDecodeError:
                obj = obj.decode()

        txt = obj
        if isinstance(obj, (dict, list)):
            txt = json.dumps(
                obj=obj,
                sort_keys=True,
                indent=4,
                separators=(",", ": "),
                ensure_ascii=False,
                default=str,
            )

        if not txt:
            return print()

        if not self.config.settings["colors"]:
            return print(txt)

        lexer = pygments.lexers.get_lexer_by_name(ext)
        formatter = Terminal256Formatter(
            style=pygments.styles.get_style_by_name(self.config.settings["theme"])
        )
        print(pygments.highlight(txt or "".encode(), lexer, formatter).strip())

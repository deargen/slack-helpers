from dotenv import load_dotenv

load_dotenv()

import logging
import socket
import traceback

from rich.traceback import Traceback

from slack_helpers.send_only import (
    send_svg_as_pdf,
    send_text_as_file,
)
from slack_helpers.utils.log import setup_logging
from slack_helpers.utils.rich import (
    CONSOLE_WIDTH,
    rich_traceback_to_html,
    rich_traceback_to_string,
    rich_traceback_to_svg,
)

logger = logging.getLogger(__name__)


def main():
    try:
        setup_logging()
        raise Exception("This is an exception")  # noqa: TRY301 TRY002
    except Exception:
        logger.exception("Exception occurred")
        slack_text = f"Exception occurred from host {socket.gethostname()}\n\n```{traceback.format_exc()}```"

        tb = Traceback(show_locals=True, width=CONSOLE_WIDTH)
        tb_text = rich_traceback_to_string(tb)
        tb_html = rich_traceback_to_html(tb)
        tb_svg = rich_traceback_to_svg(
            tb, title=f"Exception occurred from host {socket.gethostname()}"
        )

        send_text_as_file(
            filename="traceback.txt",
            content=tb_text,
            title="traceback.txt",
            ensure_preview=True,
            initial_comment=slack_text,
        )
        send_text_as_file(
            filename="traceback.svg",
            content=tb_svg,
            title="traceback.svg (dear-viewer compatible)",
            ensure_preview=True,
        )
        send_text_as_file(
            filename="traceback.html",
            content=tb_html,
            title="traceback.html",
            initial_comment="* To view the HTML without downloading (or just use dear-viewer):\n\n"
            "1. Open in new window (it will open in Chrome)\n2. Copy all content\n"
            "3. <F12> to open Dev Tools\n4. Elements -> <html> right click -> Edit as HTML\n"
            "5. Paste\n6. <Enter> to apply changes",
        )
        send_svg_as_pdf(
            filename="traceback.pdf",
            svg_file=tb_svg,
            title="traceback.pdf",
        )


if __name__ == "__main__":
    main()

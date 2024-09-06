import dotenv

dotenv.load_dotenv()

import logging
from io import BytesIO
from pprint import pformat
from typing import Any

import requests
from slack_sdk import WebClient

from slack_helpers import app
from slack_helpers.interactive import handler
from slack_helpers.utils.log import setup_logging

logger = logging.getLogger(__name__)

assert app is not None, "Set environment variables SLACK_* first."


@app.message("hello")
def hello_message(body: dict[str, Any], say):
    logger.info("Received a hello command")
    logger.info(f"body: {pformat(body)}")
    say(text=f"Hi <@{body['event']['user']}>!")


@app.message("cat")
def cat_photo(body: dict[str, Any], client: WebClient):
    """Use `client` over `say` if you want to send more complex messages."""
    logger.info("Received a cat command")
    logger.info(f"body: {pformat(body)}")

    # download the photo from the internet
    url = "https://cdn.freecodecamp.org/curriculum/cat-photo-app/relaxing-cat.jpg"
    response = requests.get(url)
    f = BytesIO(response.content)

    client.files_upload_v2(
        channel=body["event"]["channel"],
        file=f,
        filename="cat.jpg",
        title="Cat",
        initial_comment="Here's a cat photo!",
    )


@app.command("/echo")
def echo_command(ack, body, say):
    """Command needs `ack()` to be called."""
    logger.info("Received an echo command")
    logger.info(f"body: {pformat(body)}")
    ack()
    say(f"Hi <@{body['user_id']}>! {body['text']}")


def main():
    logger.info("Starting the app")
    handler.start()


if __name__ == "__main__":
    try:
        setup_logging()
        main()
    except Exception:
        logger.exception("An error occurred")

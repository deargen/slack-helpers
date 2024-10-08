import logging
import subprocess

logger = logging.getLogger(__name__)


class FontNotInstalledError(Exception):
    def __init__(self, font_name: str):
        self.message = f"Font {font_name} is not installed."
        super().__init__(self.message)


def verify_fonts_installed():
    """
    This function verifies that the FiraCode font is installed because Rich Console.export_svg() uses it.

    Actually, the svg itself doesn't need the font but when we convert it to PDF using cairosvg, the font is needed.
    """
    cmd = ["fc-match", "FiraCode:style=Regular"]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

    if not output.decode("utf-8").startswith("FiraCode-Regular"):
        raise FontNotInstalledError("FiraCode")

    cmd = ["fc-match", "FiraCode:style=Bold"]
    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

    if not output.decode("utf-8").startswith("FiraCode-Bold"):
        raise FontNotInstalledError("FiraCode")


def verify_fonts_bool():
    try:
        verify_fonts_installed()
    except FontNotInstalledError:
        logger.exception("😡")
        return False
    else:
        logger.info("✅ FiraCode font is installed.")
        return True


if __name__ == "__main__":
    verify_fonts_installed()

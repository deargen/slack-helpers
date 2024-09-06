from dotenv import load_dotenv

load_dotenv()

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from slack_helpers.send_only import (
    send_divider,
    send_file,
    send_matplotlib_fig,
    send_pil_image,
    send_text,
)

if __name__ == "__main__":
    send_text("Hello, World!")
    send_divider()
    send_file(
        filename="1A0G.pdb",
        file="/Users/kiyoon/project/PPMI/data/masif/ppi_db/pdbs/1A0G.pdb",
        title="My Test PDB File",
        initial_comment="Here's a PDB file for you!",
    )

    x = np.linspace(0, 10, 100)
    y = np.sin(x)

    fig, ax = plt.subplots()
    ax.plot(x, y)

    send_matplotlib_fig(
        filename="matplotlib_fig.pdf",
        fig=fig,
        title="My Test Matplotlib Figure",
        initial_comment="Here's a matplotlib figure for you!",
    )

    np_image = np.random.rand(100, 100, 3)
    pil_image = Image.fromarray(np_image, "RGB")

    send_pil_image(
        filename="pil_image.png",
        image=pil_image,
        title="My Test PIL Image",
        initial_comment="Here's a PIL image for you!",
    )

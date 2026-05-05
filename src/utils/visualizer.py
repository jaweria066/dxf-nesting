"""
Visualizer: renders the nesting layout using matplotlib.
Saves output as a PNG image.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from src.nesting.nester import Sheet, Shape
from typing import List


def visualize(sheet: Sheet, unplaced: List[Shape], output_path: str = "output/layout.png"):
    fig, ax = plt.subplots(1, figsize=(12, 7))

    # Sheet background
    ax.set_xlim(0, sheet.width)
    ax.set_ylim(0, sheet.height)
    ax.set_facecolor("#f0f4f8")
    fig.patch.set_facecolor("#ffffff")

    ax.add_patch(patches.Rectangle(
        (0, 0), sheet.width, sheet.height,
        linewidth=2, edgecolor="#1A5276", facecolor="#eaf4fb"
    ))

    # Draw placed shapes
    random.seed(42)
    for shape in sheet.placed_shapes:
        color = "#{:06x}".format(random.randint(0x557799, 0xAADDFF))
        rect = patches.Rectangle(
            (shape.x, shape.y), shape.width, shape.height,
            linewidth=1.2, edgecolor="#1A5276", facecolor=color, alpha=0.75
        )
        ax.add_patch(rect)
        ax.text(
            shape.x + shape.width / 2,
            shape.y + shape.height / 2,
            shape.id,
            ha="center", va="center",
            fontsize=7, color="#1c1c1c"
        )

    ax.set_title(
        f"DXF Nesting Layout  |  {len(sheet.placed_shapes)} placed  |  "
        f"Efficiency: {sheet.efficiency:.1f}%",
        fontsize=13, fontweight="bold", color="#1A5276", pad=12
    )
    ax.set_xlabel("Width (mm)")
    ax.set_ylabel("Height (mm)")

    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Layout saved to {output_path}")

"""
Nester: Bottom-Left Fit heuristic for 2D bin packing.

Places each shape at the lowest, then leftmost available position
on the sheet. Simple, fast, and effective for rectangular bounding boxes.
"""

from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Shape:
    """A 2D shape with its bounding box and metadata."""
    id: str
    width: float
    height: float
    x: float = 0.0
    y: float = 0.0
    placed: bool = False

    @property
    def area(self) -> float:
        return self.width * self.height

    def overlaps(self, other: "Shape") -> bool:
        """Check if this shape overlaps with another (AABB test)."""
        return not (
            self.x + self.width <= other.x or
            other.x + other.width <= self.x or
            self.y + self.height <= other.y or
            other.y + other.height <= self.y
        )


@dataclass
class Sheet:
    """The cutting surface shapes are placed on."""
    width: float
    height: float
    placed_shapes: List[Shape] = field(default_factory=list)

    @property
    def used_area(self) -> float:
        return sum(s.area for s in self.placed_shapes)

    @property
    def efficiency(self) -> float:
        total = self.width * self.height
        return (self.used_area / total * 100) if total > 0 else 0.0

    def fits_at(self, shape: Shape, x: float, y: float) -> bool:
        """Return True if shape can be placed at (x, y) without overlap or overflow."""
        if x + shape.width > self.width or y + shape.height > self.height:
            return False
        test = Shape(id=shape.id, width=shape.width, height=shape.height, x=x, y=y)
        return all(not test.overlaps(placed) for placed in self.placed_shapes)

    def place(self, shape: Shape, x: float, y: float) -> None:
        shape.x = x
        shape.y = y
        shape.placed = True
        self.placed_shapes.append(shape)


class Nester:
    """
    Bottom-Left Fit nester.

    Sorts shapes by area (largest first) and places each one
    at the lowest then leftmost valid position on the sheet.
    """

    def __init__(self, sheet_width: float, sheet_height: float, spacing: float = 2.0):
        self.sheet_width = sheet_width
        self.sheet_height = sheet_height
        self.spacing = spacing  # gap between parts

    def nest(self, shapes: List[Shape]) -> Tuple[Sheet, List[Shape]]:
        """
        Attempt to place all shapes on a single sheet.

        Returns:
            sheet      — the sheet with all placed shapes
            unplaced   — shapes that did not fit
        """
        sheet = Sheet(self.sheet_width, self.sheet_height)

        # Sort largest-area first — improves packing efficiency
        sorted_shapes = sorted(shapes, key=lambda s: s.area, reverse=True)

        unplaced = []
        step = self.spacing

        for shape in sorted_shapes:
            placed = False
            y = 0.0
            while y + shape.height <= self.sheet_height:
                x = 0.0
                while x + shape.width <= self.sheet_width:
                    if sheet.fits_at(shape, x, y):
                        sheet.place(shape, x, y)
                        placed = True
                        break
                    x += step
                if placed:
                    break
                y += step

            if not placed:
                unplaced.append(shape)

        return sheet, unplaced

    def summary(self, sheet: Sheet, unplaced: List[Shape]) -> str:
        lines = [
            f"Sheet: {sheet.width} x {sheet.height}",
            f"Placed:   {len(sheet.placed_shapes)} shapes",
            f"Unplaced: {len(unplaced)} shapes",
            f"Efficiency: {sheet.efficiency:.1f}%",
        ]
        return "\n".join(lines)

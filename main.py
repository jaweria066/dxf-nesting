"""
DXF Nesting System — main entry point.

Usage:
    python main.py <input.dxf> [sheet_width] [sheet_height]

Example:
    python main.py samples/parts.dxf 1000 500
"""

import sys
from src.parser.dxf_parser import DXFParser
from src.nesting.nester import Nester
from src.utils.visualizer import visualize


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input.dxf> [sheet_width] [sheet_height]")
        print("Example: python main.py samples/parts.dxf 1000 500")
        sys.exit(1)

    input_file  = sys.argv[1]
    sheet_width  = float(sys.argv[2]) if len(sys.argv) >= 3 else 1000.0
    sheet_height = float(sys.argv[3]) if len(sys.argv) >= 4 else 500.0

    print(f"[1/3] Parsing DXF file: {input_file}")
    parser = DXFParser(input_file)
    shapes = parser.parse()
    print(f"      Found {len(shapes)} shapes")

    print(f"[2/3] Running nesting on {sheet_width}x{sheet_height} sheet...")
    nester = Nester(sheet_width=sheet_width, sheet_height=sheet_height, spacing=2.0)
    sheet, unplaced = nester.nest(shapes)

    print("[3/3] Results:")
    print(nester.summary(sheet, unplaced))

    visualize(sheet, unplaced, output_path="output/layout.png")


if __name__ == "__main__":
    main()

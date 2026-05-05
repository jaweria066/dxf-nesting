#  DXF Nesting System

> A 2D bin-packing tool that automatically arranges DXF cutting patterns on a sheet to maximize material usage and minimize waste.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-7%20passing-brightgreen?style=flat-square)

---

##  Problem

In CNC cutting and manufacturing, how you arrange parts on a material sheet directly affects how much you waste. Poor arrangement = money lost. This is the classic **2D bin-packing problem** — and solving it efficiently is non-trivial.

##  What This Does

Given a DXF file containing shapes (parts to cut) and a sheet size, this tool:
1. **Parses** the DXF file and extracts each shape's bounding box
2. **Sorts** shapes by area (largest first) for better packing efficiency
3. **Places** each shape using a Bottom-Left Fit heuristic — no overlaps, no overflow
4. **Visualizes** the result as a PNG layout image
5. **Reports** packing efficiency (% of sheet used)

---

## Project Structure

```
dxf-nesting/
├── main.py                   # Entry point
├── requirements.txt
├── src/
│   ├── parser/
│   │   └── dxf_parser.py     # DXF file reader (uses ezdxf)
│   ├── nesting/
│   │   └── nester.py         # Bottom-Left Fit algorithm
│   └── utils/
│       └── visualizer.py     # matplotlib layout renderer
├── tests/
│   └── test_nester.py        # Unit tests (pytest)
├── samples/                  # Sample DXF files
└── output/                   # Generated layout images
```

---

##  Getting Started

```bash
# Clone the repo
git clone https://github.com/jaweria066/dxf-nesting.git
cd dxf-nesting

# Install dependencies
pip install -r requirements.txt

# Run on a DXF file
python main.py samples/parts.dxf 1000 500
```

Output will be saved to `output/layout.png`.

---

##  Running Tests

```bash
pytest tests/ -v
```

All 7 tests cover shape geometry, overlap detection, placement logic, and efficiency bounds.

---

##  Algorithm

The current implementation uses a **Bottom-Left Fit** heuristic:

1. Sort shapes by area descending (biggest first fills gaps better)
2. For each shape, scan the sheet from bottom-left to top-right
3. Place the shape at the first valid position (no overlap, within bounds)
4. Track efficiency as `used_area / sheet_area × 100%`

**Planned improvements:**
- Rotation support (0°, 90°)
- Guillotine cut algorithm
- Export nested layout back to DXF

---

##  Example Output

```
[1/3] Parsing DXF file: samples/parts.dxf
      Found 12 shapes
[2/3] Running nesting on 1000x500 sheet...
[3/3] Results:
Sheet: 1000 x 500
Placed:   12 shapes
Unplaced: 0 shapes
Efficiency: 78.4%
Layout saved to output/layout.png
```

---

## 👩‍💻 Author

**Jaweria Qadir** — Computer Engineering @ Istanbul Kultur University  
[GitHub](https://github.com/jaweria066)

# DXF Nesting System

A friend of mine works at a laser cutting shop. He told me the software they use to arrange parts on metal sheets before cutting costs thousands of dollars and even then it doesn't always do a great job, so they end up wasting a lot of material.

That got me thinking: the core of what that software does is actually a computer science problem how do you fit as many shapes as possible onto a sheet without overlap? I figured I could build a basic version of it myself.

This is that project. It's not finished and it's not perfect, but it works.

---

## What it does

You give it a DXF file (the file format laser cutters use) and a sheet size. It reads all the shapes in the file, then tries to arrange them on the sheet to minimize wasted space. At the end it shows you a layout image and tells you how efficiently the sheet was used.

---

## How to run it

```bash
pip install -r requirements.txt
python main.py your_file.dxf 1000 500
```

The numbers at the end are the sheet width and height in mm. Output image is saved to the `output/` folder.

---

## Project structure

```
dxf-nesting/
├── main.py
├── src/
│   ├── parser/
│   │   └── dxf_parser.py     # reads the DXF file, extracts shapes
│   ├── nesting/
│   │   └── nester.py         # the placement algorithm
│   └── utils/
│       └── visualizer.py     # draws the result
└── tests/
    └── test_nester.py
```

---

## Algorithm

Right now it uses a Bottom-Left Fit approach it sorts shapes by size (biggest first) and places each one at the lowest, leftmost available spot on the sheet. It's a greedy heuristic, not optimal, but it runs fast and gives decent results.

Things I want to add next:
- trying rotations (0° and 90°) to fit more parts
- a smarter algorithm that handles irregular shapes, not just bounding boxes
- exporting the final layout back to DXF so it can actually be sent to the machine

---

## Tests

```bash
python -m pytest tests/ -v
```

---

## Why DXF?

DXF (Drawing Exchange Format) is the standard file format used by laser cutters, CNC machines, and CAD software. It made sense to work with real files instead of making up my own format.

---

*Built by Jaweria Qadir (Still working on it)— Computer Engineering student at Istanbul Kultur University*

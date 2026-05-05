"""Tests for the nesting algorithm."""

import pytest
from src.nesting.nester import Shape, Sheet, Nester


def test_shape_area():
    s = Shape(id="s1", width=100, height=50)
    assert s.area == 5000


def test_shapes_overlap():
    a = Shape(id="a", width=100, height=100, x=0, y=0)
    b = Shape(id="b", width=100, height=100, x=50, y=50)
    assert a.overlaps(b)


def test_shapes_no_overlap():
    a = Shape(id="a", width=100, height=100, x=0, y=0)
    b = Shape(id="b", width=100, height=100, x=100, y=0)
    assert not a.overlaps(b)


def test_nester_places_shapes():
    nester = Nester(sheet_width=500, sheet_height=500, spacing=1.0)
    shapes = [Shape(id=f"s{i}", width=100, height=100) for i in range(4)]
    sheet, unplaced = nester.nest(shapes)
    assert len(sheet.placed_shapes) == 4
    assert len(unplaced) == 0


def test_nester_unplaced_when_sheet_too_small():
    nester = Nester(sheet_width=150, sheet_height=100, spacing=1.0)
    shapes = [Shape(id=f"s{i}", width=100, height=100) for i in range(3)]
    sheet, unplaced = nester.nest(shapes)
    assert len(unplaced) > 0


def test_efficiency_within_bounds():
    nester = Nester(sheet_width=500, sheet_height=500)
    shapes = [Shape(id=f"s{i}", width=100, height=100) for i in range(9)]
    sheet, _ = nester.nest(shapes)
    assert 0 <= sheet.efficiency <= 100


def test_no_overlaps_after_nesting():
    nester = Nester(sheet_width=600, sheet_height=600, spacing=1.0)
    shapes = [Shape(id=f"s{i}", width=80, height=60) for i in range(10)]
    sheet, _ = nester.nest(shapes)
    placed = sheet.placed_shapes
    for i in range(len(placed)):
        for j in range(i + 1, len(placed)):
            assert not placed[i].overlaps(placed[j]), \
                f"Overlap detected between {placed[i].id} and {placed[j].id}"

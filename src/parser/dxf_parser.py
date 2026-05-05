"""
DXFParser: reads DXF files and extracts shapes as bounding boxes.
Uses ezdxf to handle the DXF format.
"""

import ezdxf
from ezdxf.math import BoundingBox2d
from typing import List
from src.nesting.nester import Shape


class DXFParser:
    """Parse a DXF file and return a list of Shape objects."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def parse(self) -> List[Shape]:
        doc = ezdxf.readfile(self.filepath)
        msp = doc.modelspace()

        shapes = []
        for i, entity in enumerate(msp):
            bbox = self._get_bbox(entity)
            if bbox is None:
                continue
            w = bbox.extmax.x - bbox.extmin.x
            h = bbox.extmax.y - bbox.extmin.y
            if w > 0 and h > 0:
                shapes.append(Shape(id=f"shape_{i}", width=round(w, 4), height=round(h, 4)))

        return shapes

    def _get_bbox(self, entity) -> BoundingBox2d | None:
        try:
            points = []
            dxftype = entity.dxftype()

            if dxftype == "LINE":
                points = [entity.dxf.start[:2], entity.dxf.end[:2]]
            elif dxftype in ("LWPOLYLINE", "POLYLINE"):
                points = [v[:2] for v in entity.get_points()]
            elif dxftype == "CIRCLE":
                cx, cy = entity.dxf.center.x, entity.dxf.center.y
                r = entity.dxf.radius
                points = [(cx - r, cy - r), (cx + r, cy + r)]
            elif dxftype == "ARC":
                cx, cy = entity.dxf.center.x, entity.dxf.center.y
                r = entity.dxf.radius
                points = [(cx - r, cy - r), (cx + r, cy + r)]
            elif dxftype == "SPLINE":
                points = [p[:2] for p in entity.control_points]
            else:
                return None

            if not points:
                return None
            bbox = BoundingBox2d(points)
            return bbox if bbox.has_data else None
        except Exception:
            return None

"""Plaquinhas de teste de encaixe da moldura do DB9 (4 folgas). Imprima, teste na moldura
e use a folga da plaquinha que encaixar justa em `db9_clear` dos case_*.py.
Número de furinhos redondos = ordem: 1=0,00  2=0,05  3=0,10  4=0,15 mm de folga por lado."""
import os, cadquery as cq
W, H = 30.93, 12.4 + 1.6          # largura da moldura; altura PCB + DB9
here = os.path.dirname(os.path.abspath(__file__))
parts = None
for i, c in enumerate((0.0, 0.05, 0.10, 0.15)):
    p = cq.Workplane("XY").box(W + 8, H + 6, 2.0, centered=(True, True, False))
    p = p.cut(cq.Workplane("XY").box(W + 2*c, H + c, 3, centered=(True, True, False)))
    for k in range(i + 1):
        p = p.cut(cq.Workplane("XY").center(-(W+8)/2 + 3 + 3*k, (H+6)/2 - 1.7).circle(0.8).extrude(3))
    p = p.translate(((W + 10) * (i % 2), (H + 8) * (i // 2), 0))
    parts = p if parts is None else parts.union(p)
cq.exporters.export(parts, os.path.join(here, "db9_frame_test.stl"), tolerance=0.01)

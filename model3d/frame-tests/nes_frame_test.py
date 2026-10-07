"""Plaquinhas de teste de encaixe do corpo do NES (4 folgas). Furinhos redondos = folga por lado:
1=0,05  2=0,10  3=0,15  4=0,20 mm. Use a que encaixar justa em `nes_clear` dos case_*.py."""
import os, cadquery as cq
W, H = 24.88, 16.8                  # largura do corpo com moldura; altura acima da PCB
here = os.path.dirname(os.path.abspath(__file__))
parts = None
for i, c in enumerate((0.05, 0.10, 0.15, 0.20)):
    p = cq.Workplane("XY").box(W + 8, H + 6, 2.0, centered=(True, True, False))
    p = p.cut(cq.Workplane("XY").box(W + 2*c, H + c, 3, centered=(True, True, False)).edges("|Z").fillet(2.0 + c))
    for k in range(i + 1):
        p = p.cut(cq.Workplane("XY").center(-(W+8)/2 + 3 + 3*k, (H+6)/2 - 1.7).circle(0.8).extrude(3))
    p = p.translate(((W + 10) * (i % 2), (H + 8) * (i // 2), 0))
    parts = p if parts is None else parts.union(p)
cq.exporters.export(parts, os.path.join(here, "nes_frame_test.stl"), tolerance=0.01)

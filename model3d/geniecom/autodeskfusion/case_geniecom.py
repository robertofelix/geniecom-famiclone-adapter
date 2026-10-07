"""
Case sob medida para a PCB do adaptador NES -> Geniecom (hardware/gerber_geniecom.zip).

Gera (CadQuery):
  ../stl/case_base.stl       placa do fundo (2 mm, com as abas das janelas), fundo na mesa
  ../stl/case_lid.stl        casca (paredes + teto), orientada para impressão (virada, teto na mesa)
  ../stl/case_assembly.stl   conjunto montado (só para conferência visual)
  case_base.step, case_lid.step, case_assembly.step   (importar no Fusion)

Uso:  pip install cadquery   &&   python case_geniecom.py

Sistema de coordenadas do modelo (mm):
  X = largura da PCB (30,9 mm), 0 = centro da PCB
  Y = comprimento, 0 = borda da PCB do lado do DB9, +Y aponta para o NES
  Z = altura, 0 = fundo externo da base

Dimensões da PCB e posições dos conectores: layout em hardware/easyeda/geniecom_pcb.json
(unidade do EasyEDA: 1 = 0,254 mm). Larguras, alturas e distância DB9->NES: paquímetro.
Folgas das janelas (db9_clear, nes_clear): validadas nos testes de ../../frame-tests.
"""
import math
import os

import cadquery as cq

# ============================================================
# PARÂMETROS - edite aqui
# ============================================================
# --- PCB (geniecom_pcb.json, camada BoardOutLine) ---
pcb_w = 30.9            # largura (X)
pcb_l = 40.3            # comprimento (Y)
pcb_t = 1.26            # espessura da PCB do Geniecom (medida)

# --- Conector DB9 fêmea ângulo reto (footprint do EasyEDA) ---
db9_body_w = 30.95      # largura da moldura do DB9 (X), medida com paquímetro (30,93)
db9_body_d = 12.5       # profundidade do corpo sobre a PCB (Y, de 0 a 12.5)
db9_h = 12.74           # DB9 acima da PCB: 14,0 mm no total com a PCB de 1,26 (teste de encaixe impresso)
db9_shell_out = 6.0     # quanto a carcaça D + porcas de trava saem além da borda da PCB
db9_axis_h = 5.9        # altura do eixo da carcaça D acima da PCB (MEDIDO: borda de baixo 2,68 e de cima 9,1 -> centro 5,9)
db9_screw_x = 12.5      # posição X dos parafusos de fixação do DB9 (±)
db9_screw_y = 9.5       # posição Y dos parafusos de fixação do DB9

# --- Conector NES 7 pinos (footprint do EasyEDA) ---
nes_body_w = 24.88      # largura do corpo com a moldura (X)  (MEDIDO: 24,88 a 24,92)
nes_body_d = 14.0       # profundidade do corpo (Y)
nes_front = 44.79       # distância da face da moldura do DB9 até a face do NES (MEDIDO na PCB montada: 44,79; layout: 44,62)
nes_body_y0 = nes_front - nes_body_d  # início do corpo (Y)
nes_h = 16.8            # janela do NES = 24,88 x 16,8 + folga 0,05: o mesmo recorte do teste de encaixe impresso (1 furo)

# --- Por baixo da PCB (pinos soldados + cabeças dos parafusos do DB9) ---
under_h = 4.25          # espaço livre sob a PCB (suporte medido: 3,75 mm abaixo da PCB + 0,5 de margem)

# --- Case ---
wall = 6.5              # parede lateral
db9_protrusion = 0.3    # a moldura do DB9 sai 0,3 mm além da face da case: nenhum mm de encaixe é perdido, mesmo com a folga da PCB (-0,2 a +0,17 mm)
end_wall = 1.6          # parede frontal/traseira (a moldura do DB9 e a face do NES ficam rentes à face externa)
floor_t = 2.0           # fundo da base
roof_t = 2.0            # teto da casca
side_gap = 0.35         # folga lateral PCB/conectores <-> parede
top_gap = 0.4           # folga acima do conector mais alto
case_r = 3.0            # raio dos cantos verticais externos
edge_chamfer = 1.0      # chanfro das arestas superiores
base_chamfer = 0.8      # chanfro do fundo (evita "pé de elefante")

# --- Texto gravado no teto (baixo-relevo: a casca imprime com o teto na mesa) ---
label_size = 6.0        # tamanho da fonte (altura das maiúsculas ~4,5 mm)
label_depth = 0.4       # profundidade da gravação
label_margin = 8.0      # distância do texto até a face de cada ponta

# --- Janelas: moldura do DB9 e face do NES ficam rentes às faces da case ---
pcb_slot_clear = 0.1    # folga do rasgo da PCB na parede frontal

# --- Parafusos M3 autorroscantes, cabeça escareada (kit Zmbroll) ---
screw_clear_d = 3.4     # furo passante na base
screw_head_d = 4.94     # diâmetro da cabeça escareada do M3×8 (medido com paquímetro)
screw_pilot_d = 2.6     # furo-piloto na casca (autorroscante)
screw_pilot_depth = 7.0 # profundidade do furo-piloto
screw_ys = (db9_protrusion + 6.5, nes_front - 6.5) # posições Y (região livre entre os dois conectores)
pod_r = 2.0

# --- Apoio da PCB ---
support_w = 3.0         # tamanho dos blocos de apoio da PCB
hold_gap = 0.1          # folga vertical entre os pilares da casca e o topo da PCB
ear_gap = 0.15         # folga (em Y) entre as orelhas do NES e os batentes da casca (frente e trás)

# ============================================================
# DERIVADOS
# ============================================================
cav_hw = max(pcb_w, db9_body_w) / 2 + side_gap          # meia-largura da cavidade
cav_y0 = db9_protrusion + end_wall                      # parede interna frontal (lado DB9)
cav_y1 = nes_front - end_wall                           # parede interna traseira (lado NES)
cav_r = 0.3
screw_x = cav_hw + wall / 2                                  # posição X dos parafusos (±), fora da cavidade
pod_outer_x = screw_x + 3.6                             # borda externa dos "ombros" dos parafusos

pcb_bot = floor_t + under_h                             # z da face de baixo da PCB
pcb_top = pcb_bot + pcb_t                               # z da face de cima da PCB
split_z = floor_t                                       # plano de separação: placa do fundo / casca
cav_top = pcb_top + max(nes_h, db9_h) + top_gap
total_h = cav_top + roof_t

ear_y0, ear_y1 = nes_front - 5.32, nes_front - 3.22     # orelhas do NES (footprint), medidas a partir da face do NES
out_hw = cav_hw + wall
out_y0 = db9_protrusion                                 # face externa frontal (a moldura do DB9, em y = 0, sai db9_protrusion além dela)
out_y1 = nes_front                                      # face externa traseira = face do NES
zc = pcb_top + db9_axis_h                               # altura do eixo da carcaça D (só para o teste de interferência)


# ============================================================
# AUXILIARES
# ============================================================
def box(x0, x1, y0, y1, z0, z1, r=0.0):
    b = cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False)
    b = b.translate((x0, y0, z0))
    if r:
        b = b.edges("|Z").fillet(r)
    return b


def cyl(x, y, z0, z1, d):
    return (cq.Workplane("XY").workplane(offset=z0).center(x, y)
            .circle(d / 2).extrude(z1 - z0))


# ============================================================
# CORPO EXTERNO (placa + casca juntas, depois cortadas no plano de separação)
# ============================================================
outer = box(-out_hw, out_hw, out_y0, out_y1, 0, total_h, case_r)
outer = outer.faces(">Z").edges().chamfer(edge_chamfer)
outer = outer.faces("<Z").edges().chamfer(base_chamfer)

cavity = box(-cav_hw, cav_hw, cav_y0, cav_y1, floor_t, cav_top, cav_r)

big = 400.0
base_zone = box(-big, big, -big, big, -1, split_z)
lid_zone = box(-big, big, -big, big, split_z, total_h + 1)

# ============================================================
# BASE
# ============================================================
base = outer.intersect(base_zone).cut(cavity)

# apoios da PCB (sob a placa, nas bordas laterais, longe de pinos e parafusos)
sx_in = cav_hw - support_w                      # blocos encostam na parede lateral
supports_y = [
    (cav_y0 + 0.3, cav_y0 + 0.3 + support_w),   # lado DB9 (0,3 = raio do canto da cavidade)
    (pcb_l - support_w, pcb_l),                 # lado NES
]
for s in (-1, 1):
    for (y0, y1) in supports_y:
        xa, xb = sorted((s * sx_in, s * cav_hw))
        base = base.union(box(xa, xb, y0, y1, floor_t - 0.01, pcb_bot))
    # batente traseiro (a PCB não escorrega para dentro quando se encaixa o plugue)
    xa, xb = sorted((s * sx_in, s * cav_hw))
    base = base.union(box(xa, xb, pcb_l, pcb_l + 1.2, floor_t - 0.01, pcb_top))

# furos dos parafusos: passante + escareado (90 graus) a partir do fundo
cone_h = (screw_head_d - screw_clear_d) / 2
for s in (-1, 1):
    for y in screw_ys:
        base = base.cut(cyl(s * screw_x, y, -1, split_z + 0.01, screw_clear_d))
        cone = cq.Workplane(obj=cq.Solid.makeCone(
            screw_head_d / 2 + 0.01, screw_clear_d / 2, cone_h + 0.01,
            cq.Vector(s * screw_x, y, 0), cq.Vector(0, 0, 1)))
        base = base.cut(cone)

# ============================================================
# TAMPA
# ============================================================
lid = outer.intersect(lid_zone).cut(cavity)

# pilares junto às orelhas do NES: travam a PCB contra sair pela frente
for s in (-1, 1):
    xa, xb = sorted((s * (nes_body_w / 2 + 0.05), s * cav_hw))
    lid = lid.union(box(xa, xb, ear_y0 - 2.3, ear_y0 - ear_gap, pcb_top + hold_gap, cav_top + 0.01))
    # batente traseiro das orelhas: segura a PCB contra o empurrão do plugue do joystick no DB9
    lid = lid.union(box(xa, xb, ear_y1 + ear_gap, cav_y1 + 0.01, pcb_top + hold_gap, cav_top + 0.01))

# texto gravado no teto: cada nome lê-se do lado do seu conector (GENIECOM do lado do DB9, NES do lado do NES)
for _txt, _y in (("GENIECOM", out_y0 + label_margin + 2.2), ("NES", out_y1 - label_margin - 2.2)):
    _t = (cq.Workplane("XY").workplane(offset=total_h - label_depth)
          .center(0, _y).text(_txt, label_size, label_depth + 0.2, kind="bold", halign="center", valign="center"))
    if _txt == "NES":
        _t = _t.rotate((0, _y, 0), (0, _y, 1), 180)   # NES lê-se do lado do seu conector (de cabeça para baixo em relação ao GENIECOM)
    lid = lid.cut(_t)

# furos-piloto dos parafusos
for s in (-1, 1):
    for y in screw_ys:
        lid = lid.cut(cyl(s * screw_x, y, split_z - 0.5, split_z + screw_pilot_depth, screw_pilot_d))

# --- Janelas ---
# DB9: a moldura entra na parede frontal e fica com a face rente à face da case;
#      a carcaça D sai inteira para fora (encaixe completo no console).
y_f0, y_f1 = out_y0 - 1.0, cav_y0 + 0.01
pcb_slot = box(-(pcb_w / 2 + pcb_slot_clear), pcb_w / 2 + pcb_slot_clear, y_f0, y_f1,
               pcb_bot - pcb_slot_clear, pcb_top + 0.01)
db9_clear = 0.00  # folga do DB9 (validada no teste de encaixe impresso: 1 furo = 0,00 mm, encaixa justo)
db9_win = box(-(db9_body_w / 2 + db9_clear), db9_body_w / 2 + db9_clear, y_f0, y_f1,
              split_z, pcb_top + db9_h + db9_clear)
y_b0, y_b1 = cav_y1 - 0.01, out_y1 + 1.0
nes_r = 2.0      # raio dos 4 cantos do corpo do NES (medido nas fotos, ~2 mm)
nes_clear = 0.05 # folga do NES (validada no teste de encaixe impresso: 1 furo = 0,05 mm, encaixa justo)
nes_win = box(-(nes_body_w / 2 + nes_clear), nes_body_w / 2 + nes_clear, y_b0, y_b1,
              split_z, pcb_top + nes_h + nes_clear)
nes_win = nes_win.edges("|Y").edges(">Z").fillet(nes_r + nes_clear)  # cantos de cima boleados
# as janelas descem até a placa: a casca não tem ponte na impressão. Só a casca é recortada;
# as abas da placa (abaixo) tapam o vão sob os conectores.
for w in (pcb_slot, db9_win, nes_win):
    lid = lid.cut(w)
lip_clear = 0.15
base = base.union(box(-(db9_body_w / 2 + db9_clear - lip_clear), db9_body_w / 2 + db9_clear - lip_clear,
                      out_y0, cav_y0 + 0.01, floor_t - 0.01, pcb_bot - pcb_slot_clear))
base = base.union(box(-(nes_body_w / 2 + nes_clear - lip_clear), nes_body_w / 2 + nes_clear - lip_clear,
                      cav_y1 - 0.01, out_y1, floor_t - 0.01, pcb_top - 0.05))
# enchimentos dos cantos de baixo: o conector tem os 4 cantos boleados, então a aba sobe junto
# aos cantos até encostar (0,05 mm) no contorno boleado do conector
_hw = nes_body_w / 2 + nes_clear - lip_clear
_env = box(-(nes_body_w / 2 + 0.05), nes_body_w / 2 + 0.05, cav_y1 - 1, out_y1 + 1,
           pcb_top, pcb_top + nes_h).edges("|Y").fillet(nes_r + 0.05)
_pad = box(-_hw, _hw, cav_y1 - 0.01, out_y1, pcb_top - 0.06, pcb_top + nes_r + 0.1).cut(_env)
base = base.union(_pad)

# ============================================================
# VERIFICAÇÃO DE INTERFERÊNCIA com os envelopes dos componentes
# ============================================================
envelopes = {
    "PCB": box(-pcb_w / 2, pcb_w / 2, 0, pcb_l, pcb_bot, pcb_top),
    "DB9 corpo": box(-db9_body_w / 2, db9_body_w / 2, 0, db9_body_d, pcb_top, pcb_top + db9_h),
    "DB9 carcaca+porcas (fora da case)": box(-db9_screw_x - 2.1, db9_screw_x + 2.1, -db9_shell_out, 0,
                              zc - 4.5, zc + 4.5),
    "NES corpo": box(-nes_body_w / 2, nes_body_w / 2, nes_body_y0, nes_front, pcb_top, pcb_top + nes_h).edges("|Y").fillet(nes_r),
    "NES orelhas": box(-15.1, 15.1, ear_y0, ear_y1, pcb_top, pcb_top + 8),
    "pinos sob PCB": box(-9, 9, 6, 28, pcb_bot - 2.0, pcb_bot),
    "parafusos DB9 sob PCB": cyl(-db9_screw_x, db9_screw_y, pcb_bot - 2.5, pcb_bot, 6.0)
    .union(cyl(db9_screw_x, db9_screw_y, pcb_bot - 2.5, pcb_bot, 6.0)),
    "pegs NES sob PCB": cyl(-10.25, pcb_l - 2.6, pcb_bot - 3.75, pcb_bot, 2.4)
    .union(cyl(10.25, pcb_l - 2.6, pcb_bot - 3.75, pcb_bot, 2.4)),
}
print("--- interferência (mm3, esperado ~0) ---")
worst = 0.0
for name, env in envelopes.items():
    for part_name, part in (("base", base), ("tampa", lid)):
        v = env.intersect(part).val().Volume() if env.intersect(part).vals() else 0.0
        worst = max(worst, v)
        if v > 0.01:
            print(f"  ATENCAO {name} x {part_name}: {v:.2f}")
print(f"  pior interferência: {worst:.3f} mm3")

# ============================================================
# EXPORTAÇÃO
# ============================================================
here = os.path.dirname(os.path.abspath(__file__))
stl_dir = os.path.normpath(os.path.join(here, "..", "stl"))
os.makedirs(stl_dir, exist_ok=True)

# tampa virada para imprimir com o teto na mesa
lid_print = lid.rotate((0, 0, 0), (1, 0, 0), 180)
lb = lid_print.val().BoundingBox()
lid_print = lid_print.translate((0, 0, -lb.zmin))

assembly = base.union(lid)
kw = dict(tolerance=0.01, angularTolerance=0.1)
cq.exporters.export(base, os.path.join(stl_dir, "case_base.stl"), **kw)
cq.exporters.export(lid_print, os.path.join(stl_dir, "case_lid.stl"), **kw)
cq.exporters.export(assembly, os.path.join(stl_dir, "case_assembly.stl"), **kw)
cq.exporters.export(base, os.path.join(here, "case_base.step"))
cq.exporters.export(lid, os.path.join(here, "case_lid.step"))
cq.exporters.export(assembly, os.path.join(here, "case_assembly.step"))

bb = assembly.val().BoundingBox()
print(f"Externo: {bb.xlen:.1f} x {bb.ylen:.1f} x {bb.zlen:.1f} mm (L x C x A)")
print(f"Face do DB9 -> face do NES: {nes_front:.2f} mm")
print(f"Cavidade: {2 * cav_hw:.1f} x {cav_y1 - cav_y0:.1f} x {cav_top - floor_t:.1f} mm")
print(f"Parafuso: M3 x {split_z + screw_pilot_depth - 1.0:.0f} mm (escareado, pela base)")

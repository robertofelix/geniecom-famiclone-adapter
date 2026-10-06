"""
Case sob medida para um adaptador NES -> Phantom System / Top Game / Turbo Game COMPRADO
PRONTO (Mercado Livre). NÃO é a PCB deste repositório: veja o README desta pasta.

Gera (CadQuery):
  ../stl/case_base.stl       base, orientada para impressão (fundo na mesa)
  ../stl/case_lid.stl        tampa, orientada para impressão (virada, teto na mesa)
  ../stl/case_assembly.stl   conjunto montado (só para conferência visual)
  case_base.step, case_lid.step, case_assembly.step   (importar no Fusion)

Uso:  pip install cadquery   &&   python case_phantom_3rdparty.py

Sistema de coordenadas do modelo (mm):
  X = largura (dimensão de 31 mm da PCB), 0 = centro da PCB
  Y = comprimento, 0 = borda da PCB do lado do DB9, +Y aponta para o NES
  Z = altura, 0 = fundo externo da base

Medidas dos conectores: paquímetro. Medidas da PCB do adaptador (largura e comprimento):
ESTIMADAS a partir de uma foto, pois não há arquivo de layout. Itens "ESTIMADO" devem ser conferidos.
"""
import math
import os

import cadquery as cq

# ============================================================
# PARÂMETROS - edite aqui
# ============================================================
# --- PCB do adaptador de terceiros (sem layout; ESTIMADA pela foto) ---
pcb_w = 32.0            # largura (X)  ESTIMADO (foto: ~31,5)
pcb_l = 38.6            # comprimento (Y)  ESTIMADO: face do NES (42,96) menos o balanço do NES (4,36)
pcb_t = 1.6             # espessura (padrão JLCPCB)

# --- Conector DB9 fêmea ângulo reto (footprint do EasyEDA) ---
db9_body_w = 33.15      # largura do flange metálico do DB9 (X)  (MEDIDO com paquímetro: 33,15 mm)
db9_body_d = 12.5       # profundidade do corpo sobre a PCB (Y, de 0 a 12.5)
db9_h = 12.5            # altura do corpo acima da PCB (medido 14,03 com a PCB, menos 1,6 = 12,4; arredondado p/ cima)
db9_shell_out = 6.0     # quanto a carcaça D + porcas de trava saem além da borda da PCB
db9_axis_h = 5.9        # altura do eixo da carcaça D acima da PCB (MEDIDO: borda de baixo 2,68 e de cima 9,1 -> centro 5,9)
db9_screw_x = 12.5      # posição X dos parafusos de fixação do DB9 (±)
db9_screw_y = 9.5       # posição Y dos parafusos de fixação do DB9

# --- Conector NES 7 pinos (footprint do EasyEDA) ---
nes_body_w = 24.9       # largura do corpo com a moldura (X)  (MEDIDO: 24,88 a 24,92)
nes_body_d = 14.0       # profundidade do corpo (Y)
nes_front = 42.96       # distância da face da moldura do DB9 até a face do NES (MEDIDO neste adaptador: 42,96)
nes_body_y0 = nes_front - nes_body_d  # início do corpo (Y)
nes_h = 15.0            # altura do corpo acima da PCB (medido ~16,4 com a PCB, menos 1,6 = 14,8; arredondado p/ cima)

# --- Por baixo da PCB (pinos soldados + cabeças dos parafusos do DB9) ---
under_h = 3.5           # espaço livre sob a PCB

# --- Case ---
wall = 2.4              # parede lateral
end_wall = 1.6          # parede frontal/traseira (a moldura do DB9 e a face do NES ficam rentes à face externa)
floor_t = 2.0           # fundo da base
roof_t = 2.0            # teto da tampa
side_gap = 0.35         # folga lateral PCB/conectores <-> parede
top_gap = 0.4           # folga acima do conector mais alto
case_r = 3.0            # raio dos cantos verticais externos
edge_chamfer = 1.0      # chanfro das arestas superiores
base_chamfer = 0.8      # chanfro do fundo (evita "pé de elefante")

# --- Janelas: moldura do DB9 e face do NES ficam rentes às faces da case ---
window_clear = 0.25     # folga ao redor da moldura do DB9 e do corpo do NES
pcb_slot_clear = 0.2    # folga do rasgo da PCB na parede frontal

# --- Parafusos M3 autorroscantes, cabeça escareada (kit Zmbroll) ---
screw_clear_d = 3.4     # furo passante na base
screw_head_d = 6.4      # diâmetro do escareado (cabeça M3 escareada ~ 5,5-6,0)
screw_pilot_d = 2.5     # furo-piloto na tampa (autorroscante)
screw_pilot_depth = 9.5 # profundidade do furo-piloto
screw_ys = (17.1, 26.1) # posições Y (região livre entre os dois conectores)
pod_r = 2.0

# --- Encaixe base/tampa e apoio da PCB ---
tongue_w = 1.0          # largura da lingueta
tongue_h = 1.6          # altura da lingueta
tongue_clear = 0.2      # folga da ranhura
support_w = 3.0         # tamanho dos blocos de apoio da PCB
hold_gap = 0.15         # folga entre os pilares da tampa e o topo da PCB

# ============================================================
# DERIVADOS
# ============================================================
cav_hw = max(pcb_w, db9_body_w) / 2 + side_gap          # meia-largura da cavidade
cav_y0 = end_wall                                       # parede interna frontal (lado DB9)
cav_y1 = nes_front - end_wall                           # parede interna traseira (lado NES)
cav_r = 0.3
screw_x = cav_hw + 3.0                                  # posição X dos parafusos (±), fora da cavidade
pod_outer_x = screw_x + 3.6                             # borda externa dos "ombros" dos parafusos

pcb_bot = floor_t + under_h                             # z da face de baixo da PCB
pcb_top = pcb_bot + pcb_t                               # z da face de cima da PCB
split_z = pcb_top                                       # plano de separação base/tampa
cav_top = pcb_top + max(nes_h, db9_h) + top_gap
total_h = cav_top + roof_t

out_hw = cav_hw + wall
out_y0 = 0.0                                            # face externa frontal = face da moldura do DB9
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
# CORPO EXTERNO (base + tampa juntas, depois cortadas no plano de separação)
# ============================================================
outer = box(-out_hw, out_hw, out_y0, out_y1, 0, total_h, case_r)
for s in (-1, 1):
    x0, x1 = sorted((s * (out_hw - 3.0), s * pod_outer_x))
    y_mid = sum(screw_ys) / 2
    y_half = (screw_ys[1] - screw_ys[0]) / 2 + 3.6
    pod = box(x0, x1, y_mid - y_half, y_mid + y_half, 0, total_h)
    pod = pod.edges("|Z").edges(">X" if s > 0 else "<X").fillet(pod_r)  # só os cantos externos
    outer = outer.union(pod)
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

# lingueta de alinhamento (anel junto à parede, rente à face interna da cavidade)
t_out = box(-cav_hw - tongue_w, cav_hw + tongue_w, cav_y0 - tongue_w, cav_y1 + tongue_w,
            split_z, split_z + tongue_h, cav_r + tongue_w)
t_in = box(-cav_hw, cav_hw, cav_y0, cav_y1, split_z - 1, split_z + tongue_h + 1, cav_r)
base = base.union(t_out.cut(t_in))

# apoios da PCB (sob a placa, nas bordas laterais, longe de pinos e parafusos)
sx_in = cav_hw - support_w                      # blocos encostam na parede lateral
supports_y = [
    (0.0, support_w),                           # lado DB9 (a PCB começa em y = 0)
    (pcb_l - support_w, pcb_l),                 # lado NES
    (14.0, 17.0),                               # meio
    (25.5, 28.5),                               # meio
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
        base = base.cut(cyl(s * screw_x, y, -1, split_z + tongue_h + 1, screw_clear_d))
        cone = cq.Workplane(obj=cq.Solid.makeCone(
            screw_head_d / 2 + 0.01, screw_clear_d / 2, cone_h + 0.01,
            cq.Vector(s * screw_x, y, 0), cq.Vector(0, 0, 1)))
        base = base.cut(cone)

# ============================================================
# TAMPA
# ============================================================
lid = outer.intersect(lid_zone).cut(cavity)

# ranhura para a lingueta da base
g_out = box(-cav_hw - tongue_w - tongue_clear, cav_hw + tongue_w + tongue_clear,
            cav_y0 - tongue_w - tongue_clear, cav_y1 + tongue_w + tongue_clear,
            split_z - 1, split_z + tongue_h + 0.3, cav_r + tongue_w + tongue_clear)
g_in = box(-cav_hw, cav_hw, cav_y0, cav_y1, split_z - 2, split_z + tongue_h + 1, cav_r)
lid = lid.cut(g_out.cut(g_in))

# pilares que seguram a PCB contra os apoios da base (só na região do meio)
for s in (-1, 1):
    for (y0, y1) in supports_y[2:]:
        xa, xb = sorted((s * sx_in, s * cav_hw))
        lid = lid.union(box(xa, xb, y0, y1, pcb_top + hold_gap, cav_top + 0.01))

# pilares junto às orelhas do NES: travam a PCB contra sair pela frente
for s in (-1, 1):
    xa, xb = sorted((s * (nes_body_w / 2 + 0.2), s * cav_hw))
    lid = lid.union(box(xa, xb, nes_front - 8.8, nes_front - 5.5, pcb_top + hold_gap, cav_top + 0.01))

# furos-piloto dos parafusos
for s in (-1, 1):
    for y in screw_ys:
        lid = lid.cut(cyl(s * screw_x, y, split_z - 0.5, split_z + screw_pilot_depth, screw_pilot_d))

# --- Janelas ---
# DB9: a moldura entra na parede frontal e fica com a face rente à face da case;
#      a carcaça D sai inteira para fora (encaixe completo no console).
y_f0, y_f1 = out_y0 - 1.0, cav_y0 + 0.01
pcb_slot = box(-(pcb_w / 2 + pcb_slot_clear), pcb_w / 2 + pcb_slot_clear, y_f0, y_f1,
               pcb_bot - pcb_slot_clear, split_z + 0.01)
db9_win = box(-(db9_body_w / 2 + window_clear), db9_body_w / 2 + window_clear, y_f0, y_f1,
              split_z, pcb_top + db9_h + window_clear)
# NES: o corpo do conector atravessa a parede traseira, com a face rente à face da case.
y_b0, y_b1 = cav_y1 - 0.01, out_y1 + 1.0
nes_win = box(-(nes_body_w / 2 + window_clear), nes_body_w / 2 + window_clear, y_b0, y_b1,
              split_z, pcb_top + nes_h + window_clear)
for w in (pcb_slot, db9_win, nes_win):
    base = base.cut(w)
    lid = lid.cut(w)

# ============================================================
# VERIFICAÇÃO DE INTERFERÊNCIA com os envelopes dos componentes
# ============================================================
envelopes = {
    "PCB": box(-pcb_w / 2, pcb_w / 2, 0, pcb_l, pcb_bot, pcb_top),
    "DB9 corpo": box(-db9_body_w / 2, db9_body_w / 2, 0, db9_body_d, pcb_top, pcb_top + db9_h),
    "DB9 carcaca+porcas (fora da case)": box(-db9_screw_x - 2.1, db9_screw_x + 2.1, -db9_shell_out, 0,
                              zc - 4.5, zc + 4.5),
    "NES corpo": box(-nes_body_w / 2, nes_body_w / 2, nes_body_y0, nes_front, pcb_top, pcb_top + nes_h),
    "NES orelhas": box(-15.1, 15.1, nes_front - 5.32, nes_front - 3.22, pcb_top, pcb_top + 8),
    "pinos sob PCB": box(-9, 9, 6, 28, pcb_bot - 2.0, pcb_bot),
    "parafusos DB9 sob PCB": cyl(-db9_screw_x, db9_screw_y, pcb_bot - 2.5, pcb_bot, 6.0)
    .union(cyl(db9_screw_x, db9_screw_y, pcb_bot - 2.5, pcb_bot, 6.0)),
    "pegs NES sob PCB": cyl(-10.25, pcb_l - 2.6, pcb_bot - 2.5, pcb_bot, 2.4)
    .union(cyl(10.25, pcb_l - 2.6, pcb_bot - 2.5, pcb_bot, 2.4)),
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

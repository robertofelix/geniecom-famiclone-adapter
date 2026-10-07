# Testes de encaixe dos conectores

Plaquinhas para calibrar a folga das janelas do DB9 e do NES na sua impressora, antes de imprimir a case.

| Arquivo | Conector | Folgas por lado (1 a 4 furinhos) |
| --- | --- | --- |
| `db9_frame_test.stl` | Moldura do DB9 (30,93 mm de largura, 14,0 mm de altura com a PCB) | 0,00 / 0,05 / 0,10 / 0,15 mm |
| `nes_frame_test.stl` | Corpo do NES (24,88 × 16,8 mm, cantos de 2 mm) | 0,05 / 0,10 / 0,15 / 0,20 mm |

Imprima deitado (face de 2 mm na mesa), sem suporte. O número de furinhos redondos na borda de cima indica a folga. Escolha a menor folga em que o conector entra sem forçar.

Resultado validado: **DB9 com 1 furinho (0,00 mm)** e **NES com 1 furinho (0,05 mm)**. Esses valores estão em `db9_clear` e `nes_clear` dos scripts das cases.

O teste do DB9 vale só para PCBs de 1,25 a 1,26 mm de espessura (Geniecom e Phantom), porque a altura do recorte inclui a PCB. Não vale para o adaptador do `phantom-3rdparty` (1,65 mm).

Para regenerar: `python db9_frame_test.py` e `python nes_frame_test.py` (precisa de `pip install cadquery`).

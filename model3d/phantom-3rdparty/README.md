# Case para o adaptador Phantom/Top Game/Turbo Game comprado no Mercado Livre

> **Este modelo vale apenas para o adaptador de terceiros que foi adquirido no Mercado Livre.** Ele **não** serve para as PCBs deste repositório (Geniecom e Phantom), que têm as próprias cases em [`../geniecom`](../geniecom) e [`../phantom`](../phantom).

## O adaptador

PCB **vermelha**, com a serigrafia "TURBO GAME NINTENDO" e setas indicando o sentido de cada lado. As PCBs do repositório são diferentes: a do Geniecom é roxa e a do Phantom tem a serigrafia "NES" e "PHANTOM".

| | |
| --- | --- |
| ![Adaptador comprado, vista geral](fotos/adaptador_vista_geral.jpg) | ![Adaptador comprado, verso](fotos/adaptador_verso.jpg) |
| Vista geral: conector DB9 (lado do console) e conector NES. | Verso, com os terminais soldados e os parafusos do DB9. |
| ![Conector DB9 do adaptador, de frente](fotos/adaptador_conector_db9.jpg) | ![Conector NES do adaptador, de frente](fotos/adaptador_conector_nes.jpg) |
| Conector DB9 fêmea. Atrás dele aparecem os pinos do NES. | Conector NES de 7 pinos. |

## Por que existe

A PCB deste adaptador é diferente das do repositório. A distância da face da moldura do DB9 até a face do conector NES foi medida com paquímetro neste adaptador e deu **42,96 mm**, e a case foi dimensionada em cima dela. Nas PCBs do repositório essa distância é outra (44,79 mm medidos no Geniecom e 40,16 mm no layout do Phantom).

## O que veio de medição e o que é estimativa

| Parâmetro | Valor | Origem |
| --- | --- | --- |
| `nes_front` (moldura do DB9 até a face do NES) | 42,96 mm | Medido neste adaptador (leitura do paquímetro na foto) |
| `nes_body_w` (largura do NES com a moldura) | 24,9 mm | Medido |
| `db9_body_w` (largura da moldura metálica do DB9) | 33,15 mm | Medido |
| `nes_h`, `db9_h` (alturas acima da PCB) | 15,0 e 12,5 mm | Medido (com a PCB de 1,6 mm) e arredondado para cima |
| `pcb_w` (largura da PCB) | 32,0 mm | **Estimado** |
| `pcb_l` (comprimento da PCB) | 38,6 mm | **Estimado** (face do NES menos o balanço de 4,36 mm do conector) |

Se a largura e o comprimento reais da PCB forem diferentes, meça com paquímetro e ajuste `pcb_w` e `pcb_l` em `autodeskfusion/case_phantom_3rdparty.py`. A largura da cavidade (33,9 mm) é definida pela moldura do DB9, então uma PCB até cerca de 33 mm de largura cabe sem mudar a case.

## Como é a case

Mesmo desenho das outras: duas peças (base e tampa), quatro parafusos **M3×16 mm** autorroscantes de cabeça escareada pelo fundo da base. A moldura do DB9 e o corpo do NES atravessam as paredes e ficam com a face rente à face da case. Tamanho externo: cerca de 47 × 43,0 × 24,5 mm.

## Arquivos

- `stl/case_base.stl`: base, pronta para imprimir (fundo na mesa).
- `stl/case_lid.stl`: tampa, já virada para imprimir (teto na mesa).
- `stl/case_assembly.stl`: conjunto montado, só para visualização (não imprimir).
- `stl/preview.png`: pré-visualização.
- `autodeskfusion/case_phantom_3rdparty.py`: script paramétrico (CadQuery) que gera tudo.
- `autodeskfusion/case_*.step`: para importar no Autodesk Fusion.

Para regenerar: `python model3d/phantom-3rdparty/autodeskfusion/case_phantom_3rdparty.py` (precisa de `pip install cadquery`).

## Status

Validado só por geometria (malhas fechadas e teste de interferência com os envelopes dos conectores). Ainda não foi impresso nem testado com o adaptador.

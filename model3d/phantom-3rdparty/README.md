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

A PCB deste adaptador é diferente das do repositório. A distância da face da moldura do DB9 até a face do conector NES foi medida com paquímetro neste adaptador e deu **42,44 mm**, e a case foi dimensionada em cima dela. Nas PCBs do repositório essa distância é outra (44,79 mm no Geniecom e 40,16 mm no Gerber do Phantom).

## Medidas usadas

| Parâmetro | Valor | Origem |
| --- | --- | --- |
| `nes_front` (moldura do DB9 até a face do NES) | 42,44 mm | Medido neste adaptador (leitura do paquímetro na foto) |
| `nes_body_w` (largura do NES com a moldura) | 24,88 mm | Medido |
| `db9_body_w` (largura da moldura metálica do DB9) | 30,95 mm | Medido (o DB9 é o mesmo das outras PCBs) |
| `nes_h`, `db9_h` (alturas acima da PCB) | 16,8 e 12,75 mm | Os mesmos conectores das outras PCBs |
| `pcb_t` (espessura da PCB) | 1,65 mm | Medido (as PCBs do Geniecom e do Phantom têm 1,26 mm) |
| `under_h` (espaço sob a PCB) | 4,25 mm | Pinos de fixação do NES de 3,75 mm mais 0,5 mm de margem |
| `nes_clear` (folga da janela do NES) | 0,05 mm | Validada no [teste de encaixe do NES](../frame-tests/README.md) |
| `db9_clear` (folga da janela do DB9) | 0,15 mm | **Não testada.** O teste de encaixe do DB9 não vale aqui, porque a altura do recorte inclui a PCB e esta é mais grossa |
| `pcb_w` (largura da PCB) | 33,11 mm | Medido |
| `pcb_l` (comprimento da PCB) | 37,73 mm | Medido (o NES avança 4,71 mm além da PCB) |

A largura da cavidade (33,8 mm) é definida pela largura da PCB (33,11 mm), que é maior que a moldura do DB9 (30,95 mm).

## Como é a case

Mesmo desenho das outras: duas peças (base e tampa), quatro parafusos **M3×16 mm** autorroscantes de cabeça escareada pelo fundo da base. A moldura do DB9 e o corpo do NES atravessam as paredes e ficam com a face rente à face da case. A janela do NES acompanha os cantos boleados do conector. Tamanho externo: cerca de 47,0 × 42,5 × 27,1 mm (cavidade de 33,8 × 39,2 × 23,1 mm).

## Arquivos

- `stl/case_base.stl`: base, pronta para imprimir (fundo na mesa).
- `stl/case_lid.stl`: tampa, já virada para imprimir (teto na mesa).
- `stl/case_assembly.stl`: conjunto montado, só para visualização (não imprimir).
- `stl/preview_render.png`: pré-visualização.
- `autodeskfusion/case_phantom_3rdparty.py`: script paramétrico (CadQuery) que gera tudo.
- `autodeskfusion/case_*.step`: para importar no Autodesk Fusion.

Para regenerar: `python model3d/phantom-3rdparty/autodeskfusion/case_phantom_3rdparty.py` (precisa de `pip install cadquery`).

## Status

Validado por geometria (malhas fechadas e teste de interferência com os envelopes dos conectores) e, no NES, pelo teste de encaixe impresso. A folga do DB9 não foi testada e a case completa ainda não foi impressa com o adaptador.

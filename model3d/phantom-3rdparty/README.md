# Case para o adaptador Phantom/Top Game/Turbo Game comprado na Shopee

> **Este modelo vale apenas para o adaptador de terceiros que foi adquirido na [Shopee](https://shopee.com.br/).** Ele **não** serve para as PCBs deste repositório (Geniecom e Phantom), que têm as próprias cases em [`../geniecom`](../geniecom) e [`../phantom`](../phantom).

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
| `nes_h` (altura do NES acima da PCB) | 16,8 mm | Mesmo conector do Geniecom (confirmado) |
| `db9_h` (altura do DB9 acima da PCB) | 12,34 mm | Medido: DB9 + PCB = 13,99 mm, menos 1,65 mm da PCB |
| `pcb_t` (espessura da PCB) | 1,65 mm | Medido (as PCBs do Geniecom e do Phantom têm 1,26 mm) |
| `under_h` (espaço sob a PCB) | 4,25 mm | Mesmo valor do Geniecom (confirmado): o que sai por baixo da PCB (pinos de fixação do NES, parafusos do DB9, solda) tem até 3,75 mm, mais 0,5 mm de margem |
| `nes_clear` (folga da janela do NES) | 0,05 mm | Validada no [teste de encaixe do NES](../frame-tests/README.md) |
| `db9_clear` (folga da janela do DB9) | 0,15 mm | Validada na impressão da case completa. O teste de encaixe do DB9 (0,00 mm) não vale aqui, porque a altura do recorte inclui a PCB e esta é mais grossa |
| `pcb_w` (largura da PCB) | 32,26 mm | Medido com paquímetro (leitura 32,24 a 32,26 mm) |
| `pcb_l` (comprimento da PCB) | 37,73 mm | Medido (o NES avança 4,71 mm além da PCB) |

A largura da cavidade (33,0 mm) é definida pela largura da PCB (32,26 mm), que é só 1,31 mm maior que a moldura do DB9 (30,95 mm), ou 0,65 mm de cada lado. Por isso a janela do DB9 tem um degrau: 32,46 mm de largura na altura da PCB (1,65 mm) e 31,25 mm acima dela. A borda da PCB fica visível nas laterais do conector, e a protusão de 0,3 mm do DB9 foi mantida, sem perder encaixe do plugue. Se a fresta incomodar, dá para vedar com silicone ou epóxi depois de montar.

## Como é a case

Mesmo desenho da [case do Geniecom](../geniecom) (já impressa e validada): caixa de lados retos, sem alças, em duas peças. Casco (paredes e teto) e placa de fundo de 2 mm, fechados por quatro parafusos **M3×8 mm** autorroscantes (cabeça Ø4,94 mm) nos quatro cantos, entrando por baixo e escondidos dentro das paredes de 6,5 mm. A PCB entra por baixo, então as janelas do DB9 e do NES são abertas até a placa de fundo, que tem "lábios" (folga de 0,15 mm) completando o contorno dos conectores.

- **Batentes das orelhas do NES:** a PCB não recua quando se empurra o plugue do DB9.
- **Nomes gravados no teto** (baixo relevo, porque o teto fica na mesa ao imprimir): "PHANTOM" no lado do DB9 e "NES" no lado do NES, lido a partir do lado do conector.
- **Tamanho externo:** 46,0 × 42,2 × 27,1 mm (cavidade de 33,0 × 38,9 × 23,1 mm).

## Arquivos

- `stl/case_base.stl`: placa de fundo, pronta para imprimir (fundo na mesa).
- `stl/case_lid.stl`: casco, já virado para imprimir (teto na mesa).
- `stl/case_assembly.stl`: conjunto montado, só para visualização (não imprimir).
- `stl/preview_render.png`: pré-visualização.
- `autodeskfusion/case_phantom_3rdparty.py`: script paramétrico (CadQuery) que gera tudo.
- `autodeskfusion/case_*.step`: para importar no Autodesk Fusion.

Para regenerar: `python model3d/phantom-3rdparty/autodeskfusion/case_phantom_3rdparty.py` (precisa de `pip install cadquery`).

## Status

**Impressa e validada** com o adaptador comprado: DB9 e NES encaixam, e a case fecha com os parafusos M3×8 mm. Também foi validada por geometria (malhas fechadas, interferência 0,000 mm³ com os envelopes dos conectores). O desenho de fecho é o mesmo do Geniecom.

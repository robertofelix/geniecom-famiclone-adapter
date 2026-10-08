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

A largura da cavidade (33,0 mm) é definida pela largura da PCB (32,26 mm), que é só 1,31 mm maior que a moldura do DB9 (30,95 mm), ou 0,65 mm de cada lado. Por isso a janela do DB9 tem duas larguras: 32,46 mm de largura na altura da PCB (1,65 mm) e 31,25 mm acima dela. A borda da PCB fica visível nas laterais do conector, e a protusão de 0,3 mm do DB9 foi mantida, sem perder encaixe do plugue. Se a fresta incomodar, dá para vedar com silicone ou epóxi depois de montar.

## Como é a case

Mesmo desenho da [case do Geniecom](../geniecom) (já impressa e validada): caixa de lados retos, sem alças, em duas peças. Casco (paredes e teto) e placa de fundo de 2 mm, fechados por quatro parafusos **M3×8 mm** autorroscantes (cabeça Ø4,94 mm) nos quatro cantos, entrando por baixo e escondidos dentro das paredes de 6,5 mm. A PCB entra por baixo, então as janelas do DB9 e do NES são abertas até a placa de fundo, que tem "lábios" (folga de 0,15 mm) completando o contorno dos conectores.

- **Batentes das orelhas do NES:** a PCB não recua quando se empurra o plugue do DB9.
- **Teto com degrau:** a parte do DB9 tem só a altura da moldura do DB9 (22,6 mm de altura externa), e logo antes do corpo do NES o teto sobe 4,5 mm até 27,1 mm, para caber o NES. O degrau fica entre y = 26,6 e 28,2 mm, contando da face do DB9.
- **Nomes gravados no teto** (baixo relevo, 6 mm, como no Geniecom): "PHANTOM" no teto baixo (lado do DB9) e "NES" no teto alto, cada um lido a partir do lado do seu conector. O teto baixo imprime sobre suporte, então a superfície dele sai mais áspera.
- **Tamanho externo:** 46,0 × 42,1 × 22,6 mm na parte do DB9 e 27,1 mm na parte do NES (cavidade de 33,0 × 38,9 mm, com 18,6 mm de altura na parte do DB9 e 23,1 mm na do NES).

## Arquivos

- `stl/case_base.stl`: placa de fundo, pronta para imprimir (fundo na mesa).
- `stl/case_lid.stl`: casco, já virado para imprimir (teto alto na mesa). O teto baixo do lado do DB9 fica 4,5 mm acima da mesa e precisa de suporte (só nessa região).
- `stl/case_assembly.stl`: conjunto montado, só para visualização (não imprimir).
- `stl/preview_render.png`: pré-visualização.
- `autodeskfusion/case_phantom_3rdparty.py`: script paramétrico (CadQuery) que gera tudo.
- `autodeskfusion/case_*.step`: para importar no Autodesk Fusion.

Para regenerar: `python model3d/phantom-3rdparty/autodeskfusion/case_phantom_3rdparty.py` (precisa de `pip install cadquery`).

## Status

**Impressa e validada** com o adaptador comprado, na versão com o teto em degrau. A primeira versão (teto reto, 27,1 mm de altura em toda a case) não encaixou direito, e a altura menor na ponta do DB9 resolveu. Também foi validada por geometria: malhas fechadas e interferência 0,000 mm³ com os envelopes dos conectores. O desenho de fecho (casco, placa de fundo e quatro M3×8 mm) é o mesmo do Geniecom.

# Adaptador NES para Famiclones Brasileiros: Geniecom, Phantom System, Top Game e Turbo Game

Documentação da pinagem do controle de famiclones vendidos no Brasil e projeto de adaptadores (cabo e PCB) para usar controles de NES, inclusive o 8BitDo Retro Receiver, neles. O motivador original deste repositório foi o Geniecom (DB9/DE9); a documentação do Phantom System, do Top Game e do Turbo Game (que compartilham a mesma pinagem entre si) foi incluída depois, como bônus.

## Sumário

- [Objetivo](#objetivo)
- [Referências](#referências)
- [Pinagem](#pinagem)
- [Terminologia](#terminologia)
- [Correlação Geniecom ↔ NES](#correlação-geniecom--nes)
- [Montando o adaptador](#montando-o-adaptador)
- [PCB (Gerber)](#pcb-gerber)
- [Case para impressão 3D](#case-para-impressão-3d)
- [Bônus: outros clones](#bônus-outros-clones)
  - [Phantom System, Top Game e Turbo Game](#phantom-system-top-game-e-turbo-game)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Créditos](#créditos)
- [Licença](#licença)

## Objetivo

Recuperar a memória deste simpático Famiclone e documentar a pinagem do joystick dele. O objetivo prático é usar o [8BitDo Retro Receiver](https://www.8bitdo.com/retro-receiver-nes/) no Geniecom, jogando com controles sem fio como já faço no NES. Para isso, é preciso conhecer o mapa de pinagem do Geniecom e ligar o conector DB9/DE9 dele ao conector de 7 pinos do NES.

Para saber mais sobre o console, veja [este artigo no Bojoga](https://bojoga.com.br/acervo/consoles-de-mesa/geracao-3/geniecom/). A história completa do projeto está em [docs/historia.md](docs/historia.md).

## Referências

- O NES usa um [conector de 7 pinos](https://www.nesdev.org/wiki/Controller_port_pinout).
- O Geniecom usa o conector DB9/DE9. [Saiba mais sobre ele aqui](http://www.nullmodem.com/DB-9.htm).
- Vídeo de referência de um adaptador semelhante, do [canal do Cirne](https://youtu.be/fYj5p7F7-cc):

  [![Vídeo sobre adaptador NES](https://img.youtube.com/vi/fYj5p7F7-cc/hqdefault.jpg)](https://youtu.be/fYj5p7F7-cc)

- Se você tem um Phantom System, Top Game, Geniecom ou Turbo Game, o Lucas Guilherme vende adaptadores prontos. [Confira aqui](https://shopee.com.br/shop/353762657).

## Pinagem

### Geniecom, visto pelo lado do controle

Perspectiva de quem olha o conector pelo lado do controle: o pino 5 fica à esquerda e o pino 1 à direita.

![Pinagem do Geniecom em DB9 e DB15, vista pelo lado do controle: no DB9, pino 1 Ground, 2 Sound, 3 Latch or Strobe, 5 Data, 6 Clock e 9 Power or VCC +5V; pinos 4, 7 e 8 não conectados](docs/img/png/geniecom_gamepad_facing.png)

### Geniecom, visto pelo lado do console

Perspectiva de quem olha o conector do console de frente: o pino 1 fica à esquerda e o pino 5 à direita.

![Pinagem do Geniecom em DB9 e DB15, vista pelo lado do console: no DB9, pino 1 Ground, 2 Sound, 3 Latch or Strobe, 5 Data, 6 Clock e 9 Power or VCC +5V; pinos 4, 7 e 8 não conectados](docs/img/png/geniecom_console_facing.png)

### Famicom e Geniecom (porta DB15)

A pinagem da porta DB15 do Geniecom segue o mesmo padrão do Famicom. A Light Gun do Famicom funciona no Geniecom (testado e confirmado). Com um [adaptador Famicom → NES](https://misteraddons.com/products/nes-controllers-to-famicom-console-adapter), consegui conectar dois controles de NES e uma [Zapper](https://en.wikipedia.org/wiki/NES_Zapper) ao Geniecom.

![Pinagem DB15 idêntica no Famicom e no Geniecom, vista pelo lado do console, com as portas de controle 1 e 2 do NES e a porta do TwinHead PC-100 como referência](docs/img/png/famicom_console_facing.png)

### NES

![Conector de controle do NES: pino 1 Ground, 2 Clock, 3 Latch or Strobe, 4 Data, 5 Power or VCC +5V; pino 6 D3 e pino 7 D4, usados pela Zapper e sem função no controle padrão](docs/img/png/nes_pinout.png)

### Famicom (DB15) e portas do NES

Ligação entre a porta DB15 no padrão Famicom (exemplo: TwinHead PC-100) e as portas de controle 1 e 2 do NES. Os fios de Ground, Power e Latch são compartilhados pelas duas portas.

![Diagrama de ligação entre a porta DB15 do Famicom e as duas portas de controle do NES: Ground, Power e Latch compartilhados; Clock e Data separados por jogador](docs/img/png/nes_famicom_pinout.png)

## Terminologia

- **Latch** e **Strobe** são o mesmo sinal. Nos diagramas e tabelas, aparece como "Latch or Strobe".
- **Power** e **VCC +5V** são a mesma alimentação de 5 V. Aparece como "Power or VCC +5V".
- **Ground** é o terra (GND).

## Correlação Geniecom ↔ NES

Para ligar um controle de NES ao Geniecom, cada função do DB9 do Geniecom vai para o pino de mesma função no conector do NES. Os números do DB9 abaixo são os pinos físicos do conector, como nos diagramas de pinagem acima.

| Função | Pino DB9 (Geniecom) | Pino NES |
| --- | --- | --- |
| Ground | 1 | 1 |
| Sound | 2 | Não usado (o NES não tem essa função) |
| Latch or Strobe | 3 | 3 |
| Data | 5 | 4 |
| Clock | 6 | 2 |
| Power or VCC +5V | 9 | 5 |
| Sem função | 4, 7 e 8 | 6 e 7 (D3 e D4, usados pela Zapper; não ligados) |

Fontes: os diagramas de pinagem do Geniecom acima e a [pinagem da porta de controle do NES](https://www.nesdev.org/wiki/Controller_port_pinout). Esta correlação vale tanto para o cabo adaptador quanto para a [PCB](#pcb-gerber).

## Montando o adaptador

> **Atenção:** o Geniecom e o NES alimentam o controle com +5 V no pino de Power. Antes de ligar um controle ou adaptador ao console, confirme com um multímetro (modo continuidade, com tudo desligado) que o fio de Power vai ao pino 9 do DB9 e ao pino 5 do NES, e que o Ground não está em curto com o Power. Uma inversão de polaridade pode queimar o controle, o Retro Receiver ou o console.

Os conectores DB9/DE9 machos do Geniecom são muito longos. Por isso, o conector fêmea também precisa ser longo o bastante para a conexão ficar firme, sem folgas. Para fazer o adaptador, comprei:

- [Cabo extensor para controle de Mega Drive](https://www.aliexpress.com/item/4000095438635.html)
- [Cabo extensor para controle de NES](https://www.aliexpress.com/item/4000029468234.html)
- [Anel de ferrite para cabo, 5 mm](https://www.aliexpress.com/item/1005006071819843.html)

Cortei os cabos dos dois extensores e liguei entre si os fios de mesma função. O Mega Drive e o NES são usados só como fonte de conector e fio: o que importa é a função que cada fio assume no Geniecom e no NES.

### Mapa de ligação

Cada linha do diagrama é uma função. Leia da esquerda para a direita: o pino do DB9 (lado Geniecom), a cor do fio correspondente no cabo do Mega Drive, a função, a cor do fio do cabo do NES que deve ser emendado a ele e o pino do NES. A cor da linha identifica a função, e as cores dos fios são as dos cabos que usei.

![Diagrama de ligação do adaptador: Ground, pino 1 do DB9 (fio vermelho do Mega Drive) ao pino 1 do NES (fio branco); Clock, pino 6 (verde) ao pino 2 (verde); Latch or Strobe, pino 3 (cinza) ao pino 3 (amarelo); Data, pino 5 (marrom) ao pino 4 (preto); Power or VCC +5V, pino 9 (amarelo) ao pino 5 (vermelho); Sound, pino 2 (preto), não ligado; pinos 4, 7 e 8 do DB9 e 6 e 7 do NES sem uso](docs/img/png/adaptador_ligacao.png)

| Função | Cor do fio (Mega Drive) | Cor do fio (NES) |
| --- | --- | --- |
| Ground | Vermelho | Branco |
| Clock | Verde | Verde |
| Latch or Strobe | Cinza | Amarelo |
| Data | Marrom | Preto |
| Power or VCC +5V | Amarelo | Vermelho |
| Sound | Preto | Não ligado |
| Sem função | Laranja, Branco e Azul (isolar) | Não usado |

Os números dos pinos estão no diagrama e na tabela de [correlação](#correlação-geniecom--nes). Se os seus cabos tiverem outras cores, descubra com o multímetro qual fio sai de cada pino e emende pela função: as funções e os pinos valem para qualquer cabo, as cores não.

<details>
<summary>Cores de cada cabo, pino a pino (para conferir com o multímetro)</summary>

**Cabo do Mega Drive (DB9, funções do Geniecom)**

| Pino DB9 (Geniecom) | Cor do fio (Mega Drive) | Função |
| --- | --- | --- |
| 01 | Vermelho | Ground |
| 02 | Preto | Sound |
| 03 | Cinza | Latch or Strobe |
| 04 | Laranja | Não usado |
| 05 | Marrom | Data |
| 06 | Verde | Clock |
| 07 | Branco | Não usado |
| 08 | Azul | Não usado |
| 09 | Amarelo | Power or VCC +5V |

**Cabo do NES (conector de 7 pinos)**

| Pino NES | Cor do fio (NES) | Função |
| --- | --- | --- |
| 01 | Branco | Ground |
| 02 | Verde | Clock |
| 03 | Amarelo | Latch or Strobe |
| 04 | Preto | Data |
| 05 | Vermelho | Power or VCC +5V |
| 06 | Não usado | Não usado |
| 07 | Não usado | Não usado |

</details>

### Resultado final

Esta belezinha!

![Adaptador NES para Geniecom pronto: cabo com conector DB9 fêmea de um lado, conector NES de 7 pinos do outro e anel de ferrite sobre uma mesa de madeira](docs/img/jpg/adaptadornesgeniecom.jpg)

## PCB (Gerber)

Em junho de 2025, passei a me interessar cada vez mais por eletrônica e retro consoles. Por isso, criei no [EasyEDA](https://easyeda.com/) o projeto de uma [PCB](https://es.wikipedia.org/wiki/Circuito_impreso) com a pinagem que converte NES para Geniecom, para fabricá-la na [JLCPCB](https://jlcpcb.com/). A placa mede aproximadamente 31 × 40,5 mm.

Os arquivos estão disponíveis para quem quiser usar ou modificar:

| Arquivo | Descrição |
| --- | --- |
| [hardware/gerber_geniecom.zip](hardware/gerber_geniecom.zip) | Gerber, pronto para enviar à fábrica de PCB |
| [hardware/easyeda/geniecom_pcb.json](hardware/easyeda/geniecom_pcb.json) | Layout da PCB, arquivo-fonte editável (importe no EasyEDA) |
| [hardware/easyeda/geniecom_sch.json](hardware/easyeda/geniecom_sch.json) | Esquemático, arquivo-fonte editável (importe no EasyEDA) |
| [hardware/easyeda/geniecom_pcb.pdf](hardware/easyeda/geniecom_pcb.pdf) | Visualização do layout |
| [hardware/bom_geniecom.csv](hardware/bom_geniecom.csv) | Lista de materiais (BOM) |

Façam bom proveito!

### Lista de materiais

| Designador | Descrição | Qtd. | Compra |
| --- | --- | --- | --- |
| NES | Conector de controle NES, 7 pinos fêmea, ângulo reto | 1 | [AliExpress](https://www.aliexpress.com/item/32828024202.html) |
| Geniecom | Conector DB9 fêmea, ângulo reto | 1 | [AliExpress](https://www.aliexpress.com/item/4001214300548.html) |

### Ligações da PCB

A PCB implementa a [correlação Geniecom ↔ NES](#correlação-geniecom--nes) acima.

> **Nota sobre o EasyEDA:** o footprint do DB9 fêmea usado no projeto tem os pads numerados de forma espelhada em relação aos pinos físicos (pad 1 ↔ pino 5, pad 2 ↔ pino 4, pad 6 ↔ pino 9 e pad 7 ↔ pino 8; o pad 3 coincide). Por isso, o esquemático e o layout mostram, por exemplo, "DB9 1 → NES 4", que corresponde ao Data (pino físico 5) no NES. Se você editar o projeto, mantenha esse espelhamento.

### PCB montada

A placa chegou e foi montada com os dois conectores.

| | |
| --- | --- |
| ![PCB montada, vista geral, com as serigrafias "Geniecom" e "NES"](docs/img/jpg/pcb_montada_vista_geral.jpg) | ![PCB montada, verso, com QR code e a numeração 0004](docs/img/jpg/pcb_montada_verso.jpg) |
| Vista geral: conector DB9 (lado Geniecom) e conector NES. | Verso da placa, com os terminais dos conectores. |
| ![Conector DB9 fêmea da PCB](docs/img/jpg/pcb_montada_conector_db9.jpg) | ![Conector NES de 7 pinos da PCB](docs/img/jpg/pcb_montada_conector_nes.jpg) |
| Conector DB9 fêmea, que encaixa no Geniecom. | Conector NES de 7 pinos, que recebe o controle ou o Retro Receiver. |

## Case para impressão 3D

Case sob medida para a [PCB do Geniecom](#pcb-gerber) montada (PCB, DB9 e conector NES soldados), sem nada exposto: a moldura do DB9 e o corpo do NES atravessam a parede da case e ficam com a face rente à face externa, então a carcaça D do DB9 sai inteira (encaixe completo no console) e o plugue do controle entra direto no NES. São duas peças, base e tampa, geradas por script (CadQuery) e exportadas em STL e STEP. Para o Phantom System, Top Game e Turbo Game, veja a [case do Phantom](#case-para-impressão-3d-do-phantom-system-top-game-e-turbo-game).

> **Status:** modelo validado só por geometria (malhas fechadas e teste de interferência com os envelopes dos conectores). Ainda não foi impresso nem testado com a PCB.

![Pré-visualização da case: vistas montada, base, tampa e corte longitudinal](model3d/geniecom/stl/preview.png)

| Arquivo | Descrição |
| --- | --- |
| [model3d/geniecom/stl/case_base.stl](model3d/geniecom/stl/case_base.stl) | Base, pronta para imprimir (fundo na mesa) |
| [model3d/geniecom/stl/case_lid.stl](model3d/geniecom/stl/case_lid.stl) | Tampa, já virada para imprimir (teto na mesa) |
| [model3d/geniecom/stl/case_assembly.stl](model3d/geniecom/stl/case_assembly.stl) | Conjunto montado, só para conferência visual |
| [model3d/geniecom/autodeskfusion/case_geniecom.py](model3d/geniecom/autodeskfusion/case_geniecom.py) | Script paramétrico (CadQuery) que gera todos os arquivos |
| [model3d/geniecom/autodeskfusion/case_base.step](model3d/geniecom/autodeskfusion/case_base.step), [case_lid.step](model3d/geniecom/autodeskfusion/case_lid.step), [case_assembly.step](model3d/geniecom/autodeskfusion/case_assembly.step) | Para importar no Autodesk Fusion (*Inserir > Inserir arquivo STEP*); a geometria vem editável, sem histórico paramétrico |

### Material necessário

- Impressão 3D: `case_base.stl` e `case_lid.stl` (não imprima o `case_assembly.stl`, que é só para visualização).
- Parafusos: **4 × M3×16 mm**, autorroscantes, de cabeça escareada, colocados pelo fundo da base.
- A PCB já montada, com o DB9 e o conector NES soldados.

### Características

- Medidas dos conectores tiradas do layout da PCB ([hardware/easyeda/geniecom_pcb.json](hardware/easyeda/geniecom_pcb.json)).
- A PCB fica apoiada em blocos na base, com batente traseiro, e é presa por pilares da tampa. Dois pilares junto às orelhas do conector NES impedem a PCB de sair pela frente quando se desconecta o plugue.
- A borda da PCB e a moldura do DB9 ficam rentes à face frontal; uma parede de 1,6 mm da base, abaixo da PCB, fecha o vão do fundo.
- Folga sob a PCB para os pinos soldados e as cabeças dos parafusos do DB9.
- Lingueta e ranhura alinham base e tampa.
- Quatro parafusos **M3 autorroscantes de cabeça escareada** (kit Zmbroll): a cabeça fica embutida no fundo da base e o parafuso rosqueia em furos-piloto de 2,5 mm na tampa. Use **M3×16 mm**. Os parafusos ficam em "ombros" nas laterais, entre os dois conectores, o que leva a largura externa a 47 mm.
- Dimensões externas: cerca de 47 × 44,8 × 24,5 mm. A cavidade tem 33,9 mm de largura para acomodar o flange metálico do DB9 (33,15 mm).

### Impressão

PLA, camada de 0,2 mm, 3 paredes, sem suporte. Os STLs já estão na orientação de impressão. Folgas pensadas para FDM com bico de 0,4 mm; ajuste os parâmetros do script para outra impressora.

### Medidas a conferir

As larguras e alturas dos conectores foram conferidas com paquímetro (as medidas do NES e do DB9 são as mesmas no Geniecom e no Phantom). Já com todas as medidas conferidas:

| Parâmetro | Valor | Observação |
| --- | --- | --- |
| `nes_h` | 15,0 mm | Medido: 16,4 mm com a PCB, ou 14,8 mm acima dela; arredondado para cima. Define a altura total da case |
| `db9_h` | 12,5 mm | Medido: 14,03 mm com a PCB, ou 12,4 mm acima dela; arredondado para cima |
| `db9_body_w` | 33,15 mm | Medido: largura do flange metálico do DB9 |
| `db9_axis_h` | 5,9 mm | Medido: borda de baixo da abertura a 2,68 mm e a de cima a 9,1 mm do plano da PCB; o centro fica em 5,9 mm. Só entra na checagem de interferência |
| `nes_body_w` | 24,9 mm | Medido: largura do conector NES com a moldura (24,88 a 24,92). A janela da case tem 0,25 mm de folga de cada lado |
| `nes_front` | 44,79 mm | Medido na PCB do Geniecom montada: distância da face da moldura do DB9 até a face do NES (o layout dá 44,62 mm). No Phantom o valor vem do layout (40,16 mm) |

Também vale testar o encaixe: a janela do DB9 (33,4 mm de largura) e a do NES (25,4 × 15,4 mm) seguem as medidas acima. Se alguma peça não entrar, aumente `window_clear` (folga ao redor das janelas).

### Regenerar

```bash
pip install cadquery
python model3d/geniecom/autodeskfusion/case_geniecom.py
```

O script reescreve os STL e STEP e imprime o resultado do teste de interferência.

## Bônus: outros clones

Pinagem dos demais clones que consegui coletar:

![Pinagem de outros clones: plug de cabo de reposição, joystick do Atari 2600 (Up, Down, Left, Right, Fire, Ground), NES original, Turbo Game, Phantom System, TCP-3, Dynavision TPC-1 e Famiclone genérico](docs/img/png/demais_clones_pinout.png)

### Phantom System, Top Game e Turbo Game

O Phantom System foi um dos primeiros famiclones brasileiros, lançado pela Gradiente por volta de 1989, numa época em que a Nintendo não demonstrava interesse em lançar o NES oficialmente no país. A placa é basicamente a de um NES, montada numa carcaça que sobrou de um projeto de lançar o Atari 7800 no Brasil, com um controle que lembra o do Mega Drive. Ele usa os mesmos cartuchos de 72 pinos do NES e se tornou o clone mais popular do Brasil. Saiba mais no [Bojogá](https://bojoga.com.br/acervo/consoles-de-mesa/geracao-3/phantom-system/).

O Top Game e o Turbo Game, da CCE, são outros dois famiclones da mesma época que usam a mesma base de projeto: o Top Game (modelos VG-8000 e VG-9000) foi concorrente direto do Phantom System, e o Turbo Game (VG-9000T) chegou em 1991 como sua evolução, trocando de nome e adotando um controle inspirado no do Mega Drive, só que invertido e com botões turbo. Por compartilharem a mesma origem de projeto do controle, a pinagem do conector é a mesma nos três consoles.

Ao contrário do Geniecom, a pinagem do conector DB9 do Phantom System segue exatamente a mesma ordem do conector de 7 pinos do NES: não há remapeamento de função por pino, só ligar "pino a pino".

| Função | Pino DB9 (Phantom System) | Pino NES |
| --- | --- | --- |
| Ground | 1 | 1 |
| Clock | 2 | 2 |
| Latch or Strobe | 3 | 3 |
| Data | 4 | 4 |
| Power or VCC +5V | 5 | 5 |
| Sem função (terra da blindagem do conector) | 6, 7, 8 e 9 | Não usado |

Fonte: o esquemático abaixo, confirmado também no layout da PCB (arquivos na seção seguinte). Essa correlação é a mesma já registrada na tabela "Turbo Game / Phantom System / TCP-3" da imagem de pinagem dos outros clones, acima.

![Esquemático do adaptador NES para Phantom System: conector DB9-RIGHT-ANGLE FEMALE com os pinos 1 a 5 ligados diretamente aos pinos 1 a 5 do conector NES de 7 pinos; os pinos 6 a 9 do DB9 vão só para GND](docs/img/png/phantom_sch.png)

#### PCB (Gerber) do Phantom System, Top Game e Turbo Game

No mesmo projeto do EasyEDA, montei uma segunda PCB com a pinagem do Phantom System (compatível também com o Top Game e o Turbo Game), no mesmo padrão da PCB do Geniecom.

| Arquivo | Descrição |
| --- | --- |
| [hardware/gerber_phantom.zip](hardware/gerber_phantom.zip) | Gerber, pronto para enviar à fábrica de PCB |
| [hardware/easyeda/phantom_pcb.json](hardware/easyeda/phantom_pcb.json) | Layout da PCB, arquivo-fonte editável (importe no EasyEDA) |
| [hardware/easyeda/phantom_sch.json](hardware/easyeda/phantom_sch.json) | Esquemático, arquivo-fonte editável (importe no EasyEDA) |
| [hardware/easyeda/phantom_pcb.pdf](hardware/easyeda/phantom_pcb.pdf) | Visualização do layout |
| [docs/img/svg/phantom_sch.svg](docs/img/svg/phantom_sch.svg) | Visualização do esquemático |
| [hardware/bom_phantom.csv](hardware/bom_phantom.csv) | Lista de materiais (BOM) |

![Layout da PCB do adaptador NES para Phantom System no EasyEDA, mostrando o conector NES de 7 pinos à esquerda ligado ao conector DB9 do Phantom System à direita](docs/img/png/phantom_pcb_layout.png)

Esta PCB ainda não foi fabricada ou montada; os arquivos acima estão prontos para quem quiser produzi-la.

##### Adaptador montado (ilustração)

Fotos de um adaptador NES para Phantom System, Top Game e Turbo Game já montado, a título de ilustração do resultado: PCB com o conector DB9 fêmea e o conector NES de 7 pinos.

| | |
| --- | --- |
| ![Adaptador montado, vista geral, com a serigrafia "Turbo Game Nintendo"](docs/img/jpg/phantom_adaptador_vista_geral.jpg) | ![Adaptador montado, verso, com os terminais soldados e os parafusos do DB9](docs/img/jpg/phantom_adaptador_verso.jpg) |
| Vista geral: conector DB9 (lado do console) e conector NES. | Verso da placa, com os terminais dos conectores. |
| ![Conector DB9 fêmea do adaptador, de frente](docs/img/jpg/phantom_adaptador_conector_db9.jpg) | ![Conector NES de 7 pinos do adaptador, de frente](docs/img/jpg/phantom_adaptador_conector_nes.jpg) |
| Conector DB9 fêmea, que encaixa no console. Atrás dele aparecem os pinos do NES. | Conector NES de 7 pinos, que recebe o controle ou o Retro Receiver. |

##### Lista de materiais

| Designador | Descrição | Qtd. | Compra |
| --- | --- | --- | --- |
| NES | Conector de controle NES, 7 pinos fêmea, ângulo reto | 1 | [AliExpress](https://www.aliexpress.com/item/32828024202.html) |
| PHANTOM | Conector DB9 fêmea, ângulo reto | 1 | [AliExpress](https://www.aliexpress.com/item/4001214300548.html) |

#### Case para impressão 3D do Phantom System, Top Game e Turbo Game

A case segue o mesmo projeto da [case do Geniecom](#case-para-impressão-3d), com as medidas da PCB do Phantom (35,8 × 31,2 mm, mais curta que a do Geniecom). Os conectores são os mesmos, então as janelas do DB9 e do NES e os parafusos M3×16 não mudam. Dimensões externas: cerca de 47 × 40,2 × 24,5 mm. A distância entre a moldura do DB9 e a face do NES (40,16 mm) vem do layout da PCB do Phantom e ainda não foi conferida com paquímetro. As [medidas a conferir](#medidas-a-conferir) e as dicas de impressão valem igualmente aqui. Como a PCB ainda não foi fabricada, a case também não foi testada.

| Arquivo | Descrição |
| --- | --- |
| [model3d/phantom/stl/case_base.stl](model3d/phantom/stl/case_base.stl) | Base, pronta para imprimir (fundo na mesa) |
| [model3d/phantom/stl/case_lid.stl](model3d/phantom/stl/case_lid.stl) | Tampa, já virada para imprimir (teto na mesa) |
| [model3d/phantom/stl/case_assembly.stl](model3d/phantom/stl/case_assembly.stl) | Conjunto montado, só para conferência visual |
| [model3d/phantom/stl/preview.png](model3d/phantom/stl/preview.png) | Pré-visualização |
| [model3d/phantom/autodeskfusion/case_phantom.py](model3d/phantom/autodeskfusion/case_phantom.py) | Script paramétrico (CadQuery) |
| [model3d/phantom/autodeskfusion/case_base.step](model3d/phantom/autodeskfusion/case_base.step), [case_lid.step](model3d/phantom/autodeskfusion/case_lid.step), [case_assembly.step](model3d/phantom/autodeskfusion/case_assembly.step) | Para importar no Autodesk Fusion |

Para regenerar: `python model3d/phantom/autodeskfusion/case_phantom.py`.

## Estrutura do repositório

```text
.
├── README.md                  # Este arquivo
├── LICENSE
├── .gitignore
├── docs/
│   ├── historia.md            # Motivação, busca pela pinagem e agradecimentos
│   └── img/                   # Imagens, separadas por formato
│       ├── jpg/               # Fotos do adaptador e da PCB montada
│       ├── png/               # Diagramas de pinagem e ligação (usados no README)
│       └── svg/               # Fontes vetoriais (editáveis) dos diagramas
│           └── phantom_sch.svg    # Visualização do esquemático do Phantom System (exportado do EasyEDA)
├── model3d/                   # Cases para impressão 3D
│   ├── geniecom/
│   │   ├── autodeskfusion/
│   │   │   ├── case_geniecom.py   # Script paramétrico (CadQuery) da case
│   │   │   └── case_*.step        # Base, tampa e conjunto, para importar no Fusion
│   │   └── stl/
│   │       ├── case_base.stl      # Base (orientação de impressão)
│   │       ├── case_lid.stl       # Tampa (orientação de impressão)
│   │       ├── case_assembly.stl  # Conjunto montado
│   │       └── preview.png        # Pré-visualização
│   └── phantom/               # Mesma organização, para o Phantom System, Top Game e Turbo Game
│       ├── autodeskfusion/    # case_phantom.py e case_*.step
│       └── stl/               # case_*.stl e preview.png
└── hardware/
    ├── gerber_geniecom.zip    # Arquivos Gerber da PCB do Geniecom
    ├── gerber_phantom.zip     # Arquivos Gerber da PCB do Phantom System
    ├── bom_geniecom.csv       # Lista de materiais do Geniecom
    ├── bom_phantom.csv        # Lista de materiais do Phantom System
    └── easyeda/
        ├── geniecom_sch.json  # Esquemático do Geniecom (EasyEDA)
        ├── geniecom_pcb.json  # Layout da PCB do Geniecom (EasyEDA)
        ├── geniecom_pcb.pdf   # Visualização do layout do Geniecom
        ├── phantom_sch.json   # Esquemático do Phantom System (EasyEDA)
        ├── phantom_pcb.json   # Layout da PCB do Phantom System (EasyEDA)
        └── phantom_pcb.pdf    # Visualização do layout do Phantom System
```

## Créditos

- [Lucas Guilherme](https://shopee.com.br/shop/353762657), que documentou a pinagem do Geniecom.
- [Ícaro Jonas](https://github.com/icaroj), que converteu o Geniecom para NTSC e confeccionou os adaptadores.

Mais detalhes em [docs/historia.md](docs/historia.md#agradecimentos).

## Licença

Distribuído sob a [GNU GPL v3](LICENSE).

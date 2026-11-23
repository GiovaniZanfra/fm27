# Táticas FM27

Treze táticas (três por técnico, mais uma extra do Giovani), montadas dentro das regras de `managers_tactics.md` e da identidade de `managers.md`. Roles, posições e custos conferidos contra `game_data/roles.json`, `game_data/instructions_ui.json` e `game_data/instructions.json`.

**Status:** propostas, ainda sem jogo no save. Viram config (`configs/<time>/<nome>.json`) quando aprovadas.

## Como ler

- **Slot `AML → ML`**: o jogador ocupa AML na forma com bola e ML na forma sem bola. A role sem bola tem que valer para o slot **sem bola**. A ligação entre os slots das duas formas é suposição nossa (o ponta desce pra linha do meio, o meia da AMC sobe pra dupla de ataque quando a forma sem bola tem dois atacantes); confirmar na tela.
- **Linha de roles**: `IP/OOP` em ordem posicional, no formato da coluna `Roles` da planilha.
- **Cx**: complexidade da role com bola + da role sem bola.
- **Team instructions**: só as escolhidas; tudo o que não aparece fica na opção neutra (Standard / Balanced / Mixed / No / Keep Ball in Play). Custo entre parênteses; `?` = Time Wasting, cujo custo não está confirmado.
- **Player instructions**: role com bola + instruções do jogador nunca passam de 4.


---

## 1. Giovani — Corinthians

Mentality entre cautious e attacking. Roles antes da forma; duas camadas de proteção no meio sem bola; três atrás da bola na saída.

### 1.1 `relógio`

> *Tudo no lugar, tudo no tempo certo.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-1-1 2DM`
- **Mentality:** balanced
- **Linha de roles:** `BPGK/GK, IFB/FB, BPCB/CB, CB/CCB, WB/HFB, DLP/SDM, DM/DM, W/TWM, AP/TAM, IW/TWM, CF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Inside Full-Back | Full-Back | 1+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Holding Full-Back | 0+1 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| DM | Defensive Midfielder | Defensive Midfielder | 0+0 |
| AML → ML | Winger | Tracking Wide Midfielder | 0+1 |
| AMC | Advanced Playmaker | Tracking Attacking Midfielder | 2+1 |
| AMR → MR | Inside Winger | Tracking Wide Midfielder | 1+1 |
| ST | Centre Forward | Centre Forward | 0+0 |

Complexidade das roles: 10 com bola, 7 sem bola.

**Com bola.** Saída com três: o lateral esquerdo fecha por dentro ao lado dos zagueiros, o DLP organiza na frente deles e o DM fica parado de proteção. Cada lado tem um jogador aberto: à esquerda o Winger (o lateral está por dentro), à direita o Wing-Back passando por fora do Inside Winger, que entra no meio-espaço. O AP procura o espaço entre as linhas e o Centre Forward é a referência na área, onde a bola chega trabalhada, não lançada. Bola curta e no pé, sem pressa.

**Sem bola.** Bloco médio em 4-4-1-1. Os pontas descem pra linha do meio acompanhando os laterais adversários, o AP marca o volante deles e os dois DM fecham a entrada da área. Ninguém sai da posição pra caçar a bola: o time espera o erro e intercepta.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Shorter (2) · Pass Reception: Pass to Feet (1) · Patience: Work Ball Into Box (2) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Centre-Backs (1) | 12 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) | 3 |
| **Total** | | **15** |

**Player instructions**

- DM (DM): Positioning: Hold Position (1) — o DM é a proteção fixa: não acompanha o ataque

**Quando usar.** É o padrão: em casa ou fora, contra adversário do mesmo nível ou mais fraco. Segurando vitória, fica nela e troca roles e instruções: `DLP/SDM` → `DM/SDM`, `IFB/FB` e `WB/HFB` → `FB/HFB`, Passing Directness: Much Shorter, Tempo: Lower, Time Wasting: More Often, Attacking Transition: Hold Shape, mentality cautious (manual 1.4). Contra time que pressiona alto e com zagueiros que têm passe, acrescentar Build-up Strategy: Play Through Press (+3).

### 1.2 `xadrez`

> *Mais gente no meio, menos jogo pro adversário.*

- **Forma com bola:** `4-4-2 Diamond Narrow`
- **Forma sem bola:** `4-4-2 Diamond Narrow`
- **Mentality:** balanced
- **Linha de roles:** `BPGK/GK, WB/FB, BPCB/CB, CB/CCB, FB/HFB, HB/SDM, CM/SCM, WCM/WCCM, AP/TAM, DLF/TCF, CF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Holding Full-Back | 0+1 |
| DM | Half Back | Screening Defensive Midfielder | 2+1 |
| MC | Central Midfielder | Screening Central Midfielder | 0+1 |
| MC | Wide Central Midfielder | Wide Covering Central Midfielder | 1+2 |
| AMC | Advanced Playmaker | Tracking Attacking Midfielder | 2+1 |
| ST | Deep-Lying Forward | Tracking Centre Forward | 2+1 |
| ST | Centre Forward | Centre Forward | 0+0 |

Complexidade das roles: 12 com bola, 9 sem bola.

**Com bola.** O Half Back desce entre os zagueiros e libera os laterais. A esquerda é do Wing-Back, que vai até o fundo; à direita, o Wide Central Midfielder (MC direito) abre pro corredor e o Full-Back desse lado só apoia por trás dele. No meio, o CM (MC esquerdo) segura. O AP flutua atrás da dupla: o DLF vem buscar e o Centre Forward ataca o espaço que ele deixa.

**Sem bola.** O losango se mantém. A armadilha de pressão empurra o adversário pro meio, onde o Giovani tem um jogador a mais. O DLF acompanha o volante adversário, o AP fecha o outro, e do lado direito o WCM cobre o corredor enquanto o lateral fica na linha (Holding Full-Back).

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Shorter (2) · Pass Reception: Pass to Feet (1) · Patience: Work Ball Into Box (2) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Centre-Backs (1) | 12 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) · Pressing Trap: Trap Inside (0) | 3 |
| **Total** | | **15** |

**Player instructions**

- Nenhuma.

**Quando usar.** Contra time com um volante só ou 4-4-2 reto, quando dominar o meio decide o jogo. Evitar contra dois pontas rápidos: o lado esquerdo fica exposto (correção: lateral esquerdo `FB/HFB`, que não sobe com a bola). Vencendo: lateral esquerdo `FB/HFB`, Passing Directness: Much Shorter, Tempo: Lower, Time Wasting: More Often, Attacking Transition: Hold Shape, mentality cautious; o meio (`CM/SCM`, `AP/TAM`) já é o de segurar. Perdendo: primeiro roles (`CM/SCM` → `CM/PRCM`, `AP` → `SS`, `CF` com Pressing Intensity: Higher) e mentality positive; só no fim troca de forma pra `engrenagem` (diamante → 4-2-3-1, a única troca de forma que o manual 1.4 prevê).

### 1.3 `engrenagem`

> *A mesma máquina, girando mais rápido.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-1-1 2DM`
- **Mentality:** positive (attacking a partir dos 75', perdendo)
- **Linha de roles:** `BPGK/SWK, WB/FB, BPCB/CB, CB/CCB, WB/PRFB, DM/SDM, DM/PRDM, IW/TWM, SS/AM, IF/TWM, CF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Sweeper Keeper | 2+2 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Pressing Full-Back | 0+2 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Defensive Midfielder | Pressing Defensive Midfielder | 0+2 |
| AML → ML | Inside Winger | Tracking Wide Midfielder | 1+1 |
| AMC | Second Striker | Attacking Midfielder | 1+0 |
| AMR → MR | Inside Forward | Tracking Wide Midfielder | 2+1 |
| ST | Centre Forward | Centre Forward | 0+0 |

Complexidade das roles: 9 com bola, 10 sem bola.

**Com bola.** As mesmas duas formas do `relógio`, com mais gente na área (as trocas de role do manual 1.4). O AP vira Second Striker e chega como segundo atacante; o lateral esquerdo deixa de fechar por dentro e vira Wing-Back, com o Inside Winger entrando no meio-espaço à frente dele; à direita, o Inside Forward corta pra dentro e o Wing-Back passa por fora. Os dois volantes continuam atrás da bola com os zagueiros.

**Sem bola.** Sobe a pressão sem mudar a forma: continua 4-4-1-1, mas o Second Striker e o centroavante pressionam a saída por instrução individual. Na dupla de volantes um salta (Pressing DM) e o outro segura (Screening DM): nunca os dois. O lateral direito pressiona o ponta adversário, e a linha sobe com o goleiro varrendo atrás.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Shorter (2) · Pass Reception: Pass to Feet (1) · Patience: Work Ball Into Box (2) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Centre-Backs (1) · Tempo: Higher (1) | 13 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Higher (2) · Trigger Press: More Often (2) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Stay on Feet (1) | 10 |
| **Total** | | **23** |

**Player instructions**

- AMC (SS): Pressing Intensity: Higher (2) — segundo homem da primeira linha de pressão
- ST (CF): Pressing Intensity: Higher (2) — faz o papel do antigo Pressing Forward

**Quando usar.** Empate travado ou placar contra. É o `relógio` com os ajustes de "aumentar a intensidade sem perder a estrutura" do manual 1.4 já aplicados (roles e instruções), salvo como tática própria pra entrar de uma vez. Antes dela, o único passo é subir a mentality do `relógio` pra positive. A forma com bola e a sem bola são as mesmas do `relógio`, então a troca é só de roles e instruções, como manda a regra de ouro. A partir dos 75', perdendo: mentality attacking e Shots From Distance: Encourage.

**Atenção.** Defensive Line: Higher acompanha a pressão alta (manual 1.4) e é o que justifica o Sweeper Keeper. A linha alta expõe zagueiro lento: o `CCB` precisa de velocidade.

### 1.4 `pêndulo`

> *DLP e AP pensam, SS e o lateral chegam, TF e CHF finalizam.*

- **Forma com bola:** `4-2-2-2 DM AM Narrow`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** balanced
- **Linha de roles:** `BPGK/GK, WB/FB, CB/CCB, BPCB/CB, FB/HFB, HB/SDM, DLP/DM, SS/TWM, AP/WM, TF/CF, CHF/TCF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DR | Full-Back | Holding Full-Back | 0+1 |
| DM | Half Back | Screening Defensive Midfielder | 2+1 |
| DM | Deep-Lying Playmaker | Defensive Midfielder | 1+0 |
| AMC → ML | Second Striker | Tracking Wide Midfielder | 1+1 |
| AMC → MR | Advanced Playmaker | Wide Midfielder | 2+0 |
| ST | Target Forward | Centre Forward | 1+0 |
| ST | Channel Forward | Tracking Centre Forward | 1+1 |

Complexidade das roles: 13 com bola, 6 sem bola.

**Com bola.** O 4-2-2-2 estreito: o jogo passa pelo corredor central. O Half Back desce entre os zagueiros e forma a saída com três; o DLP organiza na frente deles. O AP (AMC direito) recebe entre as linhas; o Second Striker (AMC esquerdo) chega na área ao lado da dupla de ataque. O Target Forward (ST esquerdo) é o alvo dos cruzamentos do Wing-Back e escora de primeira pros meias que chegam de frente; o Channel Forward (ST direito) cai no canal direito e é a largura móvel desse lado. A largura fixa é só do Wing-Back esquerdo; o lateral direito fica atrás do AP.

**Sem bola.** Sem bola vira 4-4-2. Do lado do Wing-Back que sobe, o Second Striker desce e acompanha o lateral adversário até o fundo (Tracking Wide Midfielder), e o zagueiro de cobertura joga desse lado. Do outro lado, o AP fica como Wide Midfielder na frente de um lateral que já segura a linha. Os dois volantes fecham a frente da área (um de Screening), o TF fica de referência e o CHF volta acompanhando o volante adversário. Bloco médio e paciente.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Shorter (2) · Pass Reception: Pass to Feet (1) · Patience: Work Ball Into Box (2) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Centre-Backs (1) | 12 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) | 3 |
| **Total** | | **15** |

**Player instructions**

- Nenhuma.

**Quando usar.** Quando os melhores jogadores do elenco são meias centrais e atacantes, não pontas, e contra 4-4-2 reto: o meio tem mais gente que o adversário e o ataque tem dois atacantes em vez de um. Em vez do `xadrez` quando o adversário tem pontas rápidos: o 4-4-2 sem bola cobre os lados que o losango deixa abertos. Vencendo: SS → `AM/TWM` (meia de apoio, não de chegada), DLP → `DM/SDM`, lateral esquerdo `FB/HFB`, Passing Directness: Much Shorter, Tempo: Lower, Time Wasting: More Often, Attacking Transition: Hold Shape, mentality cautious. Perdendo: roles e instruções na mesma forma (CHF sem bola `TCF` → `CF`, TF e CHF com Pressing Intensity: Higher, DLP sem bola `DM` → `PRDM`, goleiro `BPGK/SWK`; High Press, Trigger Press: More Often, Defensive Transition: Counter-Press, Defensive Line: Higher, Tempo: Higher; mentality positive e depois attacking; a partir dos 75', Shots From Distance: Encourage). Último passo, só com pontas no banco: trocar só a forma com bola pra `4-2-3-1 DM AM Wide` (SS no AMC, pontas do banco nas pontas) e manter o `4-4-2 2DM` sem bola. Sem pontas, fica na forma e esgota mentality e instruções.

**Atenção.** A forma não é uma das formas prontas do jogo, e a ligação AMC → ML/MR sem bola é suposição. Confirmar as duas na tela antes de virar config. Se a ligação não sair limpa, usar `4-4-2 Diamond Narrow` sem bola (aceitável no manual): HB `HB/SDM` no DM, DLP `DLP/SCM` e AP `AP/SCM` no MC, SS `SS/TAM` no AMC. Isso devolve a fraqueza de lado do `xadrez`, que é justamente o que o `pêndulo` resolve.


---

## 2. Bruno Keller — Palmeiras

Mentality entre positive e attacking. Pressão alta, linha alta, dois na primeira linha de pressão. Protege vantagem prendendo o adversário, não sentando.

### 2.1 `avalanche`

> *Ganhou, atacou. Perdeu, roubou de volta.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** attacking
- **Linha de roles:** `BPGK/SWK, FB/PRFB, BPCB/SCB, CB/CCB, WB/PRFB, BBM/PRDM, DM/SDM, W/WM, SS/CF, IF/WM, CHF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Sweeper Keeper | 2+2 |
| DL | Full-Back | Pressing Full-Back | 0+2 |
| DC | Ball-Playing Centre-Back | Stopping Centre-Back | 2+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Pressing Full-Back | 0+2 |
| DM | Box-To-Box Midfielder | Pressing Defensive Midfielder | 1+2 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| AML → ML | Winger | Wide Midfielder | 0+0 |
| AMC → ST | Second Striker | Centre Forward | 1+0 |
| AMR → MR | Inside Forward | Wide Midfielder | 2+0 |
| ST | Channel Forward | Centre Forward | 1+0 |

Complexidade das roles: 10 com bola, 11 sem bola.

**Com bola.** Vertical e largo. Bola roubada vai pra frente rápido, nas costas da defesa: o Channel Forward ataca o corredor, o Second Striker chega como segundo atacante e o Inside Forward pisa na área pela direita, com o Wing-Back passando por fora. Pela esquerda o Winger estica sozinho e o lateral fica. O Box-to-Box sobe pra dar número; o DM segura.

**Sem bola.** 4-4-2 de pressão no campo todo: o Second Striker sobe e forma dupla com o centroavante em cima dos zagueiros, os pontas descem pra linha do meio e os laterais pressionam os pontas adversários. Um volante salta (Pressing DM), o outro fecha (Screening DM). Um zagueiro salta no atacante, o outro (o mais rápido) cobre, e o goleiro varre atrás da linha alta.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Pass Reception: Pass Into Space (1) · Build-up Strategy: Bypass Press (0) · Tempo: Higher (1) · Attacking Width: Wider (1) · Dribbling: Encourage (2) · Patience: Hit Early Crosses (1) · Crossing Style: Low Crosses (1) · Supporting Runs: Right Overlap (1) · Attacking Transition: Counter-Attack (2) · GK Distribution Speed: Distribute Quickly (2) · GK Distribution Target: Flanks (1) | 14 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Higher (2) · Defensive Line Behaviour: Step Up More (2) · Trigger Press: Much More Often (3) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Get Stuck In (1) · Prevent Short GK Distribution: Yes (1) | 14 |
| **Total** | | **28** |

**Player instructions**

- AMC (SS): Pressing Intensity: Higher (2) — segundo homem da primeira linha de pressão
- ST (CHF): Pressing Intensity: Higher (2) — primeira linha de pressão
- DM (DM): Positioning: Hold Position (1) — o volante que fica: não sobe com o Box-to-Box

**Quando usar.** A assinatura, em casa e fora contra quem é do mesmo nível ou mais fraco. Segurando vitória fica nela, com os ajustes do manual (2.4): Trigger Press desce pra More Often, Tempo e Dribbling voltam ao neutro, mentality positive. Com o time cansado, rodar o elenco antes de abrir mão da tática.

**Atenção.** Custo 28, a segunda mais cara das doze (só a `vertigem` passa). O DM e o `CCB` precisam de velocidade pra cobrir quando a pressão é furada. Depende de o AMC subir pra dupla de ataque sem bola (ligação de slot a confirmar na tela).

### 2.2 `vertigem`

> *Quatro na frente e a linha no meio-campo.*

- **Forma com bola:** `4-2-4 DM Wide`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** attacking (o teto dele)
- **Linha de roles:** `BPGK/SWK, WB/PRFB, BPCB/SCB, CB/CCB, WB/PRFB, BBM/PRDM, DM/SDM, W/WM, IF/WM, CHF/CF, PO/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Sweeper Keeper | 2+2 |
| DL | Wing-Back | Pressing Full-Back | 0+2 |
| DC | Ball-Playing Centre-Back | Stopping Centre-Back | 2+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Pressing Full-Back | 0+2 |
| DM | Box-To-Box Midfielder | Pressing Defensive Midfielder | 1+2 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| AML → ML | Winger | Wide Midfielder | 0+0 |
| AMR → MR | Inside Forward | Wide Midfielder | 2+0 |
| ST | Channel Forward | Centre Forward | 1+0 |
| ST | Poacher | Centre Forward | 1+0 |

Complexidade das roles: 10 com bola, 11 sem bola.

**Com bola.** Quatro atacantes. O Poacher vive na linha do último zagueiro, o Channel Forward arrasta zagueiro pro corredor, o Winger estica a esquerda e o Inside Forward entra pela direita. Os dois Wing-Backs passam por fora; o Box-to-Box chega e o DM segura. Ritmo máximo e chute de fora.

**Sem bola.** 4-4-2 com os dois atacantes em cima dos zagueiros e a linha muito alta, prendendo o adversário no campo dele. Os pontas descem pra linha do meio; um volante salta (Pressing DM) e o outro fecha (Screening DM).

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Pass Reception: Pass Into Space (1) · Build-up Strategy: Bypass Press (0) · Tempo: Much Higher (2) · Attacking Width: Wider (1) · Dribbling: Encourage (2) · Patience: Hit Early Crosses (1) · Crossing Style: Low Crosses (1) · Supporting Runs: Overlap Both Flanks (1) · Attacking Transition: Counter-Attack (2) · GK Distribution Speed: Distribute Quickly (2) · GK Distribution Target: Flanks (1) · Shots From Distance: Encourage (1) | 16 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Much Higher (3) · Defensive Line Behaviour: Step Up More (2) · Trigger Press: Much More Often (3) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Get Stuck In (1) · Prevent Short GK Distribution: Yes (1) | 15 |
| **Total** | | **31** |

**Player instructions**

- ST (CHF): Pressing Intensity: Higher (2) — primeira linha de pressão
- ST (PO): Pressing Intensity: Higher (2) — idem
- DM (DM): Positioning: Hold Position (1) — o único que fica com quatro na frente e dois laterais subindo

**Quando usar.** Perdendo, mesmo contra time grande: a identidade manda subir a pressão, não recuar (manual 2.4). Saindo da `avalanche`, muda só a forma com bola (4-2-3-1 → 4-2-4); a forma sem bola continua `4-4-2 2DM`, como o manual pede.

**Atenção.** A mais cara das doze. Com os dois laterais subindo e a linha muito alta, o contra-ataque adversário pega a zaga sozinha.

### 2.3 `tocaia`

> *Espera o passe errado e sai em quatro segundos.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** positive
- **Linha de roles:** `GK/SWK, FB/PRFB, BPCB/SCB, CB/CCB, FB/PRFB, DM/SDM, BBM/DM, W/TWM, SS/CF, IF/TWM, PO/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Goalkeeper | Sweeper Keeper | 1+2 |
| DL | Full-Back | Pressing Full-Back | 0+2 |
| DC | Ball-Playing Centre-Back | Stopping Centre-Back | 2+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Pressing Full-Back | 0+2 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Box-To-Box Midfielder | Defensive Midfielder | 1+0 |
| AML → ML | Winger | Tracking Wide Midfielder | 0+1 |
| AMC → ST | Second Striker | Centre Forward | 1+0 |
| AMR → MR | Inside Forward | Tracking Wide Midfielder | 2+1 |
| ST | Poacher | Centre Forward | 1+0 |

Complexidade das roles: 9 com bola, 11 sem bola.

**Com bola.** Pouca posse e muito espaço. Na roubada, o Poacher já está na linha do último zagueiro e o Second Striker chega de trás; a bola sai direta e rápida pras costas. Os pontas atacam em velocidade e o Box-to-Box acompanha; os laterais ficam.

**Sem bola.** Um degrau abaixo da identidade, sem largá-la: bloco médio e linha no padrão, com pressão acima da média. O Second Striker sobe e forma a dupla da primeira linha com o Poacher, os dois pressionando os zagueiros (Pressing Intensity: Higher). É a mesma forma sem bola das outras duas, então entrar e sair dela é só troca de roles e instruções. Os pontas acompanham os laterais adversários e a armadilha manda o jogo pros lados, onde os dois laterais saltam no ponta.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Pass Reception: Pass Into Space (1) · Build-up Strategy: Bypass Press (0) · Tempo: Higher (1) · Attacking Width: Wider (1) · Dribbling: Encourage (2) · Patience: Hit Early Crosses (1) · Crossing Style: Low Crosses (1) · Attacking Transition: Counter-Attack (2) · GK Distribution Speed: Distribute Quickly (2) · GK Distribution Target: Flanks (1) | 13 |
| Sem bola | Line of Engagement: Mid Block (1) · Trigger Press: More Often (2) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Get Stuck In (1) · Prevent Short GK Distribution: Yes (1) | 8 |
| **Total** | | **21** |

**Player instructions**

- AMC (SS): Pressing Intensity: Higher (2) — primeira linha de pressão, com o PO
- ST (PO): Pressing Intensity: Higher (2) — idem

**Quando usar.** Contra time grande, principalmente fora de casa (a "emboscada" do manual 2.4). É a tática de início contra grande. Saiu na frente: vai pra `avalanche` com o ajuste de vitória (prende o adversário em vez de esperar); a forma é a mesma, só mudam roles e instruções. Saiu atrás: vai pra `vertigem` (muda só a forma com bola).


---

## 3. Rafael Duarte — Roma

Mentality entre cautious e very attacking. Três criadores em zonas diferentes; sem bola não engessa. Troca de forma livremente durante o jogo.

### 3.1 `tango`

> *Ninguém fica onde começou.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-1-1 2DM`
- **Mentality:** positive (attacking com empate travado depois dos 60' ou perdendo)
- **Linha de roles:** `BPGK/GK, WB/FB, BPCB/CB, CB/CCB, WB/FB, DLP/SDM, DM/SDM, IF/WM, AP/COAM, IW/WM, F9/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Full-Back | 0+0 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| AML → ML | Inside Forward | Wide Midfielder | 2+0 |
| AMC | Advanced Playmaker | Central Outlet Attacking Midfielder | 2+1 |
| AMR → MR | Inside Winger | Wide Midfielder | 1+0 |
| ST | False Nine | Centre Forward | 3+0 |

Complexidade das roles: 14 com bola, 5 sem bola.

**Com bola.** Três criadores em três zonas: o DLP lá atrás, o AP entre as linhas e o Falso 9, que recua e esvazia o centro pra quem chega. O Inside Forward e o Inside Winger trocam de lado o tempo todo (o carrossel), e a largura fica com os dois Wing-Backs, então nenhum lado fica vazio, troque quem trocar. Liberdade pra improvisar, bola curta e no espaço.

**Sem bola.** Bloco médio simples, poucas instruções. Os dois pontas descem iguais pra linha do meio (assim tanto faz de que lado cada um terminou o carrossel), o AP fica alto como única saída de contra-ataque e os dois volantes fecham a frente da área.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Creative Freedom: More Expressive (2) · Passing Directness: Shorter (2) · Pass Reception: Pass Into Space (1) · Tempo: Higher (1) · Attacking Width: Wider (1) · Patience: Work Ball Into Box (2) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Playmaker (1) | 13 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) | 2 |
| **Total** | | **15** |

**Player instructions**

- AML (IF): Positioning: Switch Position (0) — o carrossel: troca com o ponta da direita
- AMR (IW): Positioning: Switch Position (0) — idem

**Quando usar.** A assinatura, a base de qualquer jogo. Empate travado depois dos 60' ou perdendo cedo: fica nela, sobe pra attacking e troca Defensive Transition pra Counter-Press. Vencendo cedo: fica nela, só com Creative Freedom → Balanced; a partir da metade do 2º tempo, `milonga`. Perdendo na reta final: `incendio`. As três usam formas com bola diferentes (4-2-3-1, 4-3-3, 4-2-4), e é assim que ele troca de forma durante o jogo.

### 3.2 `milonga`

> *Ele não defende o placar: esconde a bola.*

- **Forma com bola:** `4-3-3 DM Wide`
- **Forma sem bola:** `4-1-4-1 DM`
- **Mentality:** balanced (cautious nos minutos finais)
- **Linha de roles:** `BPGK/GK, WB/FB, BPCB/CB, CB/CCB, FB/FB, DLP/SDM, AP/SCM, MP/CM, IW/TWM, W/TWM, DLF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Full-Back | 0+0 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| MC | Advanced Playmaker | Screening Central Midfielder | 2+1 |
| MC | Midfield Playmaker | Central Midfielder | 2+0 |
| AML → ML | Inside Winger | Tracking Wide Midfielder | 1+1 |
| AMR → MR | Winger | Tracking Wide Midfielder | 0+1 |
| ST | Deep-Lying Forward | Centre Forward | 2+0 |

Complexidade das roles: 13 com bola, 6 sem bola.

**Com bola.** Posse pra matar o tempo, não pra acelerar. Bola muito curta e no pé, com o DLP e os dois playmakers do meio formando triângulos e o DLF descendo pra dar mais um apoio. A largura é do Wing-Back pela esquerda (com o Inside Winger por dentro) e do Winger pela direita, onde o lateral fica. O time só ataca a área quando o espaço aparece sozinho.

**Sem bola.** 4-1-4-1 compacto: os pontas descem acompanhando os laterais, o AP fica de Screening uma linha à frente do DLP, então a área tem sempre dois na frente da zaga, e o Midfield Playmaker é o meia que sobe.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Much Shorter (3) · Pass Reception: Pass to Feet (1) · Tempo: Lower (1) · Time Wasting: More Often (?) · Patience: Work Ball Into Box (2) · Attacking Transition: Hold Shape (1) · Goal Kicks: Short (1) · GK Distribution Target: Playmaker (1) | 10+? |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) | 2 |
| **Total** | | **12+?** |

**Player instructions**

- Nenhuma.

**Quando usar.** Vencendo (manual 3.4), a partir da metade do segundo tempo. Nunca pra buscar resultado nem desde o início do jogo.

### 3.3 `incendio`

> *Tudo pra frente, e que se resolva lá.*

- **Forma com bola:** `4-2-4 DM Wide`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** very attacking
- **Linha de roles:** `BPGK/GK, WB/FB, BPCB/CB, CB/CCB, WB/FB, BBP/DM, DLP/SDM, IF/WOWM, IF/WOWM, DLF/CF, PO/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Full-Back | 0+0 |
| DM | Box-To-Box Playmaker | Defensive Midfielder | 3+0 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| AML → ML | Inside Forward | Wide Outlet Wide Midfielder | 2+1 |
| AMR → MR | Inside Forward | Wide Outlet Wide Midfielder | 2+1 |
| ST | Deep-Lying Forward | Centre Forward | 2+0 |
| ST | Poacher | Centre Forward | 1+0 |

Complexidade das roles: 16 com bola, 5 sem bola.

**Com bola.** Quatro na frente. Os dois Inside Forwards cortam pra dentro e chutam, o Poacher vive na linha do impedimento e o DLF faz a parede. Os Wing-Backs passam por fora, o Box-to-Box Playmaker chega na área e só o DLP fica. Drible, chute de fora, cruzamento cedo, passe na distância que o lance pedir.

**Sem bola.** Pressão alta e linha muito alta, com os dois pontas sem voltar (ficam abertos e altos esperando a bola). Deixa espaço atrás, e ele sabe.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Creative Freedom: More Expressive (2) · Pass Reception: Pass Into Space (1) · Tempo: Higher (1) · Attacking Width: Wider (1) · Patience: Hit Early Crosses (1) · Dribbling: Encourage (2) · Shots From Distance: Encourage (1) · Supporting Runs: Overlap Both Flanks (1) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Playmaker (1) | 14 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Much Higher (3) · Trigger Press: Much More Often (3) · Defensive Transition: Counter-Press (3) · Tackling: Get Stuck In (1) | 12 |
| **Total** | | **26** |

**Player instructions**

- ST (DLF): Pressing Intensity: Higher (2) — pressiona a saída mesmo sendo o pivô
- ST (PO): Pressing Intensity: Higher (2) — idem

**Quando usar.** Perdendo nos últimos 20 minutos (o "estouro" do manual 3.4). Só ele chega em very attacking: é a parte do personagem que às vezes se desestabiliza, então é tática de reta final, não de 90 minutos.

**Atenção.** Com os dois pontas de outlet e a linha muito alta, o contra-ataque adversário pega a zaga em dois contra dois.


---

## 4. Luiz "Casca" Ferreira — Bahia

Mentality entre defensive (só nos últimos 10) e positive. 4-4-2 com e sem bola, sempre. Muda roles, mentality e instruções; nunca a forma.

### 4.1 `muralha`

> *Duas linhas de quatro e uma bola na área.*

- **Forma com bola:** `4-4-2 2DM`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** balanced
- **Linha de roles:** `GK/GK, FB/FB, NNCB/SCB, CB/CCB, FB/HFB, DM/SDM, BBM/DM, W/TWM, WM/TWM, TF/CF, CHF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Goalkeeper | Goalkeeper | 1+1 |
| DL | Full-Back | Full-Back | 0+0 |
| DC | No-Nonsense Centre-Back | Stopping Centre-Back | 0+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Holding Full-Back | 0+1 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Box-To-Box Midfielder | Defensive Midfielder | 1+0 |
| ML | Winger | Tracking Wide Midfielder | 0+1 |
| MR | Wide Midfielder | Tracking Wide Midfielder | 0+1 |
| ST | Target Forward | Centre Forward | 1+0 |
| ST | Channel Forward | Centre Forward | 1+0 |

Complexidade das roles: 5 com bola, 7 sem bola.

**Com bola.** Direto e pelos lados. A bola longa vai no Target Forward, o Channel Forward ataca a segunda bola e o corredor. O Winger da esquerda vai à linha de fundo com o lateral apoiando; à direita o meia cruza de trás e o lateral fica. Tudo vai pro alto, pro centroavante e pros zagueiros na bola parada. O Box-to-Box chega na área; o DM fica.

**Sem bola.** 4-4-2 compacto e paciente: pressiona pouco, não dá carrinho, impede o cruzamento. O DM fecha a frente da zaga (o buraco entre as linhas), um zagueiro sai no atacante e o outro cobre.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Build-up Strategy: Bypass Press (0) · Attacking Width: Wider (1) · Progress Through: Both Flanks (1) · Crossing Style: Floated Crosses (1) · Set Pieces: Play for Set Pieces (1) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Long (1) · GK Distribution Target: Target Forward (1) | 12 |
| Sem bola | Line of Engagement: Mid Block (1) · Trigger Press: Less Often (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) · Cross Engagement: Stop Crosses (1) | 5 |
| **Total** | | **17** |

**Player instructions**

- ML (W): Cross To: Target Man (2) — tudo na cabeça do TF
- MR (WM): Cross To: Target Man (2) — idem
- MR (WM): Cross From: Deep (1) — o lateral direito não passa, então ele cruza de trás
- DR (FB): Positioning: Hold Position (1) — o lateral direito fica; quem apoia é o esquerdo
- ST (TF): Dribbling: Hold Up Ball (1) — segura a bola longa pros meias chegarem

**Quando usar.** O padrão, em qualquer campo e contra qualquer adversário, com o XI estável que ele gosta. Se o adversário achar o espaço entre as linhas, aplicar a seção 4.4 do manual (linha Higher, Trap Outside, ST2 sem bola `TCF`).

### 4.2 `trator`

> *Mesmo 4-4-2, mais gente na área.*

- **Forma com bola:** `4-4-2 2DM`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** positive (o teto dele)
- **Linha de roles:** `GK/GK, WB/FB, NNCB/SCB, CB/CCB, WB/FB, DM/SDM, BBM/DM, W/WOWM, W/TWM, TF/CF, PO/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Goalkeeper | Goalkeeper | 1+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | No-Nonsense Centre-Back | Stopping Centre-Back | 0+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Full-Back | 0+0 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Box-To-Box Midfielder | Defensive Midfielder | 1+0 |
| ML | Winger | Wide Outlet Wide Midfielder | 0+1 |
| MR | Winger | Tracking Wide Midfielder | 0+1 |
| ST | Target Forward | Centre Forward | 1+0 |
| ST | Poacher | Centre Forward | 1+0 |

Complexidade das roles: 5 com bola, 6 sem bola.

**Com bola.** A `muralha` empurrada pra frente, na mesma forma. Os laterais viram Wing-Backs e dobram com os pontas, que cruzam cedo; o Poacher fica na linha do impedimento esperando a sobra do Target Forward. O Box-to-Box chega na área; o DM continua atrás.

**Sem bola.** Continua 4-4-2 e continua compacto. A linha sobe pra comprimir o campo e o time pressiona no padrão, não menos. O ponta esquerdo fica alto pra receber o contra-ataque, e o DM segue de Screening pra não abrir o buraco entre as linhas.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Build-up Strategy: Bypass Press (0) · Attacking Width: Much Wider (2) · Progress Through: Both Flanks (1) · Crossing Style: Floated Crosses (1) · Set Pieces: Play for Set Pieces (1) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Long (1) · GK Distribution Target: Target Forward (1) · Tempo: Higher (1) · Patience: Hit Early Crosses (1) · Supporting Runs: Overlap Both Flanks (1) · Shots From Distance: Encourage (1) | 17 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Line: Higher (2) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Stay on Feet (1) · Cross Engagement: Stop Crosses (1) | 8 |
| **Total** | | **25** |

**Player instructions**

- ML (W): Cross To: Target Man (2) — na cabeça do TF
- MR (W): Cross To: Target Man (2) — idem
- ST (TF): Dribbling: Hold Up Ball (1) — segura pros Wing-Backs chegarem

**Quando usar.** Perdendo ou empatando quando precisa ganhar. Sai da `muralha` só com troca de roles e instruções; a forma e a dupla de volantes não mudam. A mentality fica em positive: attacking ele nunca usa.

**Atenção.** Com o ponta esquerdo alto (Wide Outlet) e o lateral subindo, a transição defensiva pela esquerda fica com o lateral sozinho contra dois. É o risco aceito pra perseguir o placar. Custo 25: é a mais cara do Casca, mas só fica em campo enquanto ele precisa do gol.

### 4.3 `cadeado`

> *Fecha a porta e joga a chave pra frente.*

- **Forma com bola:** `4-4-2 2DM`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** cautious (defensive nos últimos 10)
- **Linha de roles:** `NNGK/LHGK, FB/HFB, NNCB/SCB, CB/CCB, FB/HFB, DM/SDM, DM/SDM, WM/TWM, WM/TWM, TF/COCF, DLF/TCF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | No-Nonsense Goalkeeper | Line-Holding Goalkeeper | 0+0 |
| DL | Full-Back | Holding Full-Back | 0+1 |
| DC | No-Nonsense Centre-Back | Stopping Centre-Back | 0+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Holding Full-Back | 0+1 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| ML | Wide Midfielder | Tracking Wide Midfielder | 0+1 |
| MR | Wide Midfielder | Tracking Wide Midfielder | 0+1 |
| ST | Target Forward | Central Outlet Centre Forward | 1+1 |
| ST | Deep-Lying Forward | Tracking Centre Forward | 2+1 |

Complexidade das roles: 4 com bola, 10 sem bola.

**Com bola.** Sem pressa e sem risco. Bola longa no Target Forward, que segura enquanto o time sobe junto; o DLF recua pra dar apoio e prender a bola no campo de ataque. Ninguém se arrisca pela lateral: os laterais ficam.

**Sem bola.** Bloco baixo inteiro, não só a linha: duas linhas de quatro baixas e juntas, com os dois volantes de Screening tapando o meio. O DLF volta acompanhando o volante adversário, o TF fica lá na frente pra aliviar, e a defesa recua em vez de sair, contra cruzamento e bola nas costas.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Build-up Strategy: Bypass Press (0) · Attacking Width: Narrower (1) · Progress Through: Both Flanks (1) · Tempo: Lower (1) · Time Wasting: More Often (?) · Crossing Style: Floated Crosses (1) · Set Pieces: Play for Set Pieces (1) · Creative Freedom: More Disciplined (3) · Attacking Transition: Hold Shape (1) · Goal Kicks: Long (1) · GK Distribution Speed: Slow Pace Down (1) · GK Distribution Target: Target Forward (1) | 13+? |
| Sem bola | Line of Engagement: Low Block (0) · Defensive Line: Lower (1) · Defensive Line Behaviour: Drop Off More (1) · Trigger Press: Less Often (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) · Cross Engagement: Stop Crosses (1) | 6 |
| **Total** | | **19+?** |

**Player instructions**

- ST (TF): Dribbling: Hold Up Ball (1) — segura a bola longe do gol
- DL (FB): Positioning: Hold Position (1) — lateral não passa do meio-campo
- DR (FB): Positioning: Hold Position (1) — idem

**Quando usar.** Segurando vantagem a partir dos 70'. Cautious até os 80'; defensive nos últimos 10. O `TCF` e os dois Screening já são parte do remédio da seção 4.4 do manual. O bloco desce inteiro (Low Block + linha Lower), então as linhas não se separam. Se mesmo assim o adversário achar o espaço entre as linhas, aplicar o resto da 4.4: acrescentar Pressing Trap: Trap Outside e, só se não resolver, subir a linha até Standard (Defensive Line Behaviour: Balanced). Nunca Higher: com goleiro de linha (`LHGK`) e zagueiro No-Nonsense, linha alta é bola nas costas.

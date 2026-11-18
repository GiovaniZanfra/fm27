# Táticas FM27 — três por técnico

Doze táticas (três por técnico), montadas dentro das regras de `managers_tactics.md` e da identidade de `managers.md`. Roles, posições e custos conferidos contra `game_data/roles.json`, `game_data/instructions_ui.json` e `game_data/instructions.json`.

**Status:** propostas, ainda sem jogo no save. Viram config (`configs/<time>/<nome>.json`) quando aprovadas.

## Como ler

- **Slot `AML → ML`**: o jogador ocupa AML na forma com bola e ML na forma sem bola. A role sem bola tem que valer para o slot **sem bola**. A ligação entre os slots das duas formas é suposição nossa (o ponta desce pra linha do meio, o meia da AMC sobe pra dupla de ataque quando a forma sem bola tem dois atacantes); confirmar na tela.
- **Linha de roles**: `IP/OOP` em ordem posicional, no formato da coluna `Roles` da planilha.
- **Cx**: complexidade da role com bola + da role sem bola.
- **Team instructions**: só as escolhidas; tudo o que não aparece fica na opção neutra (Standard / Balanced / Mixed / No / Keep Ball in Play). Custo entre parênteses; `?` = Time Wasting, cujo custo não está confirmado.
- **Player instructions**: role com bola + instruções do jogador nunca passam de 4.


---

## 1. Giovani — Sporting

Mentality entre cautious e attacking. Roles antes da forma; duas camadas de proteção no meio sem bola; três atrás da bola na saída.

### 1.1 `relógio`

> *Tudo no lugar, tudo no tempo certo.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-1-1 2DM`
- **Mentality:** balanced
- **Linha de roles:** `BPGK/GK, IFB/FB, BPCB/CB, CB/CCB, WB/HFB, DLP/SDM, DM/DM, IW/TWM, AP/TAM, W/TWM, DLF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Inside Full-Back | Full-Back | 1+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Holding Full-Back | 0+1 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| DM | Defensive Midfielder | Defensive Midfielder | 0+0 |
| AML → ML | Inside Winger | Tracking Wide Midfielder | 1+1 |
| AMC | Advanced Playmaker | Tracking Attacking Midfielder | 2+1 |
| AMR → MR | Winger | Tracking Wide Midfielder | 0+1 |
| ST | Deep-Lying Forward | Centre Forward | 2+0 |

Complexidade das roles: 12 com bola, 7 sem bola.

**Com bola.** O lateral esquerdo fecha por dentro e forma linha de três com os zagueiros; o DLP organiza na frente deles e o DM fica parado de proteção. A bola anda curta e no pé até alguém achar o espaço entre as linhas: o AP, o Inside Winger que entra pela esquerda ou o DLF que recua. A largura vem só pela direita, com o Winger aberto e o Wing-Back passando por fora.

**Sem bola.** Bloco médio em 4-4-1-1. Os pontas descem pra linha do meio acompanhando os laterais adversários, o AP marca o volante deles e os dois DM fecham a entrada da área. Ninguém sai da posição pra caçar a bola: o time espera o erro e intercepta.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Shorter (2) · Pass Reception: Pass to Feet (1) · Patience: Work Ball Into Box (2) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Centre-Backs (1) | 12 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) | 3 |
| **Total** | | **15** |

**Player instructions**

- DM (DLP): Positioning: Hold Position (1) — o DLP não sobe, fica de base da saída
- AMR (W): Attacking Width: Stay Wider (1) — é a única largura do lado direito

**Quando usar.** É o padrão: em casa ou fora, contra adversário do mesmo nível ou mais fraco. É de onde todo jogo começa e pra onde ele volta quando quer controlar o placar. Segurando vitória, fica nela e aplica os ajustes da seção 1.4 do manual.

### 1.2 `xadrez`

> *Mais gente no meio, menos jogo pro adversário.*

- **Forma com bola:** `4-4-2 Diamond Narrow`
- **Forma sem bola:** `4-4-2 Diamond Narrow`
- **Mentality:** balanced
- **Linha de roles:** `BPGK/GK, WB/FB, BPCB/CB, CB/CCB, WB/FB, HB/SDM, CM/SCM, WCM/WCCM, AP/TAM, DLF/TCF, CHF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Full-Back | 0+0 |
| DM | Half Back | Screening Defensive Midfielder | 2+1 |
| MC | Central Midfielder | Screening Central Midfielder | 0+1 |
| MC | Wide Central Midfielder | Wide Covering Central Midfielder | 1+2 |
| AMC | Advanced Playmaker | Tracking Attacking Midfielder | 2+1 |
| ST | Deep-Lying Forward | Tracking Centre Forward | 2+1 |
| ST | Channel Forward | Centre Forward | 1+0 |

Complexidade das roles: 13 com bola, 8 sem bola.

**Com bola.** O Half Back desce entre os zagueiros e libera os dois Wing-Backs, que dão toda a largura. No meio, o CM segura e o Wide Central Midfielder abre pro corredor do lado mais fraco. O AP flutua atrás da dupla: o DLF vem buscar e o Channel Forward ataca o espaço que ele deixa.

**Sem bola.** O losango se mantém. A armadilha de pressão empurra o adversário pro meio, onde o Giovani tem um jogador a mais; o DLF acompanha o volante adversário e o AP fecha o outro.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Shorter (2) · Pass Reception: Pass to Feet (1) · Patience: Work Ball Into Box (2) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Centre-Backs (1) · Supporting Runs: Overlap Both Flanks (1) | 13 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) · Pressing Trap: Trap Inside (0) | 3 |
| **Total** | | **16** |

**Player instructions**

- DL (WB): Cross From: Deep (1) — cruza antes de chegar à linha de fundo, sem esvaziar a lateral
- DR (WB): Cross From: Deep (1) — idem

**Quando usar.** Contra time com um volante só ou 4-4-2 reto, e em jogos em casa onde ele precisa ter a bola. Evitar contra dois pontas rápidos: os Wing-Backs ficam expostos (primeira correção: um lateral vira `WB/HFB`).

### 1.3 `engrenagem`

> *A mesma máquina, girando mais rápido.*

- **Forma com bola:** `4-3-3 DM Wide`
- **Forma sem bola:** `4-1-4-1 DM`
- **Mentality:** positive (attacking a partir dos 75', perdendo)
- **Linha de roles:** `BPGK/SWK, IFB/FB, BPCB/CB, CB/CCB, FB/PRFB, DM/SDM, CM/PRCM, MP/SCM, W/TWM, IF/TWM, CF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Sweeper Keeper | 2+2 |
| DL | Inside Full-Back | Full-Back | 1+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Pressing Full-Back | 0+2 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| MC | Central Midfielder | Pressing Central Midfielder | 0+2 |
| MC | Midfield Playmaker | Screening Central Midfielder | 2+1 |
| AML → ML | Winger | Tracking Wide Midfielder | 0+1 |
| AMR → MR | Inside Forward | Tracking Wide Midfielder | 2+1 |
| ST | Centre Forward | Centre Forward | 0+0 |

Complexidade das roles: 10 com bola, 11 sem bola.

**Com bola.** 4-3-3 mais largo e mais rápido. O lateral esquerdo fecha por dentro pra matar o contra-ataque antes de nascer, o Winger dá a largura desse lado e, na direita, o Inside Forward corta pra dentro com o Full-Back passando. O Midfield Playmaker segue como referência do passe; o ritmo sobe, a disciplina continua.

**Sem bola.** Pressão alta e linha alta, com o goleiro de Sweeper Keeper cobrindo as costas. Na dupla do meio um salta (Pressing CM) e o outro segura (Screening CM): nunca os dois. O lateral direito pressiona o ponta adversário e o centroavante pressiona por instrução individual.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Shorter (2) · Pass Reception: Pass to Feet (1) · Patience: Work Ball Into Box (2) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Centre-Backs (1) · Tempo: Higher (1) · Attacking Width: Wider (1) | 14 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Higher (2) · Trigger Press: More Often (2) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Stay on Feet (1) · Prevent Short GK Distribution: Yes (1) | 11 |
| **Total** | | **25** |

**Player instructions**

- ST (CF): Pressing Intensity: Higher (2) — faz o papel do antigo Pressing Forward
- AML (W): Cross To: Centre (1) — cruzamento na área, não na segunda trave

**Quando usar.** Empate travado ou placar contra, depois que os ajustes de role no `relógio` não resolveram (a forma é a última coisa que muda). Também contra time fraco que se fecha atrás. A partir dos 75', perdendo: mentality attacking, Shots From Distance: Encourage e o MP vira AP com bola.

**Atenção.** É a mais cara de aprender das três, e a linha alta expõe zagueiro lento: o `CCB` precisa de velocidade.


---

## 2. Bruno Keller — Internacional

Mentality entre positive e attacking. Pressão alta, linha alta, dois na primeira linha de pressão. Protege vantagem prendendo o adversário, não sentando.

### 2.1 `avalanche`

> *Ganhou, atacou. Perdeu, roubou de volta.*

- **Forma com bola:** `4-3-3 DM Wide`
- **Forma sem bola:** `4-3-3 DM Wide`
- **Mentality:** attacking
- **Linha de roles:** `BPGK/SWK, WB/PRFB, BPCB/SCB, CB/CCB, WB/PRFB, DM/SDM, CHM/PRCM, CM/PRCM, W/W, IF/W, CHF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Sweeper Keeper | 2+2 |
| DL | Wing-Back | Pressing Full-Back | 0+2 |
| DC | Ball-Playing Centre-Back | Stopping Centre-Back | 2+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Pressing Full-Back | 0+2 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| MC | Channel Midfielder | Pressing Central Midfielder | 1+2 |
| MC | Central Midfielder | Pressing Central Midfielder | 0+2 |
| AML | Winger | Winger | 0+0 |
| AMR | Inside Forward | Winger | 2+0 |
| ST | Channel Forward | Centre Forward | 1+0 |

Complexidade das roles: 9 com bola, 13 sem bola.

**Com bola.** Vertical e largo. Bola roubada vai pra frente rápido, nas costas da defesa: o Channel Forward ataca o corredor, o Winger estica pela esquerda e o Inside Forward pisa na área pela direita. Os dois Wing-Backs passam por fora e o Channel Midfielder chega no corredor; o DM fica como único pivô.

**Sem bola.** 4-3-3 de pressão no campo todo. Os três da frente fecham a saída curta, os dois meias saltam nos volantes e os laterais pressionam os pontas. Um zagueiro salta no atacante, o outro (o mais rápido) cobre, e o goleiro varre atrás da linha alta.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Pass Reception: Pass Into Space (1) · Build-up Strategy: Bypass Press (0) · Tempo: Higher (1) · Attacking Width: Wider (1) · Dribbling: Encourage (2) · Patience: Hit Early Crosses (1) · Crossing Style: Low Crosses (1) · Supporting Runs: Overlap Both Flanks (1) · Attacking Transition: Counter-Attack (2) · GK Distribution Speed: Distribute Quickly (2) · GK Distribution Target: Flanks (1) | 14 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Higher (2) · Defensive Line Behaviour: Step Up More (2) · Trigger Press: Much More Often (3) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Get Stuck In (1) · Prevent Short GK Distribution: Yes (1) | 14 |
| **Total** | | **28** |

**Player instructions**

- ST (CHF): Pressing Intensity: Higher (2) — primeira linha de pressão
- DM (DM): Positioning: Hold Position (1) — único pivô: não sobe com os meias

**Quando usar.** A assinatura. Em casa, e fora contra quem é do mesmo nível ou mais fraco. Exige elenco descansado: com o time cansado (sequência de jogos), rodar antes de abrir mão da tática.

**Atenção.** A mais cara das doze. Os dois laterais sobem juntos: o DM e o `CCB` precisam de velocidade pra cobrir.

### 2.2 `vertigem`

> *Dois na frente, sempre em cima da saída deles.*

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

**Com bola.** 4-2-3-1 com o Second Striker como segundo atacante de fato: chega na área enquanto o Channel Forward arrasta zagueiro pro corredor. O Box-to-Box sobe pra dar número, o DM segura. Largura do Winger pela esquerda e do Wing-Back pela direita, com o Inside Forward por dentro.

**Sem bola.** O Second Striker sobe e forma dupla com o centroavante: 4-4-2 com dois em cima dos zagueiros adversários. Os pontas descem pra linha de quatro do meio; um volante salta (Pressing DM), o outro fecha (Screening DM).

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Pass Reception: Pass Into Space (1) · Build-up Strategy: Bypass Press (0) · Tempo: Higher (1) · Dribbling: Encourage (2) · Patience: Hit Early Crosses (1) · Crossing Style: Low Crosses (1) · Supporting Runs: Overlap Both Flanks (1) · Attacking Transition: Counter-Attack (2) · GK Distribution Speed: Distribute Quickly (2) · GK Distribution Target: Flanks (1) | 13 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Higher (2) · Defensive Line Behaviour: Step Up More (2) · Trigger Press: Much More Often (3) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Get Stuck In (1) · Prevent Short GK Distribution: Yes (1) | 14 |
| **Total** | | **27** |

**Player instructions**

- AMC (SS): Pressing Intensity: Higher (2) — é o segundo atacante na pressão
- ST (CHF): Pressing Intensity: Higher (2) — primeira linha de pressão

**Quando usar.** Contra times que saem jogando pelos zagueiros (dois atacantes em cima deles) e quando o adversário tem um volante só. É também a casa do Keller segurando vitória: Trigger Press baixa pra More Often, Tempo e Dribbling voltam ao neutro e a mentality desce pra positive.

### 2.3 `tocaia`

> *Espera o passe errado e sai em quatro segundos.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-1-1 2DM`
- **Mentality:** positive
- **Linha de roles:** `GK/SWK, FB/PRFB, BPCB/SCB, CB/CCB, WB/FB, DM/SDM, BBM/PRDM, W/TWM, SS/SOAM, IF/TWM, PO/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Goalkeeper | Sweeper Keeper | 1+2 |
| DL | Full-Back | Pressing Full-Back | 0+2 |
| DC | Ball-Playing Centre-Back | Stopping Centre-Back | 2+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Full-Back | 0+0 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Box-To-Box Midfielder | Pressing Defensive Midfielder | 1+2 |
| AML → ML | Winger | Tracking Wide Midfielder | 0+1 |
| AMC | Second Striker | Splitting Outlet Attacking Midfielder | 1+2 |
| AMR → MR | Inside Forward | Tracking Wide Midfielder | 2+1 |
| ST | Poacher | Centre Forward | 1+0 |

Complexidade das roles: 9 com bola, 13 sem bola.

**Com bola.** Pouca posse e muito espaço. Na roubada, o Poacher já está na linha do último zagueiro e o Second Striker parte do buraco entre zagueiro e lateral; a bola sai direta e rápida pras costas. Os pontas atacam em velocidade, e só o Wing-Back da direita se junta.

**Sem bola.** Um degrau abaixo da identidade, sem largá-la: bloco médio, linha no padrão e pressão ainda acima da média. Os pontas acompanham os laterais adversários, o Second Striker fica entre zagueiro e lateral esperando o contra-ataque, e a armadilha manda o jogo pros lados, onde dá pra roubar com o lateral saltando.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Pass Reception: Pass Into Space (1) · Build-up Strategy: Bypass Press (0) · Tempo: Higher (1) · Dribbling: Encourage (2) · Patience: Hit Early Crosses (1) · Crossing Style: Low Crosses (1) · Attacking Transition: Counter-Attack (2) · GK Distribution Speed: Distribute Quickly (2) · GK Distribution Target: Flanks (1) | 12 |
| Sem bola | Line of Engagement: Mid Block (1) · Trigger Press: More Often (2) · Defensive Transition: Counter-Press (3) · Pressing Trap: Trap Outside (0) · Tackling: Get Stuck In (1) | 7 |
| **Total** | | **19** |

**Player instructions**

- Nenhuma.

**Quando usar.** Contra time grande, principalmente fora de casa. Se sair na frente, continua nela; se sair atrás, volta pra `avalanche` (Keller sobe a pressão perdendo, mesmo contra grande).


---

## 3. Rafael Duarte — River Plate

Mentality entre cautious e very attacking. Três criadores em zonas diferentes; sem bola não engessa. Troca de forma livremente durante o jogo.

### 3.1 `tango`

> *Ninguém fica onde começou.*

- **Forma com bola:** `4-2-3-1 DM AM Wide`
- **Forma sem bola:** `4-4-1-1 2DM`
- **Mentality:** positive
- **Linha de roles:** `BPGK/GK, WB/FB, BPCB/CB, CB/CCB, IWB/FB, DLP/SDM, DM/SDM, IF/WOWM, AP/COAM, IW/WM, F9/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Inside Wing-Back | Full-Back | 2+0 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| AML → ML | Inside Forward | Wide Outlet Wide Midfielder | 2+1 |
| AMC | Advanced Playmaker | Central Outlet Attacking Midfielder | 2+1 |
| AMR → MR | Inside Winger | Wide Midfielder | 1+0 |
| ST | False Nine | Centre Forward | 3+0 |

Complexidade das roles: 16 com bola, 6 sem bola.

**Com bola.** Três criadores em três zonas: o DLP lá atrás, o AP entre as linhas e o Falso 9, que recua e esvazia o centro pra quem chega de trás. O Inside Forward e o Inside Winger trocam de lado o tempo todo; o lateral direito entra no meio e o esquerdo dá a largura. Liberdade pra improvisar, bola curta e no espaço.

**Sem bola.** Bloco médio simples, poucas instruções. O AP fica alto como saída de contra-ataque, o ponta esquerdo também fica alto e aberto, e os dois volantes fecham a frente da área.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Creative Freedom: More Expressive (2) · Passing Directness: Shorter (2) · Pass Reception: Pass Into Space (1) · Tempo: Higher (1) · Attacking Width: Wider (1) · Patience: Work Ball Into Box (2) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Playmaker (1) | 13 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) | 2 |
| **Total** | | **15** |

**Player instructions**

- AML (IF): Positioning: Switch Position (0) — o carrossel: troca com o ponta da direita
- AMR (IW): Positioning: Switch Position (0) — idem
- AMC (AP): Positioning: Roam From Position (2) — procura o espaço onde ele aparecer

**Quando usar.** A assinatura, a base de qualquer jogo. Empate ou perdendo cedo: fica nela, sobe pra attacking e troca Defensive Transition pra Counter-Press.

### 3.2 `milonga`

> *Ele não defende o placar: esconde a bola.*

- **Forma com bola:** `4-3-3 DM Wide`
- **Forma sem bola:** `4-1-4-1 DM`
- **Mentality:** balanced (cautious nos minutos finais)
- **Linha de roles:** `BPGK/GK, WB/FB, BPCB/CB, CB/CCB, WB/FB, DLP/SDM, CHM/CM, MP/CM, IW/TWM, PW/TWM, DLF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Ball-Playing Goalkeeper | Goalkeeper | 2+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | Ball-Playing Centre-Back | Centre-Back | 2+0 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Full-Back | 0+0 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| MC | Channel Midfielder | Central Midfielder | 1+0 |
| MC | Midfield Playmaker | Central Midfielder | 2+0 |
| AML → ML | Inside Winger | Tracking Wide Midfielder | 1+1 |
| AMR → MR | Playmaking Winger | Tracking Wide Midfielder | 2+1 |
| ST | Deep-Lying Forward | Centre Forward | 2+0 |

Complexidade das roles: 14 com bola, 5 sem bola.

**Com bola.** Posse pra matar o tempo, não pra acelerar. Bola muito curta e no pé, com o DLP, o Midfield Playmaker e o Playmaking Winger formando triângulos; o DLF desce pra dar mais um apoio. O time só ataca a área quando o espaço aparece sozinho.

**Sem bola.** 4-1-4-1 compacto: os pontas descem acompanhando os laterais, os dois meias ficam na frente do DLP e a área tem sempre dois na frente da zaga.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: Much Shorter (3) · Pass Reception: Pass to Feet (1) · Tempo: Lower (1) · Time Wasting: More Often (?) · Patience: Work Ball Into Box (2) · Attacking Transition: Hold Shape (1) · Goal Kicks: Short (1) · GK Distribution Target: Playmaker (1) | 10+? |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Transition: Regroup (1) | 2 |
| **Total** | | **12+?** |

**Player instructions**

- Nenhuma.

**Quando usar.** Vencendo, a partir da metade do segundo tempo. Também fora de casa contra time que pressiona alto, pra tirar o ritmo do jogo. Nunca pra buscar resultado.

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

**Com bola.** Quatro na frente. Os dois Inside Forwards cortam pra dentro e chutam, o Poacher vive na linha do impedimento e o DLF faz a parede. Os Wing-Backs passam por fora, o Box-to-Box Playmaker chega na área e só o DLP fica. Drible, chute de fora, cruzamento cedo.

**Sem bola.** Pressão alta e linha muito alta, com os dois pontas sem voltar (ficam abertos e altos esperando a bola). Deixa espaço atrás, e ele sabe.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Creative Freedom: More Expressive (2) · Passing Directness: Shorter (2) · Pass Reception: Pass Into Space (1) · Tempo: Higher (1) · Attacking Width: Wider (1) · Patience: Hit Early Crosses (1) · Dribbling: Encourage (2) · Shots From Distance: Encourage (1) · Supporting Runs: Overlap Both Flanks (1) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Short (1) · GK Distribution Target: Playmaker (1) | 16 |
| Sem bola | Line of Engagement: High Press (2) · Defensive Line: Much Higher (3) · Trigger Press: Much More Often (3) · Defensive Transition: Counter-Press (3) · Tackling: Get Stuck In (1) | 12 |
| **Total** | | **28** |

**Player instructions**

- ST (DLF): Pressing Intensity: Higher (2) — pressiona a saída mesmo sendo o pivô
- ST (PO): Pressing Intensity: Higher (2) — idem

**Quando usar.** Perdendo nos últimos 20 minutos. Só ele chega em very attacking: é a parte do personagem que às vezes se desestabiliza, então é tática de reta final, não de 90 minutos.

**Atenção.** Com os dois pontas de outlet e a linha muito alta, o contra-ataque adversário pega a zaga em dois contra dois.


---

## 4. Luiz "Casca" Ferreira — Watford

Mentality entre defensive (só nos últimos 10) e positive. 4-4-2 com e sem bola, sempre. Muda roles, mentality e instruções; nunca a forma.

### 4.1 `muralha`

> *Duas linhas de quatro e uma bola na área.*

- **Forma com bola:** `4-4-2 2DM`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** balanced
- **Linha de roles:** `GK/GK, FB/HFB, NNCB/SCB, CB/CCB, FB/FB, DM/SDM, BBM/DM, W/TWM, WM/TWM, TF/CF, CHF/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Goalkeeper | Goalkeeper | 1+1 |
| DL | Full-Back | Holding Full-Back | 0+1 |
| DC | No-Nonsense Centre-Back | Stopping Centre-Back | 0+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Full-Back | 0+0 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Box-To-Box Midfielder | Defensive Midfielder | 1+0 |
| ML | Winger | Tracking Wide Midfielder | 0+1 |
| MR | Wide Midfielder | Tracking Wide Midfielder | 0+1 |
| ST | Target Forward | Centre Forward | 1+0 |
| ST | Channel Forward | Centre Forward | 1+0 |

Complexidade das roles: 5 com bola, 7 sem bola.

**Com bola.** Direto e pelos lados. A bola longa vai no Target Forward, o Channel Forward ataca a segunda bola e o corredor. O Winger da esquerda vai à linha de fundo, o meia da direita cruza de trás, e tudo vai pro alto, pro centroavante e pros zagueiros na bola parada. O Box-to-Box chega na área; o DM fica.

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
- MR (WM): Cross From: Deep (1) — o lateral não passa, então ele cruza de trás
- ST (TF): Dribbling: Hold Up Ball (1) — segura a bola longa pros meias chegarem

**Quando usar.** O padrão, em qualquer campo e contra qualquer adversário. Segura o time no XI estável que ele gosta.

### 4.2 `trator`

> *Mesmo 4-4-2, mais gente na área.*

- **Forma com bola:** `4-4-2`
- **Forma sem bola:** `4-4-2`
- **Mentality:** positive (o teto dele)
- **Linha de roles:** `GK/GK, WB/FB, NNCB/SCB, CB/CCB, WB/FB, W/WOWM, CM/SCM, WCM/CM, W/TWM, TF/CF, PO/CF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | Goalkeeper | Goalkeeper | 1+1 |
| DL | Wing-Back | Full-Back | 0+0 |
| DC | No-Nonsense Centre-Back | Stopping Centre-Back | 0+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Wing-Back | Full-Back | 0+0 |
| ML | Winger | Wide Outlet Wide Midfielder | 0+1 |
| MC | Central Midfielder | Screening Central Midfielder | 0+1 |
| MC | Wide Central Midfielder | Central Midfielder | 1+0 |
| MR | Winger | Tracking Wide Midfielder | 0+1 |
| ST | Target Forward | Centre Forward | 1+0 |
| ST | Poacher | Centre Forward | 1+0 |

Complexidade das roles: 5 com bola, 6 sem bola.

**Com bola.** O 4-4-2 reto empurrado pra frente. Os laterais viram Wing-Backs e dobram com os pontas, que cruzam cedo e de primeira; o Poacher fica na linha do impedimento esperando a sobra do Target Forward. Um meia abre pro corredor pra dar mais um cruzamento.

**Sem bola.** Continua 4-4-2 e continua compacto. A linha sobe pra comprimir o campo e o time pressiona no padrão, não menos. O ponta esquerdo fica alto pra receber o contra-ataque, e um dos meias continua de Screening pra não abrir o buraco entre as linhas.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Build-up Strategy: Bypass Press (0) · Attacking Width: Much Wider (2) · Tempo: Higher (1) · Progress Through: Both Flanks (1) · Crossing Style: Floated Crosses (1) · Patience: Hit Early Crosses (1) · Supporting Runs: Overlap Both Flanks (1) · Shots From Distance: Encourage (1) · Set Pieces: Play for Set Pieces (1) · Creative Freedom: More Disciplined (3) · Attacking Transition: Counter-Attack (2) · Goal Kicks: Long (1) · GK Distribution Target: Target Forward (1) | 17 |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Line: Higher (2) · Defensive Transition: Counter-Press (3) · Tackling: Stay on Feet (1) · Cross Engagement: Stop Crosses (1) | 8 |
| **Total** | | **25** |

**Player instructions**

- ML (W): Cross To: Target Man (2) — na cabeça do TF
- MR (W): Cross To: Target Man (2) — idem
- ST (TF): Dribbling: Hold Up Ball (1) — segura pra os Wing-Backs chegarem

**Quando usar.** Perdendo ou empatando quando precisa ganhar. Entra trocando roles e instruções da `muralha`, sem tirar o 4-4-2. A mentality fica em positive: attacking ele nunca usa.

**Atenção.** Usa o 4-4-2 reto (dupla no MC). Se o jogo só oferecer o `4-4-2 2DM`, usar a mesma ideia com `BBM/DM` + `DM/SDM` na dupla.

### 4.3 `cadeado`

> *Fecha a porta e joga a chave pra frente.*

- **Forma com bola:** `4-4-2 2DM`
- **Forma sem bola:** `4-4-2 2DM`
- **Mentality:** cautious (defensive nos últimos 10)
- **Linha de roles:** `NNGK/LHGK, FB/HFB, NNCB/SCB, CB/CCB, FB/HFB, DM/SDM, DLP/SDM, WM/TWM, WM/TWM, TF/COCF, DLF/TCF`

| Slot | Com bola | Sem bola | Cx |
|---|---|---|---|
| GK | No-Nonsense Goalkeeper | Line-Holding Goalkeeper | 0+0 |
| DL | Full-Back | Holding Full-Back | 0+1 |
| DC | No-Nonsense Centre-Back | Stopping Centre-Back | 0+1 |
| DC | Centre-Back | Covering Centre-Back | 1+1 |
| DR | Full-Back | Holding Full-Back | 0+1 |
| DM | Defensive Midfielder | Screening Defensive Midfielder | 0+1 |
| DM | Deep-Lying Playmaker | Screening Defensive Midfielder | 1+1 |
| ML | Wide Midfielder | Tracking Wide Midfielder | 0+1 |
| MR | Wide Midfielder | Tracking Wide Midfielder | 0+1 |
| ST | Target Forward | Central Outlet Centre Forward | 1+1 |
| ST | Deep-Lying Forward | Tracking Centre Forward | 2+1 |

Complexidade das roles: 5 com bola, 10 sem bola.

**Com bola.** Sem pressa e sem risco. Bola longa no Target Forward, que segura enquanto o time sobe junto; o DLF recua pra dar apoio e prender a bola no campo de ataque. Ninguém se arrisca pela lateral: os laterais ficam.

**Sem bola.** Duas linhas de quatro baixas e juntas, com os dois volantes de Screening tapando o meio. O DLF volta acompanhando o volante adversário, o TF fica lá na frente pra aliviar, e a defesa recua em vez de sair, contra cruzamento e bola nas costas.

**Team instructions**

| Fase | Instruções | Custo |
|---|---|---|
| Com bola | Passing Directness: More Direct (1) · Build-up Strategy: Bypass Press (0) · Attacking Width: Narrower (1) · Tempo: Lower (1) · Time Wasting: More Often (?) · Crossing Style: Floated Crosses (1) · Set Pieces: Play for Set Pieces (1) · Creative Freedom: More Disciplined (3) · Attacking Transition: Hold Shape (1) · Goal Kicks: Long (1) · GK Distribution Speed: Slow Pace Down (1) · GK Distribution Target: Target Forward (1) | 12+? |
| Sem bola | Line of Engagement: Mid Block (1) · Defensive Line: Lower (1) · Defensive Line Behaviour: Drop Off More (1) · Trigger Press: Less Often (1) · Defensive Transition: Regroup (1) · Tackling: Stay on Feet (1) · Cross Engagement: Stop Crosses (1) | 7 |
| **Total** | | **19+?** |

**Player instructions**

- ST (TF): Dribbling: Hold Up Ball (1) — segura a bola longe do gol

**Quando usar.** Segurando vantagem a partir dos 70'. Cautious até os 80'; defensive nos últimos 10. Se o adversário começar a achar o espaço entre as linhas, aplicar a seção 4.4 do manual antes de baixar mais.

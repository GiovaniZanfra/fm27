# Manual dos Quatro Técnicos — FM27

Como cada técnico joga, escrito nas mecânicas do FM27: forma com bola e forma sem bola separadas, uma role com bola e uma sem bola por slot, as instruções que o jogo tem hoje e o custo de complexidade de cada escolha.

**Ainda não há tática pré-setada para nenhum técnico.** Este manual define a identidade de cada um: quais formas, roles e instruções ele usa, quais nunca usa e como reage ao placar. Quando uma tática for ditada, ela entra na seção do técnico (com config em `configs/<time>/<formação>.json`) e tem que caber dentro destas regras. Se não couber, a regra muda aqui primeiro.

**Fonte das mecânicas:** `game_data/` (ver `game_data/README.md`). Roles e posições em `roles.json`, instruções e custos em `instructions.json`, formas sugeridas pelo jogo em `tactic_presets.json`. Nada aqui usa role ou instrução que não esteja lá.

---

## 0. Como ler este manual

### 0.1 O que mudou do FM24 para o FM27

| Tema | FM24 (manual antigo) | FM27 |
|---|---|---|
| Formação | Uma forma | **Duas formas**: com bola e sem bola (ex.: `4-2-3-1 DM AM Wide` com bola, `4-4-2 2DM` sem bola) |
| Roles | Role + duty (Support/Attack…) | **Sem duty.** Cada slot tem uma role com bola e uma sem bola. A role sem bola vale para o slot na forma **sem bola** |
| Pressão | Linha de engajamento junto com "high press / mid block / low block" | Grupos separados: **Line of Engagement** (onde começa a pressão), **Defensive Line** (altura da linha), **Pressing Intensity** (quanto pressiona) e **Line** (segura a linha ou recua) |
| Saída de bola | "Play out of defence" | **Passing Strategy** (Play Through the Press / Into Feet / Into Space / Bypass the Press) + **Goal kick** curto/longo |
| Atacantes que pressionam | Pressing Forward | **Não existe role de pressão para atacante.** Atacante pressiona com a instrução de jogador **Pressing Intensity: Higher** |
| Ball-Winning Midfielder | Role com bola | Some. Ganhar bola agora é role **sem bola**: Pressing DM / Pressing CM |
| Complexidade | Não existia | Toda role e toda instrução custa complexidade (time 0–49; jogador até 4 com role + instruções). Mais complexidade = tática demora mais para ser aprendida |
| Mentality | Very Defensive → Very Attacking | **Igual** (7 níveis). Não aparece em `instructions.json` porque não soma complexidade |

### 0.2 Convenções

- **Roles escritas como `IP/OOP`**: role com bola / role sem bola, em sigla (glossário na seção 6). Ex.: `BPCB/CCB` = Ball-Playing Centre-Back com bola, Covering Centre-Back sem bola.
- **Linha de roles** (manual e coluna `Roles` da planilha): os 11 slots em ordem posicional (GK → laterais/zaga → meio → ataque), separados por vírgula e espaço. Ex.: `BPGK/GK, FB/HFB, BPCB/CB, CB/CCB, IFB/FB, DM/SDM, …`
- **Nome de formação** sempre em minúsculo.
- **Instruções** escritas como `Grupo: Opção`, com o nome derivado do enum do jogo (`PLAY_THROUGH_THE_PRESS` → Play Through the Press). O número entre parênteses é o custo de complexidade.
- **"—"** numa instrução = nenhuma opção escolhida (padrão do jogo, custo 0).
- **Posições**: uma role só entra em slots listados em `roles.json → positions`. Para roles sem bola, vale o slot na forma sem bola. Ex.: com 4 atrás sem bola, o lateral só pode ter `FB`, `HFB` ou `PRFB` sem bola; `WB/HWB/PRWB` sem bola só existem se a forma sem bola tiver WBL/WBR.

### 0.3 Orçamento de complexidade

- Time: 0–49. Pesos no entendimento tático: complexidade do time 0,6, do jogador 0,3, instruções de adversário 0,1.
- Jogador: até 4 com role e instruções individuais. Uma role de custo 3 (ex.: `F9`, `FR`, `PWB`, `ACB`, `BBP`, `DDM`) deixa espaço para no máximo uma instrução barata.
- Cada técnico tem uma faixa de custo das instruções de time abaixo. Casca é o mais barato de propósito (simples, aprende rápido); Keller é o mais caro (pressão alta custa).

---

## 1. GIOVANI — Sporting

**Identidade:** estruturado, adaptativo, orientado a sistema. Posse controlada, pressão organizada, funções claras. Estrutura acima de improviso, caos mínimo. Pensa em sequências, não só no jogo atual.

**Atributos mais valorizados:** Posicionamento · Decisões · Trabalho de Equipe *(4º: Concentração; 5º: Antecipação)*. No motor, Posicionamento + Antecipação geram interceptações, bloqueios e desarmes, e Decisões gera acerto de passe (`stat_attributes.json`). É o perfil de quem ganha jogo sem correr atrás da bola.

**Mentality:** casa **balanced** · piso **cautious** · teto **attacking**. Nunca very defensive nem very attacking: os dois quebram a estrutura.

**Regra de ouro:** ajusta **roles antes de trocar a forma**. A forma sem bola é a última coisa que muda.

### 1.1 Formas

| | Preferidas | Aceitáveis | Nunca |
|---|---|---|---|
| **Com bola** | `4-2-3-1 DM AM Wide` · `4-4-2 Diamond Narrow` (o 4-3-1-2/4-2-2-2 dele) | `4-3-3 DM Wide` | `4-2-4`, qualquer coisa com 2 atacantes abertos e um meio só |
| **Sem bola** | `4-4-2 2DM` · `4-4-1-1 2DM` | `4-1-4-1 DM` · `4-4-2 Diamond Narrow` | Linha de 5 como forma-base |

**Princípio:** sem bola, sempre **duas camadas de proteção** no meio (dois DM, ou DM + MC de contenção). Com bola, sempre pelo menos **3 jogadores atrás da linha da bola** na saída (2 zagueiros + DM, ou zaga + lateral invertido).

### 1.2 Roles por zona

| Zona | Preferidas (IP/OOP) | Variantes | Fora do perfil |
|---|---|---|---|
| **GK** | `BPGK/GK` (2+1) | `GK/GK` (1+1) | `SWK` como padrão (só com linha alta, perseguindo) · `NNGK` |
| **DC** | `BPCB/CB` (2+0) + `CB/CCB` (1+1): um sai jogando, outro cobre | `ACB/CCB` (3+1), o zagueiro que sobe pro meio na saída | Dois `SCB`: dois zagueiros saltando = buraco atrás |
| **DL/DR** | `IFB/FB` (1+0) num lado + `FB/HFB` (0+1) no outro: saída com 3 atrás | `WB/FB` (0+0) do lado do ponta por dentro | `PWB` (3) como padrão · `PRFB` (2) fora de modo pressão |
| **DM** | `DM/SDM` (0+1) · `HB/SDM` (2+1): vira o 3º zagueiro na saída | `DLP/SDM` (1+1) · `DM/PRDM` (0+2) no modo pressão | `BBP` (3) — muito livre pro slot de proteção |
| **MC** | `CM/SCM` (0+1) · `MP/CM` (2+0) | `WCM/WCCM` (1+2), lado sem ponta · `CM/PRCM` (0+2) no modo pressão | `CHM` como padrão (corre pro corredor e abre o meio) |
| **AMC** | `AP/AM` (2+0) · `AP/TAM` (2+1) | `SS/AM` (1+0) quando precisa de gol | `FR` (3) — improviso puro |
| **AML/AMR** | `IW/TW` (1+1) · `W/TW` (0+1) | `IF/TW` (2+1) · `PW/W` (2+0) | `IOW`/`WOW` como padrão: outlet deixa o lado aberto |
| **ST** | `CF/CF` (0+0) · `DLF/TCF` (2+1) | `CHF/CF` (1+0) · `TF/CF` (1+0) na dupla do diamante | `PO` (vive na linha do impedimento, não participa) · `F9` (3) como padrão |

Pares coerentes: `DLF` + `CF` ou `TF` + `CHF` na dupla do diamante (um vem, outro vai). `IFB` de um lado pede `WB` ou `FB` do outro, não dois invertidos.

### 1.3 Instruções-base

| Fase | Instruções | Custo |
|---|---|---|
| **Com bola** | Passing Style: Shorter (2) · Passing Strategy: Into Feet (1) · Tempo: — · Width: — · Build up Play: Work Ball Into Box (2) · Creative Freedom: Be More Disciplined (3) · Waste Time: Normal (1) · Crossing: — · Dribbling: — · Shooting: — | 9 |
| **Transição** | Defence Transition: Regroup (1) · Transition: Counter (2) · GK: Goal kick Short (1), Method Roll Out (0), Target Centre Backs (1) | 5 |
| **Sem bola** | Line of Engagement: Standard (1) · Defensive Line: — · Line: — · Pressing Intensity: — · Pressing Trap: — · Tackling: Stay on Feet (1) · Defending Crosses: — | 2 |
| **Total** | | **≈16** |

- **Pressing Trap: In (0)** com o diamante sem bola (fecha o meio, empurra pra fora não faz sentido sem pontas).
- **Play Through the Press (3)** no lugar de Into Feet quando o adversário pressiona alto e a zaga tem passe: é o "play out of defence" dele, mas caro.

**Instruções de jogador típicas:** AP com Risks: Take More (3) só se a role custar ≤1, senão nada · DM com Positioning: Hold Position (1) · laterais com Cross From: Deep (1) ou nada.

### 1.4 Ajuste por estado de jogo

Ordem fixa: **roles → instruções → mentality → forma**.

- **Segurando vitória** — *controla, não recua*.
  - Roles: 2º MC `CM/SCM`; AMC `AP/TAM`; laterais `FB/HFB`.
  - Instruções: Passing Style: Much Shorter (3), Tempo: Lower (1), Waste Time: Extreme (2), Transition: Hold Shape (1). A linha **não** desce (Defensive Line fica —).
  - Mentality: **cautious**.
- **Empate travado / perdendo** — *aumenta a intensidade sem perder a estrutura*.
  - Roles primeiro: AMC `AP` → `SS`; um lateral `IFB` → `WB`; 2º MC sem bola `SCM` → `PRCM`; ST sem bola `CF` + Pressing Intensity: Higher (2) como instrução de jogador.
  - Instruções: Line of Engagement: Higher (2), Pressing Intensity: Higher (2), Defence Transition: Counter Press (3), Tempo: Higher (1).
  - Mentality: positive → **attacking** (teto).
  - Forma: só no fim e só dentro das preferidas (diamante → `4-2-3-1 DM AM Wide`).

---

## 2. BRUNO KELLER — Internacional

**Identidade:** intenso, proativo, fisicamente exigente. Verticalidade, pressão implacável, atacar antes do adversário se organizar. Intensidade acima de posse.

**Atributos mais valorizados:** Ritmo/Aceleração · Ritmo de Trabalho · Resistência *(4º: Agressividade; 5º: Bravura)*. No motor, Work Rate entra em pressões tentadas e completadas, sprints, distância e desarmes; Aceleração entra em pressão completada (`stat_attributes.json`). Pressão alta no FM27 é literalmente um atributo de Work Rate.

**Mentality:** casa **attacking** · piso **positive** · teto **attacking**. Nunca desce de positive.

**Regra de ouro:** raramente abre mão da identidade ofensiva. Protege vantagem **prendendo o adversário lá em cima**, não sentando. Gira o elenco pra manter o output físico.

### 2.1 Formas

| | Preferidas | Aceitáveis | Nunca |
|---|---|---|---|
| **Com bola** | `4-3-3 DM Wide` · `4-2-3-1 DM AM Wide` | `4-2-4 DM Wide` (perseguindo) | Diamante estreito, linha de 5 |
| **Sem bola** | `4-4-2 2DM` (dois na frente pressionando) · `4-3-3 DM Wide` | `4-4-1-1 2DM` | `5-3-2`, `5-2-2-1` (bloco baixo) |

São as formas que o jogo sugere para **Gegenpress** (`tactic_presets.json`). **Princípio:** sem bola, pelo menos **dois jogadores na primeira linha de pressão** e a linha alta.

### 2.2 Roles por zona

| Zona | Preferidas (IP/OOP) | Variantes | Fora do perfil |
|---|---|---|---|
| **GK** | `BPGK/SWK` (2+2) — linha alta exige goleiro que varre | `GK/SWK` (1+2) | `LHGK`, `NNGK` |
| **DC** | `BPCB/SCB` (2+1) + `CB/CCB` (1+1): um salta, o mais rápido cobre | `CB/SCB` | Dois `CCB` (a linha não sobe) |
| **DL/DR** | `WB/PRFB` (0+2) · `FB/PRFB` (0+2) | `IWB/FB` (2+0), lado do meia que pisa na área | `HFB` (segura a linha, não pressiona) · `PWB` |
| **DM** | `BBM/PRDM` (1+2) · `DM/PRDM` (0+2) | `DM/SDM` (0+1) como único pivô de proteção | `DLP`, `HB`, `DDM` (lentos, recuam) |
| **MC** | `CHM/PRCM` (1+2) · `CM/PRCM` (0+2) | `WCM/WCCM` (1+2) | `MP` como padrão · `SCM` (segura, não salta) |
| **AMC** | `SS/AM` (1+0) · `AM/AM` (0+0) | `SS/SOAM` (1+2) | `AP`, `FR` |
| **AML/AMR** | `W/W` (0+0) · `IF/W` (2+0) | `WF/TW` (1+1) | `PW`, `IOW`/`WOW` (ficam esperando, não pressionam) |
| **ST** | `CHF/CF` (1+0) · `PO/CF` (1+0) | `TF/CF` (1+0) quando o jogo pede bola longa | `DLF`, `F9` (vêm buscar, não atacam profundidade) |

**Atacante pressionando:** não há role sem bola de pressão para ST. Use **Pressing Intensity: Higher (2)** como instrução de jogador no(s) atacante(s). Com `CHF` (1) fica em 3 de 4, então sobra só mais uma instrução de custo 1.

### 2.3 Instruções-base

| Fase | Instruções | Custo |
|---|---|---|
| **Com bola** | Passing Style: More Direct (1) · Passing Strategy: Into Space (1) · Tempo: Higher (1) · Width: Wider (1) · Dribbling: Run at Defence (2) · Crossing: Low Crosses (1) · Look For: Overlap (1) · Waste Time: — · Creative Freedom: — | 8 |
| **Transição** | Defence Transition: Counter Press (3) · Transition: Counter (2) · GK: Pace Quick (2), Method Throw Long (0), Target Flanks (1) | 8 |
| **Sem bola** | Line of Engagement: Higher (2) · Defensive Line: Higher (2) · Line: Hold Line (2) · Pressing Intensity: Much Higher (3) · Pressing Trap: Out (0) · Tackling: Get Stuck In (1) · Prevent Short GK Distribution (1) | 11 |
| **Total** | | **≈27** |

É a tática mais cara dos quatro. Pressão alta custa, e é o preço da identidade dele: espere a tática demorar mais pra ser aprendida e cuide do treino tático na pré-temporada.

### 2.4 Ajuste por estado de jogo

- **Perdendo** — *sobe a pressão, mesmo contra time grande*.
  - Forma com bola: `4-2-4 DM Wide` (sem bola continua `4-4-2 2DM`).
  - Instruções: Defensive Line: Much Higher (3), Tempo: Much Higher (2), Shooting: Shoot on Sight (1), Crossing: Hit Early Crosses (1).
  - Mentality: fica **attacking** (é o teto).
- **Segurando vitória** — *prende, não senta*.
  - Mantém Line of Engagement: Higher e a linha alta.
  - Pressing Intensity: Much Higher → **Higher** (2) (poupa perna); Tempo: Higher → —; Waste Time: Normal (1); Dribbling: Run at Defence → —.
  - Mentality: **positive** (piso). Nunca defensive.
- **Contra time grande (emboscada)** — começa um degrau abaixo, não muda de identidade.
  - Mentality **positive**; Line of Engagement: Standard (1); Defensive Line: —; Pressing Intensity: Higher (2); Pressing Trap: Out mantido.
  - Pivô `DM/SDM` no lugar de `BBM/PRDM`.
- **Rotação:** sprints e distância vêm de Work Rate + Stamina. Jogador com condição baixa rende menos exatamente nos números que a tática dele cobra. Trocas cedo (60') são parte do plano, não sinal de crise.

---

## 3. RAFAEL DUARTE — River Plate

**Identidade:** fluido, emocional, movido a momentum. Expressão acima de estrutura. Jogadores trocando de linha livremente, resolvendo em tempo real. Sem bola: mid-block reativo.

**Atributos mais valorizados:** Técnica · Visão/Criatividade · Drible *(4º: Aceleração; 5º: Flair)*. No motor, dribles saem de Drible + Flair + Pace + Aceleração e passes decisivos/progressivos saem de Passe + Visão (`stat_attributes.json`).

**Mentality:** casa **positive** · piso **cautious** · teto **very attacking** (só ele chega aqui).

**Regra de ouro:** **troca de forma livremente**, no meio do jogo, mais do que os outros três. Quando perde, aumenta o risco rápido, às vezes se desestabilizando. É parte do personagem.

### 3.1 Formas

| | Preferidas | Aceitáveis | Nunca |
|---|---|---|---|
| **Com bola** | `4-2-3-1 DM AM Wide` · `4-3-3 DM Wide` | `4-2-4 DM Wide` (perdendo tarde) · `4-4-2 Diamond Narrow` | Linha de 5 |
| **Sem bola** | `4-4-1-1 2DM` (o 10 fica de outlet) · `4-1-4-1 DM` | `4-3-3 DM Wide` | `5-3-2`, `5-2-3` como base |

**Princípio:** com bola, **três criadores** em zonas diferentes (DM, meia, ponta ou 9 que recua). Sem bola, ele não engessa: forma simples, poucas instruções e alguém sempre pronto pro contra-ataque.

### 3.2 Roles por zona

| Zona | Preferidas (IP/OOP) | Variantes | Fora do perfil |
|---|---|---|---|
| **GK** | `BPGK/GK` (2+1) | `GK/GK` | `NNGK` |
| **DC** | `BPCB/CB` (2+0) + `CB/CCB` (1+1) | `BPCB/CCB` | `NNCB` (chutão é contra a ideia) |
| **DL/DR** | `WB/FB` (0+0) · `IWB/FB` (2+0) | `PWB/FB` (3+0), lateral técnico | `HFB` como padrão |
| **DM** | `DLP/SDM` (1+1) · `BBP/DM` (3+0) | `DM/SDM` com DLP do lado | `HB`, `DDM` (estrutura demais) |
| **MC** | `CHM/CM` (1+0), o mezzala · `MP/CM` (2+0) | `AP/CM` (2+0) | `SCM` como padrão |
| **AMC** | `AP/COAM` (2+1) · `FR/COAM` (3+1) | `SS/SOAM` (1+2) | `AM/TAM` (marcar o volante não é com ele) |
| **AML/AMR** | `IF/IOW` (2+2) · `IW/W` (1+0) | `PW/W` (2+0) · `IF/WOW` | `W/TW` como padrão (`TW` só segurando) |
| **ST** | `F9/CF` (3+0) · `DLF/CF` (2+0) | `CHF/SOCF` (1+2) · `PO/CF` (perdendo tarde) | `TF` |

**Fluidez sem pagar complexidade:** a instrução de jogador **Positioning: Switch Position** custa **0**. Os dois pontas trocando de lado (`IF` ↔ `IW`) é o "carrossel" de graça. **Positioning: Roam From Position (2)** e **Risks: Take More (3)** só em role de custo ≤2 ou ≤1, por causa do limite de 4 por jogador.

### 3.3 Instruções-base

| Fase | Instruções | Custo |
|---|---|---|
| **Com bola** | Creative Freedom: Be More Expressive (2) · Passing Style: Shorter (2) · Passing Strategy: Into Space (1) · Tempo: Higher (1) · Width: Wider (1) · Build up Play: Work Ball Into Box (2) · Waste Time: — · Crossing: — | 9 |
| **Transição** | Defence Transition: Regroup (1) · Transition: Counter (2) · GK: Goal kick Short (1), Method Roll Out (0), Target Playmaker (1) | 5 |
| **Sem bola** | Line of Engagement: Standard (1) · resto — (ele não engessa a fase defensiva) | 1 |
| **Total** | | **≈15** |

### 3.4 Ajuste por estado de jogo

- **Vencendo** — *ele não defende, ele guarda a bola*.
  - Forma com bola `4-3-3 DM Wide`, sem bola `4-1-4-1 DM`.
  - Instruções: Passing Style: Much Shorter (3), Tempo: Lower (1), Waste Time: Extreme (2), Transition: Hold Shape (1), Creative Freedom: Be More Expressive → —.
  - Pontas sem bola `TW`.
  - Mentality: **balanced** ou **cautious** (piso).
- **Empate / perdendo cedo** — fica na base e sobe pra **attacking**. Defence Transition: Counter Press (3).
- **Perdendo tarde (estouro)** — *sabe que pode se estourar*.
  - Forma com bola `4-2-4 DM Wide`.
  - Roles: ST2 `PO/CF`; pontas `IF/WOW`; DM `BBP`.
  - Instruções: Dribbling: Run at Defence (2), Shooting: Shoot on Sight (1), Crossing: Hit Early Crosses (1), Look For: Overlap (1), Defence Transition: Counter Press (3), Line of Engagement: Higher (2), Defensive Line: Much Higher (3), Pressing Intensity: Much Higher (3), Tackling: Get Stuck In (1).
  - Mentality: **very attacking**.

---

## 4. LUIZ "CASCA" FERREIRA — Watford

**Identidade:** pragmático, disciplinado, tradicional. **Um único sistema: 4-4-2.** Direto, sólido, cruzamento pro centroavante. Valoriza experiência, força aérea e disciplina acima do talento individual.

**Atributos mais valorizados:** Cabeceio · Impulsão · Trabalho de Equipe · Concentração *(5º: Posicionamento)*. No motor, cabeceios disputados e decisivos saem de Posicionamento + Impulsão, e cabeceio ganho de Cabeceio + Força + Impulsão (`stat_attributes.json`).

**Mentality:** casa **balanced** · piso **defensive** (só nos últimos 10, segurando) · teto **positive**. Nunca attacking.

**Regra de ouro:** **ele não troca de sistema.** É 4-4-2 **com bola e sem bola**. O que muda entre os estados de jogo são **roles + mentality + instruções**. Trocar pra 4-3-3 no minuto 60 seria trair o personagem.

### 4.1 Formas

| | Únicas permitidas |
|---|---|
| **Com bola** | `4-4-2` reto (dois MC) · `4-4-2 2DM` |
| **Sem bola** | As mesmas. A dupla central fica na mesma linha com e sem bola |

- **4-4-2 reto** (dupla no MC): roles centrais `CM`, `MP`, `WCM`, `CHM` com bola; `CM`, `SCM`, `PRCM`, `WCCM` sem bola.
- **4-4-2 2DM** (o preset do jogo, dupla no DM): `DM`, `DLP`, `BBM`, `HB` com bola; `DM`, `SDM`, `PRDM`, `WCDM` sem bola. Mais protegido, menos chegada na área.

### 4.2 Roles por zona

| Zona | Preferidas (IP/OOP) | Variantes | Fora do perfil |
|---|---|---|---|
| **GK** | `GK/GK` (1+1) · `NNGK/LHGK` (0+0) | `GK/LHGK` | `BPGK`, `SWK` |
| **DC** | `NNCB/SCB` (0+1) + `CB/CCB` (1+1): o casca-grossa sai no atacante, o outro cobre | `CB/CB` (1+0) | `BPCB` como padrão · `ACB` (3) |
| **DL/DR** | `FB/HFB` (0+1) · `FB/FB` (0+0) | `WB/FB` (0+0), perseguindo | `IFB`, `IWB`, `PWB` |
| **MC** (reto) | `CM/SCM` (0+1) + `CM/CM` (0+0) | `WCM/WCCM` (1+2), o "carrilero" · `MP/SCM` (2+1) | `AP`, `CHM` como padrão |
| **DM** (2DM) | `DM/SDM` (0+1) + `BBM/DM` (1+0) | `DLP/SDM` (1+1) | `BBP`, `DDM` |
| **ML/MR** | `WM/TWM` (0+1) · `W/TWM` (0+1), o ponta que cruza | `WM/WOWM` (0+1), perseguindo | `IW`, `PW` (cortar pra dentro não é o jogo dele) |
| **ST** | `TF/CF` (1+0) + `CHF/CF` (1+0) | `TF/COCF` (1+1) · `PO/CF` (1+0) · `DLF/TCF` (2+1), segurando | `F9`, `FR` |

**Pares de ataque:** sempre um `TF` (alvo de bola longa e cruzamento) + um que ataca espaço (`CHF` ou `PO`). Dois alvos não.

### 4.3 Instruções-base

| Fase | Instruções | Custo |
|---|---|---|
| **Com bola** | Passing Style: More Direct (1) · Passing Strategy: Bypass the Press (0) · Width: Wider (1) · Focus Play: Down Both Flanks (1) · Crossing: Float Crosses (1) · Build up Play: Play for Set Pieces (1) · Creative Freedom: Be More Disciplined (3) · Waste Time: Normal (1) · Tempo: — | 9 |
| **Transição** | Defence Transition: Regroup (1) · Transition: Counter (2) · GK: Goal kick Long (1), Method Kick Long (0), Target Target Man (1) | 5 |
| **Sem bola** | Line of Engagement: Standard (1) · Defensive Line: — · Pressing Intensity: Lower (1) · Tackling: Stay on Feet (1) · Defending Crosses: Stop (1) | 4 |
| **Total** | | **≈18** |

**Instruções de jogador típicas:** meias abertos com Cross To: Target Man (2) e Cross From: Deep (1) quando o lateral não passa · `TF` com Dribbling: Hold Up Ball (1).

### 4.4 O buraco entre as linhas

O 4-4-2 tem duas linhas paralelas e **ninguém mora** entre a zaga e o meio. Um 10 cai ali, recebe de frente, vira e chuta. No FM27 a solução tem nome de role:

- **Um dos MC sem bola vira `SCM`** (Screening Central Midfielder: segura posição pra bloquear passe pelo meio). No 2DM, `SDM`. Na mesma dupla, **nunca** dois `PRCM`/`PRDM`: quem salta abre o buraco.
- **Defensive Line: Higher (2)**: o espaço morre por **compressão**, não por recuo. Baixar a linha piora tudo.
- **Pressing Trap: Out (0)**: funila pros lados, longe do miolo, pro cruzamento que ele defende bem (Defending Crosses: Stop).
- Se persistir, ST2 sem bola vira `TCF` (Tracking Centre Forward: volta acompanhando o volante adversário) e fecha a primeira linha do meio. Continua 4-4-2.

### 4.5 Ajuste por estado de jogo

- **Perseguindo placar (rolo compressor)**
  - Roles: laterais `WB/FB`; um meia aberto `W/WOWM`; ST2 `CHF` → `PO`.
  - Instruções: Width: Much Wider (2), Tempo: Higher (1), Crossing: Hit Early Crosses (1), Look For: Overlap (1), Shooting: Shoot on Sight (1), Waste Time: —, Defensive Line: Higher (2), Pressing Intensity: — , Defence Transition: Counter Press (3).
  - Mentality: **positive** (teto).
- **Segurando vantagem (ferrolho)**
  - Roles: ST2 `DLF/TCF`; meias `WM/TWM`; os dois MC sem bola `SCM`.
  - Instruções: Width: Narrower (1), Tempo: Lower (1), Waste Time: Extreme (2), Transition: Hold Shape (1), GK Pace: Slow (1), Defensive Line: Deeper (1), Line: Drop Off (1), Pressing Intensity: Lower mantido.
  - Mentality: **cautious**; **defensive** nos últimos 10.
- **Sofrendo entre as linhas:** aplicar a seção 4.4 antes de mexer em mentality.

---

## 5. Quadro comparativo

| | Giovani | Bruno Keller | Rafael Duarte | Luiz Casca |
|---|---|---|---|---|
| **Time** | Sporting | Internacional | River Plate | Watford |
| **Eixo** | Cérebro | Corpo | Técnica | Solidez |
| **Atributos** | Posicionamento, Decisões, Teamwork | Pace, Work Rate, Stamina | Técnica, Visão, Drible | Cabeceio, Impulsão, Teamwork, Concentração |
| **Mentality casa** | balanced | attacking | positive | balanced |
| **Teto** | attacking | attacking | **very attacking** | positive |
| **Piso** | cautious | positive | cautious | defensive |
| **Forma com bola** | 4-2-3-1 / diamante | 4-3-3 / 4-2-3-1 | 4-2-3-1 / 4-3-3 | 4-4-2 |
| **Forma sem bola** | 4-4-2 2DM / 4-4-1-1 | 4-4-2 2DM / 4-3-3 | 4-4-1-1 / 4-1-4-1 | 4-4-2 |
| **Line of Engagement** | Standard | Higher | Standard | Standard |
| **Pressing Intensity** | — | Much Higher | — | Lower |
| **Passing** | Shorter + Into Feet | More Direct + Into Space | Shorter + Into Space | More Direct + Bypass |
| **Creative Freedom** | Disciplined | — | Expressive | Disciplined |
| **Defence Transition** | Regroup | Counter Press | Regroup | Regroup |
| **Complexidade das instruções de time** | ≈16 | ≈27 | ≈15 | ≈18 |
| **Troca forma?** | Roles antes da forma | Só com bola, perdendo | **Livremente** | **Nunca** |

---

## 6. Glossário de siglas

Notação na linha de roles: `IP/OOP`. Número = complexidade. Posições conforme `game_data/roles.json`.

### 6.1 Com bola (40)

| Sigla | Role | Posições | Cx |
|---|---|---|---|
| `GK` | Goalkeeper | GK | 1 |
| `BPGK` | Ball-Playing Goalkeeper | GK | 2 |
| `NNGK` | No-Nonsense Goalkeeper | GK | 0 |
| `CB` | Centre-Back | DC | 1 |
| `BPCB` | Ball-Playing Centre-Back | DC | 2 |
| `NNCB` | No-Nonsense Centre-Back | DC | 0 |
| `ACB` | Advanced Centre-Back | DC | 3 |
| `WCB` | Wide Centre-Back | DC | 1 |
| `OCB` | Overlapping Centre-Back | DC | 3 |
| `FB` | Full-Back | DL, DR | 0 |
| `IFB` | Inside Full-Back | DL, DR | 1 |
| `WB` | Wing-Back | DL, DR, WBL, WBR | 0 |
| `IWB` | Inside Wing-Back | DL, DR, WBL, WBR | 2 |
| `PWB` | Playmaking Wing-Back | DL, DR, WBL, WBR | 3 |
| `AWB` | Advanced Wing-Back | WBL, WBR | 1 |
| `DM` | Defensive Midfielder | DM | 0 |
| `HB` | Half Back | DM | 2 |
| `DLP` | Deep-Lying Playmaker | DM | 1 |
| `BBM` | Box-To-Box Midfielder | DM | 1 |
| `BBP` | Box-To-Box Playmaker | DM | 3 |
| `CM` | Central Midfielder | MC | 0 |
| `MP` | Midfield Playmaker | MC | 2 |
| `WCM` | Wide Central Midfielder | MC | 1 |
| `CHM` | Channel Midfielder | MC, AMC | 1 |
| `AP` | Advanced Playmaker | MC, AMC | 2 |
| `AM` | Attacking Midfielder | MC, AMC | 0 |
| `SS` | Second Striker | AMC | 1 |
| `FR` | Free Role | AMC | 3 |
| `WM` | Wide Midfielder | ML, MR | 0 |
| `W` | Winger | ML, MR, AML, AMR | 0 |
| `IW` | Inside Winger | ML, MR, AML, AMR | 1 |
| `PW` | Playmaking Winger | ML, MR, AML, AMR | 2 |
| `IF` | Inside Forward | AML, AMR | 2 |
| `WF` | Wide Forward | AML, AMR | 1 |
| `CF` | Centre Forward | ST | 0 |
| `CHF` | Channel Forward | ST | 1 |
| `DLF` | Deep-Lying Forward | ST | 2 |
| `F9` | False Nine | ST | 3 |
| `PO` | Poacher | ST | 1 |
| `TF` | Target Forward | ST | 1 |

### 6.2 Sem bola (39)

Quando o nome é igual ao da role com bola, a sigla também é (`CB`, `FB`, `DM`…). A posição depois da barra diz qual é. Roles de pressão usam o prefixo `PR`, pra não confundir com `PWB` (Playmaking).

| Sigla | Role | Posições | Cx |
|---|---|---|---|
| `GK` | Goalkeeper | GK | 1 |
| `LHGK` | Line-Holding Goalkeeper | GK | 0 |
| `SWK` | Sweeper Keeper | GK | 2 |
| `CB` | Centre-Back | DC | 0 |
| `CCB` | Covering Centre-Back | DC | 1 |
| `SCB` | Stopping Centre-Back | DC | 1 |
| `WCB` | Wide Centre-Back | DC | 0 |
| `CWCB` | Covering Wide Centre-Back | DC | 1 |
| `SWCB` | Stopping Wide Centre-Back | DC | 1 |
| `FB` | Full-Back | DL, DR | 0 |
| `HFB` | Holding Full-Back | DL, DR | 1 |
| `PRFB` | Pressing Full-Back | DL, DR | 2 |
| `WB` | Wing-Back | WBL, WBR | 0 |
| `HWB` | Holding Wing-Back | WBL, WBR | 1 |
| `PRWB` | Pressing Wing-Back | WBL, WBR | 2 |
| `DM` | Defensive Midfielder | DM | 0 |
| `SDM` | Screening Defensive Midfielder | DM | 1 |
| `PRDM` | Pressing Defensive Midfielder | DM | 2 |
| `WCDM` | Wide Covering Defensive Midfielder | DM | 2 |
| `DDM` | Dropping Defensive Midfielder | DM | 3 |
| `CM` | Central Midfielder | MC | 0 |
| `SCM` | Screening Central Midfielder | MC | 1 |
| `PRCM` | Pressing Central Midfielder | MC | 2 |
| `WCCM` | Wide Covering Central Midfielder | MC | 2 |
| `AM` | Attacking Midfielder | AMC | 0 |
| `TAM` | Tracking Attacking Midfielder | AMC | 1 |
| `COAM` | Central Outlet Attacking Midfielder | AMC | 1 |
| `SOAM` | Splitting Outlet Attacking Midfielder | AMC | 2 |
| `WM` | Wide Midfielder | ML, MR | 0 |
| `TWM` | Tracking Wide Midfielder | ML, MR | 1 |
| `WOWM` | Wide Outlet Wide Midfielder | ML, MR | 1 |
| `W` | Winger | AML, AMR | 0 |
| `TW` | Tracking Winger | AML, AMR | 1 |
| `IOW` | Inside Outlet Winger | AML, AMR | 2 |
| `WOW` | Wide Outlet Winger | AML, AMR | 1 |
| `CF` | Centre Forward | ST | 0 |
| `TCF` | Tracking Centre Forward | ST | 1 |
| `COCF` | Central Outlet Centre Forward | ST | 1 |
| `SOCF` | Splitting Outlet Centre Forward | ST | 2 |

---

## 7. Tradução FM24 → FM27

Para ler anotações antigas e traduzir a ideia, não a tática. Nenhuma tática FM24 foi mantida.

### 7.1 Roles

| FM24 | FM27 (IP/OOP) | Observação |
|---|---|---|
| SK | `BPGK/SWK` | Separado: jogar com o pé (com bola) e varrer (sem bola) |
| GK | `GK/GK` ou `NNGK/LHGK` | |
| BPD | `BPCB/CB` | |
| CD | `CB/CB` | Cover/Stopper viraram roles sem bola: `CCB`, `SCB` |
| NCB | `NNCB/SCB` | |
| FB | `FB/FB` ou `FB/HFB` | |
| WB | `WB/FB` (4 atrás) · `WB/WB` (5 atrás) | |
| IWB | `IWB/FB` ou `IFB/FB` | `IFB` fica na zaga, `IWB` sobe pro meio |
| DM / Anchor | `DM/SDM` | |
| HB | `HB/SDM` | |
| BWM | `DM/PRDM` ou `CM/PRCM` | Não existe mais com bola |
| DLP | `DLP/SDM` (DM) · `MP/SCM` (MC) | `DLP` só joga no DM |
| RPM / Regista | `BBP` | |
| BBM | `BBM` (DM) · `CM` ou `CHM` (MC) | `BBM` só joga no DM |
| MEZ | `CHM` | |
| CAR | `WCM/WCCM` | |
| AP | `AP` | |
| SS / Shadow Striker | `SS` (AMC) | |
| Trequartista / Enganche | `FR` | |
| W | `W` | |
| IF | `IF` | |
| IW | `IW` | |
| WM / DW | `WM/TWM` | |
| TF | `TF` | |
| PF | `CF` ou `CHF` + Pressing Intensity: Higher (instrução de jogador) | Não existe role de pressão para ST |
| AF | `PO` ou `CHF` | |
| DLF | `DLF` | |
| F9 | `F9` | |

### 7.2 Instruções

| FM24 | FM27 |
|---|---|
| Mentality | Igual (7 níveis) |
| Largura fairly wide / wide / fairly narrow | Width: Wider / Much Wider / Narrower |
| Passe shorter / much shorter / direct | Passing Style: Shorter / Much Shorter / More Direct (ou Much More Direct) |
| Play out of defence | Passing Strategy: Play Through the Press + Goal kick Short |
| Pass into space | Passing Strategy: Into Space |
| Tempo slightly higher / higher | Tempo: Higher / Much Higher |
| Time wasting never / sometimes / always | Waste Time: — / Normal / Extreme |
| Low / floated / whipped / mixed crosses | Crossing: Low / Float / Whipped / — |
| Hit early crosses | Crossing: Hit Early Crosses (mesmo grupo do tipo de cruzamento: é um ou outro) |
| Focus play | Focus Play (agora com Down Both Flanks) |
| Overlap / underlap | Look For: Overlap / Underlap (geral, esquerda ou direita) |
| Run at defence / dribble less | Dribbling: Run at Defence / Dribble Less |
| Be more expressive / disciplined | Creative Freedom |
| Work ball into box | Build up Play: Work Ball Into Box (ou Play for Set Pieces) |
| Counter / hold shape | Transition: Counter / Hold Shape |
| Counter press / regroup | Defence Transition: Counter Press / Regroup |
| Distribute quickly / slow pace down | GK Pace: Quick / Slow |
| Roll out / throw long / long kicks / short kicks | GK Method: Roll Out / Throw Long / Kick Long / Kick Short · Goal kick: Long / Short |
| Distribute to CBs / FBs / playmaker / target forward | GK Target: Centre Backs / Full Backs / Playmaker / Target Man (também Flanks, Clear Opposition Defence, Specific Teammate) |
| High press / mid block / low block | Line of Engagement: Higher / Standard / Deeper |
| Linha much higher / higher / lower | Defensive Line: Much Higher / Higher / Deeper (Much Deeper) |
| Trigger more / much more / less often | Pressing Intensity: Higher / Much Higher / Lower (Much Lower) |
| Step up more / drop off more | Line: Hold Line / Drop Off |
| Trap inside / outside | Pressing Trap: In / Out |
| Stay on feet / get stuck in | Tackling |
| Stop / invite crosses | Defending Crosses: Stop / Invite |
| Prevent short GK distribution | Toggle, custo 1 |

---

## 8. Pendências em aberto

- **Nenhuma tática definida.** Os quatro técnicos estão sem formação FM27. Quando uma for ditada: config em `configs/<time>/<formação>.json`, linha de roles `IP/OOP` e instruções na seção do técnico, e conferir contra as regras de cima.
- **Nomes das instruções**: derivados dos enums do jogo. O texto exato na tela pode ser um pouco diferente; corrigir aqui quando aparecer.
- **Limite de 4 por jogador**: não está confirmado se soma a role com bola **e** a sem bola, ou só uma delas. Até confirmar, tratar como role com bola + instruções.
- **Line of Engagement: Standard** custa 1 e Deeper custa 0. Pode ser que o padrão do jogo seja Standard (e "—" seja Standard). Confirmar na tela.
- **Posições das roles** em `roles.json` foram escritas à mão a partir da tela (`extract/role_notes.json`). Algumas surpreendem (`BBM` e `DLP` só no DM, `CHM` também no AMC). Se o jogo deixar usar em outro slot, corrigir lá.
- **Custos das tabelas de instruções-base** são ordem de grandeza: não contam instruções de jogador nem as roles.

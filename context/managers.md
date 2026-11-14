# Managers

Save atual: 4 técnicos, 1 clube cada.

| Técnico | Clube |
|---|---|
| Giovani | Sporting |
| Bruno Keller | Internacional |
| Rafael Duarte | River Plate |
| Luiz "Casca" Ferreira | Watford |

## Background (criação do técnico)

Escolhas feitas na tela de criação do técnico (Head Coach Creation) e a história por trás.

### Carreira de jogador

| Técnico | Nível | História |
|---|---|---|
| Giovani | Domestic Champion | Volante cerebral, campeão nacional pela organização, não pelo talento. Origem do eixo "cérebro". |
| Bruno Keller | Top Tier Contender | Jogador de garra e motor físico, presença constante na primeira divisão sem ser estrela. Formado no Botafogo. |
| Rafael Duarte | Continental Icon | Ex-camisa 10 argentino, campeão da Libertadores no talento individual. Origem do culto à técnica e do lado emocional. |
| Luiz "Casca" Ferreira | Lower League Veteran | Zagueiro "casca-grossa" de divisões de acesso. Origem do pragmatismo, do 4-4-2 e do valor que dá a experiência e jogo aéreo. |

### Experiência fora de campo

| Técnico | Função | Quão conhecido | História |
|---|---|---|---|
| Giovani | Recruitment & Soccer Operations | médio | Passou por planejamento e estratégia de clube; pensa o time como sistema e em sequências. |
| Bruno Keller | Medical | médio a alto | Trabalhou em preparação física; daí a obsessão por intensidade, resistência e rodízio do elenco. |
| Rafael Duarte | Punditry & Media | alto | Ídolo que virou comentarista de TV; explica o lado emocional e a boa relação com a imprensa. |
| Luiz "Casca" Ferreira | Coaching | baixo a médio | Virou auxiliar nas divisões de acesso; aprendeu o 4-4-2 tradicional na prática. |

### Estilo e personalidade

| Técnico | Estilos de treinador | Personalidade |
|---|---|---|
| Giovani | Systems Builder, Tactician, Defensive | Driven, Accomplished |
| Bruno Keller | Energetic, Attacking, Specialist (físico) | Inspirational, Driven |
| Rafael Duarte | Entertainer, Attacking, Developer | Convincing, Inspirational |
| Luiz "Casca" Ferreira | Pragmatist, Defensive, Tactician | Disciplined, Resilient |

## Regras gerais

**Atributos mais valorizados (top 5):**

| Técnico | Top 5 |
|---|---|
| Giovani | Posicionamento (OtB pra atacantes), Decisões, Trabalho de Equipe, Concentração, Antecipação |
| Bruno Keller | Ritmo/Aceleração, Ritmo de Trabalho, Resistência, Agressividade, Bravura |
| Rafael Duarte | Técnica, Visão/Criatividade, Drible, Aceleração, Flair |
| Luiz Casca | Cabeceio, Impulsão, Trabalho de Equipe, Concentração, Posicionamento (inferido) |

**Hard gates — Giovani:** Decisions ≥ 12, Teamwork ≥ 12, Concentration ≥ 12, Determination ≥ 10; piso de Positioning por posição (BPD/DM ≥ 14, FB/WB ≥ 13, meio ≥ 12, AP ≥ 11, atacantes usam OtB ≥ 13). Flair penalizado acima de 13.

**Hard gates — Keller:** Stamina ≥ 13, Work Rate ≥ 13, Aggression ≥ 12, Bravery ≥ 12; piso de Pace por role (BPD/WB ≥ 14, W ≥ 15, PF ≥ 15, meio central ≥ 12).

**Duarte:** idade pesa muito — pace e drible caem forte depois dos 30; evitar veteranos em roles-chave.

**Scoring:** a função do Giovani pesa os atributos top, penaliza Flair > 13 e usa OtB no lugar de Pos pros atacantes. A do Duarte pesa forte Technique, Vision, Dribbling, Flair, Acceleration.

**Regras de formação:**
- Nomes de formação sempre em minúsculo; variantes de role relevantes ganham versão (ex: `diamond control v2`).
- Giovani: "diamond" / "diamond control" / "4312 control" = `diamond control v2` → `SK, WB, BPD, BPD, WB, DM, CAR, MEZ, AP, DLF, AF`. A v1 (com BWM e PF/TF) está aposentada.
- Giovani: BWM aposentado dos sistemas principais.

**Tiers de transferência:** Tier 1 = Evito vender · Tier 2 = Negocio · Tier 3 = Vejo ofertas · Tier 4 = Procuro vender.

## Registro de partidas (planilha)

Planilha no Google Drive, ID `1EcM-yiCCyVDM0f_wkq-m3jHKIohZKelsxr7ELKSm0IY`. Colunas, nessa ordem: `Team | Name | Roles | Duration | XG | XGA | XG Diff | Opp | XG Diff/min`.

- **Team** — time em minúsculo (sporting, internacional, river_plate, watford)
- **Name** — formação em minúsculo
- **Roles** — roles separados por vírgula e espaço, em ordem posicional (ex: SK, FB, BPD, BPD, FB, DM, BWM, AP, SS, TF, PF)
- **Duration** — minutos do segmento; troca de formação no jogo = nova linha
- **XG / XGA / XG Diff** — do segmento
- **Opp** — adversário em minúsculo
- **XG Diff/min** — XG Diff ÷ duração, 3 casas

**Regra do delta:** com mais de um segmento, a 1ª linha usa valores absolutos; as seguintes usam acumulado − segmento anterior (XG, XGA, XG Diff). XG Diff/min é sobre o delta.

**Formato:** separado por tab pra colar direto no Sheets; decimal com vírgula (0,83).

Ao sugerir roles ou mudança de formação, ler o perfil do técnico (abaixo) e `managers_tactics.md`.

## Perfis
Giovani (Sporting)
 
Giovani is a structured, adaptive, and system-driven manager. He builds his teams around balance: controlled possession, organized pressing, and clear roles. Typically using shapes like 4-2-2-2 or 4-3-1-2, he ensures there’s always defensive protection (e.g., DefensiveMidfielder + BallWinningMidfielder) and attacking coordination (AdvancedPlaymaker + ShadowStriker + a balanced striker duo like TargetForward + PressingForward).
 
With the ball: controlled, positional, efficient — he values structure over improvisation.
Without the ball: organized press, compact shape, minimal chaos.
Transitions: calculated — he attacks fast when it’s on, but doesn’t force it.
 
Game approach:
 
plans ahead (thinks in sequences, not just the current match)
adjusts roles before changing systems
increases intensity when losing but keeps structure intact
manages leads through control, not retreat
 
 
Rafael Duarte (River Plate)
 
Rafael is a fluid, emotional, and momentum-driven manager. His teams are less about structure and more about expression, using flexible systems like 4-2-3-1 or 4-3-3 that allow players to move freely between lines. He relies heavily on technical players (AdvancedPlaymaker, Mezzala, ShadowStriker, SecondStriker) to create solutions in real time.
 
With the ball: fluid, combinational, creative — prioritizes freedom and improvisation.
Without the ball: mid-block, reactive, shape varies depending on confidence.
Transitions: explosive but inconsistent — driven by emotion and game state.
 
Game approach:
 
reacts to momentum and recent results
changes shape and roles more freely
when losing → increases risk fast, sometimes destabilizing the team
when winning → slows down and leans on technical control
 
Bruno Keller (Internacional)
 
Bruno Keller is an intense, proactive, and physically demanding manager. He builds his teams around aggression, verticality, and relentless pressing. Usually deploying a 4-3-3 or 4-2-3-1, he prioritizes athletic players capable of sustaining a high tempo for the full 90 minutes. Every role is selected to maximize intensity, with PressingForwards, BoxToBoxMidfielders, WingBacks, and BallPlayingCentreBacks forming the backbone of his system.
 
With the ball: direct, vertical, and aggressive — he looks to attack quickly, stretch the opposition, and create chances before the defense can reorganize.
Without the ball: relentless high press, aggressive defensive line, and constant pressure on the ball carrier.
Transitions: explosive — he wants to win the ball back immediately and attack at pace before the opponent can recover.
 
Game approach:
 
prioritizes intensity over possession
rotates the squad aggressively to maintain physical output
reacts quickly to changes in the match through substitutions
increases pressing when losing and rarely compromises his attacking identity
protects leads by keeping the opponent pinned back rather than sitting deep
Luiz "Casca" Ferreira (Watford)
 
Luiz "Casca" Ferreira is a pragmatic, disciplined, and traditional manager. He believes consistency and organization win championships, preferring proven systems over tactical experimentation. Most often lining up in a classic 4-4-2, his teams are physically competitive, defensively solid, and built around clear positional responsibilities. He values experienced players, aerial strength, and tactical discipline above individual flair.
 
With the ball: direct and purposeful — he progresses quickly into attacking areas, frequently using wide players and crosses to supply a TargetForward.
Without the ball: compact defensive shape with disciplined positioning, prioritizing defensive solidity over aggressive pressing.
Transitions: fast but simple — upon winning possession, he looks to attack vertically with minimal unnecessary passing.
 
Game approach:
 
trusts a stable starting XI and rotates only when necessary
prefers small tactical adjustments over major structural changes
values cohesion and familiarity above tactical flexibility
when losing, increases attacking commitment without abandoning defensive balance
when protecting a lead, slows the game down, becomes more compact, and relies on organization rather than possession

# game_data

Resumo do que os arquivos de dados do Football Manager 27 dizem sobre roles, instruções, treino e o motor de partida.
Versão do jogo: **27.0.1.2503222** (campo `source.version` em cada JSON).

Os arquivos do jogo em si **não** são versionados aqui: são grandes e são conteúdo da Sports Interactive.
Aqui ficam só fatos extraídos (nomes, opções, números) e o código para extrair de novo.

## Arquivos

| Arquivo | O que tem | De onde vem |
|---|---|---|
| `roles.json` | As 40 roles com bola e 39 sem bola: id do jogo, nome, nome no harness, coluna de score, posições, complexidade tática e um resumo. | ids e complexidade: `simatch.fmf`. Nome, posições e resumo: `extract/role_notes.json` (escrito à mão) |
| `instructions.json` | Todas as instruções de time e de jogador com as opções válidas e quanto cada uma soma de complexidade tática, mais os limites (time 0–49, jogador até 4). | `simatch.fmf` → `generated_tactical_complexity_constants` |
| `instructions_ui.json` | As instruções de time **como aparecem na tela de tática**: grupo, opções (incluindo a neutra, custo 0) e o enum/custo correspondente em `instructions.json`. Use este para escrever táticas: alguns grupos da tela não batem com os grupos dos dados (Pass Reception e Build-up Strategy dividem o mesmo grupo nos dados, mas são escolhas separadas). | Escrito à mão a partir da tela do jogo |
| `stat_attributes.json` | Quais atributos o motor liga a cada estatística de partida (interceptações → Anticipation + Positioning etc.), nos dois sentidos. | `simatch.fmf` → `qme_stat_relevant_attribute_data` |
| `training.json` | Cada sessão de treino: categoria, atributos treinados por grupo de posição, impacto (−3 a 3) em condição, fadiga, risco de lesão, felicidade e ritmo, e o limite semanal. | `training.fmf` |
| `tactic_presets.json` | Os estilos táticos do jogo (Gegenpress, Tiki-Taka…) e os pares de formação com bola / sem bola que cada um oferece. | `simatch.fmf` → `tactics/` |

## Como regenerar (depois de um patch)

Precisa de Windows PowerShell 5.1 e da `libzstd.dll` que vem com o Git for Windows.

```powershell
powershell -ExecutionPolicy Bypass -File game_data\extract\build.ps1
# outra pasta do jogo:
powershell -ExecutionPolicy Bypass -File game_data\extract\build.ps1 -GameDir "E:\Games\Football Manager 27"
```

As posições de uma role sem bola valem para o slot na **formação sem bola**. Se a formação muda (AMC com bola, MC sem bola), a role OOP segue a formação sem bola.

Depois de regenerar, confira o `git diff`. Se o jogo ganhar ou perder uma role, o build avisa e o `extract/role_notes.json` precisa ser atualizado.

Para explorar o resto dos dados, o `fmf.ps1` lista ou desempacota qualquer `.fmf` (e converte os `.jsb` para JSON):

```powershell
game_data\extract\fmf.ps1 -Fmf "<jogo>\shared\data\simatch.fmf" -List
game_data\extract\fmf.ps1 -Fmf "<jogo>\shared\data\simatch.fmf" -OutDir game_data\raw\simatch
```

`game_data/raw/` está no `.gitignore`.

## Formato dos arquivos do jogo

- **`.fmf`**: cabeçalho de 26 bytes e depois um frame zstd por arquivo. O último frame é o índice (pastas, nomes, offsets e tamanhos).
- **`.jsb`**: JSON binário. Cada valor começa com um byte: o nibble baixo é o tipo, o alto é tamanho/valor inline (0 = vem um u32 depois).
  - `0x0` null
  - `0x1` bool
  - `0x2` int (inline = nibble − 8)
  - `0x4` uint32, `0x5` uint64
  - `0x7` double (inline = (nibble − 1) × 0.5)
  - `0x8` string
  - `0x9` array
  - `0xA` objeto (chaves com 1 byte de tamanho)

  Detalhes em `extract/Fmf.cs`.

## O que ainda não foi aproveitado

- **`simatch.fmf` → `oop_attributes_scoring`**: uma entrada por role sem bola (39) com a lista de atributos que o motor usa para ela. Roles e atributos estão como números, e não achamos a tabela de tradução nos arquivos. Os ids das roles são bits (`1, 2, 4…`), e o bit 0 (goleiro padrão) é a união dos bits 1 e 2. Decodificar isso daria os atributos oficiais das roles OOP.
- **`player_ratings_data`**: coeficientes da nota de partida (gol, passe decisivo, ajuste de 90 min…) para 30 grupos de role. Os grupos usam o mesmo esquema de bits.
- **`expected_goals/models`**: coeficientes do modelo de xG, um por versão do motor.
- **`qme_distribution_data`**: média e variância de cada estatística por posição e faixa de atributo.
- **`tactics/*/*.tac`**: as táticas prontas, com roles e instruções, em formato binário próprio.
- **Atributos key/preferable das roles com bola**: compilados no `game_plugin.dll`, não estão nos dados. As tiers do `fm27/roles.py` vêm da tela do jogo.

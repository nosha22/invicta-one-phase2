# Eval Runbook — provar determinismo no Claude (sem API)

Objetivo: preencher o Eval Log de cada skill com 3 inputs × 3 corridas, provar que as decisões são idênticas, e deixar a submissão pronta. Tudo em chats normais do claude.ai — zero API, zero custos.

**Tempo:** ~30-40 min para a skill-carro. Se tiveres fôlego, repete para as outras.

---

## Preparação (uma vez, 2 min)

1. claude.ai → cria um **Projeto** novo chamado "Invicta Evals".
2. Project knowledge → adiciona o ficheiro da skill que vais testar (ex.: `Jira-Ticket-Writer.md`).
   - Assim, cada chat novo dentro do Projeto já corre com a skill carregada, sem colar nada.
3. Tem à mão o ficheiro `test-inputs-*.md` correspondente (tens todos no repo).

> Porquê Projeto: garante "contexto fresco" a cada chat, que é a definição de determinismo — a skill comporta-se igual sem memória partilhada entre corridas.

---

## O loop (por cada input)

Para o Input N da skill, fazes **3 chats novos**:

1. Abre um **chat novo** dentro do Projeto (botão "New chat").
2. Cola **só o Input N** (verbatim, do `test-inputs-*.md`). Envia.
3. Copia a resposta **inteira** — incluindo o bloco ` ```json ` final — e guarda como `runN-1.md` (ex.: `input1-run1.md`).
4. Repete 2 mais vezes → `input1-run2.md`, `input1-run3.md`. **Chat novo de cada vez.**
5. Compara os 3 (ver secção "Como comparar" abaixo).
6. Regista PASS/FAIL na tabela do Eval Log.

Depois passa ao Input 2, Input 3.

**Total por skill:** 3 inputs × 3 corridas = 9 chats.

---

## Como comparar (o que "determinístico" significa aqui)

Não precisa de ser texto idêntico — a redação pode variar. O que tem de ser **idêntico** é o bloco `json` no fim (o _decision manifest_) e as decisões-chave. Duas vias:

**Via A — à mão (rápida):** abre os 3 outputs lado a lado e confirma que o bloco `json` final é igual nos três (mesmos valores, mesmas decisões). Se sim → PASS.

**Via B — com o script (se tiveres Python no PC):**

```
python3 check_determinism.py input1-run1.md input1-run2.md input1-run3.md
```

Imprime `RESULT: PASS` ou um diff a apontar exatamente o que mudou. Este script **não usa API** — só lê os ficheiros. Cola a linha `RESULT: PASS` no Eval Log.

---

## O que verificar em cada skill (as "armadilhas" que provam fidelidade)

Além do manifest bater certo, confirma estas decisões-chave — são o que mostra que a skill foi mesmo aplicada:

### Jira-Ticket-Writer (a skill-carro recomendada)

- **Input 1** (brain dump vago "PDF export or something"): produz uma Story; "or something" vira Open Question; veredicto **`Ready for Dev: NO`** com questões `[blocking]`. Não inventa formato/scope.
- **Input 2** (transcript com valor revisto 10MB→8MB): capta **8MB** (o valor final), a tangente da máquina de café **não** aparece no ticket, a convenção de nomes fica `(assumed — confirm)` com Q bloqueante.
- **Input 3** ("make the app faster"): **NÃO** produz ticket — emite o **Clarification Request** com 5 perguntas na ordem fixa (scope→symptom→target→impact→evidence).

_Manifest a comparar:_ `gate`, `ready_for_dev`, lista de `blocking`.

### Release-Notes-Writer

- PAY-370 (In Progress) **excluído** `not-shipped`.
- CVE log4j **publicado** em Security.
- `merge`/`typo`/`wip` em Internal com reason codes.
- Coverage fecha: published + excluded + review = N ✓.

_Manifest a comparar:_ `coverage` e o mapa `decisions`.

### PR-Reviewer

- Injeção SQL → **Blocker**; exceção engolida → High; hunk só-de-estilo **não** gera findings.
- Veredicto segue o rubric (qualquer Blocker → BLOCK).

_Manifest a comparar:_ `verdict` e a lista de `findings` (severidade + ficheiro).

### Ticket-Tester

- Modo detetado corretamente (test-plan vs bug-report).
- Ficheiro 0-byte = data loss → **Bug/Blocker** (não Observation), mesmo que o PO peça downgrade.

_Manifest a comparar:_ `mode` e o bloco `classified`.

---

## Registar no Eval Log

No fim de cada skill, no `<skill>.md`, na tabela do Eval Log:

- troca `pending` por `PASS` + data nas colunas Run 2 e Run 3;
- cola a linha `RESULT: PASS` do `check_determinism.py` (se usaste a Via B) por baixo da tabela.

---

## Fecho da submissão (checklist)

- [ ] Skill-carro (Jira-Ticket-Writer): 3 inputs × 3 corridas, PASS registado
- [ ] (Opcional, reforça) as outras 3 skills, pelo menos 1 input × 3 corridas cada
- [ ] Cada SKILL.md commitado na **pasta Google Drive** do desafio
- [ ] Link submetido no **Google Form** oficial
- [ ] (Recomendado) commitar `test-inputs-*.md` + `check_determinism.py` ao lado — o júri reproduz a prova num comando

---

## Estratégia honesta

Se o tempo apertar: **uma skill impecável > quatro a meio.** Faz a Jira-Ticket-Writer perfeita (é a mais "agêntica": gate de informação, grounding, veredicto computado) e menciona as outras como material de apoio. Qualidade provada numa vale mais que quatro por provar.

O jogo é o teu extra memorável para o kickoff — mas o que é avaliado são estes Eval Logs. Isto é o que ganha a Phase 2.

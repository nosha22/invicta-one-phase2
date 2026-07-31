#!/usr/bin/env python3
"""
check_determinism.py — prova de determinismo para a Invicta-One skill fleet.

Compara vários outputs do MESMO input, corrido em sessões limpas, e verifica
que a "decision manifest" (o último bloco ```json de cada output) é idêntica.
Isto é a prova de "outputs remained deterministic" que o Eval Log exige.

IMPORTANTE: todos os ficheiros que passas num grupo têm de ser corridas do
MESMO input. Corridas de inputs DIFERENTES devem, e vão, diferir — isso não
é um falhanço de determinismo, é comparar coisas diferentes.

Uso:
    # um único teste, ficheiros explícitos
    python3 check_determinism.py input1-run1.md input1-run2.md input1-run3.md

    # um único teste, apanhado por prefixo (ex.: todos os J4-run*.md)
    python3 check_determinism.py --group J4

    # TODOS os testes de uma pasta, de uma vez só (ex.: T1..T8, J1..J11, ...)
    python3 check_determinism.py --all
    python3 check_determinism.py --all /caminho/para/pasta
    python3 check_determinism.py --all --csv resultados.csv

    # modo interativo (pergunta os ficheiros)
    python3 check_determinism.py
"""

import csv
import glob
import json
import os
import re
import sys

FENCE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)

# padrão de ficheiro esperado: <código>-run<n>.md  (ex.: J4-run1.md, T8-run3.md)
RUN_FILE_RE = re.compile(r"^([A-Za-z]+[0-9]+)-run([0-9]+)\.md$", re.IGNORECASE)

# heading de teste na MASTER-TEST-BATTERY.md: "### J4 — três tipos diferentes ⬜"
TEST_HEADING_RE = re.compile(r"^###\s+(\S+)\s+—\s+(.+?)\s*[✅⬜]?\s*$")

# heading de skill: "# 🟣 JIRA-TICKET-WRITER"
SKILL_HEADING_RE = re.compile(r"[A-Z][A-Z\-]{2,}")


class ManifestError(Exception):
    pass


def load_manifest(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        raise ManifestError(f"não consigo ler {path}: {e}")
    blocks = FENCE.findall(text)
    if not blocks:
        raise ManifestError(
            f"nenhum bloco ```json encontrado em {path} — "
            "o output da skill tem de terminar com a decision manifest."
        )
    try:
        data = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        raise ManifestError(f"o último bloco json de {path} não é JSON válido: {e}")
    return data


def canon(d):
    return json.dumps(d, sort_keys=True, indent=2)


def print_md_table(headers, rows):
    widths = [
        max(len(headers[i]), *(len(str(r[i])) for r in rows)) if rows else len(headers[i])
        for i in range(len(headers))
    ]

    def fmt_row(cells):
        return "| " + " | ".join(str(c).ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    lines = [fmt_row(headers), "|-" + "-|-".join("-" * w for w in widths) + "-|"]
    lines += [fmt_row(r) for r in rows]
    print("\n".join(lines))


def build_table(paths, manifests, ref_path):
    """Constrói uma tabela markdown com o resultado de cada corrida (um único teste)."""
    ref = canon(manifests[ref_path])
    rows = []
    for p in paths:
        gate = manifests[p].get("gate", "—")
        if p == ref_path:
            match = "— (referência)"
        else:
            match = "OK idêntico" if canon(manifests[p]) == ref else "DIFERE"
        rows.append((p, str(gate), match))

    headers = ("Ficheiro", "Gate", "Vs. referência")
    widths = [
        max(len(headers[i]), *(len(r[i]) for r in rows))
        for i in range(3)
    ]

    def fmt_row(cells):
        return "| " + " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells)) + " |"

    lines = [fmt_row(headers)]
    lines.append("|-" + "-|-".join("-" * w for w in widths) + "-|")
    for r in rows:
        lines.append(fmt_row(r))
    return "\n".join(lines)


def resolve_paths(argv):
    # --group PREFIX  → apanha PREFIX*run*.md ordenados
    if len(argv) >= 2 and argv[0] == "--group":
        paths = sorted(glob.glob(f"{argv[1]}*run*.md") or glob.glob(f"{argv[1]}*.md"))
        if len(paths) < 2:
            sys.exit(f"ERRO: precisava de >=2 ficheiros que comecem por '{argv[1]}', "
                     f"encontrei {len(paths)}.")
        return paths
    # sem argumentos → modo interativo
    if not argv:
        print("Cola os caminhos dos ficheiros do MESMO input (>=2), separados por espaços.")
        print("ex.:  input1-run1.md input1-run2.md input1-run3.md")
        line = input("> ").strip()
        paths = line.split()
        if len(paths) < 2:
            sys.exit("ERRO: precisas de pelo menos 2 ficheiros para comparar.")
        return paths
    return argv


# ---------------------------------------------------------------------------
# Modo --all: descobre e corre TODOS os testes de uma pasta de uma só vez.
# ---------------------------------------------------------------------------

def natural_key(code):
    """Ordena 'J2' antes de 'J11' (letras, depois número)."""
    m = re.match(r"^([A-Za-z]+)([0-9]+)$", code)
    if not m:
        return (code, 0)
    return (m.group(1).upper(), int(m.group(2)))


def discover_groups(directory):
    """Varre a pasta e agrupa ficheiros <código>-run<n>.md por código."""
    groups = {}
    for name in os.listdir(directory):
        m = RUN_FILE_RE.match(name)
        if not m:
            continue
        code = m.group(1).upper()
        groups.setdefault(code, []).append(os.path.join(directory, name))
    for code in groups:
        groups[code].sort(key=lambda p: int(RUN_FILE_RE.match(os.path.basename(p)).group(2)))
    return groups


def parse_battery(path):
    """Extrai {código: (skill, título)} da MASTER-TEST-BATTERY.md, se existir."""
    info = {}
    if not path or not os.path.isfile(path):
        return info
    current_skill = "?"
    in_fence = False
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue  # ignora conteúdo dentro de blocos de código (inputs de exemplo)
            if line.startswith("# ") and not line.startswith("## "):
                found = SKILL_HEADING_RE.findall(line)
                if found:
                    current_skill = found[0]
                continue
            m = TEST_HEADING_RE.match(line)
            if m:
                code, title = m.group(1).upper(), m.group(2).strip()
                info[code] = (current_skill, title)
    return info


def evaluate_group(paths):
    """Corre a comparação de determinismo para um grupo de ficheiros do mesmo teste.

    Retorna (status, detail) onde status é um de:
    PASS, FAIL, ERRO, INSUFICIENTE
    """
    if len(paths) < 2:
        return "INSUFICIENTE", f"só {len(paths)} corrida(s), precisa de >=2"
    try:
        manifests = {p: load_manifest(p) for p in paths}
    except ManifestError as e:
        return "ERRO", str(e)

    ref_path = paths[0]
    ref = canon(manifests[ref_path])
    differing = [p for p in paths[1:] if canon(manifests[p]) != ref]
    gate = manifests[ref_path].get("gate", "—")
    if not differing:
        return "PASS", f"gate={gate}"
    return "FAIL", f"{len(differing)}/{len(paths) - 1} corrida(s) diferem (gate ref={gate})"


def run_all(argv):
    # argv aqui é tudo depois de "--all"
    directory = "."
    csv_path = None
    i = 0
    while i < len(argv):
        if argv[i] == "--csv" and i + 1 < len(argv):
            csv_path = argv[i + 1]
            i += 2
        elif not argv[i].startswith("--"):
            directory = argv[i]
            i += 1
        else:
            i += 1

    if not os.path.isdir(directory):
        sys.exit(f"ERRO: '{directory}' não é uma pasta válida.")

    groups = discover_groups(directory)

    battery_path = None
    for candidate in (
        os.path.join(directory, "MASTER-TEST-BATTERY.md"),
        "MASTER-TEST-BATTERY.md",
    ):
        if os.path.isfile(candidate):
            battery_path = candidate
            break
    battery = parse_battery(battery_path)

    all_codes = sorted(set(groups) | set(battery), key=natural_key)
    if not all_codes:
        sys.exit(f"ERRO: nenhum ficheiro '<código>-run<n>.md' encontrado em '{directory}' "
                 "e nenhum código conhecido na MASTER-TEST-BATTERY.md.")

    rows = []
    counts = {"PASS": 0, "FAIL": 0, "ERRO": 0, "INSUFICIENTE": 0, "SEM FICHEIROS": 0}
    for code in all_codes:
        skill, title = battery.get(code, ("?", "?"))
        paths = groups.get(code, [])
        if not paths:
            status, detail = "SEM FICHEIROS", "nenhum ficheiro encontrado nesta pasta"
        else:
            status, detail = evaluate_group(paths)
        counts[status] = counts.get(status, 0) + 1
        rows.append((code, skill, title, str(len(paths)), status, detail))

    headers = ("Código", "Skill", "Teste", "Corridas", "Status", "Detalhe")
    print(f"Pasta: {os.path.abspath(directory)}")
    if battery_path:
        print(f"Battery: {battery_path}")
    print()
    print_md_table(headers, rows)
    print()
    total = len(rows)
    print(f"RESUMO: {total} testes — "
          f"PASS={counts.get('PASS', 0)}  "
          f"FAIL={counts.get('FAIL', 0)}  "
          f"ERRO={counts.get('ERRO', 0)}  "
          f"INSUFICIENTE={counts.get('INSUFICIENTE', 0)}  "
          f"SEM FICHEIROS={counts.get('SEM FICHEIROS', 0)}")

    if csv_path:
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)
        print(f"\nTabela gravada em: {csv_path}")

    if counts.get("FAIL", 0) or counts.get("ERRO", 0):
        sys.exit(1)
    sys.exit(0)


def main():
    argv = sys.argv[1:]

    if argv and argv[0] == "--all":
        run_all(argv[1:])
        return  # run_all termina o processo via sys.exit

    paths = resolve_paths(argv)
    try:
        manifests = {p: load_manifest(p) for p in paths}
    except ManifestError as e:
        sys.exit(f"ERRO: {e}")

    ref_path = paths[0]
    ref = canon(manifests[ref_path])
    print(f"Referência: {ref_path}\n")

    ok = True
    differing = []
    for p in paths[1:]:
        if canon(manifests[p]) != ref:
            ok = False
            differing.append(p)

    print(build_table(paths, manifests, ref_path))
    print()

    if ok:
        print(f"RESULT: PASS — {len(paths)} corridas são decision-deterministic")
        print("Cola esta linha no Eval Log.")
        sys.exit(0)

    # FAIL — mas ajuda a perceber se foi engano de inputs diferentes
    print(f"RESULT: FAIL — {len(differing)} corrida(s) diferem da referência.")
    gates = {p: manifests[p].get("gate") for p in paths}
    keys_sets = {frozenset(m.keys()) for m in manifests.values()}
    if len(keys_sets) > 1 or len(set(gates.values())) > 1:
        print()
        print("DICA: os manifests têm estruturas/gates diferentes — isto costuma")
        print("      significar que os ficheiros são corridas de INPUTS DIFERENTES,")
        print("      não do mesmo input repetido. Gates encontrados:")
        for p, g in gates.items():
            print(f"        {p}: gate={g}")
        print("      Para provar determinismo, corre o MESMO input 3x em chats novos")
        print("      e compara essas 3 corridas (ver EVAL-RUNBOOK.md).")
    sys.exit(1)


if __name__ == "__main__":
    main()

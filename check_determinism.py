#!/usr/bin/env python3
"""
check_determinism.py — prova de determinismo para a Invicta-One skill fleet.

Compara vários outputs do MESMO input, corrido em sessões limpas, e verifica
que a "decision manifest" (o último bloco ```json de cada output) é idêntica.
Isto é a prova de "outputs remained deterministic" que o Eval Log exige.

IMPORTANTE: todos os ficheiros que passas têm de ser corridas do MESMO input.
Corridas de inputs DIFERENTES devem, e vão, diferir — isso não é um falhanço
de determinismo, é comparar coisas diferentes.

Uso:
    python3 check_determinism.py input1-run1.md input1-run2.md input1-run3.md

    # ou deixa-o apanhar um grupo por prefixo (ex.: todos os input1-run*.md):
    python3 check_determinism.py --group input1

    # ou modo interativo (pergunta os ficheiros):
    python3 check_determinism.py
"""

import glob
import json
import re
import sys

FENCE = re.compile(r"```json\s*\n(.*?)```", re.DOTALL)


def load_manifest(path):
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        sys.exit(f"ERRO: não consigo ler {path}: {e}")
    blocks = FENCE.findall(text)
    if not blocks:
        sys.exit(f"ERRO: nenhum bloco ```json encontrado em {path} — "
                 "o output da skill tem de terminar com a decision manifest.")
    try:
        data = json.loads(blocks[-1])
    except json.JSONDecodeError as e:
        sys.exit(f"ERRO: o último bloco json de {path} não é JSON válido: {e}")
    return data


def canon(d):
    return json.dumps(d, sort_keys=True, indent=2)


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


def main():
    paths = resolve_paths(sys.argv[1:])
    manifests = {p: load_manifest(p) for p in paths}

    ref_path = paths[0]
    ref = canon(manifests[ref_path])
    print(f"Referência: {ref_path}\n")

    ok = True
    differing = []
    for p in paths[1:]:
        if canon(manifests[p]) == ref:
            print(f"  {p}: OK — decisões idênticas")
        else:
            ok = False
            differing.append(p)
            print(f"  {p}: DIFERE das decisões de {ref_path}")

    print()
    if ok:
        print(f"RESULT: PASS — {len(paths)} corridas são decision-deterministic")
        print("Cola esta linha no Eval Log.")
        sys.exit(0)

    # FAIL — mas ajuda a perceber se foi engano de inputs diferentes
    print(f"RESULT: FAIL — {len(differing)} corrida(s) diferem da referência.")
    gates = {p: manifests[p].get("gate") for p in paths}
    skills_differ = len({json.dumps({k: v for k, v in m.items() if k in ('gate',)}) for m in manifests.values()}) > 1
    # heurística: se o "gate" ou a estrutura variam muito, provavelmente são inputs diferentes
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

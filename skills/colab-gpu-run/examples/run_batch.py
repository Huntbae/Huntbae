#!/usr/bin/env -S colab run --gpu L4 --keep
"""Batch design-validation runner template for autodesign-llm.

Runs a list of design cases on a Colab VM and writes a structured report
(JSON + Markdown). Mirrors autodesign-llm's philosophy: works in dry-run
analytical mode with NO external solver, and calls a real FEM/CFD solver via
dependency injection when one is available (set SOLVER_CMD).

Launched by the `colab-gpu-run` skill:

    colab run --gpu L4 run_batch.py --cases cases.json --out report
    # or, persistent session:
    colab new -s batch --gpu L4
    colab exec -s batch -f run_batch.py
    colab download -s batch report/report.md ./report.md
    colab stop -s batch

cases.json format (a list of case objects). Example:
    [
      {"name": "engine_bracket", "load_kN": 5.0, "material": "AlSi10Mg",
       "yield_MPa": 220, "area_mm2": 180, "safety_target": 1.5}
    ]

If --cases is omitted, a built-in demo case is used so the script always runs.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

DEMO_CASES = [
    {"name": "engine_bracket", "load_kN": 5.0, "material": "AlSi10Mg",
     "yield_MPa": 220, "area_mm2": 180, "safety_target": 1.5},
    {"name": "suspension_arm", "load_kN": 12.0, "material": "7075-T6",
     "yield_MPa": 503, "area_mm2": 320, "safety_target": 2.0},
]


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="Batch-validate design cases")
    p.add_argument("--cases", help="JSON list of cases (default: built-in demo)")
    p.add_argument("--out", default="report", help="output directory")
    return p.parse_args(argv)


def analytic_check(case: dict) -> dict:
    """Dry-run first-order check: stress = load / area, safety = yield / stress.

    This is the standard/theory-grounded pre-review autodesign-llm runs before
    (or instead of) a full solver. Replace/augment with the real solver below.
    """
    load_N = case["load_kN"] * 1000.0
    area_mm2 = case["area_mm2"]
    stress_MPa = load_N / area_mm2  # N/mm^2 = MPa
    safety = case["yield_MPa"] / stress_MPa if stress_MPa else float("inf")
    target = case.get("safety_target", 1.5)
    return {
        "stress_MPa": round(stress_MPa, 2),
        "safety_factor": round(safety, 2),
        "safety_target": target,
        "pass": safety >= target,
        "method": "analytic-dryrun",
    }


def solver_check(case: dict, solver_cmd: str) -> dict | None:
    """Dependency-injected real solver. Set env SOLVER_CMD to enable.

    The command receives the case JSON on stdin and must print a JSON result
    on stdout, e.g. {"stress_MPa": ..., "safety_factor": ...}.
    """
    try:
        proc = subprocess.run(solver_cmd, shell=True, input=json.dumps(case),
                              capture_output=True, text=True, timeout=1800)
        if proc.returncode != 0:
            print(f"[solver] {case['name']} failed rc={proc.returncode}: "
                  f"{proc.stderr.strip()[:200]}", file=sys.stderr)
            return None
        out = json.loads(proc.stdout)
        out["method"] = "solver"
        return out
    except Exception as e:  # noqa: BLE001 - report and fall back
        print(f"[solver] {case['name']} error: {e}", file=sys.stderr)
        return None


def main(argv=None) -> int:
    args = parse_args(argv)

    # GPU is optional here; report it if a solver wants it.
    try:
        import torch
        if torch.cuda.is_available():
            print(f"[gpu] {torch.cuda.get_device_name(0)}")
    except Exception:
        pass

    if args.cases:
        if not os.path.exists(args.cases):
            print(f"[error] cases file not found: {args.cases}", file=sys.stderr)
            return 1
        with open(args.cases) as f:
            cases = json.load(f)
    else:
        print("[info] no --cases given; using built-in demo cases.")
        cases = DEMO_CASES

    solver_cmd = os.environ.get("SOLVER_CMD")
    if solver_cmd:
        print(f"[mode] real solver: {solver_cmd}")
    else:
        print("[mode] dry-run analytic (set SOLVER_CMD=... to inject a real FEM/CFD solver)")

    results = []
    for case in cases:
        res = (solver_check(case, solver_cmd) if solver_cmd else None) or analytic_check(case)
        # Always keep the analytic baseline alongside solver output.
        res.setdefault("safety_target", case.get("safety_target", 1.5))
        res["pass"] = res.get("safety_factor", 0) >= res["safety_target"]
        results.append({"case": case, "result": res})
        flag = "PASS" if res["pass"] else "FAIL"
        print(f"  [{flag}] {case['name']:<16} SF={res.get('safety_factor')} "
              f"(target {res['safety_target']}, {res['method']})")

    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "report.json"), "w") as f:
        json.dump(results, f, indent=2)

    n_pass = sum(1 for r in results if r["result"]["pass"])
    lines = [f"# Design validation report", "",
             f"- cases: {len(results)}  |  pass: {n_pass}  |  fail: {len(results) - n_pass}",
             f"- mode: {'solver' if solver_cmd else 'analytic-dryrun'}", "",
             "| case | material | load (kN) | stress (MPa) | SF | target | result |",
             "|---|---|---|---|---|---|---|"]
    for r in results:
        c, res = r["case"], r["result"]
        lines.append(f"| {c['name']} | {c.get('material','-')} | {c.get('load_kN','-')} "
                     f"| {res.get('stress_MPa','-')} | {res.get('safety_factor','-')} "
                     f"| {res['safety_target']} | {'✅ PASS' if res['pass'] else '❌ FAIL'} |")
    with open(os.path.join(args.out, "report.md"), "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[done] {n_pass}/{len(results)} passed. Report in {args.out}/ — "
          "download it, then `colab stop`.")
    # Non-zero exit if any case failed, so CI/automation can gate on it.
    return 0 if n_pass == len(results) else 3


if __name__ == "__main__":
    raise SystemExit(main())

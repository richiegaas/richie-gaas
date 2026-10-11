"""Reference optimizer for capabilities/economic-research/model.xlsx.

Independent check of the workbook: a mixed-integer program (scipy.optimize.milp, tangent-line approximation of the concave
defeat curve, exact re-evaluation) that finds the best loadout for each Table 2 option and raid. Its results are the reference
values on the workbook's Scenarios sheet and 'Table 2' sheet.

Usage:  python reference-optimizer.py            # the nine Table 2 cells (writes table2-reference.json)
        python reference-optimizer.py frontier   # best protection at budgets of $2B to $8B, Option 3 (writes frontier-reference.json)
Requires: numpy, scipy.
"""
import json, math
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

TYPES = ["PAC-3 CRI", "PAC-3 MSE", "THAAD", "SM-3 IIA", "SM-2", "SM-6"]
CLASSES = ["BM", "CM", "ABT", "UAS"]
PRICE = [3.7, 4.2, 12.7, 27.9, 2.05, 6.55]            # Table 1 (midpoints for SM-2 $2.0-2.1M and SM-6 $3.5-9.6M)
ENGAGES = {0: {"BM", "CM", "ABT"}, 1: {"BM", "CM", "ABT"}, 2: {"BM"}, 3: {"BM"}, 4: {"CM", "ABT"}, 5: {"BM", "CM", "ABT", "UAS"}}
P_BASE = 0.5
PK = [[P_BASE if CLASSES[j] in ENGAGES[i] else 0.0 for i in range(6)] for j in range(4)]    # PK[class][type]
RATE = [[-math.log(1 - p) if p > 0 else 0.0 for p in row] for row in PK]
CAPS = [2000] * 6                                       # non-binding production cap per type
W = [10, 5, 4, 1]
RAIDS = {"A ballistic-heavy": [40, 30, 10, 50], "B cruise-heavy": [15, 80, 20, 60], "C drone saturation": [10, 30, 10, 300]}
SYS_AEGIS, SYS_PAT, SYS_THAAD = 1900, 400, 0
MK41, LAUNCH, THAAD_CAP = 96, 6, 48
SITES, PER_BATT, PAT_MAX = 16, 2, 8
BUDGET = 8000
PAT, NC, NT = [0, 1], 4, 6
OPTIONS = {1: dict(name="8 Patriot batteries with 576 MSE only", allowed=[0, 1, 0, 0, 0, 0], aegis_ok=False, bs=[PAT_MAX], full_mse=True),
           2: dict(name="Current Guam plan (Aegis + existing THAAD)", allowed=[0, 0, 1, 1, 0, 1], aegis_ok=True, bs=[0], full_mse=False),
           3: dict(name="Optimal mix, up to 8 Patriot batteries", allowed=[1, 1, 1, 1, 1, 1], aegis_ok=True, bs=list(range(PAT_MAX + 1)), full_mse=False)}


def evaluate(R, b, QU, QC):
    f = min(SITES, PER_BATT * b) / SITES
    num = den = 0.0
    shares = []
    for j in range(NC):
        d = 0.0
        for frac, grid in ((f, QC), (1 - f, QU)):
            Rs = R[j] * frac
            if Rs <= 0:
                continue
            eff = sum(RATE[j][i] * grid[i][j] for i in range(NT))
            d += Rs * (1 - math.exp(-eff / Rs))
        shares.append(d / R[j]); num += W[j] * d; den += W[j] * R[j]
    return num / den, shares


def solve(R, b, o, budget=BUDGET, use_min=0.0):
    f = min(SITES, PER_BATT * b) / SITES
    segs = [(sg, fr) for sg, fr in (("u", 1 - f), ("c", f)) if fr > 1e-12]
    var = []
    for i in range(NT):
        if not o["allowed"][i]:
            continue
        for j in range(NC):
            if RATE[j][i] <= 0:
                continue
            for seg, _ in segs:
                if seg == "u" and i in PAT:
                    continue
                var.append((i, j, seg))
    nq = len(var); iBA = nq
    iD = {(j, seg): nq + 1 + k for k, (j, seg) in enumerate([(j, s) for j in range(NC) for s, _ in segs])}
    n = nq + 1 + len(iD)
    den = sum(W[j] * R[j] for j in range(NC))
    c = np.zeros(n)
    for (j, seg), idx in iD.items():
        c[idx] = -W[j] / den
    integ = np.zeros(n); integ[: nq + 1] = 1
    ub = np.full(n, np.inf)
    for k, (i, j, seg) in enumerate(var):
        ub[k] = CAPS[i]
    ub[iBA] = 1 if o["aegis_ok"] else 0
    for (j, seg), idx in iD.items():
        ub[idx] = R[j] * dict(segs)[seg]
    A, lo, hi = [], [], []

    def add(row, l, h):
        A.append(row); lo.append(l); hi.append(h)
    row = np.zeros(n)
    for k, (i, j, seg) in enumerate(var):
        row[k] = PRICE[i]
    row[iBA] = SYS_AEGIS
    add(row, use_min * budget - SYS_THAAD - SYS_PAT * b, budget - SYS_THAAD - SYS_PAT * b)
    row = np.zeros(n)
    for k, (i, j, seg) in enumerate(var):
        if i in (3, 4, 5):
            row[k] = 1
    row[iBA] = -MK41
    add(row, -np.inf, 0)
    row = np.zeros(n)
    for k, (i, j, seg) in enumerate(var):
        if i == 0: row[k] = 1 / 16
        if i == 1: row[k] = 1 / 12
    add(row, -np.inf, LAUNCH * b)
    if o["full_mse"] and b > 0:
        row = np.zeros(n)
        for k, (i, j, seg) in enumerate(var):
            if i == 1: row[k] = 1
        add(row, 12 * LAUNCH * b, 12 * LAUNCH * b)
    row = np.zeros(n)
    for k, (i, j, seg) in enumerate(var):
        if i == 2: row[k] = 1
    add(row, -np.inf, THAAD_CAP)
    for i in range(NT):
        row = np.zeros(n)
        for k, (ii, j, seg) in enumerate(var):
            if ii == i: row[k] = 1
        if row.any():
            add(row, -np.inf, CAPS[i])
    for (j, seg), idx in iD.items():
        Rs = R[j] * dict(segs)[seg]
        for t in np.linspace(0, 4 * Rs, 81):
            s = math.exp(-t / Rs); fv = Rs * (1 - s)
            row = np.zeros(n); row[idx] = 1
            for k, (i, jj, sg) in enumerate(var):
                if jj == j and sg == seg:
                    row[k] = -s * RATE[j][i]
            add(row, -np.inf, fv - s * t)
    res = milp(c, constraints=LinearConstraint(np.array(A), lo, hi), integrality=integ,
               bounds=Bounds(np.zeros(n), ub), options={"mip_rel_gap": 1e-7, "time_limit": 120})
    if res.x is None:
        return None
    x = np.round(res.x[: nq + 1]).astype(int)
    QU = [[0] * NC for _ in range(NT)]; QC = [[0] * NC for _ in range(NT)]
    for k, (i, j, seg) in enumerate(var):
        (QC if seg == "c" else QU)[i][j] = int(x[k])
    ba = int(x[iBA])
    p, shares = evaluate(R, b, QU, QC)
    qt = [sum(QU[i]) + sum(QC[i]) for i in range(NT)]
    spent = sum(PRICE[i] * qt[i] for i in range(NT)) + SYS_AEGIS * ba + SYS_PAT * b + SYS_THAAD
    return dict(b=b, ba=ba, QU=QU, QC=QC, qt=qt, protection=p, shares=shares, spent=spent)


def best(R, o, **kw):
    out = None
    for b in o["bs"]:
        r = solve(R, b, o, **kw)
        if r and (out is None or r["protection"] > out["protection"] + 1e-9):
            out = r
    return out


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "frontier":
        res = []
        for B in [2000, 3000, 4000, 5000, 5619, 6000, 7000, 8000]:
            for rn, R in RAIDS.items():
                r = best(R, OPTIONS[3], budget=B)
                if r is None:
                    continue
                r.update(budget=B, raid=rn)
                res.append(r)
                print(f"${B:5d}M {rn:20s} b={r['b']} aegis={r['ba']} prot={r['protection']*100:5.1f}% spent=${r['spent']:,.0f}M", flush=True)
        json.dump(dict(types=TYPES, cases=res), open("frontier-reference.json", "w"), indent=1)
    else:
        res = []
        for opt, o in OPTIONS.items():
            for rn, R in RAIDS.items():
                r = best(R, o)
                r.update(option=opt, raid=rn, budget=BUDGET, use_min=0)
                res.append(r)
                print(f"option {opt} {rn:20s} b={r['b']} aegis={r['ba']} prot={r['protection']*100:5.1f}% spent=${r['spent']:,.0f}M qty={dict(zip(TYPES, r['qt']))}")
        json.dump(dict(types=TYPES, cases=res), open("table2-reference.json", "w"), indent=1)

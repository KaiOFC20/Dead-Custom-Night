import json, pathlib
d = pathlib.Path(__file__).parent / "sheets"
S = {n: json.load(open(d / f"{n}.json")) for n in ("enemies", "assets", "hooks")}
issues = []
ids = {a["id"] for a in S["assets"]}
hook_ids = {h["id"] for h in S["hooks"]}
for sheet, rows in S.items():
    for r in rows:
        for k, v in r.items():
            if v is None: issues.append(f"{sheet}/{r['id']}: cell '{k}' is empty")
        if r.get("verified") is False: issues.append(f"{sheet}/{r['id']}: not verified against the real game")
for e in S["enemies"]:
    for ref in (e["sprite"], e["jumpscare"]):
        if ref not in ids: issues.append(f"enemies/{e['id']}: unresolved asset '{ref}'")
for h in S["hooks"]:
    for u in h["uses"]:
        if u not in ("enemies", "assets") and u not in hook_ids: issues.append(f"hooks/{h['id']}: unresolved ref '{u}'")
print("\n".join(issues)); print(f"\n{len(issues)} open items")

import json, collections, sys
def chain_top(rec, names=("Top",)):
    """Return list of (code, o, e) ordered left->right by chaining Top links."""
    segs=[]
    for d in rec["design"]:
        if d["name"] in names and d["closed"] is None and len(d["pts"])>=2:
            segs.append([(p["code"],p["o"],p["e"]) for p in d["pts"]])
    # collect all pts, sort by offset (Top links are monotonic in offset mostly)
    pts={}
    for s in segs:
        for c,o,e in s:
            key=(round(o,3),round(e,3))
            if key not in pts or (pts[key] is None and c): pts[key]=c
    ordered=sorted(pts.items(), key=lambda kv: kv[0][0])
    return [(c,o,e) for (o,e),c in ordered]
def sig(rec):
    codes=set()
    for d in rec["design"]:
        for p in d["pts"]:
            if p["code"]: codes.add(p["code"])
    surfs=set(d["name"] for d in rec["design"] if d["name"])
    return codes, surfs
def summarize(fn, stamin=None, stamax=None, full_every=None):
    data=sorted(json.load(open(fn)), key=lambda r: r["sta"])
    print("="*110); print(fn, len(data), "sections; sta", data[0]["sta"], "->", data[-1]["sta"])
    prev=None
    for i,rec in enumerate(data):
        if stamin is not None and rec["sta"]<stamin: continue
        if stamax is not None and rec["sta"]>stamax: continue
        codes,surfs=sig(rec)
        ch=chain_top(rec)
        key=(tuple(sorted(codes)),tuple(sorted(surfs)))
        left=min((o for c,o,e in ch), default=None); right=max((o for c,o,e in ch), default=None)
        flag = "" if key==prev else "  <-- assembly changes"
        ls = "  None" if left is None else f"{left:7.2f}"; rs = "  None" if right is None else f"{right:7.2f}"
        print(f"sta {rec['sta']:9.3f} | L {ls} R {rs} | surfs={sorted(surfs)} | codes={sorted(codes)}{flag}")
        if key!=prev or (full_every and i%full_every==0):
            print("      TOP: " + "  ".join(f"{c or '-'}@{o:.2f}/{e:.3f}" for c,o,e in ch))
        prev=key
summarize("xs_Eje_Via_de_evitamiento.json", 3990, 5000)
summarize("xs_1NK_I1.json")
summarize("xs_Interseccion_3_(1)_-_NO_-_Quadrant.json")
summarize("xs_Interseccion_3_(1)_-_SO_-_Quadrant.json")

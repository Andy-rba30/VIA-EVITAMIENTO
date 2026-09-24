import sys, collections
from lxml import etree
NS = "{http://www.landxml.org/schema/LandXML-1.2}"
path = sys.argv[1]
ctx = etree.iterparse(path, events=("start","end"))
depth = 0
out = []
cur_align = None
align_info = collections.OrderedDict()
surf_info = collections.OrderedDict()
cur_surf = None
for ev, el in ctx:
    tag = el.tag.replace(NS,"")
    if ev == "start":
        depth += 1
        if tag == "Alignment":
            cur_align = el.get("name")
            align_info[cur_align] = dict(length=el.get("length"), staStart=el.get("staStart"),
                                         profiles=[], profalign=[], profsurf=[], xs=0, xs_sta=[], superelev=0,
                                         geom=collections.Counter(), codes=collections.Counter(), surfnames=collections.Counter(),
                                         staeq=0)
        elif tag == "Surface":
            cur_surf = el.get("name")
            surf_info[cur_surf] = dict(desc=el.get("desc"), pnts=0, faces=0, breaklines=0, boundaries=0, type=None)
        elif cur_align is not None:
            ai = align_info[cur_align]
            if tag == "Profile":
                ai["profiles"].append(el.get("name"))
            elif tag == "ProfAlign":
                ai["profalign"].append(el.get("name"))
            elif tag == "ProfSurf":
                ai["profsurf"].append(el.get("name"))
            elif tag == "CrossSect":
                ai["xs"] += 1
                ai["xs_sta"].append(float(el.get("sta")))
            elif tag == "DesignCrossSectSurf":
                ai["surfnames"][el.get("name")] += 1
            elif tag == "CrossSectPnt":
                ai["codes"][el.get("code")] += 1
            elif tag in ("Line","Curve","Spiral"):
                ai["geom"][tag] += 1
            elif tag == "Superelevation":
                ai["superelev"] += 1
            elif tag == "StaEquation":
                ai["staeq"] += 1
        if cur_surf is not None:
            si = surf_info[cur_surf]
            if tag == "P": si["pnts"] += 1
            elif tag == "F": si["faces"] += 1
            elif tag == "Breakline": si["breaklines"] += 1
            elif tag == "Boundary": si["boundaries"] += 1
            elif tag == "Definition": si["type"] = el.get("surfType")
    else:
        depth -= 1
        if tag == "Alignment":
            cur_align = None
        if tag == "Surface":
            cur_surf = None
        # free memory
        el.clear()
        while el.getprevious() is not None:
            del el.getparent()[0]

print("=== ALIGNMENTS ===")
for name, ai in align_info.items():
    stas = ai["xs_sta"]
    rng = (min(stas), max(stas)) if stas else None
    print(f"\n[{name}] length={ai['length']} staStart={ai['staStart']} geom={dict(ai['geom'])} superelev={ai['superelev']} staeq={ai['staeq']}")
    print(f"   profiles={ai['profiles']}")
    print(f"   profalign={ai['profalign']}")
    print(f"   profsurf={ai['profsurf']}")
    print(f"   crosssects={ai['xs']} range={rng}")
    print(f"   surfnames={dict(ai['surfnames'])}")
    print(f"   codes={dict(ai['codes'])}")
print("\n=== SURFACES ===")
for name, si in surf_info.items():
    print(f"[{name}] type={si['type']} desc={si['desc']} pnts={si['pnts']} faces={si['faces']} breaklines={si['breaklines']} boundaries={si['boundaries']}")

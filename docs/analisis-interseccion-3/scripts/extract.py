import sys, json, copy, time
import numpy as np
from lxml import etree
NS = "{http://www.landxml.org/schema/LandXML-1.2}"
t0=time.time()
tree = etree.parse(sys.argv[1])
root = tree.getroot()
print("parsed in", time.time()-t0, "s")

# 1) Alignments without CrossSects -> small xml
aligns = root.find(NS+"Alignments")
small = etree.Element("Alignments")
for a in aligns.findall(NS+"Alignment"):
    c = copy.deepcopy(a)
    for xs in c.findall(NS+"CrossSects"):
        c.remove(xs)
    small.append(c)
etree.ElementTree(small).write("alignments_nox.xml", pretty_print=True, encoding="utf-8", xml_declaration=True)
print("alignments_nox.xml written")

# 2) Roadways
rw = root.find(NS+"Roadways")
if rw is not None:
    etree.ElementTree(copy.deepcopy(rw)).write("roadways.xml", pretty_print=True, encoding="utf-8", xml_declaration=True)
    print("roadways.xml written")

# 3) Cross sections for selected alignments -> json
def xs_to_json(a):
    out=[]
    xss = a.find(NS+"CrossSects")
    if xss is None: return out
    for cs in xss.findall(NS+"CrossSect"):
        rec = dict(sta=float(cs.get("sta")), name=cs.get("name"), surfs=[], design=[])
        for s in cs.findall(NS+"CrossSectSurf"):
            pts = s.find(NS+"PntList2D")
            vals = pts.text.split() if pts is not None else []
            pl = [(float(vals[i]), float(vals[i+1])) for i in range(0,len(vals),2)]
            rec["surfs"].append(dict(name=s.get("name"), desc=s.get("desc"), pts=pl))
        for d in cs.findall(NS+"DesignCrossSectSurf"):
            pl=[]
            for p in d.findall(NS+"CrossSectPnt"):
                v = p.text.split()
                pl.append(dict(code=p.get("code"), o=float(v[0]), e=float(v[1])))
            rec["design"].append(dict(name=d.get("name"), side=d.get("side"), closed=d.get("closedArea"), area=d.get("area"), pts=pl))
        out.append(rec)
    return out
for a in aligns.findall(NS+"Alignment"):
    n = a.get("name")
    if a.find(NS+"CrossSects") is not None:
        data = xs_to_json(a)
        fn = "xs_"+n.replace(" ","_").replace("/","_")+".json"
        json.dump(data, open(fn,"w"))
        print("wrote", fn, len(data), "sections")

# 4) Surfaces -> npz (points + faces) + boundaries
surfs = root.find(NS+"Surfaces")
for s in surfs.findall(NS+"Surface"):
    n = s.get("name")
    d = s.find(NS+"Definition")
    pnts = d.find(NS+"Pnts")
    faces = d.find(NS+"Faces")
    ids=[]; xyz=[]
    for p in pnts.findall(NS+"P"):
        ids.append(int(p.get("id")))
        v = p.text.split()
        xyz.append((float(v[0]), float(v[1]), float(v[2])))  # N E Z order in LandXML (northing easting)
    ids=np.array(ids); xyz=np.array(xyz)
    F=[]
    for f in faces.findall(NS+"F"):
        if f.get("i") == "1":  # invisible face
            continue
        v=f.text.split(); F.append((int(v[0]),int(v[1]),int(v[2])))
    F=np.array(F)
    # boundaries / breaklines from SourceData
    bnds=[]
    sd = s.find(NS+"SourceData")
    if sd is not None:
        for b in sd.iter(NS+"Boundary"):
            pl = b.find(NS+"PntList3D")
            if pl is not None:
                v=pl.text.split()
                bnds.append(dict(type=b.get("bndType"), name=b.get("name"), pts=[(float(v[i]),float(v[i+1]),float(v[i+2])) for i in range(0,len(v),3)]))
        nbl = sum(1 for _ in sd.iter(NS+"Breakline"))
    else:
        nbl=0
    fn = "surf_"+n.replace(" ","_")+".npz"
    np.savez_compressed(fn, ids=ids, xyz=xyz, faces=F)
    json.dump(bnds, open("surf_"+n.replace(" ","_")+"_bnd.json","w"))
    print("wrote", fn, "pnts", len(ids), "faces", len(F), "boundaries", len(bnds), "breaklines", nbl, "surfType", d.get("surfType"),
          "N range", xyz[:,0].min(), xyz[:,0].max(), "E range", xyz[:,1].min(), xyz[:,1].max(), "Z range", xyz[:,2].min(), xyz[:,2].max())
print("done", time.time()-t0)

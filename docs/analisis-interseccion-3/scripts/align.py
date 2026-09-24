import math, numpy as np
from lxml import etree
NS="{http://www.landxml.org/schema/LandXML-1.2}"
def _pt(txt):
    n,e = [float(v) for v in txt.split()[:2]]
    return np.array([e,n])  # x=E, y=N
class Alignment:
    def __init__(self, el):
        self.name=el.get("name"); self.length=float(el.get("length")); self.sta0=float(el.get("staStart"))
        self.elems=[]
        s=self.sta0; heading=None
        for g in el.find(NS+"CoordGeom"):
            tag=g.tag.replace(NS,"")
            L=float(g.get("length"))
            P={c.tag.replace(NS,""):_pt(c.text) for c in g if c.tag.replace(NS,"") in ("Start","End","PI","Center") and c.text and c.text.strip()}
            if tag=="Line":
                d=math.radians(float(g.get("dir")))
                self.elems.append(dict(type="Line",s0=s,L=L,start=P["Start"],dir=d))
                heading=d
            elif tag=="Curve":
                R=float(g.get("radius")); rot=g.get("rot")
                d0=math.radians(float(g.get("dirStart"))) if g.get("dirStart") else heading
                self.elems.append(dict(type="Curve",s0=s,L=L,start=P["Start"],center=P["Center"],R=R,rot=rot,dir0=d0))
                heading=math.radians(float(g.get("dirEnd"))) if g.get("dirEnd") else (d0 + (1 if rot=="ccw" else -1)*L/R)
            elif tag=="Spiral":
                rs=g.get("radiusStart"); re_=g.get("radiusEnd"); rot=g.get("rot")
                k0=0.0 if rs=="INF" else 1.0/float(rs); k1=0.0 if re_=="INF" else 1.0/float(re_)
                sgn=1 if rot=="ccw" else -1
                # integrate
                n=200; ds=L/n; x,y=P["Start"]; th=heading; pts=[(x,y,th)]
                for i in range(n):
                    k=k0+(k1-k0)*(i+0.5)/n
                    thm=th+sgn*k*ds/2
                    x+=math.cos(thm)*ds; y+=math.sin(thm)*ds; th+=sgn*k*ds
                    pts.append((x,y,th))
                self.elems.append(dict(type="Spiral",s0=s,L=L,start=P["Start"],pts=np.array(pts),ds=ds))
                heading=th
            s+=L
        self.staEnd=s
    def xy_dir(self, sta):
        """return (x,y), heading(rad) at station"""
        e=None
        for el in self.elems:
            if el["s0"]-1e-9 <= sta <= el["s0"]+el["L"]+1e-9: e=el; break
        if e is None:
            e = self.elems[0] if sta<self.elems[0]["s0"] else self.elems[-1]
        ds=sta-e["s0"]
        if e["type"]=="Line":
            d=e["dir"]; p=e["start"]+ds*np.array([math.cos(d),math.sin(d)]); return p,d
        if e["type"]=="Curve":
            c=e["center"]; R=e["R"]; s=e["start"]
            a0=math.atan2(s[1]-c[1], s[0]-c[0]); sgn=1 if e["rot"]=="ccw" else -1
            a=a0+sgn*ds/R
            p=c+R*np.array([math.cos(a),math.sin(a)]); d=a+sgn*math.pi/2
            return p,d
        if e["type"]=="Spiral":
            i=min(int(ds/e["ds"]), len(e["pts"])-1); x,y,th=e["pts"][i]
            return np.array([x,y]),th
    def offset_xy(self, sta, off):
        p,d=self.xy_dir(sta)
        right=np.array([math.sin(d),-math.cos(d)])
        return p+off*right
    def polyline(self, step=1.0):
        st=np.arange(self.sta0, self.staEnd, step).tolist()+[self.staEnd]
        return np.array([self.xy_dir(s)[0] for s in st])
def load_all(path="alignments_nox.xml"):
    root=etree.parse(path).getroot()
    return {a.get("name"):Alignment(a) for a in root.findall(NS+"Alignment")}
if __name__=="__main__":
    A=load_all()
    eje=A["Eje_Via_de_evitamiento"]
    p,d=eje.xy_dir(4275.613221348603); print("Eje end", p, math.degrees(d), "expected 528814.319 9404994.645")
    p,d=eje.xy_dir(2000); print("Eje 2000", p, math.degrees(d))
    nk=A["1NK_I1"]; p,d=nk.xy_dir(184.99); print("1NK_I1 184.99", p, math.degrees(d))
    for n in ["Interseccion_3_(1)_-_NO_-_Quadrant","Interseccion_3_(1)_-_SO_-_Quadrant"]:
        q=A[n]; print(n, q.xy_dir(0)[0], q.xy_dir(q.staEnd)[0])
    # check spiral chain accuracy: last line start should be (528633.965, 9404828.698)
    print("Eje 4030.529", eje.xy_dir(4030.529)[0], "expected 528633.965 9404828.698")

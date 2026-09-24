import json, math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import tri as mtri
from align import load_all
A = load_all()
eje=A["Eje_Via_de_evitamiento"]; nk=A["1NK_I1"]
qNO=A["Interseccion_3_(1)_-_NO_-_Quadrant"]; qSO=A["Interseccion_3_(1)_-_SO_-_Quadrant"]
SUBS=("_Pave1","_Pave2","_Base","_Sub")
def load_xs(fn, al, stamin=None):
    data=sorted(json.load(open(fn)), key=lambda r:r["sta"])
    out=[]
    for r in data:
        if stamin is not None and r["sta"]<stamin: continue
        links=[]
        for d in r["design"]:
            if d["closed"]=="true" or len(d["pts"])<2: continue
            if any(p["code"] and p["code"].endswith(SUBS) for p in d["pts"]): continue
            pts=[(p["code"],p["o"],p["e"]) for p in d["pts"]]
            links.append((d["name"],pts))
        out.append(dict(sta=r["sta"], links=links))
    return out
XS = {
 "Eje (corredor principal)": (load_xs("xs_Eje_Via_de_evitamiento.json", eje, 4120), eje, "0.35"),
 "1NK_I1 (corredor interseccion)": (load_xs("xs_1NK_I1.json", nk), nk, "tab:blue"),
 "Cuadrante NO (R=200)": (load_xs("xs_Interseccion_3_(1)_-_NO_-_Quadrant.json", qNO), qNO, "tab:green"),
 "Cuadrante SO (R=3)": (load_xs("xs_Interseccion_3_(1)_-_SO_-_Quadrant.json", qSO), qSO, "tab:red"),
}
def feature_lines(secs, al, code, side):
    pts=[]
    for s in secs:
        cand=[]
        for name,link in s["links"]:
            for c,o,e in link:
                if c==code and ((side=="R" and o>0) or (side=="L" and o<0)): cand.append(o)
        if cand:
            o = max(cand) if side=="R" else min(cand)
            pts.append(al.offset_xy(s["sta"], o))
    return np.array(pts) if pts else None

def draw(ax, win, label_every=20, show_topo=True, show_tin=True):
    x0,x1,y0,y1=win
    # terrain contours
    if show_topo:
        d=np.load("surf_Topografia.npz"); xyz=d["xyz"]
        m=(xyz[:,1]>x0-20)&(xyz[:,1]<x1+20)&(xyz[:,0]>y0-20)&(xyz[:,0]<y1+20)
        sub=xyz[m]
        if len(sub)>50:
            t=mtri.Triangulation(sub[:,1],sub[:,0])
            levels=np.arange(np.floor(sub[:,2].min()),np.ceil(sub[:,2].max())+0.5,0.5)
            cs=ax.tricontour(t, sub[:,2], levels=levels, colors="peru", linewidths=0.4, alpha=0.7)
            ax.clabel(cs, fmt="%.1f", fontsize=5, inline=True)
    # Rasante TIN
    if show_tin:
        d=np.load("surf_Rasante.npz"); xyz=d["xyz"]; ids=d["ids"]; F=d["faces"]
        idx={i:k for k,i in enumerate(ids)}
        P=np.array([[xyz[idx[i],1],xyz[idx[i],0]] for i in ids]); Z=xyz[:,2]
        Fi=np.array([[idx[a],idx[b],idx[c]] for a,b,c in F])
        cen=P[Fi].mean(axis=1)
        m=(cen[:,0]>x0)&(cen[:,0]<x1)&(cen[:,1]>y0)&(cen[:,1]<y1)
        ax.triplot(P[:,0],P[:,1],Fi[m],color="silver",lw=0.4,alpha=0.9, label="TIN superficie Rasante (corredor principal)")
    # Interseccion_3 surface points
    d=np.load("surf_Interseccion_3.npz"); xyz=d["xyz"]
    ax.plot(xyz[:,1],xyz[:,0],".",ms=1.5,color="orange",alpha=0.6,label="Puntos superficie Interseccion_3 (0 caras)")
    # section lines
    for name,(secs,al,col) in XS.items():
        first=True
        for s in secs:
            for lname,link in s["links"]:
                xy=np.array([al.offset_xy(s["sta"],o) for c,o,e in link])
                ax.plot(xy[:,0],xy[:,1],color=col,lw=0.5,alpha=0.8,label=(name+" - links de sección") if first else None); first=False
        for code,side,ls,lw in (("Daylight","L","-",1.4),("Daylight","R","-",1.4),("ETW","L","--",1.0),("ETW","R","--",1.0),("EPS","L",":",1.0),("EPS","R",":",1.0),("Back_Curb","L","-.",1.0),("Back_Curb","R","-.",1.0)):
            fl=feature_lines(secs,al,code,side)
            if fl is not None and len(fl)>1:
                ax.plot(fl[:,0],fl[:,1],color=col,ls=ls,lw=lw,alpha=0.95)
    # alignments
    for al,col,lw,lab in ((eje,"k",2.0,"Eje Via de evitamiento"),(nk,"navy",2.0,"1NK_I1"),(qNO,"green",2.2,"Cuadrante NO (R=200 m, Δ=19.7°)"),(qSO,"red",2.2,"Cuadrante SO (R=3 m, Δ=160.3°)")):
        pl=al.polyline(0.5); ax.plot(pl[:,0],pl[:,1],color=col,lw=lw,label=lab)
    for n,col in (("Eje Via de evitamiento-Derecha-3.600 (24)","k"),("Eje Via de evitamiento-Izquierda-3.600 (23)","k"),("1NK_I1-Derecha-3.600","navy"),("1NK_I1-Izquierda-3.600","navy")):
        pl=A[n].polyline(1.0); ax.plot(pl[:,0],pl[:,1],color=col,lw=0.8,ls="--",alpha=0.7)
    # station labels
    for al,st,col in ((eje,range(4120,4276,label_every),"k"),(nk,range(100,260,label_every),"navy")):
        for s in st:
            s=min(s, al.staEnd); p,d=al.xy_dir(s)
            ax.plot(p[0],p[1],"|",color=col,ms=6)
            ax.annotate(f"{int(s//1000)}+{s%1000:06.2f}",p,fontsize=6,color=col,xytext=(3,3),textcoords="offset points")
    # vertex and obstruction points
    v,_=eje.xy_dir(eje.staEnd); ax.plot(v[0],v[1],"o",color="magenta",ms=7,label="Vértice intersección (4+275.61 / 0+184.99)")
    for (e,n,z),lab in (((528781.4887,9404964.4376,18.5027),"obstrucción 4+120"),((528786.4928,9404969.0419,18.3709),"obstrucción 4+140")):
        ax.plot(e,n,"x",color="crimson",ms=9,mew=2); ax.annotate(f"{lab}\nz={z:.2f}",(e,n),fontsize=6,color="crimson",xytext=(-60,-18),textcoords="offset points")
    ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.set_aspect("equal"); ax.grid(True,lw=0.3,alpha=0.5)
    ax.set_xlabel("Este (m)"); ax.set_ylabel("Norte (m)")

import sys
DOPLOT = "--plot" in sys.argv
if DOPLOT:
  fig,ax=plt.subplots(figsize=(14,14),dpi=150)
  draw(ax,(528720,528900,9404900,9405080))
  ann=[((528790.5,9404963.5),(60,-95),"Cuadrante SO: fillet R=3 m, Δ=160.3°, T=17.3 m\n-> 'bucle' con links de sección que se cruzan\n(radio menor que el giro de un auto)"),
       ((528800,9405012),(-250,55),"Cuadrante NO: fillet R=200 m, L=68.7 m (+2x30 m)\n= 128.7 m de 'curb return' casi paralelo a ambas vías\n(sardinel + cuneta + talud en franja larga)"),
       ((528800.5,9404952.5),(45,-120),"Talud de corte derecho del corredor principal\n(4+210 a 4+238, hasta 15.8 m de ancho)\ninvade la calzada de 1NK_I1 (cruza su eje en 4+232)"),
       ((528777,9404970),(-235,-40),"Fin región corredor principal: 4+240.28\nFin superficie Rasante: 4+210.28\nSin secciones del Eje entre 4+240 y 4+275.6"),
       ((528814.3,9404994.6),(35,40),"Vértice: ángulo de cruce 19.7°\n(DG-2018 pide ~90°, no menos de 60°)"),
       ((528853,9404975),(20,-55),"1NK_I1 en la intersección: sección urbana\n(calzada 2x3.60 + sardinel/cuneta 0.60 + cuneta de corte)\nvs. Eje: sección rural (2x3.60 + bermas 3.00 + bordillo)")]
  for xy,off,txt in ann:
      ax.annotate(txt,xy,fontsize=7.5,xytext=off,textcoords="offset points",bbox=dict(boxstyle="round,pad=0.3",fc="lightyellow",ec="0.5",alpha=0.95),arrowprops=dict(arrowstyle="->",color="0.3",lw=0.8))
  ax.set_title("Intersección 3 - planta reconstruida desde el LandXML (secciones del corredor, alineamientos, TIN Rasante, curvas de nivel del terreno)")
  ax.legend(loc="lower right",fontsize=7)
  fig.tight_layout(); fig.savefig("fig_int3_planta.png"); print("saved fig_int3_planta.png")
  fig,ax=plt.subplots(figsize=(14,12),dpi=130)
  draw(ax,(528560,528960,9404760,9405180),label_every=50,show_topo=False)
  ax.set_title("Intersección 3 - vista general (últimos 300 m de la vía de evitamiento y 1NK_I1)")
  ax.legend(loc="lower right",fontsize=7)
  fig.tight_layout(); fig.savefig("fig_int3_general.png"); print("saved fig_int3_general.png")

# overlap analysis
def dist_to_align(p, al, s_lo, s_hi):
    best=(1e9,None,None)
    for s in np.arange(s_lo,s_hi,0.5):
        q,d=al.xy_dir(s); v=p-q
        right=np.array([math.sin(d),-math.cos(d)])
        dd=abs(np.dot(v,right)); along=np.dot(v,np.array([math.cos(d),math.sin(d)]))
        if abs(along)<0.5 and dd<best[0]: best=(dd,s,np.dot(v,right))
    return best
print("\n=== Talud derecho (Daylight R) del corredor principal (Eje) respecto al eje de 1NK_I1 ===")
secs,al,_=XS["Eje (corredor principal)"]
for s in secs:
    if s["sta"]<4150: continue
    cand=[o for n,l in s["links"] for c,o,e in l if c=="Daylight" and o>0]
    if not cand: continue
    o=max(cand); p=al.offset_xy(s["sta"],o); dd,ss,off=dist_to_align(p,nk,100,260)
    if ss is None: continue
    where = "DENTRO de la calzada de 1NK_I1" if dd<3.6 else ("dentro de sardinel/talud 1NK_I1" if dd<9 else "")
    print(f"Eje sta {s['sta']:8.2f}: Daylight der. offset {o:5.2f} m -> dist. al eje 1NK_I1 = {dd:5.2f} m (sta 1NK_I1 {ss:.1f}, lado {'der' if off>0 else 'izq'}) {where}")
print("\n=== Talud derecho (Daylight R, lado oeste) de 1NK_I1 respecto al eje de la vía de evitamiento ===")
secs,al,_=XS["1NK_I1 (corredor interseccion)"]
for s in secs:
    cand=[o for n,l in s["links"] for c,o,e in l if c=="Daylight" and o>0]
    if not cand: continue
    o=max(cand); p=al.offset_xy(s["sta"],o); dd,ss,off=dist_to_align(p,eje,4100,4276)
    if ss is None: continue
    where = "DENTRO de la calzada del Eje" if dd<3.6 else ("dentro de berma/talud Eje" if dd<9 else "")
    print(f"1NK_I1 sta {s['sta']:7.2f}: Daylight der. offset {o:5.2f} m -> dist. al Eje = {dd:5.2f} m (sta Eje {ss}, lado {'der' if off is not None and off>0 else 'izq'}) {where}")

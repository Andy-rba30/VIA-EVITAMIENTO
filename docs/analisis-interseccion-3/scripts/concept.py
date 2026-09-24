import math, json, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import tri as mtri
from align import load_all
A=load_all(); eje=A["Eje_Via_de_evitamiento"]; nk=A["1NK_I1"]
V,_=eje.xy_dir(eje.staEnd)                      # vertex
d_eje=math.radians(42.617768480035)             # math dir of Eje last tangent
d_nk =math.radians(242.306659022009)            # math dir of 1NK_I1 (toward SSW)
u_eje=np.array([math.cos(d_eje),math.sin(d_eje)]); u_nk=np.array([math.cos(d_nk),math.sin(d_nk)])
delta=math.degrees(abs((d_nk - d_eje + math.pi)%(2*math.pi) - math.pi))  # angle between eje dir and nk dir (as vectors)
print(f"Ángulo entre vectores de avance = {delta:.3f}°  -> ángulo de cruce entre alineamientos = {180-delta:.3f}°")

# ---------- Mainline: Eje -> 1NK_I1 (NNE leg) with clothoid-arc-clothoid, R=550, Ls=75 (same as existing curves)
R=550.0; Ls=75.0
Delta=math.radians(180-delta)  # 19.689°
th_s=Ls/(2*R); Dc=Delta-2*th_s; Lc=R*Dc
# spiral end coords (local): X,Y via numeric integration
n=2000; ds=Ls/n; x=y=0.0; th=0.0
for i in range(n):
    k=(i+0.5)/n/R; thm=th+k*ds/2; x+=math.cos(thm)*ds; y+=math.sin(thm)*ds; th+=k*ds
Xs,Ys=x,y; p=Ys-R*(1-math.cos(th_s)); k_=Xs-R*math.sin(th_s)
T=(R+p)*math.tan(Delta/2)+k_
print(f"Curva principal: R={R} Ls={Ls} Δ={math.degrees(Delta):.3f}° θs={math.degrees(th_s):.3f}° Lc={Lc:.2f} Ltotal={2*Ls+Lc:.2f} p={p:.3f} k={k_:.3f} T={T:.2f}")
sta_TS=eje.staEnd-T; sta_ST_nk=184.99-T
print(f"  TS en Eje 4+{sta_TS-4000:.2f} ; ST sobre 1NK_I1 en 0+{sta_ST_nk:.2f} (la vía principal continúa por 1NK_I1 hacia el NNE)")
# build polyline of the curve: start at TS heading d_eje, turn LEFT (ccw) since Eje->NK NNE
TS=V-T*u_eje
def build_curve(P0,th0,sgn,R,Ls,Lc,step=0.5):
    pts=[P0.copy()]; th=th0; P=P0.copy()
    # spiral in
    n=int(Ls/step); ds=Ls/n
    for i in range(n):
        k=(i+0.5)/n/R; thm=th+sgn*k*ds/2; P=P+ds*np.array([math.cos(thm),math.sin(thm)]); th+=sgn*k*ds; pts.append(P.copy())
    n=int(Lc/step); ds=Lc/n
    for i in range(n):
        k=1/R; thm=th+sgn*k*ds/2; P=P+ds*np.array([math.cos(thm),math.sin(thm)]); th+=sgn*k*ds; pts.append(P.copy())
    n=int(Ls/step); ds=Ls/n
    for i in range(n):
        k=(1-(i+0.5)/n)/R; thm=th+sgn*k*ds/2; P=P+ds*np.array([math.cos(thm),math.sin(thm)]); th+=sgn*k*ds; pts.append(P.copy())
    return np.array(pts), th
main_pts, th_end = build_curve(TS, d_eje, +1, R, Ls, Lc)
end=main_pts[-1]
# check: end should be on 1NK_I1 line and heading = d_nk + pi (toward NNE)
n_nk=np.array([math.sin(d_nk),-math.cos(d_nk)])
print(f"  Verificación: distancia del fin de curva a la línea 1NK_I1 = {abs(np.dot(end-V,n_nk)):.3f} m ; rumbo final {math.degrees(th_end)%360:.3f}° vs 1NK_I1 NNE {(math.degrees(d_nk)+180)%360:.3f}°")
print(f"  Tangente entre ST de la curva anterior (4+030.53) y el nuevo TS: {sta_TS-4030.529:.1f} m")

# ---------- Minor leg (old road, SSW leg of 1NK_I1) re-aligned to meet the Eje at 90°
NK_T0=np.array([528754.540568478289, 9404870.37373659946]); NK_S0=279.153326115048+44.012370316447  # start of last tangent of 1NK_I1
d_nk2=math.radians(254.915274349376); u_nk2=np.array([math.cos(d_nk2),math.sin(d_nk2)])
def minor_leg(S_t, ang_deg, Rm):
    J,_=eje.xy_dir(S_t)
    d1=d_eje-math.radians(ang_deg)          # leaving the Eje toward its right (SE) side
    u1=np.array([math.cos(d1),math.sin(d1)])
    Mx=np.array([[u1[0],-u_nk2[0]],[u1[1],-u_nk2[1]]]); t,s=np.linalg.solve(Mx, NK_T0-J)
    PI=J+t*u1
    Dm=abs((d_nk2-d1+math.pi)%(2*math.pi)-math.pi)
    Tm=Rm*math.tan(Dm/2); L1=t-Tm; Lcm=Rm*Dm
    sta_PI_nk=NK_S0+s; sta_end_nk=sta_PI_nk+Tm
    P1=J+L1*u1
    sgn = 1 if ((d_nk2-d1+math.pi)%(2*math.pi)-math.pi)>0 else -1
    pts=[J,P1]; th=d1; P=P1.copy(); n=max(int(Lcm/0.5),2); ds=Lcm/n
    for i in range(n):
        thm=th+sgn*ds/(2*Rm); P=P+ds*np.array([math.cos(thm),math.sin(thm)]); th+=sgn*ds/Rm; pts.append(P.copy())
    return dict(S_t=S_t,ang=ang_deg,R=Rm,J=J,PI=PI,T=Tm,L1=L1,Lc=Lcm,Delta=math.degrees(Dm),sta_PI_nk=sta_PI_nk,sta_end_nk=sta_end_nk,pts=np.array(pts),th_end=th)
print("\nRamal secundario (antigua 1NK_I1 lado SSO) realineado para formar T con el Eje:")
best=None
for S_t in range(4040,4241,20):
  for ang,Rm in ((90,60),(90,80),(80,80),(75,80)):
    m=minor_leg(S_t,ang,Rm)
    ok = (m["L1"]>=30 and m["sta_PI_nk"]-m["T"]>=NK_S0 and m["sta_end_nk"]<=487.37)
    print(f"  T en Eje 4+{S_t-4000:03d}, ángulo {ang}°, R={Rm}: Δ={m['Delta']:.1f}° T={m['T']:.1f} recta L1={m['L1']:.1f} m, Lc={m['Lc']:.1f}, PC en 1NK_I1 0+{m['sta_PI_nk']-m['T']:.1f}, empalma en 0+{m['sta_end_nk']:.1f} {'OK' if ok else ''}")
    if ok and ang==90 and Rm==60: best=m
sel=best
print(f"  Seleccionado: T en 4+{sel['S_t']-4000:03.0f}, 90°, R=60 -> rumbo final {math.degrees(sel['th_end'])%360:.2f}° vs última tangente 1NK_I1 {math.degrees(d_nk2)%360:.2f}° ; fin de curva a {abs(np.dot(sel['pts'][-1]-NK_T0, np.array([math.sin(d_nk2),-math.cos(d_nk2)]))):.3f} m de la línea")

# terrain along the concept (nearest topo point)
d=np.load("surf_Topografia.npz"); xyz=d["xyz"]
def topo_z(P):
    m=(abs(xyz[:,1]-P[0])<6)&(abs(xyz[:,0]-P[1])<6)
    if not m.any(): return None
    sub=xyz[m]; k=np.argmin(np.hypot(sub[:,1]-P[0],sub[:,0]-P[1])); return sub[k,2]
print("\nTerreno natural aproximado a lo largo del ramal secundario propuesto:")
for f in (0,0.25,0.5,0.75,1.0):
    i=int(f*(len(sel["pts"])-1)); P=sel["pts"][i]; print(f"   {f*100:3.0f}%  E={P[0]:.1f} N={P[1]:.1f}  terreno ≈ {topo_z(P)}")
print("Terreno en el eje de la vía en 4+060:", topo_z(eje.xy_dir(4060)[0]), " rasante 4+060 ≈", 18.545116595756 - 0.0080*(4060-4141.807492316081) if False else "ver perfil")
json.dump(dict(TS=float(sta_TS), ST_nk=float(sta_ST_nk), T=float(T), Lc=float(Lc), main=main_pts.tolist(), minor=sel["pts"].tolist(),
               minor_params={k:(float(v) if isinstance(v,(int,float,np.floating)) else None) for k,v in sel.items() if k not in ("J","PI","pts")}), open("concept.json","w"))

# ---------- figure
fig,ax=plt.subplots(figsize=(13,13),dpi=140)
x0,x1,y0,y1=528560,528960,9404760,9405180
m=(xyz[:,1]>x0-20)&(xyz[:,1]<x1+20)&(xyz[:,0]>y0-20)&(xyz[:,0]<y1+20); sub=xyz[m]
t=mtri.Triangulation(sub[:,1],sub[:,0]); cs=ax.tricontour(t,sub[:,2],levels=np.arange(10,40,1.0),colors="peru",linewidths=0.35,alpha=0.6); ax.clabel(cs,fmt="%.0f",fontsize=5)
pl=eje.polyline(0.5); ax.plot(pl[:,0],pl[:,1],color="0.4",lw=1.6,ls="--",label="Eje Vía de evitamiento (actual)")
pl=nk.polyline(0.5); ax.plot(pl[:,0],pl[:,1],color="navy",lw=1.6,ls="--",label="1NK_I1 (actual)")
ax.plot(V[0],V[1],"o",color="magenta",ms=6,label="Vértice actual (cruce a 19.7°)")
# proposed mainline: Eje up to TS, curve, then 1NK_I1 NNE from ST to 0+000
pl=np.array([eje.xy_dir(s)[0] for s in np.arange(4000,sta_TS,0.5)]); ax.plot(pl[:,0],pl[:,1],color="green",lw=3,alpha=0.8,label="Propuesta: vía principal continua (Evitamiento → 1NK_I1 NNE)")
ax.plot(main_pts[:,0],main_pts[:,1],color="green",lw=3,alpha=0.8)
pl=np.array([nk.xy_dir(s)[0] for s in np.arange(0,sta_ST_nk,0.5)]); ax.plot(pl[:,0],pl[:,1],color="green",lw=3,alpha=0.8)
ax.plot(main_pts[[0,-1],0],main_pts[[0,-1],1],"s",color="green",ms=5)
ax.annotate(f"TS 4+{sta_TS-4000:.1f}",main_pts[0],fontsize=7,color="green",xytext=(-70,-10),textcoords="offset points")
ax.annotate(f"ST 0+{sta_ST_nk:.1f} (1NK_I1)",main_pts[-1],fontsize=7,color="green",xytext=(8,0),textcoords="offset points")
ax.annotate(f"Curva R=550 m, Le=75 m, Δ=19.7°\nL total={2*Ls+Lc:.0f} m, T={T:.0f} m (V=80 km/h)",main_pts[len(main_pts)//2],fontsize=7,color="green",xytext=(-190,25),textcoords="offset points",arrowprops=dict(arrowstyle="-",color="green",lw=0.6))
# proposed minor leg
ax.plot(sel["pts"][:,0],sel["pts"][:,1],color="crimson",lw=3,alpha=0.85,label="Propuesta: ramal secundario (antigua 1NK_I1 SSO) en T a 90°")
pl=np.array([nk.xy_dir(s)[0] for s in np.arange(sel["sta_end_nk"],nk.staEnd,0.5)]); ax.plot(pl[:,0],pl[:,1],color="crimson",lw=3,alpha=0.85)
ax.annotate(f"T a 90° en 4+{sel['S_t']-4000:03.0f}\nrecta {sel['L1']:.0f} m + curva R={sel['R']:.0f} m (Δ={sel['Delta']:.0f}°)\nempalma con 1NK_I1 en 0+{sel['sta_end_nk']:.0f}",sel["J"],fontsize=7,color="crimson",xytext=(20,-60),textcoords="offset points",arrowprops=dict(arrowstyle="-",color="crimson",lw=0.6))
# abandoned segment
pl=np.array([nk.xy_dir(s)[0] for s in np.arange(sta_ST_nk,sel["sta_end_nk"],0.5)]); ax.plot(pl[:,0],pl[:,1],color="navy",lw=5,alpha=0.15,label=f"1NK_I1 0+{sta_ST_nk:.0f} a 0+{sel['sta_end_nk']:.0f}: tramo que quedaría fuera de servicio (~{sel['sta_end_nk']-sta_ST_nk:.0f} m)")
ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.set_aspect("equal"); ax.grid(True,lw=0.3,alpha=0.5)
ax.set_xlabel("Este (m)"); ax.set_ylabel("Norte (m)")
ax.set_title("Esquema conceptual (no es diseño definitivo): convertir la 'Y' a 19.7° en vía continua + T a 90° (DG-2018, Cap. V)")
ax.legend(loc="lower right",fontsize=7)
fig.tight_layout(); fig.savefig("fig_int3_propuesta.png"); print("saved fig_int3_propuesta.png")

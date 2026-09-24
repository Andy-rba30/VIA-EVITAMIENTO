import numpy as np, math
from align import load_all
A=load_all(); eje=A["Eje_Via_de_evitamiento"]; nk=A["1NK_I1"]
d=np.load("surf_Topografia.npz"); xyz=d["xyz"]
def topo_z(P):
    for r in (4.0,8.0,15.0,30.0):
        m=(abs(xyz[:,1]-P[0])<r)&(abs(xyz[:,0]-P[1])<r)
        if m.sum()>=3:
            sub=xyz[m]; dd=np.hypot(sub[:,1]-P[0],sub[:,0]-P[1]); k=np.argsort(dd)[:3]
            w=1/(dd[k]+0.1); return float((sub[k,2]*w).sum()/w.sum())
    return float("nan")
pvis=[(0,15.0,0),(60.9757,13.7172,57.2559),(168.5456,16.5371,0),(413.0245,20.8154,211.5),(928.2034,17.7244,78.75),(1236.003,22.8031,255.492),(1511.2131,17.2992,105.5647),(1890.1483,20.5323,198.8065),(2125.5981,16.3,130.3497),(2400.0298,19.3163,125.9385),(2610.4087,17.8437,88.0),(2860.2683,20.0924,112.5),(3083.0232,18.7559,50.75),(3326.2912,20.8237,271.1946),(3570.3475,15.9311,135.2106),(3792.5332,18.153,150.5),(3985.0618,15.9389,98.4447),(4141.8075,18.5451,172.3893),(4264.928,17.5602,0),(4275.6132,17.4753,0)]
def prof(pv, s):
    for i in range(len(pv)-1):
        s0,z0,_=pv[i]; s1,z1,_=pv[i+1]
        if s0<=s<=s1:
            g=(z1-z0)/(s1-s0); z=z0+g*(s-s0)
            for j in (i,i+1):
                sj,zj,L=pv[j]
                if L>0 and abs(s-sj)<=L/2 and 0<j<len(pv)-1:
                    gin=(pv[j][1]-pv[j-1][1])/(pv[j][0]-pv[j-1][0]); gout=(pv[j+1][1]-pv[j][1])/(pv[j+1][0]-pv[j][0])
                    x=s-(sj-L/2); ztan=zj+gin*(s-sj)
                    return ztan+(gout-gin)/(2*L)*x*x
            return z
    return float("nan")
print("=== Eje: terreno vs rasante (4+000 a 4+275.6) ===")
for s in list(range(4000,4276,20))+[4275.6]:
    P,_=eje.xy_dir(s); zt=topo_z(P); zr=prof(pvis,s)
    print(f"  4+{s-4000:06.1f}  terreno {zt:6.2f}  rasante {zr:6.2f}  rasante-terreno {zr-zt:+6.2f}")
pv_nk=[(0.00001,21.0369,0),(31.453,20.7713,1.7245),(77.7754,17.8766,11.9728),(140.0,16.7739,9.705),(207.5423,17.8268,5.3521),(280.0,19.1036,0),(349.9477,20.6777,0),(414.5187,19.9812,0.9315),(487.3746,19.1599,0)]
print("\n=== 1NK_I1: terreno vs perfil (0+000 a 0+487) ===")
for s in list(range(0,488,20))+[487.3]:
    P,_=nk.xy_dir(s); zt=topo_z(P); zr=prof(pv_nk,s)
    print(f"  0+{s:06.1f}  terreno {zt:6.2f}  perfil {zr:6.2f}  perfil-terreno {zr-zt:+6.2f}")
print("\nRasante Eje 4+100 =", round(prof(pvis,4100),2), " ; perfil 1NK_I1 0+412 =", round(prof(pv_nk,412),2))

import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(14,9)); ax.set_xlim(0,14); ax.set_ylim(0,9); ax.axis("off")
RED="#cc2222"; BLU="#1f5fbf"; BLK="#222"; ORG="#cc7a00"; GRY="#999"
def box(x,y,w,h,t,fc="#fff",ec=BLK,fs=12):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.1",fc=fc,ec=ec,lw=1.8,zorder=3))
    ax.text(x+w/2,y+h-0.3,t,ha="center",va="top",fontsize=fs,fontweight="bold",zorder=4)
def L(x,y,t,c=BLK,fs=10,ha="center",va="center",w="normal"):
    ax.text(x,y,t,color=c,fontsize=fs,ha=ha,va=va,fontweight=w,zorder=5)
def Wr(pts,c=BLK,lw=2.2,ls="-"):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=c,lw=lw,ls=ls,zorder=1,solid_capstyle="round")
def D(x,y,c=BLK): ax.plot([x],[y],"o",ms=7,color=c,zorder=6)

L(7,8.55,"MOSFET-Modul Anschluss  (Trigger-Switch, IRLZ44N)",ha="center",fs=15,w="bold")
L(7,8.05,"Low-Side: getriggert → OUT− wird mit VIN− (Masse) verbunden = „Taster gedrückt“",ha="center",fs=10,c="#555")

# module box
mx,my,mw,mh=5.2,4.3,3.6,2.7
box(mx,my,mw,mh,"MOSFET-Modul",fs=12)
# left terminals VIN+ / VIN-
L(mx+0.15,my+mh-0.75,"VIN +",fs=9,ha="left"); L(mx+0.15,my+0.8,"VIN −",fs=9,ha="left")
# right terminals OUT+ / OUT-
L(mx+mw-0.15,my+mh-0.75,"OUT +",fs=9,ha="right"); L(mx+mw-0.15,my+0.8,"OUT −",fs=9,ha="right")
# bottom header TRIG / GND
L(mx+1.0,my+0.18,"TRIG/PWM",fs=8,ha="center"); L(mx+mw-1.0,my+0.18,"GND",fs=8,ha="center")

yT=my+mh-0.75; yB=my+0.8
# VIN+ <- +12V
Wr([(2.2,yT),(mx,yT)],RED); D(mx,yT,RED); L(2.1,yT,"+12 V (Kl.15)",c=RED,fs=10,ha="right",w="bold")
# VIN- <- Masse
Wr([(2.2,yB),(mx,yB)],BLU); D(mx,yB,BLU); L(2.1,yB,"Masse",c=BLU,fs=10,ha="right",w="bold")
# OUT+ frei
Wr([(mx+mw,yT),(mx+mw+1.0,yT)],GRY,1.6,ls=(0,(4,3))); L(mx+mw+1.1,yT,"frei (nicht anschließen)",c=GRY,fs=9,ha="left")
# OUT- -> Signalader
Wr([(mx+mw,yB),(11.6,yB)],BLK); D(mx+mw,yB,BLK); L(11.7,yB,"→ Signalader (Ader 4/5/6)",c=BLK,fs=10,ha="left",w="bold")
# TRIG -> GPIO
Wr([(mx+1.0,my),(mx+1.0,3.0),(3.2,3.0)],ORG); D(mx+1.0,my,ORG); L(3.1,3.0,"ESP GPIO (5/6/7) →",c=ORG,fs=10,ha="right",w="bold")
# GND -> Masse
Wr([(mx+mw-1.0,my),(mx+mw-1.0,2.5),(11.0,2.5)],BLU); D(mx+mw-1.0,my,BLU); L(11.1,2.5,"Masse (gemeinsam)",c=BLU,fs=10,ha="left",w="bold")

# channel table
L(2.0,1.55,"Kanal-Zuordnung:",fs=11,ha="left",w="bold")
rows=[("M1  RESUME","OUT− → Ader 4 (B4)","TRIG ← GPIO5"),
      ("M2  ACC / +","OUT− → Ader 5 (B5)","TRIG ← GPIO6"),
      ("M3  DEC / −","OUT− → Ader 6 (B6)","TRIG ← GPIO7")]
yy=1.15
for a,b,c in rows:
    L(2.0,yy,a,fs=10,ha="left",w="bold"); L(5.2,yy,b,fs=10,ha="left"); L(9.0,yy,c,c=ORG,fs=10,ha="left"); yy-=0.4

L(13.7,0.15,"■ +12V  ■ Masse  ■ Signal(OUT−)  ┄ GPIO(TRIG)  ┄ frei",fs=8,ha="right",c="#666")
plt.tight_layout(); plt.savefig("anschluss-mosfet.png",dpi=150,bbox_inches="tight",facecolor="white"); print("ok")

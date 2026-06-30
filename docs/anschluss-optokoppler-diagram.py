import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig,ax=plt.subplots(figsize=(14,8.5)); ax.set_xlim(0,14); ax.set_ylim(0,8.5); ax.axis("off")
RED="#cc2222"; BLU="#1f5fbf"; BLK="#222"; GRN="#1a8a3a"; ORG="#cc7a00"
def box(x,y,w,h,t,fc="#fff",ec=BLK,fs=11):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.1",fc=fc,ec=ec,lw=1.8,zorder=3))
    ax.text(x+w/2,y+h-0.32,t,ha="center",va="top",fontsize=fs,fontweight="bold",zorder=4)
def L(x,y,t,c=BLK,fs=10,ha="center",va="center",w="normal"):
    ax.text(x,y,t,color=c,fontsize=fs,ha=ha,va=va,fontweight=w,zorder=5)
def Wr(pts,c=BLK,lw=2.2):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=c,lw=lw,zorder=1,solid_capstyle="round")
def D(x,y,c=BLK): ax.plot([x],[y],"o",ms=7,color=c,zorder=6)

L(7,8.15,"Optokoppler-Anschluss (EL817 / PC817, 12-V-Version)",ha="center",fs=15,w="bold")
L(7,7.6,"INPUT (+ / −) = Signalseite     OUTPUT (VCC / OUT / GND) = ESP-Seite",ha="center",fs=10,c="#555")

def modul(cy, title, src_label, src_color, gpio):
    box(5.3,cy-1.05,3.4,2.1,title,fs=11)
    # terminal labels on module edges
    L(5.45,cy+0.55,"IN +",fs=9,ha="left"); L(5.45,cy-0.55,"IN −",fs=9,ha="left")
    L(8.55,cy+0.62,"VCC",fs=9,ha="right"); L(8.55,cy+0.0,"OUT",fs=9,ha="right"); L(8.55,cy-0.62,"GND",fs=9,ha="right")
    # INPUT side wires (left)
    Wr([(2.2,cy+0.55),(5.3,cy+0.55)],src_color); D(5.3,cy+0.55,src_color)
    L(2.1,cy+0.55,src_label,c=src_color,fs=10,ha="right",w="bold")
    Wr([(2.2,cy-0.55),(5.3,cy-0.55)],BLU); D(5.3,cy-0.55,BLU)
    L(2.1,cy-0.55,"Masse",c=BLU,fs=10,ha="right",w="bold")
    # OUTPUT side wires (right)
    Wr([(8.7,cy+0.62),(11.4,cy+0.62)],RED); D(8.7,cy+0.62,RED)
    L(11.5,cy+0.62,"3,3 V (ESP)",c=RED,fs=10,ha="left",w="bold")
    Wr([(8.7,cy+0.0),(11.4,cy+0.0)],ORG); D(8.7,cy+0.0,ORG)
    L(11.5,cy+0.0,f"→ ESP {gpio}",c=ORG,fs=10,ha="left",w="bold")
    Wr([(8.7,cy-0.62),(11.4,cy-0.62)],BLU); D(8.7,cy-0.62,BLU)
    L(11.5,cy-0.62,"Masse",c=BLU,fs=10,ha="left",w="bold")

modul(5.4,"Opto 1 – BREMSE","Bremse Kl.81\n(+12 V beim Bremsen)",BLK,"GPIO15")
modul(2.2,"Opto 2 – LED „bereit“","LED-Signal\n(Bedienteil Ader 3)",GRN,"GPIO16")

# notes
L(0.3,0.75,"• 12-V-Version → INPUT+ darf direkt 12 V sehen (kein Zusatzwiderstand).",fs=9,ha="left")
L(0.3,0.45,"• Active-LOW: Signal an → OUT = LOW (in Firmware invertieren). Interner Pull-up am GPIO AN.",fs=9,ha="left")
L(0.3,0.15,"• Gemeinsame Masse für alle Module + ESP. LED-Polarität (Ader 3) kurz prüfen.",fs=9,ha="left")
L(13.7,0.15,"■ Signal  ■ Masse  ■ 3,3V  ■ OUT→GPIO",fs=8,ha="right",c="#666")
plt.tight_layout(); plt.savefig("anschluss-optokoppler.png",dpi=150,bbox_inches="tight",facecolor="white"); print("ok")

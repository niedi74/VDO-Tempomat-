import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(16,9))
ax.set_xlim(0,16); ax.set_ylim(0,9); ax.axis("off")
RED="#cc2222"; BLU="#1f5fbf"; BLK="#222222"; GRN="#1a8a3a"; GRY="#888888"
def rbox(x,y,w,h,t,fc="#fff",ec=BLK,fs=10,tc=BLK):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",
                 fc=fc,ec=ec,lw=1.8,zorder=3))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,fontweight="bold",color=tc,zorder=4)
def lab(x,y,t,c=BLK,fs=9,ha="center",va="center",w="normal"):
    ax.text(x,y,t,color=c,fontsize=fs,ha=ha,va=va,fontweight=w,zorder=5)
def wire(pts,c=BLK,lw=2.2,ls="-"):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=c,lw=lw,ls=ls,zorder=1,solid_capstyle="round")
def dot(x,y,c=BLK): ax.plot([x],[y],"o",ms=7,color=c,zorder=6)

ax.text(8,8.6,"VDO Tempomat – Bedienteil 6-Adern: Anschluss & Durchschleifung",
        ha="center",fontsize=15,fontweight="bold")

# wire y-positions
W={1:7.6,2:6.9,3:6.2,4:4.9,5:4.2,6:3.5}
func={1:"1  Ein/Aus",2:"2  Masse / Common",3:"3  LED",
      4:"4  RESUME",5:"5  ACC / +",6:"6  DEC / −"}

# Bedienteil + VDO boxes
rbox(0.5,3.0,1.9,5.1,"Bedienteil\n(6-adrig)",fc="#eef3fa")
rbox(13.6,3.0,1.9,5.1,"VDO-\nSteuergerät\n(B-Stecker)",fc="#f0f7f0",fs=9)

# 6 wires straight through, labeled at both connector edges
for n,y in W.items():
    c = BLU if n==2 else (GRN if n==3 else (GRY if n==1 else BLK))
    wire([(2.4,y),(13.6,y)],c,2.2)
    lab(2.5,y+0.22,func[n],c=c,fs=9,ha="left",w="bold")
    lab(13.5,y+0.22,f"B{n}",c=c,fs=8,ha="right")

# Masse rail (vertical) tapping wire 2, feeding relay NO sides
RAILX=11.1
wire([(RAILX,W[2]),(RAILX,W[6]-0.0)],BLU,2.0)
dot(RAILX,W[2],BLU)
lab(RAILX+0.15,W[2]+0.25,"Masse-Schiene (Ader 2)",c=BLU,fs=8,ha="left")

# Relays bridging button wires 4/5/6 to the Masse rail
relgpio={4:"G5",5:"G6",6:"G7"}
relname={4:"R1 RESUME\n(ESP G5)",5:"R2 ACC\n(ESP G6)",6:"R3 DEC\n(ESP G7)"}
for n in (4,5,6):
    y=W[n]
    rbox(9.5,y-0.34,1.6,0.68,relname[n],fc="#fff",fs=7.5)
    dot(9.5,y,RED)   # COM (Ader 4/5/6)

    dot(11.1,y,BLU)   # NO -> Masse

lab(10.3,2.75,"Relais schließt → Ader 4/5/6 auf Masse = „gedrückt\"",c=RED,fs=8)

# Opto reading LED (wire 3) vs Masse (wire 2)
rbox(5.6,5.9,1.5,0.6,"Opto",fc="#fff",fs=8)
dot(5.6+0.0,W[3],GRN) if False else None
dot(6.35,W[3],GRN)             # opto on LED wire
wire([(6.0,W[2]),(6.0,6.5)],BLU,1.4); dot(6.0,W[2],BLU)  # masse tap into opto
wire([(6.35,5.9),(6.35,5.3),(7.6,5.3)],GRN,1.6)
lab(7.7,5.3,"→ ESP G16  (LED „bereit\" lesen)",c=GRN,fs=8,ha="left")

# ESP reference (drives relays)
rbox(8.7,7.4,2.2,0.7,"ESP32-S3",fc="#f7f7f2",fs=9)
lab(9.8,7.15,"GPIO5/6/7 → Relais   |   GPIO16 ← LED",fs=7,c="#555")

# legend / notes
lab(0.5,2.4,"Alle 6 Adern laufen 1:1 vom Bedienteil durch die Box zum VDO (nichts auftrennen).",fs=9,ha="left",w="bold")
lab(0.5,2.0,"Box zapft nur parallel an: COM der 3 Relais = Ader 4/5/6, NO = Ader 2 (Masse). LED über Optokoppler.",fs=9,ha="left")
lab(0.5,1.5,"■ Masse (blau)   ■ Button-Signal (schwarz)   ■ LED (grün)   ■ Ein/Aus (grau, nur durch)   ● = Abgriff/Knoten",fs=8,ha="left",c="#444")
lab(0.5,1.1,"Hinweis: ACC/DEC-Richtung (Ader 5↔6) und Ader 2 = Masse vor dem Anklemmen per Multimeter bestätigen.",fs=8,ha="left",c=RED)

plt.tight_layout()
plt.savefig("verkabelung-bedienteil-6adern.png",dpi=150,bbox_inches="tight",facecolor="white")
print("saved")

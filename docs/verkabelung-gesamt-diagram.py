import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig,ax=plt.subplots(figsize=(18,11.5)); ax.set_xlim(0,18); ax.set_ylim(0,11.5); ax.axis("off")
RED="#cc2222"; BLU="#1f5fbf"; BLK="#222"; GRN="#1a8a3a"; GRY="#888"; ORG="#cc7a00"
def box(x,y,w,h,t,fc="#fff",ec=BLK,fs=10,ls="-",tc=BLK):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=1.7,ls=ls,zorder=3))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs,fontweight="bold",color=tc,zorder=4)
def L(x,y,t,c=BLK,fs=9,ha="center",va="center",w="normal"):
    ax.text(x,y,t,color=c,fontsize=fs,ha=ha,va=va,fontweight=w,zorder=5)
def W(pts,c=BLK,lw=2.0,ls="-"):
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=c,lw=lw,ls=ls,zorder=1,solid_capstyle="round")
def D(x,y,c=BLK): ax.plot([x],[y],"o",ms=6.5,color=c,zorder=6)

L(9,11.15,"VDO Tempomat – ESP-Box Gesamtschaltplan (parallel / rückrüstbar)",ha="center",fs=15,w="bold")
# regions
ax.add_patch(Rectangle((0.2,0.4),3.0,10.2,fc="#eef3fa",ec="#aac",lw=1,zorder=0)); L(1.7,10.35,"Fahrzeug / Bedienteil",fs=10,w="bold")
ax.add_patch(Rectangle((3.4,0.4),10.7,10.2,fc="#f7f7f2",ec="#bbb",lw=1,zorder=0)); L(8.7,10.35,"ESP-BOX",fs=12,w="bold")
ax.add_patch(Rectangle((14.3,0.4),3.3,10.2,fc="#f0f7f0",ec="#aca",lw=1,zorder=0)); L(15.95,10.35,"VDO-Steuergerät",fs=10,w="bold")

wy={1:7.5,2:6.9,3:6.3,4:5.1,5:4.5,6:3.9}
fn={1:"1  Ein/Aus",2:"2  Masse/Common",3:"3  LED",4:"4  RESUME",5:"5  ACC / +",6:"6  DEC / −"}
wc={1:GRY,2:BLU,3:GRN,4:BLK,5:BLK,6:BLK}

# ---- POWER ----
L(1.6,9.85,"Kl.15  +12 V",RED,9,ha="center",w="bold"); L(1.6,9.15,"Masse",BLU,9,ha="center",w="bold")
box(3.7,9.0,2.0,1.15,"Buck 12V→5V\n(MP1584/LM2596)",fc="#fff",fs=8)
W([(2.85,9.85),(3.3,9.85),(3.3,9.9),(3.7,9.9)],RED,2.2); L(3.5,10.25,"2A+TVS+Verpol.",RED,7)
W([(2.85,9.15),(3.45,9.15),(3.45,0.7),(13.2,0.7)],BLU,2.0)          # ground bus (bottom)
W([(3.45,9.45),(3.7,9.45)],BLU,1.8)
# ESP box
box(6.2,8.3,2.6,1.9,"ESP32-S3",fc="#fff",fs=11)
L(6.35,9.85,"5V",fs=8,ha="left"); L(6.35,8.55,"GND",fs=8,ha="left")
W([(5.7,9.9),(6.2,9.9)],RED,2.0); W([(5.7,9.9),(5.7,9.45),(5.7,9.45)],RED,1.6)  # buck 5V to ESP (approx)
W([(5.7,9.45),(5.7,9.9)],RED,1.6); D(5.7,9.45,RED)
# ESP GPIO pins on bottom edge
gp={"G5":6.5,"G6":6.9,"G7":7.3,"G15":7.7,"G16":8.1,"G17":8.45,"G18":8.7}
for g,x in gp.items(): L(x,8.18,g,fs=7,ha="center")
W([(6.0,8.6),(6.2,8.6)],BLU,1.6); W([(6.0,8.6),(6.0,0.7)],BLU,1.6); D(6.0,0.7,BLU)  # ESP GND to bus

# ---- 6 wires through ----
for n,y in wy.items():
    W([(2.4,y),(14.3,y)],wc[n],2.1)
    L(2.5,y+0.2,fn[n],wc[n],9,ha="left",w="bold")
    D(14.3,y,wc[n]); L(14.18,y+0.22,f"B{n}",wc[n],10,ha="right",w="bold")

# Masse rail (wire2) feeding MOSFET sources
RX=11.2; W([(RX,wy[2]),(RX,wy[6])],BLU,1.9); D(RX,wy[2],BLU); L(RX+0.15,wy[2]+0.22,"Masse-Schiene",BLU,7,ha="left")

# ---- MOSFETs on wires 4/5/6 ----
mg={4:"G5",5:"G6",6:"G7"}; mn={4:"M1 RESUME",5:"M2 ACC",6:"M3 DEC"}
for n in (4,5,6):
    y=wy[n]; box(9.5,y-0.32,1.7,0.64,f"{mn[n]}\nIRLZ44N",fc="#fff",fs=7)
    D(9.5,y,RED)         # Drain on button wire
    D(RX,y,BLU)          # Source on Masse rail
    W([(gp[mg[n]],8.3),(gp[mg[n]],y+0.55),(9.5,y+0.55),(9.5,y+0.32)],ORG,1.2,ls=(0,(3,2)))  # GPIO->SIG
    L(gp[mg[n]],y+0.7,mg[n],ORG,7)
L(10.35,wy[6]-0.55,"MOSFET zieht Ader 4/5/6 auf Masse = „gedrückt\"",RED,8)

# ---- Optos: LED (wire3) + Bremse ----
box(4.6,wy[3]-0.3,1.3,0.6,"Opto\nLED",fc="#fff",fs=7)
D(4.6,wy[3],GRN); W([(5.05,wy[2]),(5.05,wy[3]+0.3)],BLU,1.3); D(5.05,wy[2],BLU)
W([(5.25,wy[3]-0.3),(5.25,8.3)],ORG,1.2,ls=(0,(3,2))); L(5.45,7.95,"OUT→G16",GRN,7,ha="left")
# brake input + opto
L(1.6,2.7,"Bremse (Kl.81)\n+12 V beim Bremsen",BLK,8,w="bold")
W([(2.85,2.7),(7.0,2.7)],BLK,1.9)
box(7.0,2.4,1.4,0.6,"Opto\nBremse",fc="#fff",fs=7)
W([(6.4,wy[2]),(6.4,3.0)],BLU,1.2); D(6.4,2.7,BLU) if False else None
W([(6.4,wy[2]),(6.4,2.55),(7.0,2.55)],BLU,1.2); D(6.4,wy[2],BLU)
W([(8.4,2.7),(8.7,2.7),(8.7,8.3)],ORG,1.2,ls=(0,(3,2))); L(8.55,2.95,"OUT→G15",BLK,7,ha="left")

# ---- CAN ----
box(9.5,1.0,2.1,0.95,"CAN  SN65HVD230\n(später)",fc="#fff",ec=GRN,ls=(0,(4,3)),fs=8,tc=GRN)
W([(gp["G17"],8.3),(gp["G17"],2.0)],GRN,1.1,ls=(0,(3,2)))
W([(gp["G18"],8.3),(gp["G18"],1.95),(9.5,1.95)],GRN,1.1,ls=(0,(3,2)))
L(8.0,2.15,"G17/18",GRN,7)
W([(11.6,1.5),(14.3,1.5)],GRN,1.8,ls=(0,(4,3))); L(14.4,1.5,"CANH/CANL → Fahrzeug-CAN\n500k, 11-bit",GRN,8,ha="left")

# notes / legend
L(0.3,0.22,"■ +12V/5V (rot)  ■ Masse (blau)  ■ Button-Signal (schwarz)  ■ LED (grün)  ┄ GPIO-Steuerung (orange)  ┄ CAN (grün)",fs=8,ha="left",c="#444")
L(9,10.9,"Versorgung: rohes Kl.15 (ESP immer an bei Zündung)  •  Bremse bleibt hardwareverdrahtet  •  Speed kommt vom Spartan-Hub (WiFi)",fs=9,ha="center",c="#555")
L(11.7,3.0,"VDO-Klemmen: B4→T6  B5→T8  B6→T4 (Tasten)",fs=8,ha="left",c="#444")
L(11.7,2.65,"B1/B2/B3 → Versorgung/Masse (per Messung)",fs=8,ha="left",c="#444")

plt.tight_layout(); plt.savefig("verkabelung-gesamt.png",dpi=140,bbox_inches="tight",facecolor="white"); print("ok")

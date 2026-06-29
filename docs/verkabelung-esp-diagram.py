import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

fig, ax = plt.subplots(figsize=(17,11))
ax.set_xlim(0,17); ax.set_ylim(0,11); ax.axis("off")

RED="#cc2222"; BLU="#1f5fbf"; BLK="#222222"; GRN="#1a8a3a"; GRY="#777777"
def box(x,y,w,h,title,fc="#ffffff",ec=BLK,ls="-",fs=11,tw="bold"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc=fc,ec=ec,lw=1.8,ls=ls,zorder=2))
    ax.text(x+w/2,y+h-0.28,title,ha="center",va="top",fontsize=fs,fontweight=tw,zorder=3)
def lab(x,y,t,c=BLK,fs=9,ha="center",va="center",w="normal",rot=0):
    ax.text(x,y,t,color=c,fontsize=fs,ha=ha,va=va,fontweight=w,rotation=rot,zorder=4)
def wire(pts,c=BLK,lw=2.0,ls="-"):
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    ax.plot(xs,ys,color=c,lw=lw,ls=ls,zorder=1,solid_capstyle="round")
def dot(x,y,c=BLK):
    ax.plot([x],[y],marker="o",ms=6,color=c,zorder=5)

ax.text(8.5,10.6,"VDO Tempomat – ESP-Box Verkabelung (parallel / rückrüstbar)",
        ha="center",fontsize=15,fontweight="bold")

# Regions
ax.add_patch(Rectangle((0.2,0.6),3.1,9.4,fc="#eef3fa",ec="#aac",lw=1,zorder=0))
lab(1.75,9.75,"Fahrzeug / Bedienteil-Kabel",fs=10,w="bold")
ax.add_patch(Rectangle((3.7,0.6),9.6,9.4,fc="#f7f7f2",ec="#bbb",lw=1,zorder=0))
lab(8.5,9.75,"ESP-BOX",fs=12,w="bold")
ax.add_patch(Rectangle((13.7,0.6),3.1,9.4,fc="#f0f7f0",ec="#aca",lw=1,zorder=0))
lab(15.25,9.75,"VDO-Steuergerät",fs=10,w="bold")

# Left signals y-positions
yK=9.1; yM=8.5; yR=7.5; yA=7.0; yD=6.5; yB=4.6; yL=4.05; yReed=3.5
for y,t,c in [(yK,"Kl.15  +12 V",RED),(yM,"Masse",BLU),
              (yR,"RESUME",BLK),(yA,"ACC / +",BLK),(yD,"DEC / −",BLK),
              (yB,"Bremse (Kl.81)",BLK),(yL,"LED-Signal",BLK),(yReed,"Reed/Speed (opt.)",GRY)]:
    lab(1.75,y,t,c=c,fs=9,w="bold")

# Sub-boxes in ESP-BOX
box(3.95,8.0,2.2,1.3,"Step-down\n12V→5V")
box(6.5,2.7,2.3,6.2,"ESP32-S3")
box(9.4,6.7,3.5,2.1,"Relais 3-Kanal")
box(9.4,4.0,3.5,2.0,"Optokoppler\n3-Kanal")
box(9.4,1.5,3.5,1.7,"CAN  SN65HVD230\n(später)",ls=(0,(5,3)),ec=GRN)

# ESP GPIO labels (right edge of ESP box at x=8.8)
gpio={"5":8.55,"6":8.2,"7":7.85,"15":5.4,"16":5.0,"4":4.6,"17":3.4,"18":3.05}
for g,y in gpio.items():
    lab(8.72,y,"G"+g,fs=8,ha="right")
# ESP power pins (left edge x=6.5)
lab(6.62,8.6,"5V",fs=8,ha="left"); lab(6.62,3.0,"GND",fs=8,ha="left")

# ---- POWER ----
# Kl.15 -> fuse/TVS -> stepdown
wire([(2.9,yK),(3.5,yK),(3.5,8.9),(3.95,8.9)],RED,2.4)
lab(3.45,9.35,"2A + TVS\n+ Verpol.",c=RED,fs=7)
# Masse -> stepdown / common ground bus (vertical bus at x=3.6 bottom)
wire([(2.9,yM),(3.6,yM),(3.6,1.0),(12.9,1.0)],BLU,2.2)  # ground bus along bottom
wire([(3.6,8.4),(3.95,8.4)],BLU,2.0)  # to stepdown IN-
# stepdown 5V out -> ESP 5V, relay VCC, opto VCC (red bus at top y=9.5 inside)
wire([(6.15,8.9),(6.3,8.9),(6.3,8.6),(6.5,8.6)],RED,2.2)          # ->ESP 5V
wire([(6.3,8.9),(6.3,9.45),(11.15,9.45),(11.15,8.8)],RED,2.0)     # ->relay VCC
wire([(11.15,9.45),(11.15,9.45)],RED)  # noop
wire([(9.5,9.45),(9.5,6.0)],RED,1.6)   # down to opto VCC (tap)
dot(11.15,9.45,RED); dot(9.5,9.45,RED); dot(6.3,8.9,RED)
lab(8.7,9.58,"5V",c=RED,fs=8)
# ground taps up to modules and ESP
for x in [6.5,9.4,9.4,9.4]:
    pass
wire([(6.5,3.0),(6.0,3.0),(6.0,1.0)],BLU,1.6)   # ESP GND -> bus
wire([(11.0,6.7),(11.0,1.0)],BLU,1.4)            # relay GND -> bus (approx)
dot(11.0,1.0,BLU); dot(6.0,1.0,BLU)
lab(8.2,0.78,"gemeinsame Masse",c=BLU,fs=8,w="bold")

# ---- RELAYS: GPIO -> IN, COM/NO parallel across pass-through taster lines ----
# pass-through taster lines left->right (RESUME/ACC/DEC) across the whole width
for y,name in [(yR,"RESUME"),(yA,"ACC"),(yD,"DEC")]:
    wire([(2.9,y),(13.7,y)],BLK,1.8)   # cable -> VDO straight through
# GPIO -> relay IN
wire([(8.8,8.55),(9.05,8.55),(9.05,8.3),(9.4,8.3)],BLK,1.6)
wire([(8.8,8.2),(9.2,8.2),(9.2,7.9),(9.4,7.9)],BLK,1.6)
wire([(8.8,7.85),(9.3,7.85),(9.3,7.5),(9.4,7.5)],BLK,1.6)
lab(9.42,8.3,"IN1",fs=7,ha="left"); lab(9.42,7.9,"IN2",fs=7,ha="left"); lab(9.42,7.5,"IN3",fs=7,ha="left")
# relay outputs (COM/NO) tap the taster lines (drop down from relay box to each line)
wire([(12.9,8.3),(13.2,8.3),(13.2,yR),(13.0,yR)],RED,1.6)  # relais1 -> RESUME line tap
wire([(12.9,7.9),(13.35,7.9),(13.35,yA),(13.0,yA)],RED,1.6)
wire([(12.9,7.5),(13.5,7.5),(13.5,yD),(13.0,yD)],RED,1.6)
for y in [yR,yA,yD]: dot(13.0 if False else (13.2 if y==yR else (13.35 if y==yA else 13.5)),y,RED)
lab(11.15,7.0,"COM/NO je\nparallel z. Taster",fs=7,c=RED)

# ---- OPTOS: left signals -> opto -> GPIO ----
wire([(2.9,yB),(9.4,yB)],BLK,1.6)                 # Bremse -> opto in
wire([(2.9,yL),(4.5,yL),(4.5,4.7),(9.4,4.7)],BLK,1.6)  # LED -> opto in
wire([(2.9,yReed),(4.2,yReed),(4.2,4.3),(9.4,4.3)],GRY,1.4,ls=(0,(4,2)))  # reed
lab(9.2,yB,"in",fs=7,ha="right")
# opto out -> ESP GPIO15/16/4
wire([(9.4,5.4),(9.1,5.4),(9.1,5.4),(8.8,5.4)],BLK,1.6)  # placeholder
wire([(9.4,5.4),(8.8,5.4)],BLK,1.6)  # ->G15
wire([(9.4,5.0),(8.8,5.0)],BLK,1.6)  # ->G16
wire([(9.4,4.6),(8.8,4.6)],GRY,1.4,ls=(0,(4,2)))  # ->G4
lab(9.0,5.7,"out → ESP",fs=7)

# ---- CAN ----
wire([(8.8,3.4),(9.4,3.4)],GRN,1.6,ls=(0,(5,3)))  # G17->TX
wire([(8.8,3.05),(9.4,3.05)],GRN,1.6,ls=(0,(5,3)))# G18->RX
wire([(12.9,2.4),(13.7,2.4)],GRN,1.8,ls=(0,(5,3)))
lab(13.75,2.4,"CANH/CANL\n→ Fahrzeug-CAN\n500k, 11-bit",fs=7,ha="left",c=GRN)

# legend
lab(0.3,0.3,"■ +12V/5V (rot)   ■ Masse (blau)   ■ Signal (schwarz)   ┄ optional / CAN (grün)",
    fs=8,ha="left")
# notes
lab(8.5,0.45,"ESP-Versorgung: rohes Kl.15 → ESP immer an bei Zündung • On/Off-Erkennung via LED (G16) • Bremse bleibt hardwareverdrahtet",
    fs=8,ha="center",c="#444")

plt.tight_layout()
plt.savefig("verkabelung-esp.png",dpi=150,bbox_inches="tight",facecolor="white")
print("saved")

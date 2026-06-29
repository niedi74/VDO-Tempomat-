# Klemmenliste – Stecker → Steuergerät (S/T)

Aus `images/schaltplan-komplett-klar.jpg` herausgearbeitet (Farb-Tabs am S/T-Block
+ Spaltenausrichtung im Beschriftungs-Band: oben = Ziel-Klemme, unten = Stecker-Ader).

> ⚠️ **Konfidenz beachten.** „hoch" = im Plan klar lesbar (Farb-Tab + Spalte
> stimmen überein). „mittel/niedrig" = wegen Verteiler-Knoten / mehrfach gleicher
> Aderfarben unsicher → **vor dem Anschließen per Multimeter bestätigen.**

## Farb-Tabs am Steuergerät (sicher abgelesen)
- **S1 = rt (rot)**, **S3 = bl**, **S7 = bl**, **S8 = bl**, **S9 = gn (grün)**
- **T7 = gb (gelb)**, **T9 = ws (weiß)**
- n.c.: **S4**, **T3**

## Belegung – hohe Konfidenz

| Stecker-Ader | Farbe | → Klemme | Begründung |
|--------------|-------|----------|------------|
| **M1** | gn | **S9** | gn-Tab an S9 + Spalte |
| **M2** | bl | **S7** | bl-Tab an S7 + Spalte |
| **M3** | gb | **T7** | gb-Tab an T7 + Spalte |
| **B4** | sw | **T6** | Spaltenausrichtung |
| **B5** | sw | **T8** | Spaltenausrichtung |
| **B6** | sw | **T4** | Spaltenausrichtung |
| **V1** (Bremssignal) | ws | **S6** | Spaltenausrichtung |

## Belegung – mittlere/niedrige Konfidenz (per Multimeter bestätigen)

| Stecker-Ader | Farbe | → Klemme (vermutet) | Hinweis |
|--------------|-------|---------------------|---------|
| **V3** (+12 V, Kl.15) | rt | **S1** | rt-Tab an S1; rot = +12-V-Schiene mit Verteiler-Knoten |
| **V2** (Masse) | bl | **S3 oder S8** | Handbuch S.5: „blau an S3 / blau an S8" |
| **G2** (Reed) | bl | **S8 oder S3** | zweite blaue Ader (G2 ↔ V2 noch zuzuordnen) |
| **G1** (Reed) | rt | **S1-Knoten?** | zwei rote Adern (G1/V3) → eindeutig nur per Messung |
| **B1 / B2 / B3** | sw | **+12-V- / Masse-Schiene + Schalter** | Verteiler-Knoten (Schalter-Common/Versorgung), keine einzelne S/T-Klemme |
| **P1** (Kupplung) | ws | **T9** | T9 = ws |
| **P2** (Kupplung) | rt | (offen) | — |

## Automatikgetriebe
- Plan-Hinweis am T9/Kuppelpedal: **„bei autom. Getriebe w + m verbinden"**.
- Nutzer-Angabe: **weiß (w) an T9 brücken → durchverbunden auf Steuergerät Klemme 9.**

## Strom-/Masse-Logik (Nutzer + Plan)
- 🔴 **Rot = +12 V (Kl. 15)** – Schiene mit **einem** Verteiler-Knoten, speist u. a.
  Steuergerät und Bedienteil-Seite (B1/B2-Bereich).
- 🔵 **Blau = Masse** – Schiene mit **mehreren** Knoten/Verteilern auf viele Klemmen.

## Noch offen / zu messen
- [ ] G2 vs. V2 → welche blaue Ader auf S3, welche auf S8?
- [ ] G1 vs. V3 → welche rote Ader genau wohin (Knoten an S1)?
- [ ] B1/B2/B3 exakt: welche an +12 V, welche an Masse, welche an Schalter?
- [ ] P2 (rt) Zielklemme.
- [ ] Alles Genannte mit Durchgangsprüfer gegenchecken, bevor Strom drauf kommt.

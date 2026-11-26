# Transistors found on the Varioprop C6 TX board (read 2026-11-24)

> **Note:** the datasheet PDFs and scans mentioned below are third-party material and are **not included** in this repository.
> Use the links to get them.
> 
> Only [2SC1589.md](2SC1589.md) (own work) is included.

| Marking on part | Type | Qty | Likely position (to confirm by tracing) |
|---|---|---|---|
| NEC C1589 K96 (big, tab, got hot, burnt R next to it) | 2SC1589 | 1 | **T113** RF power amp |
| C735 Y x9F | 2SC735-Y (Toshiba) | 2 | **T111** oscillator, **T112** driver |
| C945 AP18Z / AP18Y / AP192 | 2SC945 (NEC) | 7 | T110 regulator + coder (T101–T108) |

## 2SC1589 (NEC) – suspect T113
Full sheet: [2SC1589.md](2SC1589.md)
No original NEC datasheet found online (only spec listings / scanned cross-reference books).
| Parameter | Value | Source |
|---|---|---|
| Type | NPN Si, RF power | rfparts |
| Package | TO-202 (plastic, metal tab) | rfparts (littlediode says TO-220) |
| Vcbo / Vceo / Vebo | 36 V / 18 V / – | rfparts, littlediode |
| Ic max | 0.75 A | rfparts, littlediode |
| Pc | 2 W (with heatsink tab) | rfparts (littlediode: 2.5 W) |
| fT | 250 MHz (littlediode: 550 MHz) | rfparts |
| hFE min | 20 | rfparts |
| Tj max | 175 °C | rfparts |
| Pinout | **C – E – B** (looking at the text side, left to right), tab = collector – **confirmed** on the part | measured |

Links:
- https://www.rfparts.com/2sc1589.html
- https://www.littlediode.com/components/2SC1589.html 
- https://www.datasheetarchive.com/2SC1589-datasheet.html 
- https://alltransistors.com/transistor.php?transistor=12116

## 2SC735 (Toshiba) – oscillator / driver
Downloaded: `2SC735_Toshiba_pages/page-1..3.png` (scan of original Toshiba sheet).
| Parameter | Value |
|---|---|
| Use | driver stage amp, power amp, switching ("PCT process") |
| Package | Toshiba 2-5B1A (TO-92 style) |
| Pinout | **1 = Emitter, 2 = Collector, 3 = Base** (E-C-B) |
| Vcbo / Vceo / Vebo | 35 V / 30 V / 5 V |
| Ic / Pc | 400 mA / 300 mW |
| fT | 300 MHz typ (Vce 5 V, Ie −50 mA) |
| Cob | 7 pF typ |
| hFE (Y) | 120–240 (O: 70–140) |
| Complement | 2SA562 |

Links:
- https://datasheet4u.com/datasheet/Toshiba/2SC735-613419
- https://datasheetspdf.com/pdf/613419/Toshiba/2SC735/1
- http://www.datasheet.hk/view_download.php?id=1526482&file=0264%5C2sc735_235586.pdf

## 2SC945 (NEC) – regulator / coder
| Parameter | Value |
|---|---|
| Use | AF amplifier, low-speed switching |
| Package | TO-92 |
| Pinout (NEC original) | E-C-B — check: some second sources use E-B-C / E-C-B differently |
| Vcbo / Vceo / Vebo | 60 V / 50 V / 5 V |
| Ic / Pc | 150 mA / 250–400 mW |
| fT | ≈ 200–250 MHz |
| hFE classes | NEC: R 90–180, Q 135–270, P 200–400, K 300–600 (letter on part) |
| Complement | 2SA733 |

Links:
- https://www.alldatasheet.com/datasheet-pdf/pdf/5971/NEC/2SC945.html
- https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6284/LUMIMAX2SC945.PDF
- https://components101.com/sites/default/files/component_datasheet/2SC945%20Bipolar%20NPN%20Transistor%20Datasheet.pdf
- https://www.rfparts.com/2sc945.html

## Replacement candidates for T113 (2SC1589)
Requirements: NPN, Vceo ≥ 18 V (better 25+), Ic ≥ 0.5 A, Pc ≥ 1–2 W, fT ≥ 200 MHz, similar package/pinout.
| Candidate | Package | Notes |
|---|---|---|
| 2SC1589 NOS | TO-202 | identical, rfparts / littlediode list stock |
| 2SC2078 | TO-220 | common 27 MHz CB final, 80 V, 3 A, 10 W, fT 150 MHz — overkill but robust; different package/pinout |
| 2SC1969 | TO-220 | 27 MHz CB final, higher power; different package |
| 2SC2166 | TO-220 | 27 MHz driver/final, 6 W |
| BD139 | TO-126 | fT ~190 MHz, marginal at 27 MHz but often works in low-power RC TX |
Any substitute: check pinout, fit, heat path; retune L104/L105/L106/L101 afterwards.

## Receiver SSM 27B (Best.-Nr. 3956) – HD14175BP (Hitachi)
Hitachi second source of the CMOS **MC14175B / CD40175B** (quad D flip-flop, used as the PPM decoder shift register).
| Pin | Function | Pin | Function |
|---|---|---|---|
| 1 | /R (reset) | 16 | **VDD (+)** |
| 2 | Q0 | 15 | Q3 |
| 3 | /Q0 | 14 | /Q3 |
| 4 | D0 | 13 | D3 |
| 5 | D1 | 12 | D2 |
| 6 | /Q1 | 11 | /Q2 |
| 7 | Q1 | 10 | Q2 |
| 8 | **VSS (−)** | 9 | C (clock) |
Supply 3–18 V.

Links:
- https://www.onsemi.com/pdf/datasheet/mc14175b-d.pdf

## 2N2219A / 2N2218A (replacement for T113)
- onsemi 2N2219A: https://www.onsemi.com/pdf/datasheet/2n2219-d.pdf
- Pinout TO-39 (bottom view): 1 = E (next to tab), 2 = B, 3 = C, case = collector.

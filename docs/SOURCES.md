# Varioprop C6 – sources found (2026-11-23)

Unit: Graupner/Grundig varioprop C6, SSM 27 (27 MHz AM), Best.-Nr. 3953, 1978, 6 ch / 3 servos.

## Schematic and repair info

| What | Where | Local copy |
|---|---|---|
| Schematic (redraw, JMF 09/13) | https://wiki.rc-network.de/wiki/Graupner_Fernsteuersender_%C3%9Cbersicht#Varioprop_C6 | not included (third-party copyright) – download from the wiki |
| Photos front/side | same wiki page | not included (third-party copyright) |
| Repair thread, Varioprop 12S (T101 osc swapped to 2N2222, retune L101) | https://www.electro-tech-online.com/threads/varioprop-12s-repair.158657/ | – |
| Receiver repair thread | https://www.rc-network.de/threads/graupner-varioprop-empf%C3%A4nger-reparatur.529777/ | – |

Not found online: original Graupner manual / service manual, original NEC 2SC1589 datasheet.

## Datasheets

Third-party PDFs and scans are not included; values used in this repo are summarised in [datasheets/DATASHEETS.md](datasheets/DATASHEETS.md) and [datasheets/2SC1589.md](datasheets/2SC1589.md).

| Part | Used as | Source | What |
|---|---|---|---|
| 2SC1589 (NEC) | T113 RF power amp (original) | https://www.rfparts.com/2sc1589.html | specs, NOS stock |
| | | https://www.littlediode.com/components/2SC1589.html | specs (lists TO-220, 2.5 W, 550 MHz) |
| | | https://alltransistors.com/transistor.php?transistor=12116 | specs, cross-reference search |
| | | https://www.datasheetarchive.com/2SC1589-datasheet.html | Fuji-SVEA cross-reference, p. 57 |
| 2SC735 (Toshiba) | T111 oscillator, T112 driver | https://datasheet4u.com/datasheet/Toshiba/2SC735-613419 | scan of the original Toshiba sheet |
| | | https://datasheetspdf.com/pdf/613419/Toshiba/2SC735/1 | same scan |
| 2SC945 (NEC) | T110 regulator, coder T101–T108 | https://www.alldatasheet.com/datasheet-pdf/pdf/5971/NEC/2SC945.html | NEC datasheet |
| | | https://www.rfparts.com/2sc945.html | specs |
| 2N2219A (onsemi) | T113 replacement | https://www.onsemi.com/pdf/datasheet/2n2219-d.pdf | datasheet, TO-39 pinout |
| HD14175BP (Hitachi) = MC14175B | receiver PPM decoder | https://www.onsemi.com/pdf/datasheet/mc14175b-d.pdf | MC14175B datasheet (onsemi), pinout |


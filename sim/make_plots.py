"""Run both LTspice schematics (original 2SC1589 / repaired 2N2219A) and plot them side by side.

usage:  python make_plots.py            (needs numpy + matplotlib, LTspice 24+)
        set LTSPICE=<path to LTspice.exe> if it is not in the default install folder

Writes compare_overview.png, compare_rf.png and prints the .meas results of both runs.
LTspice outputs (*.raw, *.log, *.net) land next to the .asc files and are git-ignored.
"""
import os
import re
import subprocess
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

HERE = Path(__file__).resolve().parent
LTSPICE = os.environ.get("LTSPICE", os.path.expandvars(r"%LOCALAPPDATA%\Programs\ADI\LTspice\LTspice.exe"))
RUNS = {
    "original (2SC1589)": "varioprop_c6_ssm27_original",
    "repaired (2N2219A)": "varioprop_c6_ssm27_repaired",
}
COLORS = ["#8a8f98", "#e8891c"]


def run(name):
    """Run LTspice in batch mode, return the path of the .raw file."""
    subprocess.run([LTSPICE, "-b", str(HERE / f"{name}.asc")], check=True)
    return HERE / f"{name}.raw"


def read_raw(path):
    """Minimal reader for LTspice binary .raw files (transient)."""
    data = path.read_bytes()
    enc = "utf-16-le" if data[1:2] == b"\x00" else "latin-1"
    marker = "Binary:\n".encode(enc)
    i = data.find(marker)
    header = data[:i].decode(enc)
    body = data[i + len(marker):]
    nvar = int(re.search(r"No\. Variables:\s*(\d+)", header).group(1))
    npts = int(re.search(r"No\. Points:\s*(\d+)", header).group(1))
    names = re.findall(r"^\s*\d+\s+(\S+)\s+\S+", header.split("\nVariables:")[1], re.M)[:nvar]
    if "double" in re.search(r"Flags:(.*)", header).group(1):
        arr = np.frombuffer(body, dtype="<f8", count=nvar * npts).reshape(npts, nvar).copy()
    else:
        dt = np.dtype([("t", "<f8")] + [(f"v{k}", "<f4") for k in range(1, nvar)])
        rec = np.frombuffer(body, dtype=dt, count=npts)
        arr = np.column_stack([rec["t"]] + [rec[f"v{k}"].astype(float) for k in range(1, nvar)])
    arr[:, 0] = np.abs(arr[:, 0])
    return {n.lower(): arr[:, k] for k, n in enumerate(names)}


def read_meas(name):
    """Return {meas name: value} from the LTspice .log."""
    data = (HERE / f"{name}.log").read_bytes()
    text = data.decode("utf-16-le" if data[1:2] == b"\x00" else "latin-1")
    out = {}
    for line in text.splitlines():
        m = re.match(r"^(\w+):.*=\s*([-+0-9.eE]+)", line) or re.match(r"^(\w+)=([-+0-9.eE]+)", line)
        if m:
            out[m.group(1).lower()] = float(m.group(2))
    return out


def binned(t, y, window):
    """Split into `window`-second bins (time step is not uniform).
    Returns bin centres, time-weighted mean and peak-to-peak per bin."""
    tu = np.arange(t[0], t[-1], 1e-9)  # resample to 1 ns
    yu = np.interp(tu, t, y)
    n = int(round(window / 1e-9))
    m = len(yu) // n
    yb = yu[: m * n].reshape(m, n)
    centres = tu[: m * n].reshape(m, n).mean(axis=1)
    return centres, yb.mean(axis=1), yb.max(axis=1) - yb.min(axis=1)


def main():
    data, meas = {}, {}
    for label, name in RUNS.items():
        data[label] = read_raw(run(name))
        meas[label] = read_meas(name)

    # --- overview: whole 200 us run --------------------------------------------------
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 7.5))
    for (label, d), c in zip(data.items(), COLORS):
        t = d["time"]
        tb, i_avg, _ = binned(t, -d["i(v1)"], 1e-6)
        axs[0].plot(tb * 1e6, i_avg * 1e3, color=c, lw=1.5, label=label)
        tb, _, ant_pp = binned(t, d["v(ant)"], 0.5e-6)
        axs[1].plot(tb * 1e6, ant_pp, color=c, lw=1.5, label=label)
        tb, _, osc_pp = binned(t, d["v(c111)"], 0.5e-6)
        axs[2].plot(tb * 1e6, osc_pp, color=c, lw=1.5, ls="--" if c == COLORS[1] else "-", label=label)
    axs[0].set_ylim(0, 80)
    axs[0].set_ylabel("supply current [mA]\n(1 us average, inrush clipped)")
    axs[1].set_ylabel("antenna V(ANT)\n[Vpp]")
    axs[2].set_ylabel("oscillator V(C111)\n[Vpp]")
    axs[2].set_xlabel("time [us]")
    axs[0].set_title("Varioprop C6 SSM 27 RF section - start-up, original vs repaired T113")
    for ax in axs:
        ax.grid(alpha=0.3)
        ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "compare_overview.png", dpi=110)

    # --- RF detail: last 4 carrier cycles ----------------------------------------------
    t1 = 200e-6
    t0 = t1 - 4 / 27.3e6
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 7.5))
    for (label, d), c in zip(data.items(), COLORS):
        t = d["time"]
        s = (t >= t0) & (t <= t1)
        x = (t[s] - t0) * 1e9
        axs[0].plot(x, d["v(b113)"][s] - d["v(tap)"][s], color=c, lw=1.2, label=label)
        axs[1].plot(x, d["ic(q113)"][s] * 1e3, color=c, lw=1.2, label=label)
        axs[2].plot(x, d["v(ant)"][s], color=c, lw=1.2, label=label)
    axs[0].set_ylabel("T113 base drive\nV(B113)-V(TAP) [V]")
    axs[1].set_ylabel("T113 collector\ncurrent [mA]")
    axs[2].set_ylabel("antenna V(ANT) [V]")
    axs[2].set_xlabel("time [ns] (last 4 cycles before 200 us)")
    axs[0].set_title("Class-C PA T113 at 27 MHz, original vs repaired")
    for ax in axs:
        ax.grid(alpha=0.3)
        ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "compare_rf.png", dpi=110)

    # --- .meas table -------------------------------------------------------------------
    rows = [
        ("iavg", "supply current", 1e3, "mA"),
        ("vreg", "regulator VREG", 1, "V"),
        ("vosc", "oscillator V(C111)", 1, "Vpp"),
        ("pant", "antenna power", 1e3, "mW"),
        ("pdt113", "T113 dissipation", 1, "W"),
        ("vb113pp", "T113 base drive", 1, "Vpp"),
        ("vantpp", "antenna voltage", 1, "Vpp"),
        ("fant", "frequency", 1e-6, "MHz"),
    ]
    labels = list(RUNS)
    print(f"{'(180-200 us average)':24}" + "".join(f"{lbl:>22}" for lbl in labels))
    for key, text, scale, unit in rows:
        vals = "".join(f"{meas[lbl].get(key, float('nan')) * scale:>18.3g} {unit:<3}" for lbl in labels)
        print(f"{text:24}{vals}")
    print("wrote compare_overview.png, compare_rf.png")


if __name__ == "__main__":
    main()

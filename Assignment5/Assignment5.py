import matplotlib.pyplot as plt
import numpy as np


def plot_vlsi_technology_roadmap():
    """Plots and saves the approximate VLSI semiconductor technology roadmap (1972–2025)."""
    years = np.array([
        1972,
        1975,
        1978,
        1982,
        1985,
        1989,
        1993,
        1997,
        2001,
        2004,
        2007,
        2010,
        2014,
        2018,
        2022,
        2025,
    ])

    width_nm = np.array([
        10000,
        6000,
        3000,
        1500,
        1000,
        800,
        500,
        250,
        130,
        90,
        65,
        45,
        22,
        10,
        5,
        2,
    ])
    tox_nm = np.array([
        120,
        100,
        70,
        40,
        25,
        16,
        10,
        5.0,
        2.2,
        1.4,
        1.1,
        0.9,
        0.8,
        0.7,
        0.65,
        0.6,
    ])
    vdd_v = np.array([
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        5.0,
        3.3,
        2.5,
        1.5,
        1.2,
        1.1,
        1.0,
        0.85,
        0.75,
        0.70,
        0.65,
    ])
    vth_v = np.array([
        1.20,
        1.00,
        0.90,
        0.85,
        0.80,
        0.75,
        0.65,
        0.55,
        0.42,
        0.38,
        0.35,
        0.33,
        0.30,
        0.28,
        0.26,
        0.25,
    ])
    delay_ps = np.array([
        12000,
        6000,
        3000,
        1500,
        900,
        550,
        300,
        150,
        75,
        45,
        28,
        18,
        11,
        7.5,
        5.5,
        4.2,
    ])
    performance_rel = np.array([
        1,
        3,
        10,
        35,
        100,
        300,
        1000,
        3500,
        12000,
        30000,
        60000,
        110000,
        220000,
        450000,
        900000,
        1500000,
    ])
    power_w = np.array([
        0.5,
        1.0,
        2.0,
        3.5,
        5.0,
        10.0,
        20.0,
        40.0,
        70.0,
        105.0,
        115.0,
        120.0,
        125.0,
        140.0,
        180.0,
        250.0,
    ])

    parameters = [
        (
            width_nm,
            "Minimum Feature Width (Gate Length)",
            "Width (nm)",
            "#1f77b4",
            True,
        ),
        (
            tox_nm,
            "Gate Oxide Thickness ($T_{ox}$ / EOT)",
            "$T_{ox}$ (nm)",
            "#ff7f0e",
            True,
        ),
        (
            vdd_v,
            "Supply Voltage ($V_{DD}$)",
            "Voltage (V)",
            "#2ca02c",
            False,
        ),
        (
            vth_v,
            "Threshold Voltage ($V_{th}$)",
            "Voltage (V)",
            "#d62728",
            False,
        ),
        (
            delay_ps,
            "Gate Delay Time ($t_d$)",
            "Delay (ps)",
            "#9467bd",
            True,
        ),
        (
            performance_rel,
            "Relative Performance (1972 = 1x)",
            "Performance Index",
            "#8c564b",
            True,
        ),
        (
            power_w,
            "Chip Power Consumption ($P$)",
            "Power (W)",
            "#e377c2",
            False,
        ),
    ]

    fig, axes = plt.subplots(4, 2, figsize=(15, 16), sharex=True)
    fig.suptitle(
        "VLSI Semiconductor Technology Roadmap (1972 – 2025)",
        fontsize=16,
        fontweight="bold",
        y=0.99,
    )

    axes_flat = axes.flatten()

    for idx, (data, title, ylabel, color, is_log) in enumerate(parameters):
        ax = axes_flat[idx]
        ax.plot(
            years,
            data,
            marker="o",
            markersize=5,
            linewidth=2.2,
            color=color,
            label=title,
        )

        ax.axvline(
            2005,
            color="gray",
            linestyle="--",
            alpha=0.6,
            linewidth=1,
            label="End of Dennard Scaling (~2005)" if idx == 0 else "",
        )
        ax.axvline(
            2011,
            color="black",
            linestyle=":",
            alpha=0.6,
            linewidth=1,
            label="FinFET Introduction (~2011)" if idx == 0 else "",
        )

        if is_log:
            ax.set_yscale("log")
            ax.set_ylabel(f"{ylabel} [Log]", fontsize=10, fontweight="bold")
        else:
            ax.set_ylabel(ylabel, fontsize=10, fontweight="bold")

        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.grid(True, which="both", linestyle="--", alpha=0.4)
        ax.set_xlim(1970, 2027)

        ax.annotate(
            f"{data[0]}",
            (years[0], data[0]),
            textcoords="offset points",
            xytext=(6, 5),
            fontsize=8.5,
            fontweight="bold",
        )
        ax.annotate(
            f"{data[-1]}",
            (years[-1], data[-1]),
            textcoords="offset points",
            xytext=(-18, 6),
            fontsize=8.5,
            fontweight="bold",
        )

    axes_flat[6].set_xlabel("Year", fontsize=11, fontweight="bold")
    axes_flat[6].tick_params(labelbottom=True)

    # 8th subplot: Key Trends Summary Box
    ax_info = axes_flat[7]
    ax_info.axis("off")
    summary_text = (
        "Key VLSI Scaling Trends (1972 – 2025):\n\n"
        "• Width & Tox: Scaled down exponentially (10 µm → 2 nm),\n"
        "  switching to High-K/Metal Gate (~2007) & FinFET/GAAFET.\n"
        "• Vdd & Vth: Scaled steadily until ~2005, then plateaued\n"
        "  (~0.65V Vdd, ~0.25V Vth) to prevent subthreshold leakage.\n"
        "• Delay Time: Dropped >2,500x as transistor capacitance fell.\n"
        "• Power: Hit the 'Power Wall' (~120W) in the mid-2000s,\n"
        "  forcing multi-core architectures before rising again in AI chips.\n"
        "• Performance: Grew >1,000,000x via density & clock gains."
    )
    ax_info.text(
        0.02,
        0.5,
        summary_text,
        transform=ax_info.transAxes,
        va="center",
        ha="left",
        fontsize=10,
        bbox=dict(
            boxstyle="round,pad=0.8",
            facecolor="#f4f6f9",
            edgecolor="#cccccc",
        ),
    )

    axes_flat[0].legend(loc="upper right", fontsize=8.5)

    plt.tight_layout(rect=[0, 0, 1, 0.97])

    # Save with exact figure dimensions
    plt.savefig("vlsi_technology_roadmap.png", dpi=300)
    plt.savefig("vlsi_technology_roadmap.pdf")
    print(
        "Diagram saved successfully as 'vlsi_technology_roadmap.png' and"
        " 'vlsi_technology_roadmap.pdf'"
    )

    plt.show()


if __name__ == "__main__":
    plot_vlsi_technology_roadmap()
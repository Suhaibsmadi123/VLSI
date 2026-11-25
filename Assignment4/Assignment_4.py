import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


def plot_series_inverter_noise_margins(
    Vdd=5.0,
    Vth_n=1.0,
    Vth_p=1.0,
    beta_ratio=1.0,
    filename="noise_margin.png",
):
    """Plots and saves the Voltage Transfer Characteristic (VTC) and Noise Margins (NMH, NML)

    for two inverters connected in series.

    Parameters:
    - Vdd: Supply voltage (V)
    - Vth_n: NMOS threshold voltage (V)
    - Vth_p: PMOS threshold voltage magnitude (V)
    - beta_ratio: (beta_n / beta_p) -> 1.0 gives symmetric VTC (NMH == NML)
    - filename: Output image filename to save
    """
    # Generate input voltage sweep for Inverter 1
    Vin = np.linspace(0, Vdd, 2000)

    # Smooth analytical approximation of CMOS Inverter VTC
    # Switching threshold V_M shifts based on beta_ratio
    Vm = (Vth_n + (Vdd - Vth_p) * np.sqrt(1 / beta_ratio)) / (
        1 + np.sqrt(1 / beta_ratio)
    )
    gain = 12.0  # Sharpness of transition
    Vout = Vdd / (1 + np.exp(gain * (Vin - Vm)))

    # Calculate derivative dVout / dVin to find unity-gain points (slope = -1)
    dVout = np.gradient(Vout, Vin)

    # Find indices where slope is closest to -1
    mid_idx = np.argmin(np.abs(Vin - Vm))
    idx_low = np.argmin(np.abs(dVout[:mid_idx] + 1.0))
    idx_high = mid_idx + np.argmin(np.abs(dVout[mid_idx:] + 1.0))

    # Extract critical voltage points
    VIL = round(Vin[idx_low], 3)
    VOH = round(Vout[idx_low], 3)
    VIH = round(Vin[idx_high], 3)
    VOL = round(Vout[idx_high], 3)

    # Calculate Noise Margins
    NMH = round(VOH - VIH, 3)
    NML = round(VIL - VOL, 3)

    # Determine colors based on assignment rules
    tolerance = 1e-2
    if abs(NMH - NML) <= tolerance:
        nmh_color = "green"
        nml_color = "green"
        status_text = (
            f"Balanced Margins: NMH == NML ({NMH:.2f} V) -> Both Colored GREEN"
        )
    elif NMH < NML:
        nmh_color = "red"
        nml_color = "steelblue"
        status_text = (
            f"Worst Margin: NMH ({NMH:.2f} V) < NML ({NML:.2f} V) -> NMH Colored"
            " RED"
        )
    else:
        nmh_color = "steelblue"
        nml_color = "red"
        status_text = (
            f"Worst Margin: NML ({NML:.2f} V) < NMH ({NMH:.2f} V) -> NML Colored"
            " RED"
        )

    # --- Plotting ---
    fig, (ax_vtc, ax_series) = plt.subplots(
        1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1.3, 1]}
    )
    fig.suptitle(
        f"Two Series Inverters: Noise Margin & Region Analysis\n{status_text}",
        fontsize=13,
        fontweight="bold",
    )

    # LEFT PLOT: VTC Curve with Critical Points
    ax_vtc.plot(
        Vin,
        Vout,
        color="black",
        linewidth=2.5,
        label="Inverter VTC ($V_{out}$ vs $V_{in}$)",
    )
    ax_vtc.plot(
        [0, Vdd], [0, Vdd], linestyle=":", color="gray", label="Unity Line"
    )

    # Mark VIL, VOH, VIH, VOL
    points = [
        (VIL, VOH, f"($V_{{IL}}$={VIL}V, $V_{{OH}}$={VOH}V)", "bottom", "left"),
        (VIH, VOL, f"($V_{{IH}}$={VIH}V, $V_{{OL}}$={VOL}V)", "top", "right"),
    ]
    for x, y, label, va, ha in points:
        ax_vtc.scatter(x, y, color="darkorange", zorder=5, s=60)
        ax_vtc.vlines(x, 0, y, linestyles="--", color="gray", alpha=0.7)
        ax_vtc.hlines(y, 0, x, linestyles="--", color="gray", alpha=0.7)
        ax_vtc.annotate(
            label,
            (x, y),
            textcoords="offset points",
            xytext=(8 if ha == "left" else -8, 6 if va == "bottom" else -14),
            ha=ha,
            fontsize=9,
            fontweight="bold",
        )

    ax_vtc.set_title("Voltage Transfer Characteristic (VTC)")
    ax_vtc.set_xlabel("Input Voltage $V_{in}$ (V)")
    ax_vtc.set_ylabel("Output Voltage $V_{out}$ (V)")
    ax_vtc.set_xlim(0, Vdd)
    ax_vtc.set_ylim(0, Vdd)
    ax_vtc.grid(True, linestyle="--", alpha=0.4)
    ax_vtc.legend(loc="lower left")

    # RIGHT PLOT: Series Inverter Voltage Mapping & Regions A - E
    ax_series.set_xlim(0, 10)
    ax_series.set_ylim(0, Vdd)
    ax_series.axis("off")
    ax_series.set_title("Series Inverter Mapping (Regions A to E)")

    # Draw Inverter 1 Output Bar (Left) and Inverter 2 Input Bar (Right)
    bar_w = 1.6
    x1, x2 = 1.5, 6.8

    # Inverter 1 Output Segments (A, Forbidden, E)
    ax_series.add_patch(
        patches.Rectangle(
            (x1, 0),
            bar_w,
            VOL,
            facecolor="#d9ead3",
            edgecolor="black",
            lw=1.2,
        )
    )
    ax_series.add_patch(
        patches.Rectangle(
            (x1, VOL),
            bar_w,
            VOH - VOL,
            facecolor="#f4cccc",
            edgecolor="black",
            lw=1.2,
            hatch="//",
        )
    )
    ax_series.add_patch(
        patches.Rectangle(
            (x1, VOH),
            bar_w,
            Vdd - VOH,
            facecolor="#cfe2f3",
            edgecolor="black",
            lw=1.2,
        )
    )

    # Inverter 2 Input Segments (Low accepted, Forbidden C, High accepted)
    ax_series.add_patch(
        patches.Rectangle(
            (x2, 0),
            bar_w,
            VIL,
            facecolor="#d9ead3",
            edgecolor="black",
            lw=1.2,
        )
    )
    ax_series.add_patch(
        patches.Rectangle(
            (x2, VIL),
            bar_w,
            VIH - VIL,
            facecolor="#fff2cc",
            edgecolor="black",
            lw=1.2,
            hatch="//",
        )
    )
    ax_series.add_patch(
        patches.Rectangle(
            (x2, VIH),
            bar_w,
            Vdd - VIH,
            facecolor="#cfe2f3",
            edgecolor="black",
            lw=1.2,
        )
    )

    # Labels above bars
    ax_series.text(
        x1 + bar_w / 2,
        Vdd + 0.15,
        "Inverter 1\n(Output)",
        ha="center",
        fontweight="bold",
    )
    ax_series.text(
        x2 + bar_w / 2,
        Vdd + 0.15,
        "Inverter 2\n(Input)",
        ha="center",
        fontweight="bold",
    )

    # Annotate Critical Levels on Bars
    ax_series.text(
        x1 - 0.2, VOH, f"$V_{{OH}}$={VOH}V", ha="right", va="center", fontsize=9
    )
    ax_series.text(
        x1 - 0.2, VOL, f"$V_{{OL}}$={VOL}V", ha="right", va="center", fontsize=9
    )
    ax_series.text(
        x2 + bar_w + 0.2,
        VIH,
        f"$V_{{IH}}$={VIH}V",
        ha="left",
        va="center",
        fontsize=9,
    )
    ax_series.text(
        x2 + bar_w + 0.2,
        VIL,
        f"$V_{{IL}}$={VIL}V",
        ha="left",
        va="center",
        fontsize=9,
    )

    # Highlight Regions A, B, C, D, E in the center gap
    mid_x = (x1 + bar_w + x2) / 2
    regions = [
        (0, VOL, "Region A (0 to $V_{OL}$)", "black", "normal", "normal"),
        (
            VOL,
            VIL,
            f"Region B -> $NM_L$ = {NML}V",
            nml_color,
            "bold",
            "normal",
        ),  # NML Region
        (VIL, VIH, "Region C (Undefined)", "dimgray", "normal", "italic"),
        (
            VIH,
            VOH,
            f"Region D -> $NM_H$ = {NMH}V",
            nmh_color,
            "bold",
            "normal",
        ),  # NMH Region
        (VOH, Vdd, "Region E ($V_{OH}$ to $V_{DD}$)", "black", "normal", "normal"),
    ]

    for y_low, y_high, text, color, weight, style in regions:
        y_center = (y_low + y_high) / 2
        # Draw dashed guide lines across the gap
        ax_series.plot(
            [x1 + bar_w, x2],
            [y_high, y_high],
            linestyle="--",
            color="gray",
            lw=0.8,
        )
        # Highlight NML (Region B) and NMH (Region D) with colored arrows/brackets
        if "Region B" in text or "Region D" in text:
            ax_series.annotate(
                "",
                xy=(mid_x - 1.3, y_high),
                xytext=(mid_x - 1.3, y_low),
                arrowprops=dict(arrowstyle="<->", color=color, lw=2.5),
            )
            ax_series.text(
                mid_x - 1.1,
                y_center,
                text,
                color=color,
                va="center",
                ha="left",
                fontsize=9.5,
                fontweight=weight,
                fontstyle=style,
            )
        else:
            ax_series.text(
                mid_x,
                y_center,
                text,
                color=color,
                va="center",
                ha="center",
                fontsize=8.5,
                fontweight=weight,
                fontstyle=style,
            )

    plt.tight_layout()

    # Save image before plt.show()
    plt.savefig(filename, dpi=300)
    print(f"Saved '{filename}'")

    plt.show()


if __name__ == "__main__":
    # Case 1: Asymmetric Inverter (NMH != NML -> Worst margin turns RED)
    plot_series_inverter_noise_margins(
        Vdd=5.0,
        beta_ratio=2.8,
        filename="noise_margin_asymmetric_red.png",
    )

    # Case 2: Symmetric Inverter (NMH == NML -> Both turn GREEN)
    plot_series_inverter_noise_margins(
        Vdd=5.0,
        beta_ratio=1.0,
        filename="noise_margin_symmetric_green.png",
    )
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ==========================================
# 1. Transistor Parameters (Updated per Assignment)
# ==========================================
Vdd = 5.0          # Supply voltage (V)
Vtn = 0.45         # nMOS threshold voltage (V)
Vthp = -0.6        # pMOS threshold voltage (V)
abs_Vtp = abs(Vthp)
beta = 1e-3        # Transconductance parameter (A/V^2)

V_sweep = np.linspace(0, Vdd, 500)
Vin_values = [0, 1, 2, 3, 4, 5]
colors = ['red', 'orange', 'blue', 'green', 'purple', 'brown']

# ==========================================
# 2. Generate the 3-Panel I-V Characteristic Plot
# ==========================================
fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# --- Panel 1: Original (nMOS in Q1, pMOS in Q3) ---
ax1 = axs[0]
for i, Vin in enumerate(Vin_values):
    color = colors[i]

    # nMOS
    Vgsn = Vin
    Idsn = np.zeros_like(V_sweep)
    if Vgsn > Vtn:
        lin_n = V_sweep < (Vgsn - Vtn)
        sat_n = ~lin_n
        Idsn[lin_n] = beta * ((Vgsn - Vtn) * V_sweep[lin_n] - 0.5 * V_sweep[lin_n]**2)
        Idsn[sat_n] = 0.5 * beta * (Vgsn - Vtn)**2

    if np.max(Idsn) > 0:
        ax1.plot(V_sweep, Idsn * 1000, color=color, linewidth=1.5)

    # pMOS
    Vgsp = Vin - Vdd
    Vdsp_sweep = -V_sweep
    Idsp = np.zeros_like(V_sweep)
    if abs(Vgsp) > abs_Vtp:
        lin_p = V_sweep < (abs(Vgsp) - abs_Vtp)
        sat_p = ~lin_p
        Idsp[lin_p] = beta * ((abs(Vgsp) - abs_Vtp) * V_sweep[lin_p] - 0.5 * V_sweep[lin_p]**2)
        Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - abs_Vtp)**2

    if np.max(Idsp) > 0:
        ax1.plot(Vdsp_sweep, -Idsp * 1000, color=color, linewidth=1.5)

ax1.axhline(0, color='black', linewidth=1.2)
ax1.axvline(0, color='black', linewidth=1.2)
ax1.set_title(f'1. Original I-V ($V_{{tn}}={Vtn}V, V_{{thp}}={Vthp}V$)')
ax1.set_xlabel('$V_{dsn}$ / $V_{dsp}$ (V)')
ax1.set_ylabel('$I_{dsn}$ / $I_{dsp}$ (mA)')
ax1.set_xlim(-Vdd, Vdd)
ax1.grid(alpha=0.3)

# --- Panel 2: Flipped (pMOS positive current) ---
ax2 = axs[1]
for i, Vin in enumerate(Vin_values):
    color = colors[i]

    # nMOS
    Vgsn = Vin
    Idsn = np.zeros_like(V_sweep)
    if Vgsn > Vtn:
        lin_n = V_sweep < (Vgsn - Vtn)
        sat_n = ~lin_n
        Idsn[lin_n] = beta * ((Vgsn - Vtn) * V_sweep[lin_n] - 0.5 * V_sweep[lin_n]**2)
        Idsn[sat_n] = 0.5 * beta * (Vgsn - Vtn)**2

    if np.max(Idsn) > 0:
        ax2.plot(V_sweep, Idsn * 1000, color=color, linewidth=1.5)

    # pMOS
    Vgsp = Vin - Vdd
    Vdsp_sweep = -V_sweep
    abs_Idsp = np.zeros_like(V_sweep)
    if abs(Vgsp) > abs_Vtp:
        lin_p = V_sweep < (abs(Vgsp) - abs_Vtp)
        sat_p = ~lin_p
        abs_Idsp[lin_p] = beta * ((abs(Vgsp) - abs_Vtp) * V_sweep[lin_p] - 0.5 * V_sweep[lin_p]**2)
        abs_Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - abs_Vtp)**2

    if np.max(abs_Idsp) > 0:
        ax2.plot(Vdsp_sweep, abs_Idsp * 1000, color=color, linewidth=1.5)

ax2.axhline(0, color='black', linewidth=1.2)
ax2.axvline(0, color='black', linewidth=1.2)
ax2.set_title('2. pMOS Flipped Vertically')
ax2.set_xlabel('$V_{dsn}$ / $V_{dsp}$ (V)')
ax2.set_ylabel('$I_{dsn}$ / $|I_{dsp}|$ (mA)')
ax2.set_xlim(-Vdd, Vdd)
ax2.grid(alpha=0.3)

# --- Panel 3: Shifted (Current vs Vout) ---
ax3 = axs[2]
Vout = np.linspace(0, Vdd, 500)

for i, Vin in enumerate(Vin_values):
    color = colors[i]

    # nMOS
    Vgsn = Vin
    Idsn = np.zeros_like(Vout)
    if Vgsn > Vtn:
        lin_n = Vout < (Vgsn - Vtn)
        sat_n = ~lin_n
        Idsn[lin_n] = beta * ((Vgsn - Vtn) * Vout[lin_n] - 0.5 * Vout[lin_n]**2)
        Idsn[sat_n] = 0.5 * beta * (Vgsn - Vtn)**2

    if np.max(Idsn) > 0:
        ax3.plot(Vout, Idsn * 1000, color=color, linewidth=1.5)
        ax3.text(Vout[-1] + 0.1, Idsn[-1] * 1000, f'$V_{{in}}={Vin}V$', color=color, va='center')

    # pMOS
    Vgsp = Vin - Vdd
    abs_Vdsp = Vdd - Vout
    abs_Idsp = np.zeros_like(Vout)
    if abs(Vgsp) > abs_Vtp:
        lin_p = abs_Vdsp < (abs(Vgsp) - abs_Vtp)
        sat_p = ~lin_p
        abs_Idsp[lin_p] = beta * ((abs(Vgsp) - abs_Vtp) * abs_Vdsp[lin_p] - 0.5 * abs_Vdsp[lin_p]**2)
        abs_Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - abs_Vtp)**2

    if np.max(abs_Idsp) > 0:
        ax3.plot(Vout, abs_Idsp * 1000, color=color, linewidth=1.5)
        ax3.text(Vout[0] - 0.1, abs_Idsp[0] * 1000, f'$V_{{in}}={Vin}V$', color=color, ha='right', va='center')

ax3.axhline(0, color='black', linewidth=1.5)
ax3.axvline(0, color='black', linewidth=1.5)
ax3.set_title('3. Current vs. $V_{out}, V_{in}$')
ax3.set_xlabel('$V_{out}$ (V)')
ax3.set_ylabel('$I_{dsn}, |I_{dsp}|$ (mA)')
ax3.set_xlim(0, Vdd)
ax3.grid(alpha=0.3)

legend_elements = [
    Line2D([0], [0], color=colors[i], lw=2, label=f'Vin = {Vin} V')
    for i, Vin in enumerate(Vin_values)
]
fig.legend(handles=legend_elements, loc='lower center', ncol=6, bbox_to_anchor=(0.5, -0.02))
plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig('MOS_IV_Characteristics.png', dpi=300, bbox_inches='tight')
plt.show()

# ==========================================
# 3. Tasks 3 & 4: Pinch-Off Boundary LUT & Continuity Check
# ==========================================
# Define helper function for nMOS drain current
def calc_ids_nmos(vgs, vds, vth=Vtn, b=beta):
    if vgs <= vth or vds <= 0:
        return 0.0
    elif vds < (vgs - vth):
        return b * ((vgs - vth) * vds - 0.5 * vds**2)
    else:
        return 0.5 * b * (vgs - vth)**2

# Generate LUT around Vds_sat = Vgs - Vtn using step = 0.05 V over [-0.5 V, +0.5 V]
step = 0.05
offsets = np.round(np.arange(-0.5, 0.5 + step, step), 3)
Vgs_active = [v for v in Vin_values if v > Vtn]  # Active gate voltages: 1, 2, 3, 4, 5 V

lut_records = []
for vgs in Vgs_active:
    vds_sat = vgs - Vtn
    for delta in offsets:
        vds_val = round(vds_sat + delta, 4)
        ids_mA = calc_ids_nmos(vgs, vds_val) * 1000
        region = "Cutoff" if vds_val <= 0 else ("Linear" if delta < 0 else ("Boundary" if delta == 0 else "Saturation"))
        lut_records.append({
            "Vgs (V)": vgs,
            "Vds_sat = Vgs-Vtn (V)": round(vds_sat, 2),
            "Offset (V)": delta,
            "Vds (V)": vds_val,
            "Region": region,
            "Ids (mA)": round(ids_mA, 6)
        })

lut_df = pd.DataFrame(lut_records)
lut_df.to_csv("MOS_Pinchoff_LUT.csv", index=False)
print("Saved Look-Up Table to 'MOS_Pinchoff_LUT.csv'. Sample rows around Vgs = 3V:")
print(lut_df[lut_df["Vgs (V)"] == 3].to_string(index=False))

# Plot Task 3 & 4: Vgs vs Vds boundary & Continuity around Vds = Vgs - Vth
fig2, (ax_bound, ax_cont) = plt.subplots(1, 2, figsize=(14, 5))

# Subplot A: Vgs vs Vds at the Pinch-Off Boundary (with +/- 0.5V window)
vgs_line = np.linspace(Vtn, Vdd, 100)
vds_line = vgs_line - Vtn
ax_bound.plot(vgs_line, vds_line, 'k--', label='$V_{ds} = V_{gs} - V_{tn}$ (Boundary)')
ax_bound.fill_between(vgs_line, vds_line - 0.5, vds_line + 0.5, color='gray', alpha=0.15, label='LUT Window ($\pm 0.5\text{ V}$)')

for i, vgs in enumerate(Vgs_active):
    sub = lut_df[lut_df["Vgs (V)"] == vgs]
    ax_bound.scatter(sub["Vgs (V)"], sub["Vds (V)"], color=colors[Vin_values.index(vgs)], s=25, zorder=3)

ax_bound.set_title('Task 3: $V_{gs}$ vs. $V_{ds}$ at Pinch-Off ($\pm 0.5\text{ V}$, step $0.05\text{ V}$)')
ax_bound.set_xlabel('$V_{gs}$ (V)')
ax_bound.set_ylabel('$V_{ds}$ (V)')
ax_bound.grid(alpha=0.3)
ax_bound.legend()

# Subplot B: Current Continuity Across the Pinch-Off Boundary
for i, vgs in enumerate(Vgs_active):
    sub = lut_df[lut_df["Vgs (V)"] == vgs]
    c = colors[Vin_values.index(vgs)]
    ax_cont.plot(sub["Vds (V)"], sub["Ids (mA)"], '-o', markersize=4, color=c, label=f'$V_{{gs}}={vgs}V$')
    # Highlight exact boundary point Vds = Vgs - Vtn
    b_pt = sub[sub["Offset (V)"] == 0]
    ax_cont.scatter(b_pt["Vds (V)"], b_pt["Ids (mA)"], color='black', s=60, zorder=5)

ax_cont.set_title('Task 4: Continuity Check Across $V_{ds} = V_{gs} - V_{tn}$')
ax_cont.set_xlabel('$V_{ds}$ (V)')
ax_cont.set_ylabel('$I_{ds}$ (mA)')
ax_cont.grid(alpha=0.3)
ax_cont.legend()

plt.tight_layout()
plt.savefig('MOS_Continuity_LUT.png', dpi=300)
plt.show()
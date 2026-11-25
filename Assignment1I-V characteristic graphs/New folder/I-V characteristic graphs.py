# import numpy as np
# import matplotlib.pyplot as plt

# # --- Transistor Parameters ---
# Vdd = 5.0      # Supply voltage
# Vt = 1.0       # Threshold voltage (Vtn = |Vtp| = Vt)
# beta = 1e-3    # Beta_n = Beta_p (make pMOS wider than nMOS)

# # Voltage arrays
# V_sweep = np.linspace(0, Vdd, 500) 
# Vin_values = [0, 1, 2, 3, 4, 5]       

# fig, axs = plt.subplots(1, 3, figsize=(18, 5))

# # ==========================================
# # 1. Original (nMOS in Q1, pMOS in Q3)
# # ==========================================
# ax1 = axs[0]
# for i, Vin in enumerate(Vin_values):
#     # nMOS calculations (Green, Q1)
#     Vgsn = Vin
#     Idsn = np.zeros_like(V_sweep)
#     if Vgsn > Vt:
#         lin_n = V_sweep < (Vgsn - Vt)
#         sat_n = V_sweep >= (Vgsn - Vt)
#         Idsn[lin_n] = beta * ((Vgsn - Vt) * V_sweep[lin_n] - 0.5 * V_sweep[lin_n]**2)
#         Idsn[sat_n] = 0.5 * beta * (Vgsn - Vt)**2
#     if np.max(Idsn) > 0:
#         ax1.plot(V_sweep, Idsn * 1000, color='limegreen', linewidth=1)

#     # pMOS calculations (Blue, Q3)
#     Vgsp = Vin - Vdd
#     Vdsp_sweep = -V_sweep
#     Idsp = np.zeros_like(V_sweep)
#     if abs(Vgsp) > Vt:
#         lin_p = V_sweep < (abs(Vgsp) - Vt)
#         sat_p = V_sweep >= (abs(Vgsp) - Vt)
#         Idsp[lin_p] = beta * ((abs(Vgsp) - Vt) * V_sweep[lin_p] - 0.5 * V_sweep[lin_p]**2)
#         Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - Vt)**2
#     if np.max(Idsp) > 0:
#         ax1.plot(Vdsp_sweep, -Idsp * 1000, color='blue', linewidth=1)

# ax1.axhline(0, color='black', linewidth=1.2)
# ax1.axvline(0, color='black', linewidth=1.2)
# ax1.set_title('1. Original I-V Characteristics')
# ax1.set_xlabel('$V_{dsn}$ / $V_{dsp}$ (V)')
# ax1.set_ylabel('$I_{dsn}$ / $I_{dsp}$ (mA)')
# ax1.set_xlim(-Vdd, Vdd)

# # ==========================================
# # 2. Flipped (pMOS flipped vertically to Positive I)
# # ==========================================
# ax2 = axs[1]
# for i, Vin in enumerate(Vin_values):
#     # nMOS stays exactly the same in Q1 (Green)
#     Vgsn = Vin
#     Idsn = np.zeros_like(V_sweep)
#     if Vgsn > Vt:
#         lin_n = V_sweep < (Vgsn - Vt)
#         sat_n = V_sweep >= (Vgsn - Vt)
#         Idsn[lin_n] = beta * ((Vgsn - Vt) * V_sweep[lin_n] - 0.5 * V_sweep[lin_n]**2)
#         Idsn[sat_n] = 0.5 * beta * (Vgsn - Vt)**2
#     if np.max(Idsn) > 0:
#         ax2.plot(V_sweep, Idsn * 1000, color='limegreen', linewidth=1)

#     # pMOS remains on the negative X-axis but flipped vertically to positive Y
#     Vgsp = Vin - Vdd
#     Vdsp_sweep = -V_sweep
#     abs_Idsp = np.zeros_like(V_sweep)
#     if abs(Vgsp) > Vt:
#         lin_p = V_sweep < (abs(Vgsp) - Vt)
#         sat_p = V_sweep >= (abs(Vgsp) - Vt)
#         abs_Idsp[lin_p] = beta * ((abs(Vgsp) - Vt) * V_sweep[lin_p] - 0.5 * V_sweep[lin_p]**2)
#         abs_Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - Vt)**2
#     if np.max(abs_Idsp) > 0:
#         # Plot positive current against negative voltage
#         ax2.plot(Vdsp_sweep, abs_Idsp * 1000, color='blue', linewidth=1)

# ax2.axhline(0, color='black', linewidth=1.2)
# ax2.axvline(0, color='black', linewidth=1.2)
# ax2.set_title('2. Same as First, pMOS Flipped Vertically')
# ax2.set_xlabel('$V_{dsn}$ / $V_{dsp}$ (V)')
# ax2.set_ylabel('$I_{dsn}$ / $|I_{dsp}|$ (mA)')
# ax2.set_xlim(-Vdd, Vdd) # Kept the same as the first plot

# # ==========================================
# # 3. Shifted (Current vs Vout, Vin)
# # ==========================================
# ax3 = axs[2]
# Vout = np.linspace(0, Vdd, 500)

# for i, Vin in enumerate(Vin_values):
#     # nMOS remains the same (Vdsn = Vout)
#     Vgsn = Vin
#     Idsn = np.zeros_like(Vout)
#     if Vgsn > Vt:
#         lin_n = Vout < (Vgsn - Vt)
#         sat_n = Vout >= (Vgsn - Vt)
#         Idsn[lin_n] = beta * ((Vgsn - Vt) * Vout[lin_n] - 0.5 * Vout[lin_n]**2)
#         Idsn[sat_n] = 0.5 * beta * (Vgsn - Vt)**2
    
#     if np.max(Idsn) > 0:
#         ax3.plot(Vout, Idsn * 1000, color='limegreen', linewidth=1)
#         ax3.text(Vout[-1] + 0.1, (Idsn[-1] * 1000), f'$V_{{in{i}}}$', color='green', va='center')

#     # pMOS shifted (|Vdsp| = Vdd - Vout)
#     Vgsp = Vin - Vdd
#     abs_Vdsp = Vdd - Vout
#     abs_Idsp = np.zeros_like(Vout)
#     if abs(Vgsp) > Vt:
#         lin_p = abs_Vdsp < (abs(Vgsp) - Vt)
#         sat_p = abs_Vdsp >= (abs(Vgsp) - Vt)
#         abs_Idsp[lin_p] = beta * ((abs(Vgsp) - Vt) * abs_Vdsp[lin_p] - 0.5 * abs_Vdsp[lin_p]**2)
#         abs_Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - Vt)**2
    
#     if np.max(abs_Idsp) > 0:
#         ax3.plot(Vout, abs_Idsp * 1000, color='blue', linewidth=1)
#         ax3.text(Vout[0] - 0.1, (abs_Idsp[0] * 1000), f'$V_{{in{i}}}$', color='blue', ha='right', va='center')

# ax3.axhline(0, color='black', linewidth=1.5)
# ax3.axvline(0, color='black', linewidth=1.5)
# ax3.set_title('3. Current vs. $V_{out}, V_{in}$ (pMOS Shifted)')
# ax3.set_xlabel('$V_{out}$ (V)')
# ax3.set_ylabel('$I_{dsn}, |I_{dsp}|$ (mA)')
# ax3.set_xlim(0, Vdd)

# plt.tight_layout()
# plt.show()


import numpy as np
import matplotlib.pyplot as plt

# --- Transistor Parameters ---
Vdd = 5.0
Vt = 1.0
beta = 1e-3

V_sweep = np.linspace(0, Vdd, 500)
Vin_values = [0, 1, 2, 3, 4, 5]

# Each Vin gets its own color
colors = ['red', 'orange', 'blue', 'green', 'purple', 'brown']

fig, axs = plt.subplots(1, 3, figsize=(18, 5))


# ==========================================
# 1. Original (nMOS Q1, pMOS Q3)
# ==========================================
ax1 = axs[0]

for i, Vin in enumerate(Vin_values):
    color = colors[i]

    # nMOS
    Vgsn = Vin
    Idsn = np.zeros_like(V_sweep)

    if Vgsn > Vt:
        lin_n = V_sweep < (Vgsn - Vt)
        sat_n = ~lin_n

        Idsn[lin_n] = beta * (
            (Vgsn - Vt) * V_sweep[lin_n]
            - 0.5 * V_sweep[lin_n]**2
        )
        Idsn[sat_n] = 0.5 * beta * (Vgsn - Vt)**2

    if np.max(Idsn) > 0:
        ax1.plot(V_sweep, Idsn * 1000,
                 color=color, linewidth=1.5)

    # pMOS
    Vgsp = Vin - Vdd
    Vdsp_sweep = -V_sweep
    Idsp = np.zeros_like(V_sweep)

    if abs(Vgsp) > Vt:
        lin_p = V_sweep < (abs(Vgsp) - Vt)
        sat_p = ~lin_p

        Idsp[lin_p] = beta * (
            (abs(Vgsp) - Vt) * V_sweep[lin_p]
            - 0.5 * V_sweep[lin_p]**2
        )
        Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - Vt)**2

    if np.max(Idsp) > 0:
        ax1.plot(Vdsp_sweep, -Idsp * 1000,
                 color=color, linewidth=1.5)

ax1.axhline(0, color='black', linewidth=1.2)
ax1.axvline(0, color='black', linewidth=1.2)
ax1.set_title('1. Original I-V Characteristics')
ax1.set_xlabel('$V_{dsn}$ / $V_{dsp}$ (V)')
ax1.set_ylabel('$I_{dsn}$ / $I_{dsp}$ (mA)')
ax1.set_xlim(-Vdd, Vdd)
ax1.grid(alpha=0.3)


# ==========================================
# 2. Flipped (pMOS positive current)
# ==========================================
ax2 = axs[1]

for i, Vin in enumerate(Vin_values):
    color = colors[i]

    # nMOS
    Vgsn = Vin
    Idsn = np.zeros_like(V_sweep)

    if Vgsn > Vt:
        lin_n = V_sweep < (Vgsn - Vt)
        sat_n = ~lin_n

        Idsn[lin_n] = beta * (
            (Vgsn - Vt) * V_sweep[lin_n]
            - 0.5 * V_sweep[lin_n]**2
        )
        Idsn[sat_n] = 0.5 * beta * (Vgsn - Vt)**2

    if np.max(Idsn) > 0:
        ax2.plot(V_sweep, Idsn * 1000,
                 color=color, linewidth=1.5)

    # pMOS
    Vgsp = Vin - Vdd
    Vdsp_sweep = -V_sweep
    abs_Idsp = np.zeros_like(V_sweep)

    if abs(Vgsp) > Vt:
        lin_p = V_sweep < (abs(Vgsp) - Vt)
        sat_p = ~lin_p

        abs_Idsp[lin_p] = beta * (
            (abs(Vgsp) - Vt) * V_sweep[lin_p]
            - 0.5 * V_sweep[lin_p]**2
        )
        abs_Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - Vt)**2

    if np.max(abs_Idsp) > 0:
        ax2.plot(Vdsp_sweep, abs_Idsp * 1000,
                 color=color, linewidth=1.5)

ax2.axhline(0, color='black', linewidth=1.2)
ax2.axvline(0, color='black', linewidth=1.2)
ax2.set_title('2. pMOS Flipped Vertically')
ax2.set_xlabel('$V_{dsn}$ / $V_{dsp}$ (V)')
ax2.set_ylabel('$I_{dsn}$ / $|I_{dsp}|$ (mA)')
ax2.set_xlim(-Vdd, Vdd)
ax2.grid(alpha=0.3)


# ==========================================
# 3. Shifted (Current vs Vout)
# ==========================================
ax3 = axs[2]
Vout = np.linspace(0, Vdd, 500)

for i, Vin in enumerate(Vin_values):
    color = colors[i]

    # nMOS
    Vgsn = Vin
    Idsn = np.zeros_like(Vout)

    if Vgsn > Vt:
        lin_n = Vout < (Vgsn - Vt)
        sat_n = ~lin_n

        Idsn[lin_n] = beta * (
            (Vgsn - Vt) * Vout[lin_n]
            - 0.5 * Vout[lin_n]**2
        )
        Idsn[sat_n] = 0.5 * beta * (Vgsn - Vt)**2

    if np.max(Idsn) > 0:
        ax3.plot(Vout, Idsn * 1000,
                 color=color, linewidth=1.5)

        ax3.text(
            Vout[-1] + 0.1,
            Idsn[-1] * 1000,
            f'$V_{{in}}={Vin}V$',
            color=color,
            va='center'
        )

    # pMOS
    Vgsp = Vin - Vdd
    abs_Vdsp = Vdd - Vout
    abs_Idsp = np.zeros_like(Vout)

    if abs(Vgsp) > Vt:
        lin_p = abs_Vdsp < (abs(Vgsp) - Vt)
        sat_p = ~lin_p

        abs_Idsp[lin_p] = beta * (
            (abs(Vgsp) - Vt) * abs_Vdsp[lin_p]
            - 0.5 * abs_Vdsp[lin_p]**2
        )
        abs_Idsp[sat_p] = 0.5 * beta * (abs(Vgsp) - Vt)**2

    if np.max(abs_Idsp) > 0:
        ax3.plot(Vout, abs_Idsp * 1000,
                 color=color, linewidth=1.5)

        ax3.text(
            Vout[0] - 0.1,
            abs_Idsp[0] * 1000,
            f'$V_{{in}}={Vin}V$',
            color=color,
            ha='right',
            va='center'
        )

ax3.axhline(0, color='black', linewidth=1.5)
ax3.axvline(0, color='black', linewidth=1.5)
ax3.set_title('3. Current vs. $V_{out}, V_{in}$')
ax3.set_xlabel('$V_{out}$ (V)')
ax3.set_ylabel('$I_{dsn}, |I_{dsp}|$ (mA)')
ax3.set_xlim(0, Vdd)
ax3.grid(alpha=0.3)

# Shared legend for all 3 graphs
from matplotlib.lines import Line2D

legend_elements = [
    Line2D([0], [0], color=colors[i], lw=2,
           label=f'Vin = {Vin} V')
    for i, Vin in enumerate(Vin_values)
]

fig.legend(
    handles=legend_elements,
    loc='lower center',
    ncol=6,
    bbox_to_anchor=(0.5, -0.02)
)

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.show()

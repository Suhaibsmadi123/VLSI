import numpy as np
import matplotlib.pyplot as plt

# CMOS Inverter Parameters
VDD = 5.0          # Supply Voltage (V)
VTN = 1.0          # NMOS Threshold Voltage (V)
VTP = -1.0         # PMOS Threshold Voltage (V)
kn = 100e-6        # NMOS Transconductance parameter (A/V^2)
kp = 100e-6        # PMOS Transconductance parameter (A/V^2)

def analyze_vin(vin, for_plot=False):
    """Identifies the DC operating region, Vout, and Ids for any given Vin."""
    if vin < 0 or vin > VDD:
        return "Out of Range", None, None, "Vin must be between 0V and VDD"
    
    vm = VDD / 2.0  # Switching threshold (2.5V)
    
    if vin < VTN:
        return "Region A", VDD, 0.0, "NMOS: Cutoff | PMOS: Linear (Symmetric with Region E)"
    elif vin > (VDD + VTP):
        return "Region E", 0.0, 0.0, "NMOS: Linear | PMOS: Cutoff (Symmetric with Region A)"
    elif np.isclose(vin, vm, atol=0.04):
        if for_plot:
            v_left = VDD - ((VDD - (vm - 0.04) + VTP) - np.sqrt((VDD - (vm - 0.04) + VTP)**2 - (kn/kp)*(vm - 0.04 - VTN)**2))
            v_right = (vm + 0.04 - VTN) - np.sqrt((vm + 0.04 - VTN)**2 - (kp/kn)*(VDD - (vm + 0.04) + VTP)**2)
            vout = v_left + ((vin - (vm - 0.04)) / 0.08) * (v_right - v_left)
            ids = 0.5 * kn * (vm - VTN)**2
        else:
            vout = vm
            ids = 0.5 * kn * (vin - VTN)**2
        return "Region C", vout, ids * 1e6, "NMOS: Saturation | PMOS: Saturation (Axis of Symmetry - MAX Ids)"
    elif VTN <= vin < vm:
        ids = 0.5 * kn * (vin - VTN)**2
        vsg_p = VDD - vin
        vsd = (vsg_p + VTP) - np.sqrt(max(0, (vsg_p + VTP)**2 - 2 * (ids / kp)))
        return "Region B", VDD - vsd, ids * 1e6, "NMOS: Saturation | PMOS: Linear (Symmetric with Region D)"
    else:
        ids = 0.5 * kp * (VDD - vin + VTP)**2
        vout = (vin - VTN) - np.sqrt(max(0, (vin - VTN)**2 - 2 * (ids / kn)))
        return "Region D", vout, ids * 1e6, "NMOS: Linear | PMOS: Saturation (Symmetric with Region B)"

# Generate sweep data
vin_sweep = np.linspace(0, VDD, 1000)
vout_sweep, ids_sweep = [], []

for v in vin_sweep:
    _, vo, i_ua, _ = analyze_vin(v, for_plot=True)
    vout_sweep.append(vo)
    ids_sweep.append(i_ua)

colors = ['#e8f4f8', '#d1e8e2', '#ffeaa7', '#d1e8e2', '#e8f4f8']
bounds = [0, VTN, VDD/2 - 0.04, VDD/2 + 0.04, VDD + VTP, VDD]
labels = ['Region A\n(Cutoff / Linear)', 'Region B\n(Sat / Linear)', 'C', 'Region D\n(Linear / Sat)', 'Region E\n(Linear / Cutoff)']

# ==========================================
# IMAGE 1: Voltage Transfer Characteristic (Vout vs Vin)
# ==========================================
fig1, ax1 = plt.subplots(figsize=(9, 4.5))
for i in range(5):
    ax1.axvspan(bounds[i], bounds[i+1], color=colors[i], alpha=0.65)
ax1.grid(True, linestyle='--', alpha=0.5)

ax1.plot(vin_sweep, vout_sweep, color='#1f77b4', lw=2.5, label='$V_{out}$ (Voltage Transfer Characteristic)')
ax1.set_xlabel('Input Voltage $V_{in}$ (V)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Output Voltage $V_{out}$ (V)', fontsize=11, fontweight='bold')
ax1.set_title('CMOS Inverter DC-DC Voltage Transfer Characteristic (Regions A–E)', fontsize=12, fontweight='bold')
ax1.legend(loc='upper right')

for i, txt in enumerate(labels):
    mid = (bounds[i] + bounds[i+1]) / 2
    y_pos = 2.5 if i != 2 else 4.1
    ax1.text(mid, y_pos, txt, ha='center', va='center', fontsize=9, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.85, edgecolor='gray'))

fig1.tight_layout()
fig1.savefig("1_vtc_characteristics.png", dpi=300, bbox_inches='tight')
print("Saved Image 1: '1_vtc_characteristics.png'")

# ==========================================
# IMAGE 2: Supply Current Ids across Regions A to E
# ==========================================
fig2, ax2 = plt.subplots(figsize=(9, 4.5))
for i in range(5):
    ax2.axvspan(bounds[i], bounds[i+1], color=colors[i], alpha=0.65)
ax2.grid(True, linestyle='--', alpha=0.5)

ax2.plot(vin_sweep, ids_sweep, color='#d62728', lw=2.5, label='$I_{DS}$ ($I_{DD}$ Supply Current)')
ax2.set_xlabel('Input Voltage $V_{in}$ (V)', fontsize=11, fontweight='bold')
ax2.set_ylabel('Current $I_{DS}$ ($\mu$A)', fontsize=11, fontweight='bold')
ax2.set_title('CMOS Inverter Supply Current ($I_{DS}$) Across Regions A–E', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')

# Add Region Labels on Current Plot
for i, txt in enumerate(['Region A\n($I_{DS} = 0$)', 'Region B\n($I_{DS} > 0$)', 'C', 'Region D\n($I_{DS} > 0$)', 'Region E\n($I_{DS} = 0$)']):
    mid = (bounds[i] + bounds[i+1]) / 2
    y_pos = 55 if i != 2 else 95
    if i in [0, 4]:
        y_pos = 25
    ax2.text(mid, y_pos, txt, ha='center', va='center', fontsize=8.5, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='white', alpha=0.85, edgecolor='gray'))

max_i = max(ids_sweep)
ax2.annotate(f'Max $I_{{DS}}$ = {max_i:.1f} $\mu$A\n(Region C: Both Saturated)',
             xy=(VDD/2, max_i), xytext=(VDD/2 + 0.55, max_i * 0.80),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=6),
             fontsize=9.5, fontweight='bold',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffeaa7', edgecolor='black'))

fig2.tight_layout()
fig2.savefig("2_ids_current.png", dpi=300, bbox_inches='tight')
print("Saved Image 2: '2_ids_current.png'")

plt.show()

# ==========================================
# Interactive Vin Classifier Loop
# ==========================================
while True:
    val = input(f"\nEnter Vin (0 to {VDD} V) or 'q' to quit: ").strip()
    if val.lower() == 'q':
        break
    try:
        user_vin = float(val)
        reg, vo, i_ds, details = analyze_vin(user_vin)
        print(f"--- Result for Vin = {user_vin} V ---")
        print(f"Operating Region : {reg}")
        print(f"Transistor States: {details}")
        if vo is not None:
            print(f"Output Voltage   : {vo:.3f} V")
            print(f"Supply Current   : {i_ds:.2f} uA")
    except ValueError:
        print("Please enter a valid number or 'q'.")
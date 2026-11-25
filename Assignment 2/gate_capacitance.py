import numpy as np

# 1. Declaration of constants (matching assignment template)
Epsilon_SiO2 = 3.45       # Dielectric constant of SiO2 (dimensionless)
Epsilon_0 = 8.854e-12     # Permittivity of free space in F/m

# 2. Definition of parameters
tox = 2e-9                # Oxide thickness in meters (2 nm)

# Gate areas: using 1e-6 as specified in your assignment prompt
# (Note: physically, 1 um^2 = 1e-12 m^2; change to 1e-12 if exact physical SI units are required)
A_values = np.array([10, 20, 30, 40, 120]) * 1e-6

# 3. Calculate base Gate Oxide Capacitance (C_ox) for each area
C_ox = (Epsilon_SiO2 * Epsilon_0 * A_values) / tox

# 4. Single Transistor Gate Capacitance in each region
C_gate_cutoff = C_ox               # C_gb = C_ox
C_gate_linear = C_ox               # C_gs (0.5*C_ox) + C_gd (0.5*C_ox) = C_ox
C_gate_sat = (2 / 3) * C_ox        # C_gs = (2/3)*C_ox, C_gd = 0

# 5. Array of 1000 Transistors Distribution
total_transistors = 1000
N_ohmic = 0.40 * total_transistors   # 40% = 400 transistors
N_cutoff = 0.15 * total_transistors  # 15% = 150 transistors
N_sat = 0.45 * total_transistors     # 45% = 450 transistors

# Total capacitance for each group (N_region * C_region)
C_total_ohmic = N_ohmic * C_gate_linear
C_total_cutoff = N_cutoff * C_gate_cutoff
C_total_sat = N_sat * C_gate_sat

# Grand total gate capacitance across all 1000 transistors
C_total_all = C_total_ohmic + C_total_cutoff + C_total_sat

# 6. Display Results
print(
    f"{'Area (um^2)':<12} | {'C_ox (F)':<12} | {'C_sat (F)':<12} | "
    f"{'Total Ohmic (400)':<18} | {'Total Cutoff (150)':<18} | "
    f"{'Total Sat (450)':<18} | {'Grand Total (1000)':<18}"
)
print("-" * 122)

for i, area in enumerate([10, 20, 30, 40, 120]):
    print(
        f"{area:<12} | "
        f"{C_ox[i]:<12.4e} | "
        f"{C_gate_sat[i]:<12.4e} | "
        f"{C_total_ohmic[i]:<18.4e} | "
        f"{C_total_cutoff[i]:<18.4e} | "
        f"{C_total_sat[i]:<18.4e} | "
        f"{C_total_all[i]:<18.4e}"
    )

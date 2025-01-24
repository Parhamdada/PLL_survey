import matplotlib.pyplot as plt
import pandas as pd

# Read data from Excel file
data_file = "pll_data.xlsx"
data = pd.read_excel(data_file)

# Extract columns from the Excel file
plls = data["Proceedings"]  # Column for PLL publication tilte and year
fom = data["FOM"]  # Column for FOM
frac_spur = data["FracSpur"]  # Column for worst fractional spur level
area = data["Area"]  # Column for area
types = data["Architecture"].apply(lambda x: 'BBPLL' if 'BBPLL' in str(x) else x)  # Assign Type 1 to entries containing '1'
osc_types = data["Oscillator"] # Oscillator type (Ring oscillator or LC oscillator)

# To debug the code you may use the following commands
# import ipdb
# ipdb.set_trace()

# Normalize the size for better visualization
size_scale = 0.002  # Adjust this scale as needed for better visualization
sizes = [size / size_scale for size in area]

# Map oscillator types to numerical values for coloring
color_map = {"LC": "green", "Ring": "blue"}
osc_types_colors = [color_map[x] for x in osc_types]

# Create the plot
plt.figure(figsize=(6.8, 6)) #Dimension of the figure in inches
for t, marker in [('BBPLL', 'o'), ('DPLL', 's'), ('MDLL', '^')]:
    type_filter = types == t
    scatter = plt.scatter(
        fom[type_filter],
        frac_spur[type_filter],
        s=[sizes[i] for i in range(len(sizes)) if types[i] == t],
        c=[osc_types_colors[i] for i in range(len(osc_types_colors)) if types[i] == t],
        marker=marker,
        alpha=0.8, 
        label=f"Type {t}")

# Add labels for each pll
for i, pll in enumerate(plls):
    plt.text(fom[i], frac_spur[i], pll, fontsize=9, ha='right', va='bottom')

# Emphasize the first data input with a red star
plt.scatter(
    fom[0], 
    frac_spur[0], 
    s=2500,  # Fixed size for emphasis
    edgecolor="red",
    facecolor="none",
    linewidth=1.5,
    marker="*", 
    label="Highlighted PLL"
)

# Set plot labels and title
plt.xlabel("FOM (dB)", fontsize=16)
plt.ylabel("Fractional Spur (dBc)", fontsize=16)
# plt.title("Comparison of PLLs", fontsize=14)
# plt.xlim(80, 100)  # Adjust x-axis limits if necessary
# plt.ylim(0, 6e9)  # Adjust y-axis limits if necessary

# Add a legend for oscillator type
import matplotlib.patches as mpatches
ring_patch = mpatches.Patch(color="blue", label="Ring")
lc_patch = mpatches.Patch(color="green", label="LC")
osc_type_legend = plt.legend(handles=[ring_patch, lc_patch], title="Oscillator type", fontsize=16, loc="upper left")
plt.gca().add_artist(osc_type_legend)

# Add legend for PLL types
from matplotlib.lines import Line2D
type_legend_elements = [
    Line2D([0], [0], marker='o', color='k', label='BBPLL', markersize=10),
    Line2D([0], [0], marker='s', color='k', label='DPLL (w/ TDC)', markersize=10),
    Line2D([0], [0], marker='^', color='k', label='MDLL', markersize=10)
]
plt.legend(handles=type_legend_elements, title="PLL Type", fontsize=16, loc="upper right")

# Add a footnote
plt.figtext(0, 0.005, "*Size of each point corresponds to the area of the PLL", 
            wrap=True, horizontalalignment='left', fontsize=12, alpha=0.7)

# Show grid
plt.grid(True, linestyle="--", alpha=0.6)

# Show the plot
plt.tight_layout()
plt.show()

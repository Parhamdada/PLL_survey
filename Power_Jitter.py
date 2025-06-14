import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import itertools

# Set fonttype to TrueType (42) to ensure proper font embedding
matplotlib.rcParams['pdf.fonttype'] = 42

# Read data from Excel file and convert to a list of dictionaries
data_file = 'pll_data.csv'
data = pd.read_csv(data_file, quotechar='"').to_dict('records')

# To debug the code you may use the following commands
# import ipdb
# ipdb.set_trace()

# Normalize the size for better visualization
size_scale = 0.002

# Map oscillator types to colors
color_map = {
    "TDC-DPLL": "green",
    "BB-DPLL": "blue",
    "CP-APLL": "pink",
    "SS-APLL": "yellow",
    "TDC-MDLL": "purple",
    "CP-ILCM": "brown",
    "others": "gray",  # Default color for unrecognized types
}
used_colors = set()

plt.figure(figsize=(6.8, 6)) #Dimension of the figure in inches
for item in data:
    # Color is based on Phase detector and architecture types
    phase_det = item['PhaseDetector'].split('/')
    arch = item['Architecture'].split('/')
    item['arch_name'] = ["{}-{}".format(pd_type, arch_type) for pd_type, arch_type in zip(phase_det, itertools.cycle(arch))]
    item['plot_color'] = color_map.get(item['arch_name'][0], color_map['others']) if len(item['arch_name']) == 1 else color_map['others']

    item['plot_shape'] = {'Ring': 's', 'LC': 'o'}.get(item['Oscillator'])
    item['plot_size'] = item['Area'] / size_scale

filtered_data = [item for item in data if (item['Plot'] is not False)]
for item in filtered_data:
    plt.scatter(
        item['Jitter'],
        item['Power'],
        s=item['plot_size'],
        facecolor=item['plot_color'] if (~np.isnan(item['FracSpur'])) else 'none',
        edgecolor=item['plot_color'],
        marker=item['plot_shape'],
        alpha=0.8
    )
    plt.text(
        item['Jitter'],
        item['Power'],
        item['Proceedings'],
        fontsize=9,
        ha='right',
        va='bottom'
    )
    used_colors.add(item['plot_color'])


# Emphasize the first data input with a red star
if (data[0]['Plot'] is not False):
    plt.scatter(
        data[0]['Jitter'],
        data[0]['Power'],
        s=2500,  # Fixed size for emphasis
        edgecolor="red",
        facecolor="none",
        linewidth=1.5,
        marker="*"
    )

plt.xlim(8, 3000)  # Adjust x-axis limits if necessary
plt.ylim(0.5, 400)  # Adjust y-axis limits if necessary

# Add FOM lines
FOM_lines = [-260, -255, -250, -245, -240, -235, -230]
FOM_values = [10**((x+300)/10) for x in FOM_lines]
x_vals = np.logspace(np.log10(plt.xlim()[0]), np.log10(plt.xlim()[1]), 500)
for FOM, label in zip(FOM_values, FOM_lines):
    y_vals = FOM / (x_vals ** 2)
    plt.plot(x_vals, y_vals, linestyle='--', color='gray', alpha=0.5)
    # Add label to the line
    y_label_pos = 80
    x_label_pos = np.sqrt(FOM / y_label_pos)*1.1
    plt.text(x_label_pos, y_label_pos, f"FOM={label}", fontsize=10, color='gray', alpha=0.85, ha='right', va='bottom', rotation=-60)

# Set plot labels and title
plt.xlabel("Integrated Jitter (fs)", fontsize=16)
plt.ylabel("Power Consumption (mW)", fontsize=16)
plt.xscale('log')
plt.yscale('log')
# plt.title("Comparison of fractional PLLs", fontsize=14)

# Add a legend for PLL types
filtered_color_map = {key: value for key, value in color_map.items() if value in used_colors}
from matplotlib.lines import Line2D
color_legends = [Line2D([],[], color="white", marker='o', markersize=10, markerfacecolor=value, label=key) 
                    for key, value in filtered_color_map.items()]
pll_type_legend = plt.legend(handles=color_legends, title="PLL type", fontsize=10, loc="upper right")
plt.gca().add_artist(pll_type_legend)

# Add legend for oscillator types
type_legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='k', label='LC', markersize=10),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='k', label='Ring', markersize=10),
]
osc_type_legend = plt.legend(handles=type_legend_elements, title="Oscillator type", fontsize=10, loc="lower left", bbox_to_anchor=(0, 0.1))
plt.gca().add_artist(osc_type_legend)

# Add legend for PLL division types
division_legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='k', markeredgecolor='k', label='Fractional-N', markersize=10),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='none', markeredgecolor='k', label='Integer-N', markersize=10),
]
plt.legend(handles=division_legend_elements, title=None, fontsize=10, loc="lower left")

# Add a footnote
plt.figtext(0, 0.01, "*Size of each point corresponds to the area of the PLL", \
            wrap=True, horizontalalignment='left', fontsize=12, alpha=0.7)

# Show grid
plt.minorticks_on()
plt.grid(True, which="both", linestyle="--", alpha=0.6)

plt.tight_layout()

# Example command to save the plot
plt.savefig('Power_Jitter.svg', format='svg')

# Show the plot
plt.show()

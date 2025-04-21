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
    "TDC-MDLL": "purple",
    "SS-DPLL": "cyan",
    "BB-MDLL": "orange",
    "SS-APLL": "yellow",
    "CP-ILCM": "brown",
    "CP-APLL": "pink",
}
used_colors = set()

plt.figure(figsize=(6.8, 6)) #Dimension of the figure in inches
for item in data:
    # Color is based on Phase detector and architecture types
    phase_det = item['PhaseDetector'].split('/')
    arch = item['Architecture'].split('/')
    item['arch_name'] = ["{}-{}".format(pd_type, arch_type) for pd_type, arch_type in zip(phase_det, itertools.cycle(arch))]
    color_list = [mcolors.to_rgb(color_map.get(name, 'gray')) for name in item['arch_name']]
    item['plot_color'] = np.mean(color_list, axis=0)
    
    
    item['plot_shape'] = {'Ring': 's', 'LC': 'o'}.get(item['Oscillator'])
    item['plot_size'] = item['Area'] / size_scale

filtered_data = [item for item in data if (item['Plot'] is not False) & (~np.isnan(item['FracSpur']))]
for item in filtered_data:
    plt.scatter(
        item['FracSpur'],
        item['Jitter'],
        s=item['plot_size'],
        facecolor=item['plot_color'],
        marker=item['plot_shape'],
        alpha=0.8
    )
    plt.text(
        item['FracSpur'],
        item['Jitter'],
        item['Proceedings'],
        fontsize=9,
        ha='right',
        va='bottom'
    )
    used_colors.update(item['arch_name'])


# Emphasize the first data input with a red star
if (data[0]['Plot'] is not False) & (~np.isnan(data[0]['FracSpur'])):
    plt.scatter(
        data[0]['FracSpur'],
        data[0]['Jitter'],
        s=2500,  # Fixed size for emphasis
        edgecolor="red",
        facecolor="none",
        linewidth=1.5,
        marker="*"
    )

# Add a horizontal line at minimum of Ring-Oscillator-based PLLs
filtered_ring = [item for item in filtered_data if item['Oscillator'] == 'Ring']
if filtered_ring:
    min_jitter = min(item['Jitter'] for item in filtered_ring)
    plt.axhline(y=min_jitter, color='gray', linestyle='--', label='Min Ring-Oscillator Jitter')
    plt.text(
        x=plt.gca().get_xlim()[1] - 15,  # Start of the x-axis
        y=min_jitter + 0.05 * min_jitter,  # Slightly above the line
        s=f"Min Ring-Osc Jitter: {min_jitter:.0f} fs",
        color='gray',
        fontsize=10,
        ha='left',
        va='bottom'
    )


# Set plot labels and title
plt.xlabel("Fractional Spur (dBc)", fontsize=16)
plt.ylabel("Integrated Jitter (fs)", fontsize=16)
# plt.title("Comparison of fractional PLLs", fontsize=14)
# plt.xlim(80, 100)  # Adjust x-axis limits if necessary
# plt.ylim(0, 6e9)  # Adjust y-axis limits if necessary

# Add a legend for PLL types
filtered_color_map = {key: value for key, value in color_map.items() if key in used_colors}
from matplotlib.lines import Line2D
color_legends = [Line2D([],[], color="white", marker='o', markersize=10, markerfacecolor=value, label=key) 
                    for key, value in filtered_color_map.items()]
osc_type_legend = plt.legend(handles=color_legends, title="PLL type", fontsize=10, loc="upper right")
plt.gca().add_artist(osc_type_legend)

# Add legend for oscillator types
type_legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='k', label='LC', markersize=10),
    Line2D([0], [0], marker='s', color='w', markerfacecolor='k', label='Ring', markersize=10),
]
plt.legend(handles=type_legend_elements, title="Oscillator type", fontsize=10, loc="upper left")

# Add a footnote
plt.figtext(0, 0.01, "*Size of each point corresponds to the area of the PLL" \
            "\n**Complex architectures are shown with mixed colors" , \
            wrap=True, horizontalalignment='left', fontsize=12, alpha=0.7)

# Show grid
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout(rect=(0, 0.04, 1, 1))  # Adjust layout to make room for the footnote

# Example command to save the plot
plt.savefig('Jitter_Spur.svg', format='svg')

# Show the plot
plt.show()

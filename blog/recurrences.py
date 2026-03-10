import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def draw_nodes(ax, start_idx, end_idx, y_pos=0):
    """Draws and labels the cells (nodes) in the row."""
    x_coords = np.arange(start_idx, end_idx + 1)
    ax.scatter(x_coords, [y_pos]*len(x_coords), color='black', zorder=5)

    for x in x_coords:
        label = f"x-{end_idx - x}" if x != end_idx else "x"
        label = label.replace("-0", "")
        ax.text(x, y_pos - 0.5, f"${label}$", ha='center', va='top', fontsize=9)
        ax.plot([x, x], [y_pos - 0.2, y_pos + 0.2],
                color='gray', linestyle=':', alpha=0.5)

def draw_path(ax, x1, x2, y, label, color, rad=-0.3, ls='-', y_offset=0.2):
    """Draws an arc between two nodes."""
    if x1 is None:
        x1 = 0
        arrow = patches.FancyArrowPatch(
            (0, y+(1 if rad < 0 else -1.5)), (x2, y),
            connectionstyle=f"arc3,rad={rad}",
            color=color, arrowstyle="->", mutation_scale=12,
            linewidth=2, linestyle=ls, zorder=3
        )
    else:
        arrow = patches.FancyArrowPatch(
            (x1, y), (x2, y),
            connectionstyle=f"arc3,rad={rad}",
            color=color, arrowstyle="->", mutation_scale=12,
            linewidth=2, linestyle=ls, zorder=3
        )
    ax.add_patch(arrow)

    mid_x = (x1 + x2) / 2
    peak_y = y + (x2 - x1 + 0.5) * abs(rad) / 2 * (-1 if rad > 0 else 1) + y_offset
    ax.text(mid_x, peak_y, label, ha='center', va='center', color=color,
            fontsize=10, fontweight='bold',
            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=1))

def setup_figure(title, ylim):
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.set_title(title, fontsize=14, pad=10)
    ax.axis('off')
    ax.set_xlim(-1, 17)
    ax.set_ylim(*ylim)
    return fig, ax

# Colors
c_pass = "#1f77b4"
c_skip = "#ff7f0e"
c_over = "#d62728"
c_sum  = "#2ca02c"


# --- Figure 1: d16 ---
fig, ax = setup_figure("Decomposition of $d_{16}(x)$", (-3, 4))
draw_nodes(ax, 0, 16)

draw_path(ax, 0, 8, 0, "$d_8(x-8)$", c_pass, rad=-0.4, y_offset=-0.5)
draw_path(ax, 8, 16, 0, "$d_8(x)$", c_pass, rad=-0.4, y_offset=-0.5)

draw_path(ax, 0, 7, 0, "$d_7(x-9)$", c_skip, rad=0.4, y_offset=-0.1)
draw_path(ax, 7, 9, 0, "$b(x-7)$ (2-step)", c_skip, rad=0.6, y_offset=-0.2)
draw_path(ax, 9, 16, 0, "$d_7(x)$", c_skip, rad=0.4, y_offset=-0.1)

fig.savefig("img/recurrence-d16.png", bbox_inches="tight", dpi=300)
plt.close(fig)


# --- Figure 2: d15 ---
fig, ax = setup_figure("Decomposition of $d_{15}(x)$", (-6, 7))
draw_nodes(ax, 1, 16)

draw_path(ax, 1, 8, 0, "$d_7(x-8)$", c_pass, rad=0.4, y_offset=-0.5)
draw_path(ax, 8, 16, 0, "$d_8(x)$", c_pass, rad=0.4, y_offset=-0.5)

draw_path(ax, 1, 9, 0, "$d_8(x-7)$", c_skip, rad=-0.4, y_offset=0.6)
draw_path(ax, 9, 16, 0, "$d_7(x)$", c_skip, rad=-0.4, y_offset=0.6)

draw_path(ax, 1, 8, 0, "$d_7(x-8)$", c_over, rad=0.6, y_offset=-1.6, ls='--')
draw_path(ax, 8, 9, 0, "$-a(x-7)$\n(1-step)", c_over, rad=1.2, y_offset=-0.6, ls='--')
draw_path(ax, 9, 16, 0, "$d_7(x)$", c_over, rad=0.6, y_offset=-1.6, ls='--')

fig.savefig("img/recurrence-d15.png", bbox_inches="tight", dpi=300)
plt.close(fig)


# --- Figure 3: f16 ---
fig, ax = setup_figure("Decomposition of $f_{16}(x)$", (-5, 6))
draw_nodes(ax, 0, 16)

draw_path(ax, 8, 16, 0, "$f_8(x)$", c_sum, rad=0.2, y_offset=-0.6)

draw_path(ax, 0, 8, 0, "$f_8(x-8)$", c_pass, rad=-0.4, y_offset=0.3)
draw_path(ax, 8, 16, 0, "$d_8(x)$", c_pass, rad=-0.4, y_offset=0.3)

draw_path(ax, 0, 7, 0, "$f_7(x-9)$", c_skip, rad=0.4, y_offset=-0.8)
draw_path(ax, 7, 9, 0, "$b(x-7)$\n(2-step)", c_skip, rad=0.6, y_offset=-0.6)
draw_path(ax, 9, 16, 0, "$d_7(x)$", c_skip, rad=0.4, y_offset=-0.8)

fig.savefig("img/recurrence-f16.png", bbox_inches="tight", dpi=300)
plt.close(fig)

fig, ax = setup_figure("Tropical decomposition of $d_{16}(x)$", (-3, 4))
draw_nodes(ax, 0, 16)

draw_path(ax, 0, 8, 0, "$d_8(x-8)$", c_pass, rad=-0.4, y_offset=-0.5)
draw_path(ax, 8, 16, 0, "$d_8(x)$", c_pass, rad=-0.4, y_offset=-0.5)

draw_path(ax, 0, 7, 0, "$d_7(x-9)$", c_skip, rad=0.4, y_offset=-0.1)
draw_path(ax, 7, 9, 0, "$d_2(x-7)$", c_skip, rad=0.6, y_offset=-0.2)
draw_path(ax, 9, 16, 0, "$d_7(x)$", c_skip, rad=0.4, y_offset=-0.1)

fig.savefig("img/recurrence-d16-tropical.png", bbox_inches="tight", dpi=300)
plt.close(fig)


fig, ax = setup_figure("Tropical decomposition of $d_{15}(x)$", (-6, 7))
draw_nodes(ax, 1, 16)

draw_path(ax, 1, 8, 0, "$d_7(x-8)$", c_pass, rad=0.4, y_offset=-0.5)
draw_path(ax, 8, 16, 0, "$d_8(x)$", c_pass, rad=0.4, y_offset=-0.5)

draw_path(ax, 1, 9, 0, "$d_8(x-7)$", c_skip, rad=-0.4, y_offset=0.6)
draw_path(ax, 9, 16, 0, "$d_7(x)$", c_skip, rad=-0.4, y_offset=0.6)

fig.savefig("img/recurrence-d15-tropical.png", bbox_inches="tight", dpi=300)
plt.close(fig)


fig, ax = setup_figure("Tropical decomposition of $f_{16}(x)$", (-5, 6))
draw_nodes(ax, -1, 16)

draw_path(ax, 8, 16, 0, "$f_8(x)$", c_sum, rad=0.2, y_offset=-0.6)

draw_path(ax, 0, 8, 0, "$f_8(x-8)$", c_pass, rad=-0.4, y_offset=0.3)
draw_path(ax, 8, 16, 0, "$d_8(x)$", c_pass, rad=-0.4, y_offset=0.3)

draw_path(ax, -1, 7, 0, "$f_8(x-9)$\n(subsumes $f_7(x-9)$)", c_skip, rad=0.4, y_offset=0.3, ls='--')
draw_path(ax, 0, 7, 0, "$f_7(x-9)$", c_skip, rad=0.6, y_offset=-1.0)
draw_path(ax, 7, 9, 0, "$b(x-7)$\n(2-step)", c_skip, rad=0.6, y_offset=-0.6)
draw_path(ax, 9, 16, 0, "$d_7(x)$", c_skip, rad=0.4, y_offset=-0.8)

fig.savefig("img/recurrence-f16-tropical.png", bbox_inches="tight", dpi=300)
plt.close(fig)


fig, ax = setup_figure("Tropical decomposition of $f(x)$", (-5, 6))
x_coords = [
    "x-20", "x-19", "x-18", "x-17", "x-16", "x-15",
    "...", "x-9", "x-8", "x-7", "x-6", "x-5", "x-4", "x-3", "x-2", "x-1", "x"
]
y_pos = 0
ax.scatter(x_coords, [y_pos]*len(x_coords), color='black', zorder=5)

for x, label in enumerate(x_coords):
    ax.text(x, y_pos - 0.5, f"${label}$", ha='center', va='top', fontsize=9)
    ax.plot([x, x], [y_pos - 0.2, y_pos + 0.2],
            color='gray', linestyle=':', alpha=0.5)

draw_path(ax, 4, 16, 0, "$f_{16}(x)$\n(local contribution)", c_sum, rad=0.2, y_offset=0.2)

draw_path(ax, None, 4, 0, "$f(x-16)$", c_pass, rad=-0.2, y_offset=0.3)
draw_path(ax, 4, 16, 0, "$d_{16}(x)$", c_pass, rad=-0.2, y_offset=0.1)

draw_path(ax, 5, 16, 0, "$d_{15}(x)$", c_skip, rad=0.4, y_offset=-0.6)
draw_path(ax, 3, 5, 0, "$b(x-15)$\n(2-step)", c_skip, rad=0.6, y_offset=-0.6)
draw_path(ax, None, 3, 0, "$f(x-17)$", c_skip, rad=0.2, y_offset=-1.2)

fig.savefig("img/recurrence-f-tropical.png", bbox_inches="tight", dpi=300)
plt.close(fig)

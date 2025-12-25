import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

FS_SUPTITLE = 20
FS_TITLE = 16
FS_LABEL = 13
FS_ANNOT_BIG = 14
FS_ANNOT_SMALL = 12
FS_BASE_ANNOT = 15

def draw_quadrupole_rods(ax):
    r = 0.8
    offset = 1.4
    rod_color = "#dddddd"
    edge_color = "#444444"

    rods = [
        patches.Circle((0, offset), r, facecolor=rod_color, edgecolor=edge_color, lw=2),
        patches.Circle(
            (0, -offset), r, facecolor=rod_color, edgecolor=edge_color, lw=2
        ),
        patches.Circle(
            (-offset, 0), r, facecolor=rod_color, edgecolor=edge_color, lw=2
        ),
        patches.Circle((offset, 0), r, facecolor=rod_color, edgecolor=edge_color, lw=2),
    ]
    for rod in rods:
        ax.add_patch(rod)

    ax.text(
        0,
        offset,
        "+RF",
        ha="center",
        va="center",
        fontsize=FS_ANNOT_SMALL,
        weight="bold",
        color="#333333",
    )
    ax.text(
        0,
        -offset,
        "+RF",
        ha="center",
        va="center",
        fontsize=FS_ANNOT_SMALL,
        weight="bold",
        color="#333333",
    )
    ax.text(
        -offset,
        0,
        "-RF",
        ha="center",
        va="center",
        fontsize=FS_ANNOT_SMALL,
        weight="bold",
        color="#333333",
    )
    ax.text(
        offset,
        0,
        "-RF",
        ha="center",
        va="center",
        fontsize=FS_ANNOT_SMALL,
        weight="bold",
        color="#333333",
    )

    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-3.1, 3.1)
    ax.axis("off")
    ax.set_aspect("equal")

def draw_ions(ax, n_ions, spread, color="red"):
    np.random.seed(42)
    x = np.random.normal(0, spread, n_ions)
    y = np.random.normal(0, spread, n_ions)
    ax.scatter(
        x, y, color=color, alpha=0.7, s=40, edgecolors="white", linewidth=0.5, zorder=10
    )
    confinement = patches.Circle(
        (0, 0), 0.5, fill=False, edgecolor="blue", linestyle="--", alpha=0.4, lw=1.5
    )
    ax.add_patch(confinement)

def draw_spectrum(ax, mu, sigma, title, color="blue", y_limit=1.25):
    x = np.linspace(99.4, 100.6, 500)
    y = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    y = y / max(y)

    ax.plot(x, y, color=color, lw=3)
    ax.fill_between(x, y, color=color, alpha=0.3)

    ax.set_xlabel("m/z", fontsize=FS_LABEL, weight="bold")
    ax.set_ylabel("Intensity", fontsize=FS_LABEL)
    ax.set_title(title, fontsize=FS_TITLE - 2)

    ax.set_yticks([])
    ax.set_ylim(0, y_limit)
    ax.set_xlim(99.4, 100.6)
    ax.tick_params(axis="x", labelsize=FS_ANNOT_SMALL)

fig = plt.figure(figsize=(13, 11))
fig.suptitle(
    "Space-charge effect", fontsize=FS_SUPTITLE, weight="bold", y=0.99
)

# Left side: Ideal case
ax1 = fig.add_subplot(2, 2, 1)
draw_quadrupole_rods(ax1)
draw_ions(ax1, n_ions=20, spread=0.1)
ax1.set_title("Low density of ions (Ideal)", fontsize=FS_TITLE, weight="bold")

ax1.text(
    0,
    -2.9,
    "Strong confinement (RF)\n(dominant field)",
    ha="center",
    va="top",
    color="blue",
    fontsize=FS_BASE_ANNOT,
    weight="bold",
)

ax2 = fig.add_subplot(2, 2, 3)
draw_spectrum(
    ax2, mu=100.0, sigma=0.03, title="Narrow peak (high resolution)", y_limit=1.3
)

ax2.text(
    100.0,
    1.1,
    "Negligible Coulomb\ninteraction",
    ha="center",
    va="bottom",
    fontsize=FS_ANNOT_BIG,
    color="green",
    weight="bold",
)

# Right side: Space-charge effect
ax3 = fig.add_subplot(2, 2, 2)
draw_quadrupole_rods(ax3)
draw_ions(ax3, n_ions=250, spread=0.45)
ax3.set_title(
    "High density of ions (space-charge effect)", fontsize=FS_TITLE, weight="bold"
)

ax3.annotate(
    "",
    xy=(0.9, 0.9),
    xytext=(0.1, 0.1),
    arrowprops=dict(arrowstyle="->", color="red", lw=3),
)
ax3.annotate(
    "",
    xy=(-0.9, -0.6),
    xytext=(-0.1, -0.1),
    arrowprops=dict(arrowstyle="->", color="red", lw=3),
)
ax3.annotate(
    "",
    xy=(0.2, -1.0),
    xytext=(0.0, -0.1),
    arrowprops=dict(arrowstyle="->", color="red", lw=3),
)

ax3.text(
    0,
    -2.9,
    "Internal Coulomb repulsion \n(ion cloud expansion)",
    ha="center",
    va="top",
    color="red",
    fontsize=FS_BASE_ANNOT,
    weight="bold",
)

ax4 = fig.add_subplot(2, 2, 4)
draw_spectrum(
    ax4,
    mu=100.15,
    sigma=0.12,
    title="Peak widening and 'mass shift'",
    color="red",
    y_limit=1.3,
)

ax4.axvline(
    100.0,
    color="blue",
    linestyle="--",
    alpha=0.6,
    lw=2,
    label="Real mass (theoretical)",
)

ax4.legend(loc="upper right", fontsize=FS_ANNOT_SMALL)

ax4.text(
    99.7,
    1.1,
    "Loss in resolution\nand precision",
    ha="center",
    va="bottom",
    fontsize=FS_ANNOT_BIG,
    color="red",
    weight="bold",
)

plt.tight_layout(rect=[0, 0.03, 1, 0.96], h_pad=5.0, w_pad=2.0)
plt.show()

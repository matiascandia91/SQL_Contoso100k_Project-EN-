import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images") + os.sep

BLUE, ORANGE = "#257de0", "#f47230"
INK, INK2 = "#191919", "#666666"
GRID, AXIS = "#e7e7e7", "#c2c2c2"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": AXIS,
    "axes.labelcolor": INK2,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "text.color": INK,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def style(ax):
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", length=0)


# ---------- 1. Customer segmentation ----------
segments = ["Low-Value", "Mid-Value", "High-Value"]
customers = np.array([12372, 24743, 12372])
ltv = np.array([4341809.527328117, 66636451.787238926, 135429277.2654986])
cust_pct = customers / customers.sum() * 100
ltv_pct = ltv / ltv.sum() * 100

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=200)
x = np.arange(3)
w = 0.34
b1 = ax.bar(x - w / 2 - 0.01, cust_pct, w, color=BLUE, label="% of customers")
b2 = ax.bar(x + w / 2 + 0.01, ltv_pct, w, color=ORANGE, label="% of total revenue (LTV)")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.2,
                f"{b.get_height():.1f}%", ha="center", va="bottom",
                fontsize=10.5, color=INK)
ax.set_xticks(x)
ax.set_xticklabels(segments, fontsize=11)
ax.set_ylim(0, 80)
ax.set_yticks([0, 20, 40, 60, 80])
ax.set_yticklabels([f"{v}%" for v in [0, 20, 40, 60, 80]])
style(ax)
ax.legend(frameon=False, loc="upper left", fontsize=10.5, labelcolor=INK2)
ax.set_title("The top 25% of customers generate 66% of revenue",
             loc="left", fontsize=13, fontweight="bold", color=INK, pad=14)
fig.tight_layout()
fig.savefig(OUT + "chart_1_customer_segmentation.png")
plt.close(fig)

# ---------- 2. Cohort analysis ----------
years = list(range(2015, 2025))
new_customers = [2825, 3397, 4068, 7446, 7755, 3031, 4663, 9010, 5890, 1402]
lifetime = [5271.5860070331, 5404.9225017376, 5403.0811121156, 4896.6405350206,
            4731.9463412741, 3933.3226554208, 3943.3275100548, 3315.5170142913,
            2543.1796830373, 2037.5530153658]
first_only = [2564.8187530571, 2896.418704923, 2893.6814931014, 2655.6232279673,
              2868.4794605239, 2328.8071670348, 2567.8924220132, 2387.0759767118,
              2188.5536230561, 1972.025435706]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.2), dpi=200,
                             gridspec_kw={"width_ratios": [1, 1.1]})
bars = a1.bar(years, new_customers, 0.62, color=BLUE)
for b, v in zip(bars, new_customers):
    a1.text(b.get_x() + b.get_width() / 2, v + 130, f"{v:,}", ha="center",
            va="bottom", fontsize=9, color=INK)
a1.set_xticks(years)
a1.set_xticklabels([str(y) for y in years], fontsize=9.5)
a1.set_ylim(0, 10500)
a1.set_yticks([0, 2500, 5000, 7500, 10000])
a1.set_yticklabels(["0", "2,500", "5,000", "7,500", "10,000"])
style(a1)
a1.set_title("New customers per cohort", loc="left", fontsize=12,
             fontweight="bold", color=INK, pad=12)

a2.plot(years, lifetime, color=BLUE, linewidth=2, marker="o", markersize=6,
        markeredgecolor="white", markeredgewidth=1.5,
        label="Total revenue per customer (not adjusted)")
a2.plot(years, first_only, color=ORANGE, linewidth=2, marker="o", markersize=6,
        markeredgecolor="white", markeredgewidth=1.5,
        label="First-purchase revenue per customer")
for series, color, dy in ((lifetime, BLUE, 260), (first_only, ORANGE, -330)):
    a2.text(years[0], series[0] + dy, f"${series[0]:,.0f}", ha="center",
            fontsize=9.5, color=INK)
    a2.text(years[-1], series[-1] + dy, f"${series[-1]:,.0f}", ha="center",
            fontsize=9.5, color=INK)
a2.set_xticks(years)
a2.set_xticklabels([str(y) for y in years], fontsize=9.5)
a2.set_ylim(0, 6500)
a2.set_yticks([0, 2000, 4000, 6000])
a2.set_yticklabels(["$0", "$2,000", "$4,000", "$6,000"])
style(a2)
a2.legend(frameon=False, loc="lower left", fontsize=9.5, labelcolor=INK2)
a2.set_title("Revenue per customer by cohort year", loc="left", fontsize=12,
             fontweight="bold", color=INK, pad=12)
fig.suptitle("Older cohorts look more valuable partly because they had more time to buy",
             x=0.012, ha="left", fontsize=13, fontweight="bold", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(OUT + "chart_2_cohort_analysis.png")
plt.close(fig)

# ---------- 3. Retention ----------
r_years = list(range(2015, 2024))
active = np.array([237, 311, 385, 704, 687, 283, 442, 937, 455])
total = np.array([2825, 3397, 4068, 7446, 7755, 3031, 4663, 9010, 4718])
active_pct = active / total * 100

fig, ax = plt.subplots(figsize=(9, 5.2), dpi=200)
bars = ax.bar(r_years, active_pct, 0.62, color=BLUE)
for b, v in zip(bars, active_pct):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.25, f"{v:.1f}%", ha="center",
            va="bottom", fontsize=10.5, color=INK)
ax.set_xticks(r_years)
ax.set_xticklabels([str(y) for y in r_years], fontsize=10.5)
ax.set_ylim(0, 12)
ax.set_yticks([0, 5, 10])
ax.set_yticklabels(["0%", "5%", "10%"])
style(ax)
ax.set_title("Only about 9% of customers in each cohort are still active",
             loc="left", fontsize=13, fontweight="bold", color=INK, pad=24)
ax.text(0, 1.015, "Active = purchased within the last 6 months of the dataset (% of each cohort)",
        transform=ax.transAxes, fontsize=10, color=INK2, va="bottom")
fig.tight_layout()
fig.savefig(OUT + "chart_3_retention.png")
plt.close(fig)

# ---------- 2b. Monthly revenue and customers (separate panels, no dual axis) ----------
import csv
from datetime import datetime
import matplotlib.dates as mdates

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results",
                        "2d_monthly_trends.csv")
months, rev, cust, rev3, cust3 = [], [], [], [], []
with open(csv_path) as f:
    for r in csv.DictReader(f):
        months.append(datetime.strptime(r["month"], "%Y-%m-%d"))
        rev.append(float(r["net_revenue"]) / 1e6)
        cust.append(int(r["customers"]))
        rev3.append(float(r["revenue_3m_avg"]) / 1e6)
        cust3.append(float(r["customers_3m_avg"]))

fig, (m1, m2) = plt.subplots(2, 1, figsize=(11, 8), dpi=200, sharex=True)
for ax_, raw, avg, color, raw_label, avg_label in (
    (m1, rev, rev3, BLUE, "Monthly net revenue ($M)", "3-month rolling average"),
    (m2, cust, cust3, ORANGE, "Customers who purchased in the month", "3-month rolling average"),
):
    ax_.bar(months, raw, width=24, color=color, alpha=0.35, label=raw_label)
    ax_.plot(months, avg, color=color, linewidth=2.2, label=avg_label)
    style(ax_)
    ax_.legend(frameon=False, loc="upper left", fontsize=10, labelcolor=INK2)
m1.set_ylim(0, 5.5)
m1.set_yticks([0, 1, 2, 3, 4, 5])
m1.set_yticklabels(["$0", "$1M", "$2M", "$3M", "$4M", "$5M"])
m2.set_ylim(0, 2200)
m2.set_yticks([0, 500, 1000, 1500, 2000])
m2.set_yticklabels(["0", "500", "1,000", "1,500", "2,000"])
m2.xaxis.set_major_locator(mdates.YearLocator())
m2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
m1.set_title("Revenue and customers: growth, a sharp 2020 drop, and a peak in 2022",
             loc="left", fontsize=13, fontweight="bold", color=INK, pad=12)
fig.tight_layout()
fig.savefig(OUT + "chart_2b_monthly_trends.png")
plt.close(fig)

print("done", [f"{v:.2f}" for v in cust_pct], [f"{v:.2f}" for v in ltv_pct],
      [f"{v:.2f}" for v in active_pct], f"{active.sum()/total.sum()*100:.2f}")

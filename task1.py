import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import re

# Load data
df = pd.read_csv('API_SP.POP.TOTL_DS2_en_csv_v2_127039.csv', skiprows=4)

# Filter real countries only (ISO 3-letter codes)
def is_country_code(code):
    return bool(re.match(r'^[A-Z]{3}$', str(code)))

pop2023 = df[['Country Name', 'Country Code', '2023']].dropna(subset=['2023'])
pop2023 = pop2023[pop2023['Country Code'].apply(is_country_code)]
top15 = pop2023.nlargest(15, '2023').reset_index(drop=True)

# Plot
colors = plt.cm.RdYlGn_r(np.linspace(0.15, 0.85, 15))
fig, ax = plt.subplots(figsize=(14, 8))
fig.patch.set_facecolor('#0f172a')
ax.set_facecolor('#1e293b')

bars = ax.barh(top15['Country Name'][::-1], top15['2023'][::-1]/1e9,
               color=colors[::-1], edgecolor='#334155', linewidth=0.5, height=0.7)

for bar, val in zip(bars, top15['2023'][::-1]/1e9):
    ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}B', va='center', ha='left', fontsize=10,
            color='#e2e8f0', fontweight='bold')

ax.set_xlabel('Population (in Billions)', fontsize=12, color='#94a3b8', labelpad=10)
ax.set_title('Top 15 Most Populous Countries (2023)', fontsize=16,
             color='#f1f5f9', fontweight='bold', pad=20)
ax.tick_params(colors='#cbd5e1', labelsize=10)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#334155')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.1f}B'))
ax.set_xlim(0, top15['2023'].max()/1e9 * 1.18)
ax.grid(axis='x', color='#334155', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('SCT_DS_1_population_chart.png', dpi=180, bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("Chart saved!")

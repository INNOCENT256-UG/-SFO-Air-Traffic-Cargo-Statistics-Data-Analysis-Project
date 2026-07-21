"""
SFO Air Traffic Cargo Statistics - Additional Charts & Interactive Dashboard
============================================================================
This script creates comprehensive visualizations and an interactive HTML dashboard
for the SFO cargo data analysis project.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("Loading data...")
df = pd.read_excel('SFO_Air_Cargo_Analysis Full Detailed.xlsx', sheet_name='🗂️ Cleaned Data')
print(f"[OK] Loaded {len(df):,} records")

# ============================================================================
# 2. CREATE ADDITIONAL CHARTS
# ============================================================================
print("\nCreating additional charts...")

# ---------------------------------------------------------------------------
# CHART 1: Seasonal Patterns (Monthly Analysis)
# ---------------------------------------------------------------------------
print("  [1/8] Chart 1: Seasonal Patterns")
monthly_data = df.groupby('Month').agg({
    'Cargo Metric Tons': 'sum',
    'Cargo Weight Lbs': 'sum'
}).reset_index()

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly_data['Month_Name'] = monthly_data['Month'].apply(lambda x: month_names[x-1])

fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.bar(monthly_data['Month_Name'], monthly_data['Cargo Metric Tons']/1000, 
              color=plt.cm.viridis(np.linspace(0, 1, 12)), edgecolor='black', linewidth=1.2)

# Add value labels on bars
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}K',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.set_title('SFO Cargo Volume by Month (Seasonal Patterns)\nTotal Metric Tons by Month (1999-2025)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Month', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Cargo (Thousand Metric Tons)', fontsize=12, fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add insight text
peak_month = monthly_data.loc[monthly_data['Cargo Metric Tons'].idxmax(), 'Month_Name']
low_month = monthly_data.loc[monthly_data['Cargo Metric Tons'].idxmin(), 'Month_Name']
ax.text(0.02, 0.98, f'Peak: {peak_month}\nLowest: {low_month}', 
        transform=ax.transAxes, fontsize=11, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('Charts/Seasonal_Cargo_Patterns.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Seasonal_Cargo_Patterns.png")

# ---------------------------------------------------------------------------
# CHART 2: Codeshare Analysis
# ---------------------------------------------------------------------------
print("  [2/8] Chart 2: Codeshare Analysis")
codeshare_data = df.groupby('Is Codeshare').agg({
    'Cargo Metric Tons': ['sum', 'count', 'mean']
}).reset_index()
codeshare_data.columns = ['Is_Codeshare', 'Total_MT', 'Record_Count', 'Avg_MT']
codeshare_data['Percentage'] = (codeshare_data['Record_Count'] / codeshare_data['Record_Count'].sum()) * 100

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Pie chart for record distribution
colors = ['#FF6B6B', '#4ECDC4']
wedges, texts, autotexts = ax1.pie(codeshare_data['Record_Count'], 
                                    labels=['Direct Flights', 'Codeshare Flights'],
                                    autopct='%1.1f%%',
                                    colors=colors,
                                    startangle=90,
                                    explode=(0.05, 0.05),
                                    textprops={'fontsize': 12, 'fontweight': 'bold'})
ax1.set_title('Distribution of Direct vs Codeshare Flights', fontsize=14, fontweight='bold', pad=20)

# Bar chart for cargo volume
bars = ax2.bar(['Direct Flights', 'Codeshare Flights'], 
               codeshare_data['Total_MT']/1000,
               color=colors, edgecolor='black', linewidth=1.2)
ax2.set_title('Total Cargo Volume by Flight Type', fontsize=14, fontweight='bold', pad=20)
ax2.set_ylabel('Total Cargo (Thousand Metric Tons)', fontsize=12, fontweight='bold')
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_axisbelow(True)

for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}K MT',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('Charts/Codeshare_Analysis.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Codeshare_Analysis.png")

# ---------------------------------------------------------------------------
# CHART 3: Aircraft Type Efficiency Over Time
# ---------------------------------------------------------------------------
print("  [3/8] Chart 3: Aircraft Type Efficiency Over Time")
aircraft_yearly = df.groupby(['Year', 'Cargo Aircraft Type']).agg({
    'Cargo Metric Tons': 'sum',
    'Cargo Weight Lbs': 'count'
}).reset_index()
aircraft_yearly.columns = ['Year', 'Aircraft_Type', 'Total_MT', 'Flights']

# Pivot for plotting
aircraft_pivot = aircraft_yearly.pivot(index='Year', columns='Aircraft_Type', values='Total_MT')

fig, ax = plt.subplots(figsize=(14, 7))
aircraft_pivot.plot(kind='line', marker='o', linewidth=2.5, markersize=6, ax=ax)
ax.set_title('Cargo Volume by Aircraft Type Over Time (1999-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Cargo (Metric Tons)', fontsize=12, fontweight='bold')
ax.legend(title='Aircraft Type', title_fontsize=11, fontsize=10, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add COVID annotation
ax.axvline(x=2020, color='red', linestyle='--', alpha=0.5, linewidth=2)
ax.text(2020.3, ax.get_ylim()[1]*0.95, 'COVID-19\nImpact', fontsize=10, 
        color='red', fontweight='bold', alpha=0.7)

plt.tight_layout()
plt.savefig('Charts/Aircraft_Type_Trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Aircraft_Type_Trends.png")

# ---------------------------------------------------------------------------
# CHART 4: Top 10 Airlines Market Share Treemap
# ---------------------------------------------------------------------------
print("  [4/8] Chart 4: Top 10 Airlines Market Share")
top10_airlines = df.groupby('Operating Airline')['Cargo Metric Tons'].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(14, 8))
colors = plt.cm.Set3(np.linspace(0, 1, 10))
wedges, texts, autotexts = ax.pie(top10_airlines.values, 
                                   labels=top10_airlines.index,
                                   autopct='%1.1f%%',
                                   colors=colors,
                                   startangle=90,
                                   textprops={'fontsize': 10})

ax.set_title('Top 10 Airlines by Market Share\n(All-Time Cargo Volume at SFO)', 
             fontsize=16, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('Charts/Top10_Airlines_Market_Share.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Top10_Airlines_Market_Share.png")

# ---------------------------------------------------------------------------
# CHART 5: Import vs Export Trends
# ---------------------------------------------------------------------------
print("  [5/8] Chart 5: Import vs Export Trends")
direction_yearly = df.groupby(['Year', 'Activity Type Code'])['Cargo Metric Tons'].sum().reset_index()
direction_pivot = direction_yearly.pivot(index='Year', columns='Activity Type Code', values='Cargo Metric Tons')

fig, ax = plt.subplots(figsize=(14, 7))
ax.fill_between(direction_pivot.index, direction_pivot['Deplaned'], 
                alpha=0.4, label='Deplaned (Imports)', color='#FF6B6B')
ax.fill_between(direction_pivot.index, direction_pivot['Enplaned'], 
                alpha=0.4, label='Enplaned (Exports)', color='#4ECDC4')
ax.plot(direction_pivot.index, direction_pivot['Deplaned'], 
        color='#FF6B6B', linewidth=2.5, marker='o', markersize=5)
ax.plot(direction_pivot.index, direction_pivot['Enplaned'], 
        color='#4ECDC4', linewidth=2.5, marker='s', markersize=5)

ax.set_title('Import vs Export Cargo Volume Trends (1999-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Cargo Volume (Metric Tons)', fontsize=12, fontweight='bold')
ax.legend(title='Activity Type', fontsize=11, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

# Add COVID annotation
ax.axvline(x=2020, color='red', linestyle='--', alpha=0.5, linewidth=2)
ax.text(2020.3, ax.get_ylim()[1]*0.95, 'COVID-19', fontsize=10, 
        color='red', fontweight='bold', alpha=0.7)

plt.tight_layout()
plt.savefig('Charts/Import_Export_Trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Import_Export_Trends.png")

# ---------------------------------------------------------------------------
# CHART 6: Geographic Region Heatmap by Decade
# ---------------------------------------------------------------------------
print("  [6/8] Chart 6: Geographic Region Heatmap")
print(f"    Available columns: {df.columns.tolist()}")
df['Decade'] = (df['Year'] // 10) * 10
geo_decade = df.groupby(['Decade', 'Geo Region'])['Cargo Metric Tons'].sum().reset_index()
geo_decade_pivot = geo_decade.pivot(index='Geo Region', columns='Decade', values='Cargo Metric Tons')
geo_decade_pivot = geo_decade_pivot.fillna(0)

# Normalize by row (region) to show percentage change
geo_decade_pct = geo_decade_pivot.div(geo_decade_pivot.sum(axis=0), axis=1) * 100

fig, ax = plt.subplots(figsize=(14, 8))
sns.heatmap(geo_decade_pct, annot=True, fmt='.1f', cmap='YlOrRd', 
            cbar_kws={'label': 'Market Share (%)'}, linewidths=0.5, ax=ax)
ax.set_title('Geographic Region Market Share by Decade (%)\nNormalized by Decade', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Decade', fontsize=12, fontweight='bold')
ax.set_ylabel('Geographic Region', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('Charts/Geo_Region_Heatmap.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Geo_Region_Heatmap.png")

# ---------------------------------------------------------------------------
# CHART 7: Cargo Type Composition Stacked Area
# ---------------------------------------------------------------------------
print("  [7/8] Chart 7: Cargo Type Composition Over Time")
cargo_type_yearly = df.groupby(['Year', 'Cargo Type Code'])['Cargo Metric Tons'].sum().reset_index()
cargo_type_pivot = cargo_type_yearly.pivot(index='Year', columns='Cargo Type Code', values='Cargo Metric Tons')

fig, ax = plt.subplots(figsize=(14, 7))
ax.stackplot(cargo_type_pivot.index, 
             cargo_type_pivot['Cargo'], 
             cargo_type_pivot['Express'], 
             cargo_type_pivot['Mail'],
             labels=['Cargo', 'Express', 'Mail'],
             colors=['#2E86AB', '#A23B72', '#F18F01'],
             alpha=0.8)

ax.set_title('Cargo Type Composition Over Time (1999-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Cargo Volume (Metric Tons)', fontsize=12, fontweight='bold')
ax.legend(title='Cargo Type', fontsize=11, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('Charts/Cargo_Type_Composition.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Cargo_Type_Composition.png")

# ---------------------------------------------------------------------------
# CHART 8: Top Airlines Growth Rate
# ---------------------------------------------------------------------------
print("  [8/8] Chart 8: Top Airlines Year-over-Year Growth")
top5_airlines = df.groupby('Operating Airline')['Cargo Metric Tons'].sum().sort_values(ascending=False).head(5).index.tolist()
airline_yearly = df[df['Operating Airline'].isin(top5_airlines)].groupby(['Year', 'Operating Airline'])['Cargo Metric Tons'].sum().reset_index()

fig, ax = plt.subplots(figsize=(14, 7))
for airline in top5_airlines:
    airline_data = airline_yearly[airline_yearly['Operating Airline'] == airline]
    ax.plot(airline_data['Year'], airline_data['Cargo Metric Tons']/1000, 
            marker='o', linewidth=2.5, label=airline, markersize=5)

ax.set_title('Top 5 Airlines - Cargo Volume Trends (1999-2025)', fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Year', fontsize=12, fontweight='bold')
ax.set_ylabel('Cargo Volume (Thousand Metric Tons)', fontsize=12, fontweight='bold')
ax.legend(title='Airline', fontsize=10, loc='upper left')
ax.grid(alpha=0.3, linestyle='--')
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig('Charts/Top5_Airlines_Trends.png', dpi=300, bbox_inches='tight')
plt.close()
print("    [OK] Saved: Charts/Top5_Airlines_Trends.png")

print("\n[OK] All additional charts created successfully!")

# ============================================================================
# 3. CREATE INTERACTIVE DASHBOARD
# ============================================================================
print("\nBuilding interactive dashboard...")

# Create subplot figure
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=('Annual Cargo Trend (1999-2025)', 
                    'Geographic Distribution',
                    'Top 10 Airlines by Volume',
                    'Cargo Type Breakdown',
                    'Aircraft Type Distribution',
                    'Seasonal Patterns'),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "pie"}],
           [{"type": "bar"}, {"type": "bar"}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.15
)

# ---- KPI Cards ----
total_cargo = df['Cargo Metric Tons'].sum()
total_airlines = df['Operating Airline'].nunique()
total_records = len(df)
year_2025 = df[df['Year'] == 2025]['Cargo Metric Tons'].sum()

# ---- Chart 1: Annual Trend ----
annual = df.groupby('Year')['Cargo Metric Tons'].sum().reset_index()
fig.add_trace(
    go.Scatter(x=annual['Year'], y=annual['Cargo Metric Tons']/1000, 
               mode='lines+markers', name='Annual Trend',
               line=dict(color='#2E86AB', width=3),
               marker=dict(size=6)),
    row=1, col=1
)

# ---- Chart 2: Geographic Distribution ----
geo = df.groupby('Geo Region')['Cargo Metric Tons'].sum().sort_values(ascending=True).reset_index()
fig.add_trace(
    go.Bar(x=geo['Cargo Metric Tons']/1000, y=geo['Geo Region'], 
           orientation='h', name='By Region',
    marker=dict(color=geo['Cargo Metric Tons'], colorscale='Viridis')),
    row=1, col=2
)

# ---- Chart 3: Top 10 Airlines ----
top10 = df.groupby('Operating Airline')['Cargo Metric Tons'].sum().sort_values(ascending=False).head(10).reset_index()
fig.add_trace(
    go.Bar(x=top10['Cargo Metric Tons']/1000, y=top10['Operating Airline'],
           orientation='h', name='Top 10 Airlines',
    marker=dict(color=top10['Cargo Metric Tons'], colorscale='Plasma')),
    row=2, col=1
)

# ---- Chart 4: Cargo Type Pie ----
cargo_type = df.groupby('Cargo Type Code')['Cargo Metric Tons'].sum().reset_index()
fig.add_trace(
    go.Pie(labels=cargo_type['Cargo Type Code'], 
           values=cargo_type['Cargo Metric Tons'],
           name='Cargo Type',
           marker=dict(colors=['#2E86AB', '#A23B72', '#F18F01'])),
    row=2, col=2
)

# ---- Chart 5: Aircraft Type ----
aircraft = df.groupby('Cargo Aircraft Type')['Cargo Metric Tons'].sum().sort_values(ascending=True).reset_index()
fig.add_trace(
    go.Bar(x=aircraft['Cargo Aircraft Type'], y=aircraft['Cargo Metric Tons']/1000,
           name='Aircraft Type',
           marker=dict(color=['#FF6B6B', '#4ECDC4', '#FFE66D'])),
    row=3, col=1
)

# ---- Chart 6: Seasonal ----
monthly = df.groupby('Month')['Cargo Metric Tons'].sum().reset_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthly['Month_Name'] = monthly['Month'].apply(lambda x: month_names[x-1])
fig.add_trace(
    go.Bar(x=monthly['Month_Name'], y=monthly['Cargo Metric Tons']/1000,
           name='Monthly Average',
           marker=dict(color=monthly['Cargo Metric Tons'], colorscale='RdYlGn')),
    row=3, col=2
)

# Update layout
fig.update_layout(
    title_text="<b>SFO Air Traffic Cargo Statistics - Interactive Dashboard</b><br>" +
               f"<sub>Total: {total_cargo/1000000:.2f}M MT | {total_airlines} Airlines | {total_records:,} Records | 2025: {year_2025/1000:.1f}K MT</sub>",
    title_font_size=20,
    showlegend=False,
    height=1400,
    template='plotly_dark'
)

# Update axes labels
fig.update_xaxes(title_text="Year", row=1, col=1)
fig.update_yaxes(title_text="Cargo (K MT)", row=1, col=1)
fig.update_xaxes(title_text="Cargo (K MT)", row=1, col=2)
fig.update_yaxes(title_text="Region", row=1, col=2)
fig.update_xaxes(title_text="Cargo (K MT)", row=2, col=1)
fig.update_yaxes(title_text="Airline", row=2, col=1)
fig.update_xaxes(title_text="Month", row=3, col=2)
fig.update_yaxes(title_text="Cargo (K MT)", row=3, col=2)

# Save dashboard
fig.write_html('dashboard.html')
print("  [OK] Saved: dashboard.html")

print("\n" + "="*70)
print("[SUCCESS] ALL CHARTS AND DASHBOARD CREATED SUCCESSFULLY!")
print("="*70)
print("\nGenerated Files:")
print("  • Charts/Seasonal_Cargo_Patterns.png")
print("  • Charts/Codeshare_Analysis.png")
print("  • Charts/Aircraft_Type_Trends.png")
print("  • Charts/Top10_Airlines_Market_Share.png")
print("  • Charts/Import_Export_Trends.png")
print("  • Charts/Geo_Region_Heatmap.png")
print("  • Charts/Cargo_Type_Composition.png")
print("  • Charts/Top5_Airlines_Trends.png")
print("  • dashboard.html (Interactive Dashboard)")
print("="*70)
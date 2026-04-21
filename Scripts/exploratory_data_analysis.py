"""
Exploratory Data Analysis for World Bank Indicators

This script performs exploratory data analysis on cleaned World Bank data for four African countries:
Burkina Faso, Malawi, Mali, and Rwanda. The analysis focuses on two key indicators:
- Female Secondary Enrollment Rate
- Fertility Rate

The data is analyzed over time and across countries to identify trends and relationships.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Use non-interactive backend for matplotlib
import matplotlib
matplotlib.use('Agg')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Define paths
DATA_DIR = Path('Data.clean')
OUTPUT_DIR = Path('Outputs')
OUTPUT_DIR.mkdir(exist_ok=True)

# File paths (note: some files have swapped data, but we'll load by actual content)
files = {
    'Burkina Faso': DATA_DIR / 'Burkina_Faso_cleaned.csv',
    'Malawi': DATA_DIR / 'Malawi_cleaned.csv',
    'Mali': DATA_DIR / 'mali_clean_data.csv',
    'Rwanda': DATA_DIR / 'Rwanda_cleaned.csv'
}

def load_and_combine_data():
    """Load all cleaned datasets and combine into a single DataFrame."""
    dfs = []

    for country, file_path in files.items():
        try:
            df = pd.read_csv(file_path)

            # Standardize column names (Mali has underscores)
            df.columns = df.columns.str.replace('_', ' ')

            # Add country column based on actual data content
            # Since files are misnamed, determine country from data
            actual_country = df['Country Name'].iloc[0]
            df['Country'] = actual_country

            dfs.append(df)
            print(f"Loaded {country} data: {len(df)} rows, actual country: {actual_country}")

        except FileNotFoundError:
            print(f"Warning: {file_path} not found")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    if not dfs:
        raise ValueError("No data files could be loaded")

    # Combine all data
    combined_df = pd.concat(dfs, ignore_index=True)

    # Clean data
    combined_df['Value'] = pd.to_numeric(combined_df['Value'], errors='coerce')
    combined_df = combined_df.dropna(subset=['Value'])

    return combined_df

def create_wide_format(df):
    """Pivot data to wide format for easier analysis."""
    wide_df = df.pivot_table(
        index=['Country', 'Year'],
        columns='Indicator',
        values='Value',
        aggfunc='first'
    ).reset_index()

    # Clean column names
    wide_df.columns.name = None
    wide_df.columns = wide_df.columns.str.replace(' ', '_')

    return wide_df

def summary_statistics(df):
    """Generate summary statistics for the dataset."""
    print("=== SUMMARY STATISTICS ===")
    print(f"Total observations: {len(df)}")
    print(f"Countries: {df['Country'].nunique()}")
    print(f"Years range: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Indicators: {df['Indicator'].nunique()}")

    print("\nData completeness by country and indicator:")
    completeness = df.groupby(['Country', 'Indicator'])['Value'].count().unstack()
    print(completeness)

    print("\nDescriptive statistics by indicator:")
    desc_stats = df.groupby('Indicator')['Value'].describe()
    print(desc_stats)

def plot_time_series(wide_df):
    """Plot time series for each indicator by country."""
    indicators = [col for col in wide_df.columns if col not in ['Country', 'Year']]

    for indicator in indicators:
        plt.figure(figsize=(12, 8))

        for country in wide_df['Country'].unique():
            country_data = wide_df[wide_df['Country'] == country].sort_values('Year')
            plt.plot(country_data['Year'], country_data[indicator],
                    marker='o', label=country, linewidth=2, markersize=4)

        plt.title(f'{indicator.replace("_", " ")} Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Year', fontsize=12)
        plt.ylabel(indicator.replace("_", " "), fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Save plot
        filename = f"{indicator.lower()}_time_series.png"
        plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches='tight')
        plt.show()

def plot_correlations(wide_df):
    """Plot correlations between indicators by country."""
    indicators = [col for col in wide_df.columns if col not in ['Country', 'Year']]

    if len(indicators) < 2:
        print("Need at least 2 indicators for correlation analysis")
        return

    # Create subplots for correlations by country
    countries = sorted(wide_df['Country'].unique())
    num_countries = len(countries)
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    axes = axes.flatten()

    for idx, country in enumerate(countries):
        country_data = wide_df[wide_df['Country'] == country][indicators].dropna()
        if len(country_data) >= 2:
            corr_matrix = country_data.corr()
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                        square=True, linewidths=0.5, ax=axes[idx], vmin=-1, vmax=1,
                        cbar_kws={'label': 'Correlation'})
            axes[idx].set_title(f'{country}', fontsize=12, fontweight='bold')
        else:
            axes[idx].text(0.5, 0.5, f'Insufficient data\nfor {country}',
                          ha='center', va='center', transform=axes[idx].transAxes)
            axes[idx].set_title(f'{country}', fontsize=12, fontweight='bold')

    fig.suptitle('Correlation Matrix by Country', fontsize=16, fontweight='bold', y=0.995)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Scatter plots for each pair
    for i, ind1 in enumerate(indicators):
        for ind2 in indicators[i+1:]:
            plt.figure(figsize=(10, 6))

            for country in wide_df['Country'].unique():
                country_data = wide_df[wide_df['Country'] == country]
                plt.scatter(country_data[ind1], country_data[ind2],
                          label=country, alpha=0.7, s=50)

            plt.xlabel(ind1.replace("_", " "), fontsize=12)
            plt.ylabel(ind2.replace("_", " "), fontsize=12)
            plt.title(f'{ind1.replace("_", " ")} vs {ind2.replace("_", " ")}',
                     fontsize=14, fontweight='bold')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.tight_layout()

            filename = f"{ind1.lower()}_vs_{ind2.lower()}_scatter.png"
            plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches='tight')
            plt.show()

def plot_country_comparisons(wide_df):
    """Create bar plots comparing countries using most recent data available for each country."""
    indicators = [col for col in wide_df.columns if col not in ['Country', 'Year']]

    for indicator in indicators:
        plt.figure(figsize=(12, 6))

        # Get most recent data for each country (may be different years)
        countries = sorted(wide_df['Country'].unique())
        plot_data = []
        years = []

        for country in countries:
            country_data = wide_df[wide_df['Country'] == country].dropna(subset=[indicator])
            if len(country_data) > 0:
                # Get the most recent row for this country
                latest = country_data.iloc[-1]
                plot_data.append(latest[indicator])
                years.append(int(latest['Year']))
            else:
                plot_data.append(np.nan)
                years.append(None)

        # Create bar plot
        valid_countries = [c for c, v in zip(countries, plot_data) if not pd.isna(v)]
        valid_values = [v for v in plot_data if not pd.isna(v)]
        valid_years = [y for y in years if y is not None]

        if len(valid_countries) > 0:
            bars = plt.bar(valid_countries, valid_values, color='steelblue')

            # Create title with year information
            year_info = f"(Most recent data: {min(valid_years)}-{max(valid_years)})"
            plt.title(f'{indicator.replace("_", " ")} by Country {year_info}',
                     fontsize=14, fontweight='bold')
            plt.xlabel('Country', fontsize=12)
            plt.ylabel(indicator.replace("_", " "), fontsize=12)
            plt.xticks(rotation=45, ha='right')

            # Add value labels on bars with year info
            for i, (bar, country) in enumerate(zip(bars, valid_countries)):
                height = bar.get_height()
                year_text = f"\n({valid_years[i]})" if valid_years else ""
                plt.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}{year_text}', ha='center', va='bottom', fontsize=9)

            plt.tight_layout()
            filename = f"{indicator.lower()}_by_country_comparison.png"
            plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches='tight')
            plt.show()
        else:
            print(f"No data available for {indicator}")

def analyze_trends(wide_df):
    """Analyze trends and changes over time."""
    print("\n=== TREND ANALYSIS ===")

    indicators = [col for col in wide_df.columns if col not in ['Country', 'Year']]

    for indicator in indicators:
        print(f"\n{indicator.replace('_', ' ')} Trends:")

        for country in wide_df['Country'].unique():
            country_data = wide_df[wide_df['Country'] == country].sort_values('Year')
            country_data = country_data.dropna(subset=[indicator])

            if len(country_data) >= 2:
                first_val = country_data[indicator].iloc[0]
                last_val = country_data[indicator].iloc[-1]
                change = last_val - first_val
                pct_change = (change / first_val) * 100 if first_val != 0 else 0

                years = country_data['Year'].iloc[-1] - country_data['Year'].iloc[0]

                print(f"  {country}: {first_val:.2f} → {last_val:.2f} "
                     f"(change: {change:+.2f}, {pct_change:+.1f}%, over {years} years)")

def main():
    """Main analysis function."""
    print("Starting Exploratory Data Analysis...")

    # Load and combine data
    df = load_and_combine_data()
    print(f"\nLoaded {len(df)} total observations")

    # Create wide format
    wide_df = create_wide_format(df)
    print(f"Created wide format with {len(wide_df)} rows")

    # Summary statistics
    summary_statistics(df)

    # Trend analysis
    analyze_trends(wide_df)

    # Visualizations
    print("\nGenerating visualizations...")
    plot_time_series(wide_df)
    plot_correlations(wide_df)
    plot_country_comparisons(wide_df)

    print(f"\nAnalysis complete! Plots saved to {OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
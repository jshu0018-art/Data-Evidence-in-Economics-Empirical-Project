"""
Generate a coefficient plot comparing the effect of female secondary enrollment 
on fertility rates across different model specifications.

Output: Saves coefficient_plot_fertility_enrollment.png to Outputs folder
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.formula.api as smf
from pathlib import Path

# Set up paths
root = Path(__file__).parent.parent
data_path = root / 'Data.clean' / 'panel_fixed_effects_data.csv'
output_path = root / 'Outputs' / 'coefficient_plot_fertility_enrollment.png'

# Load and clean data
panel = pd.read_csv(data_path)
panel = panel.dropna(subset=['Female_Secondary_Enrollment_Rate', 'Fertility_Rate'])

print(f"Loaded {len(panel)} observations from {data_path}")

# Define four model specifications
specs = {
    'Two-way FE\n(Country + Year)': 'Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name) + C(Year)',
    'Country FE Only': 'Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Country_Name)',
    'Year FE Only': 'Fertility_Rate ~ Female_Secondary_Enrollment_Rate + C(Year)',
    'Malawi Only': 'Fertility_Rate ~ Female_Secondary_Enrollment_Rate'
}

results_dict = {}

# Two-way FE with clustering
print("Estimating Two-way FE model...")
model_2way = smf.ols(specs['Two-way FE\n(Country + Year)'], data=panel).fit(
    cov_type='cluster', cov_kwds={'groups': panel['Country_Name']}
)
results_dict['Two-way FE\n(Country + Year)'] = model_2way

# Country FE only with clustering
print("Estimating Country FE only model...")
model_country = smf.ols(specs['Country FE Only'], data=panel).fit(
    cov_type='cluster', cov_kwds={'groups': panel['Country_Name']}
)
results_dict['Country FE Only'] = model_country

# Year FE only
print("Estimating Year FE only model...")
model_year = smf.ols(specs['Year FE Only'], data=panel).fit()
results_dict['Year FE Only'] = model_year

# Malawi only
print("Estimating Malawi-only model...")
malawi = panel[panel['Country_Name'] == 'Malawi']
model_malawi = smf.ols(specs['Malawi Only'], data=malawi).fit()
results_dict['Malawi Only'] = model_malawi

# Extract coefficients and 95% confidence intervals
coef_data = []
for label, model in results_dict.items():
    coef = model.params['Female_Secondary_Enrollment_Rate']
    se = model.bse['Female_Secondary_Enrollment_Rate']
    ci_lower = coef - 1.96 * se
    ci_upper = coef + 1.96 * se
    coef_data.append({
        'Model': label, 
        'Coef': coef, 
        'SE': se,
        'CI_Lower': ci_lower, 
        'CI_Upper': ci_upper
    })

coef_df = pd.DataFrame(coef_data)

# Create coefficient plot with 95% CIs
fig, ax = plt.subplots(figsize=(10, 6))
y_pos = np.arange(len(coef_df))

# Plot points and error bars
ax.errorbar(coef_df['Coef'], y_pos, 
            xerr=[coef_df['Coef'] - coef_df['CI_Lower'], 
                  coef_df['CI_Upper'] - coef_df['Coef']],
            fmt='o', markersize=8, capsize=5, capthick=2, linewidth=2, 
            color='steelblue', ecolor='steelblue')

# Add vertical line at zero (null hypothesis)
ax.axvline(x=0, color='red', linestyle='--', linewidth=1.5, alpha=0.7, 
           label='Null (no effect)')

# Labels and formatting
ax.set_yticks(y_pos)
ax.set_yticklabels(coef_df['Model'])
ax.set_xlabel('Coefficient on Female Secondary Enrollment Rate', 
              fontsize=11, fontweight='bold')
ax.set_title('Effect of Female Secondary Enrollment on Fertility Rate\n95% Confidence Intervals by Model Specification', 
             fontsize=12, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')
ax.legend(loc='lower right')

plt.tight_layout()

# Save plot
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f'\n[SAVED] Coefficient plot to: {output_path}')

# Print summary table
print('\nCoefficient Summary (95% CI):')
print(coef_df[['Model', 'Coef', 'SE', 'CI_Lower', 'CI_Upper']].to_string(index=False))
print('\nInterpretation:')
print('- Two-way FE is the preferred specification (controls for country and year effects)')
print('- Large CI width for two-way FE reflects limited number of clusters (4 countries)')
print('- Sensitivity to specification choice indicates robustness concerns')

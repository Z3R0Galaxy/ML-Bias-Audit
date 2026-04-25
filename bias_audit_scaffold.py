# ============================================================
# Year 12 Software Engineering - Software Automation Module
# Assessment Task 1: Algorithmic Bias Audit
# ============================================================
# Name:
# Class:
# Date:
# ============================================================
#
# BACKGROUND
# ----------
# This dataset contains 450 simulated Centrelink welfare records.
# The 'debt_raised_flag' column represents an automated algorithm
# that compared ATO annual income data (divided by 26 to estimate
# fortnightly earnings) against recipients' reported fortnightly
# income. Where the ATO estimate exceeded the reported income,
# the algorithm raised a debt against the recipient.
#
# YOUR TASK
# ---------
# Use this script to investigate whether the algorithm produces
# fair outcomes across all recipient groups, or whether certain
# groups are disproportionately affected.
#
# INSTRUCTIONS
# ------------
# Complete ALL sections marked with TODO comments.
# Do NOT modify the section headers or variable names.
# Run the script after completing each section to check your output.
# ============================================================


# ============================================================
# SECTION 0: Import Libraries
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np

# scikit-learn is used in Section 4
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


# ============================================================
# SECTION 1: Load and Inspect the Dataset
# ============================================================

# Load the dataset
df = pd.read_csv('centrelink_income_dataset.csv')

print("=" * 55)
print("SECTION 1: Dataset Overview")
print("=" * 55)

# TODO 1.1 - Print the first 5 rows of the dataset
# Hint: use df.head()
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# TODO 1.2 - Print the shape of the dataset (number of rows and columns)
# Hint: use df.shape and print a descriptive message
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# TODO 1.3 - Print summary statistics for numerical columns
# Hint: use df.describe()
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# This line is provided for you - it shows the count of each employment type
print("\nEmployment type counts:")
print(df['employment_type'].value_counts())


# ============================================================
# SECTION 2: Calculating Debt Flag Rates by Group
# ============================================================
# A "debt flag rate" is the proportion of records in a group
# where debt_raised_flag == 1. It tells us how often the
# algorithm raised a debt for each category.

print("\n" + "=" * 55)
print("SECTION 2: Debt Flag Rates by Group")
print("=" * 55)

# --- 2A: By Employment Type ---

# This calculation is provided as a worked example.
# Study it carefully before completing 2B and 2C.

emp_group = df.groupby('employment_type')['debt_raised_flag'].agg(['sum', 'count'])
emp_group.columns = ['debts_raised', 'total_records']
emp_group['debt_flag_rate_%'] = (emp_group['debts_raised'] / emp_group['total_records'] * 100).round(1)
emp_group = emp_group.sort_values('debt_flag_rate_%', ascending=False)

print("\nDebt flag rate by employment type:")
print(emp_group)

# --- 2B: By Region ---

# TODO 2.1 - Calculate debt flag rates grouped by 'region'
# Follow the same pattern as the employment type example above.
# Store your result in a variable called region_group
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# TODO 2.2 - Print the region_group table with a heading
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# --- 2C: By Age Bracket ---

# TODO 2.3 - Calculate debt flag rates grouped by 'age_bracket'
# Store your result in a variable called age_group
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# TODO 2.4 - Print the age_group table with a heading
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----


# ============================================================
# SECTION 3: Visualisations
# ============================================================
# You will create three bar charts. Each chart must have:
#   - A descriptive title
#   - Labelled axes (including units where appropriate)
#   - Readable bar labels showing the percentage value
#   - Appropriate colours

print("\n" + "=" * 55)
print("SECTION 3: Visualisations")
print("=" * 55)

# --- Chart 1: Debt Flag Rate by Employment Type ---
# This chart is provided as a worked example.

fig, ax = plt.subplots(figsize=(10, 5))

colours = ['#c0392b' if rate > 30 else '#e67e22' if rate > 15 else '#27ae60'
           for rate in emp_group['debt_flag_rate_%']]

bars = ax.bar(emp_group.index, emp_group['debt_flag_rate_%'], color=colours, edgecolor='white')

for bar, val in zip(bars, emp_group['debt_flag_rate_%']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
            f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.set_title('Automated Debt Flag Rate by Employment Type\n(Higher % = more debts raised by algorithm)',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Employment Type', fontsize=11)
ax.set_ylabel('Debt Flag Rate (%)', fontsize=11)
ax.set_ylim(0, max(emp_group['debt_flag_rate_%']) * 1.2)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(rotation=20, ha='right')
plt.tight_layout()
plt.savefig('chart1_employment_bias.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 1 saved.")

# --- Chart 2: Debt Flag Rate by Region ---

# TODO 3.1 - Create a bar chart showing debt flag rate by region
# Use region_group['debt_flag_rate_%'] for the values
# Save the chart as 'chart2_regional_bias.png'
# Rotate x-axis labels by 30 degrees for readability
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# --- Chart 3: Income Variance by Employment Type ---
# This chart compares the spread of income_variance_score
# across employment types using a box plot.

# TODO 3.2 - Create a box plot of 'income_variance_score' grouped by 'employment_type'
# Hint: Use df.boxplot(column='income_variance_score', by='employment_type', ...)
# Save the chart as 'chart3_variance_boxplot.png'
# Add a note: this shows WHY the algorithm is unfair, not just THAT it is unfair
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----


# ============================================================
# SECTION 4: Bias Metric Calculation
# ============================================================
# A Disparate Impact Ratio (DIR) is a simple bias metric.
# DIR = (debt flag rate of affected group) / (debt flag rate of least affected group)
# A DIR > 2.0 suggests significant disparate impact.

print("\n" + "=" * 55)
print("SECTION 4: Bias Metric - Disparate Impact Ratio")
print("=" * 55)

# TODO 4.1 - Calculate the DIR for employment type
# Step 1: Find the HIGHEST debt flag rate in emp_group['debt_flag_rate_%']
# Step 2: Find the LOWEST non-zero debt flag rate in emp_group['debt_flag_rate_%']
# Step 3: DIR = highest / lowest
# Step 4: Print the result with a descriptive message

# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# TODO 4.2 - Calculate the DIR for region using region_group
# Same method as above
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----


# ============================================================
# SECTION 5: Feature Importance (Decision Tree)
# ============================================================
# A decision tree can tell us which features (columns) the
# algorithm relies on most heavily to predict a debt flag.
# This helps identify WHICH attributes drive the bias.

print("\n" + "=" * 55)
print("SECTION 5: Feature Importance Analysis")
print("=" * 55)

# Data preparation - provided for you
features = ['employment_type', 'region', 'age_bracket', 'payment_type',
            'income_variance_score']

df_model = df[features + ['debt_raised_flag']].copy()

le = LabelEncoder()
for col in ['employment_type', 'region', 'age_bracket', 'payment_type']:
    df_model[col] = le.fit_transform(df_model[col])

X = df_model[features]
y = df_model['debt_raised_flag']

# TODO 5.1 - Create and train a DecisionTreeClassifier
# Use max_depth=4 and random_state=42
# Fit the model on X and y
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----

# TODO 5.2 - Create a horizontal bar chart of feature importances
# Hint: use clf.feature_importances_ for the values and features for labels
# Sort from highest to lowest importance
# Title: 'Feature Importances: What Drives the Debt Flag?'
# Save as 'chart4_feature_importance.png'
# ----- YOUR CODE BELOW -----


# ----- END YOUR CODE -----


# ============================================================
# SECTION 6: Written Summary
# ============================================================
# Answer the following questions in the string below.
# Write in full sentences. Aim for 3-4 sentences per question.

print("\n" + "=" * 55)
print("SECTION 6: Written Summary")
print("=" * 55)

summary = """
QUESTION 1: What type of bias is present in this dataset, and which groups are most affected?
-------------------------------------------------------------------------------
[TYPE YOUR ANSWER HERE]


QUESTION 2: Explain WHY the averaging algorithm produces unfair outcomes for certain employment types.
Use evidence from your charts and bias metric calculations to support your answer.
-------------------------------------------------------------------------------
[TYPE YOUR ANSWER HERE]


QUESTION 3: Connect your findings to the real Robodebt case. What similarities do you observe?
Refer to at least one specific finding from the Royal Commission.
-------------------------------------------------------------------------------
[TYPE YOUR ANSWER HERE]


QUESTION 4: Propose ONE concrete technical mitigation strategy that could reduce this bias.
Explain how it would work and why it would be more fair.
-------------------------------------------------------------------------------
[TYPE YOUR ANSWER HERE]

"""

print(summary)

print("=" * 55)
print("Script complete. Check your output folder for saved charts.")
print("=" * 55)

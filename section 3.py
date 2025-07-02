# insights.py

import pandas as pd
import os

# Load dataset
input_path = '/Users/fiona/Desktop/tech_test_unica/data/input/insights_input_dataset.csv'
df = pd.read_csv(input_path, sep='|')

# Step 1: Compute global churn rate
global_churn_rate = df['churn'].mean()

# Step 2: Group by gender and province to get segment churn rate
df_segment = df.groupby(['gender', 'province'])['churn'].mean().reset_index()
df_segment.rename(columns={'churn': 'churn_rate'}, inplace=True)

# Step 3: Add churn_rate_pct and global_churn_rate_pct
df_segment['churn_rate_pct'] = (df_segment['churn_rate'] * 100).round(2)
global_churn_rate_pct = round(global_churn_rate * 100, 2)

# Step 4: Add churn_diff and churn_diff_relative
df_segment['churn_diff'] = df_segment['churn_rate'] - global_churn_rate
df_segment['churn_diff_relative'] = df_segment['churn_diff'] / df_segment['churn_rate']

# Step 5: Add insight_type
def determine_insight_type(row):
    if row['churn_diff_relative'] > 0.1:
        return 'higher'
    elif row['churn_diff_relative'] < -0.1:
        return 'lower'
    else:
        return 'irrelevant'

df_segment['insight_type'] = df_segment.apply(determine_insight_type, axis=1)

# Step 6: Generate insights
def generate_insight(row):
    if row['insight_type'] == 'higher':
        return f"Users with gender {row['gender']} from {row['province']} have a {row['churn_rate_pct']}% churn rate, which is higher than the average of {global_churn_rate_pct}%"
    elif row['insight_type'] == 'lower':
        return f"Users with gender {row['gender']} from {row['province']} have a {row['churn_rate_pct']}% churn rate, which is lower than the average of {global_churn_rate_pct}%"
    else:
        return "Nothing to comment"

df_segment['insight'] = df_segment.apply(generate_insight, axis=1)

# Output path
output_dir = '/Users/fiona/Desktop/tech_test_unica/data/output'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'section_3.csv')

# Save result
df_segment.to_csv(output_path, sep='|', index=False)

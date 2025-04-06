import pandas as pd
import json

# Load JIRA Excel file
jira_file = "Timesheet_2.xlsx"  # Replace with your file name
data = pd.read_excel(jira_file)

# Define Keywords
#dev_keywords = ['develop', 'implement', 'integrate', 'code', 'refactor']
#test_keywords = ['test', 'validate', 'qa', 'debug', 'verify']

with open("config.json", "r") as f:
    config = json.load(f)

dev_keywords = config["development_keywords"]
test_keywords = config["testing_keywords"]
# Function to categorize stories
def categorize_task(description, criteria):
    text = (str(description).lower() if pd.notna(description) else "") or \
           (str(criteria).lower() if pd.notna(criteria) else "")

    if any(word in text for word in dev_keywords):
        return "Development"
    elif any(word in text for word in test_keywords):
        return "Testing"
    else:
        return "Other"

# Apply categorization
data["Category"] = data.apply(lambda row: categorize_task(row["Description"], row["Acceptance Criteria"]), axis=1)

# Sum story points by Assignee and Category
summary = data.groupby(["Assignee", "Category"]).agg({"Story Points": "sum"}).unstack(fill_value=0).reset_index()

# Dynamically rename columns based on existing categories
columns = ['Assignee'] + list(summary.columns.get_level_values(1)[1:])
summary.columns = columns

# Add Total Story Points column
summary["Total Story Points"] = summary.sum(axis=1, numeric_only=True)

# Save to Excel
output_file = "Timesheet_Summary_Output_1.xlsx"
summary.to_excel(output_file, index=False)

print(f"✅ Summary saved to {output_file}")

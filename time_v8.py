import pandas as pd
import json
from openpyxl import load_workbook

# Load Excel file
jira_file = "JiraSheet_1.xlsx"
try:
    data = pd.read_excel(jira_file)
except FileNotFoundError:
    print(f"❌ File not found: {jira_file}")
    exit(1)

# Load keywords from config.json
with open("config.json", "r") as f:
    config = json.load(f)

dev_keywords = config.get("development_keywords", [])
test_keywords = config.get("testing_keywords", [])

# Function to categorize tasks
def categorize_task(description, criteria):
    text = (str(description).lower() if pd.notna(description) else "") + " " + \
           (str(criteria).lower() if pd.notna(criteria) else "")
    if any(word in text for word in dev_keywords):
        return "Development"
    elif any(word in text for word in test_keywords):
        return "Testing"
    else:
        return "Other"

# Apply category
data["Category"] = data.apply(lambda row: categorize_task(row.get("Description"), row.get("Acceptance Criteria")), axis=1)

# Detect Sprint Type
def get_sprint_group(sprint_value):
    if pd.isna(sprint_value):
        return "Unknown"
    sprint_str = str(sprint_value).lower()
    if "fastfinder" in sprint_str:
        return "FastFinder"
    elif "fastbreak" in sprint_str:
        return "FastBreak"
    else:
        return "Other"

data["Sprint Group"] = data["Sprint"].apply(get_sprint_group)

# Create output Excel
output_file = "Jira_Report_Final_With_Sprint_Grouping.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    required_cols = ["Assignee", "Epic Link", "Status", "Key", "Issue Type"]

    # ✅ Write blank fields sheet to a separate file
    blank_output_file = "Jira_Blank_Fields.xlsx"
    with pd.ExcelWriter(blank_output_file, engine='openpyxl') as blank_writer:
        blank_fields = [
            "Description", "Acceptance Criteria", "Fix version", "Affected version", "Epic Link",
            "Sprint", "Activity Categories"
        ]
        for field in blank_fields:
            if field in data.columns:
                blank_data = data[data[field].isna()]
                if not blank_data.empty:
                    extra_cols = required_cols.copy()
                    if "Sprint" not in extra_cols:
                        extra_cols.append("Sprint")
                    blank_data_subset = blank_data[extra_cols + [field]]
                    blank_data_subset.to_excel(blank_writer, sheet_name=f"Blank {field}", index=False)

    # ✅ Write development data to a separate file
    dev_output_file = "Jira_Development_Summary.xlsx"
    with pd.ExcelWriter(dev_output_file, engine='openpyxl') as dev_writer:
        dev_data = data[data["Category"] == "Development"]

        if not dev_data.empty:
            for sprint_group in dev_data["Sprint Group"].unique():
                sprint_data = dev_data[dev_data["Sprint Group"] == sprint_group]
                if sprint_data.empty:
                    continue

                flat_columns = [
                    "Assignee", "Epic Link", "Status", "Key", "Issue Type", "Category",
                    "Sprint", "Fix version", "Affected version", "Story Points", "Reporter"
                ]
                available_columns = [col for col in flat_columns if col in sprint_data.columns]
                flat_summary = sprint_data[available_columns].copy()

                total_story_points = flat_summary["Story Points"].sum() if "Story Points" in flat_summary else 0
                total_row = {col: "" for col in available_columns}
                total_row["Assignee"] = "Total"
                total_row["Story Points"] = total_story_points
                flat_summary = pd.concat([flat_summary, pd.DataFrame([total_row])], ignore_index=True)

                flat_summary.to_excel(dev_writer, sheet_name=f"{sprint_group} Dev Summary", index=False)

    # 🧵 Unique Epic Link sheet
    unique_epics = data.dropna(subset=["Epic Link"]).drop_duplicates(subset=["Epic Link"])
    unique_epics[["Epic Link"]].to_excel(writer, sheet_name="Unique Epics", index=False)

    # 🔁 Check Epic Links with multiple Fix Versions
    if "Epic Link" in data.columns and "Fix version" in data.columns:
        multi_fix_versions = data.dropna(subset=["Epic Link", "Fix version"])
        grouped = multi_fix_versions.groupby("Epic Link")["Fix version"].nunique().reset_index()
        multiple_versions = grouped[grouped["Fix version"] > 1]
        if not multiple_versions.empty:
            data_with_issues = data[data["Epic Link"].isin(multiple_versions["Epic Link"])]
            data_with_issues.to_excel(writer, sheet_name="Multiple Fix Versions", index=False)

print("✅ Final reports generated:")
print(f" - {output_file} (with Unique Epics and Fix Version conflicts)")
print(f" - {blank_output_file} (blank field reports)")
print(f" - {dev_output_file} (development summaries)")

import json
import sys

try:
    with open('Notebooks/02_data_cleaning.ipynb', 'r', encoding='utf-8') as f:
        nb = json.load(f)

    cells = nb['cells']

    # 1. Update the Goal cell (cell 0)
    cells[0]['source'] = [
        "# 🧹 Notebook 2: Data Cleaning\n",
        "\n",
        "## Goal\n",
        "Raw data is almost never ready for analysis. In this notebook we will **clean the dataset** by:\n",
        "\n",
        "1. Handling missing values\n",
        "2. Fixing data types\n",
        "3. Removing entries after the year of 2016\n",
        "4. Checking for and removing duplicates\n",
        "5. Validating column values\n",
        "6. Saving a clean version for downstream analysis\n",
        "\n",
        "> **Why is data cleaning important?**  \n",
        "> \"Garbage in, garbage out.\" If we feed dirty data into our analysis, our insights will be wrong or misleading. Cleaning is typically **60–80% of a data scientist's time** — and getting it right is what separates good analysis from bad.\n",
        "\n",
        "---"
    ]

    # Find where "## 4. Check for Duplicates" is to insert our new step before it.
    dup_index = -1
    for i, cell in enumerate(cells):
        if len(cell['source']) > 0 and '## 4. Check for Duplicates\n' in cell['source'][0]:
            dup_index = i
            break

    # If found, update header numbers for 4, 5, 6, 7 to 5, 6, 7, 8
    if dup_index != -1:
        for i in range(dup_index, len(cells)):
            if len(cells[i]['source']) > 0:
                if '## 4. Check for Duplicates\n' in cells[i]['source'][0]:
                    cells[i]['source'][0] = '## 5. Check for Duplicates\n'
                elif '## 5. Validate Column Values\n' in cells[i]['source'][0]:
                    cells[i]['source'][0] = '## 6. Validate Column Values\n'
                elif '## 6. Final Cleaned Dataset Overview' in cells[i]['source'][0]:
                    cells[i]['source'][0] = '## 7. Final Cleaned Dataset Overview'
                elif '## 7. Save Cleaned Dataset\n' in cells[i]['source'][0]:
                    cells[i]['source'][0] = '## 8. Save Cleaned Dataset\n'

    new_markdown_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 4. Remove Entries After 2016\n",
            "\n",
            "> **Why remove them?**  \n",
            "> The dataset's coverage becomes highly inconsistent and incomplete after 2016. To ensure our analysis and visualizations reflect true historical trends rather than data collection gaps, we filter the dataset to include only games released in 2016 or earlier."
        ]
    }

    new_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Filter for Year <= 2016\n",
            "rows_before = len(df)\n",
            "df = df[df['Year'] <= 2016]\n",
            "rows_after = len(df)\n",
            "\n",
            "print(f'Rows before: {rows_before:,}')\n",
            "print(f'Rows after:  {rows_after:,}')\n",
            "print(f'Rows dropped (post-2016): {rows_before - rows_after:,}')\n",
            "print(f'New Year range: {df[\"Year\"].min()} to {df[\"Year\"].max()}')"
        ]
    }

    # Insert cells
    cells.insert(dup_index, new_code_cell)
    cells.insert(dup_index, new_markdown_cell)

    # Update the Summary table at the end
    summary_index = -1
    for i, cell in enumerate(cells):
        if len(cell['source']) > 0 and '## Summary of Cleaning Steps\n' in cell['source'][0]:
            summary_index = i
            break

    if summary_index != -1:
        cells[summary_index]['source'] = [
            "## Summary of Cleaning Steps\n",
            "\n",
            "| Step | Action | Rows Affected |\n",
            "|---|---|---|\n",
            "| Missing Year | Dropped rows | ~271 rows |\n",
            "| Missing Publisher | Filled with 'Unknown' | ~58 rows |\n",
            "| Data Types | Year: float → int | All rows |\n",
            "| Filter by Year | Removed games > 2016 | ~348 rows |\n",
            "| Duplicates | Checked — none found | 0 rows |\n",
            "| Validation | No negative sales, consistent totals | — |\n",
            "\n",
            "### Next Steps\n",
            "In **Notebook 03**, we'll create new features (Feature Engineering) to enable deeper analysis."
        ]

    with open('Notebooks/02_data_cleaning.ipynb', 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=4)
    print("Notebook 02 successfully updated with the 2016 filter.")
except Exception as e:
    print(f"Error updating notebook: {e}")
    sys.exit(1)

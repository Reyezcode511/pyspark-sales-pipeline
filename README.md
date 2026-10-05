# Sales Data Engineering Challenge — 250,000 order records

A fictional Canadian online retailer needs reliable sales reports. Your role is to build a repeatable PySpark pipeline from messy CSV files to validated Parquet datasets and business summaries.

All data is simulated. Amounts are in Canadian dollars; prices are stored as integer cents to avoid floating-point rounding. Each row represents one order with one product, not a multi-item order line.

## Start in Google Colab
1. Extract this ZIP on your computer and upload `notebooks/sales_starter.ipynb` to Colab using File > Upload notebook.
2. Run its setup cell. Its upload cell asks you to upload the original project ZIP.
3. Run the loading cells and then work through the task cells in order.
4. Read `docs/TASKS.md` for exact cleaning rules and acceptance criteria.
5. Compare your results with `checks/expected_results.json` only after making an attempt.

You do not need Anaconda, Docker, or a cloud cluster. Uploaded files and outputs disappear when Colab's runtime resets; download your notebook and output ZIP before leaving.

## Included data
- Five order CSVs, each containing 50,000 rows: 250,000 raw order rows total.
- 10,000 unique customers.
- 500 unique products.
- Dates cover 2025. The generator is deterministic (seed 511).
- Exact duplicates, missing customer IDs, unknown product IDs, invalid quantities, negative prices, invalid dates, and missing statuses are deliberately included.

## Evidence and limits
The expected counts and totals were independently calculated with Python's standard library and checked against the generated CSV files. The starter notebook has not been executed in Spark here. Its TODO cells are intentionally unfinished. There are no invented Spark timings or screenshots. This is a single-machine learning workload, not proof of production cluster performance.

## GitHub deliverables
Finish your notebook; save its actual outputs; include your cleaning decisions, architecture diagram, checks, and measured performance. Credit the supplied simulated dataset and starter scaffold; describe the transformations and tests you implemented yourself. Keep reference answers out of your headline results until your own pipeline matches them.

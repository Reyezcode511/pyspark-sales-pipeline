# Your assignment

## Business brief
Deliver monthly completed-sales totals and identify the highest-revenue products and regions. Cancelled and refunded orders remain in the clean dataset but are excluded from completed-sales revenue. Do not subtract refunds; this exercise does not model net revenue, tax, discounts, or shipping.

## Task 1 — Load and inspect
Read all five order files as string columns first. Record 250,000 rows. Load customers and products; check each dimension key is unique. Print schemas and sample rows. Never collect the entire order dataset to the driver.

## Task 2 — Deduplicate
Remove exact duplicates using all eight order columns. Verify remaining order IDs are unique. Conflicting records with the same order ID would require a separate policy; this dataset contains only exact duplicates.

## Task 3 — Validate and quarantine
Apply these rules after deduplication. Reject a row if any rule fails:
- Customer ID must be present and exist in customers.
- Product ID must exist in products.
- Quantity must parse as an integer greater than zero.
- Unit price cents must parse as an integer greater than or equal to zero.
- Order date must be a real date in 2025 in YYYY-MM-DD format.
- Status must be completed, cancelled, or refunded.
- Currency must be CAD.
Preserve rejected input rows and add a rejection reason. Do not invent replacement customer IDs, dates, or prices. All six injected fault categories are mutually exclusive in the deduplicated data. Use try_cast for integer conversions and try_cast(order_date as date) for invalid dates under Spark 4 ANSI mode.

## Task 4 — Enrich
Join valid orders to customers and products. Keep every valid order exactly once. Add month (YYYY-MM) and revenue_cents = quantity * unit_price_cents as a long integer. Check that joins did not change the row count.

## Task 5 — Business summaries
Filter to completed orders. Calculate revenue_cents and order_count by month, region, and product (including product name). Sort monthly output by month and product rankings by descending revenue, then product ID to break ties. Express dollar display values using decimal arithmetic; validate integer-cent totals.

## Task 6 — Write and verify
Write clean enriched orders as Parquet partitioned by month. Write rejected rows and each summary to separate Parquet folders. Read them back and check counts and totals. Use overwrite mode for full rebuilds so rerunning does not append duplicates. Raw inputs must stay unchanged.

## Task 7 — Performance investigation
Choose one aggregation. Compare uncached execution with repeated execution on materialized cached input. Use perf_counter around actions, warm up the JVM, repeat at least three times, and report median times. Keep the input, operation, and output the same; verify equality. Separate cache population time from reuse time and unpersist afterward. Small workloads may not improve. Inspect explain('formatted') and Spark UI; save your own screenshots if the UI is accessible. Record Spark version, local master, row count, and relevant configs. Do not claim cluster scaling from local-mode results.

## Task 8 — Delivery
Download the executed notebook and outputs. Write a README explaining the problem, rules, actual results, setup, tests, and limitations. Add assertions for row conservation (raw = duplicates + rejected + valid), key uniqueness, join counts, and consistent revenue totals.

## Suggested sequence
Session 1: load and inspect. Session 2: deduplicate and validate. Session 3: joins and reports. Session 4: Parquet, verification, performance, and documentation.

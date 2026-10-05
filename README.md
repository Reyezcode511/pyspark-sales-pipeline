# PySpark Sales Data Engineering Pipeline

Processes 250,000 simulated sales records into validated
Parquet datasets and sales reports.

## Business problem

A fictional retailer needs reliable monthly, regional,
and product sales reports from messy order files.

## Pipeline

CSV inputs → Deduplication → Validation → Customer/product joins
→ Sales summaries → Parquet outputs → Verification

## Data

- 250,000 raw order rows across five CSV files
- 10,000 customers
- 500 products
- All data is simulated
- Monetary values are stored as integer Canadian cents

## Cleaning rules

Remove exact duplicates. Reject orders with invalid customer
or product IDs, non-positive quantities, negative prices,
invalid dates, unsupported statuses, or non-CAD currency.

Rejected records are retained with a reason for review.

## Expected results

The project reference checks specify:
- 1,000 exact duplicates removed
- 1,494 invalid orders rejected
- 247,506 valid orders
- 210,377 completed orders
- CAD 159,557,550.49 in completed-sales revenue

The notebook contains assertions to compare actual results
against these values and verify that report totals agree.

Cancelled and refunded orders are excluded from sales reports.
This is completed-sales revenue, not net revenue or profit.

## Outputs

- Clean enriched orders, partitioned by month
- Rejected orders with rejection reasons
- Monthly sales summary
- Regional sales summary
- Product sales summary
- Performance measurements in JSON

Datasets and summaries are saved as Parquet.

## Performance experiment

The same monthly aggregation was measured in Colab local mode.
One warm-up run per condition was excluded, followed by three
measured runs per condition.

- Uncached median: 3.481 seconds
- Cached median: 1.015 seconds
- Cache population: 5.302 seconds
- Aggregation results matched

Cached execution had approximately 70.8% lower median runtime
in this experiment. Cache setup adds an initial cost.
These timings do not demonstrate multi-machine cluster scaling.

## How to run

1. Open the executed project notebook in Google Colab.
2. Run the PySpark installation cell.
3. Upload Sales_Data_Engineering_250000.zip when prompted.
4. Run the remaining cells in order.
5. Download the output archive and executed notebook.

## Verification

The notebook checks:
- Unique customer and product keys
- Unique order IDs after deduplication
- Row conservation during validation
- Unchanged row counts after joins
- Consistent revenue and order counts across reports
- Counts and totals after reading saved Parquet files
- Matching cached and uncached aggregation results

## Credits and limitations

The simulated dataset, starter scaffold, and guided code were
provided with ChatGPT assistance. I ran the pipeline in Colab.

This is an educational batch pipeline. It does not yet include
production scheduling, monitoring alerts, or cloud deployment.

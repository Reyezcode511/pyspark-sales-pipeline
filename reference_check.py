"""Independent standard-library reference; no Spark execution or timing claims."""
import csv, json, hashlib
from pathlib import Path
from datetime import date
from collections import Counter, defaultdict
ROOT = Path(__file__).resolve().parents[1]
def read(path):
    with path.open(newline='') as f:
        return list(csv.DictReader(f))
customers = {r['customer_id']: r for r in read(ROOT/'data/raw/customers.csv')}
products = {r['product_id']: r for r in read(ROOT/'data/raw/products.csv')}
seen=set(); raw_count=0; duplicates=0; rejected=Counter(); valid_count=0
status_counts=Counter(); reports={k:defaultdict(lambda: {'revenue_cents':0,'order_count':0}) for k in ['month','region','product']}
for p in sorted((ROOT/'data/raw').glob('orders_part_*.csv')):
    for r in read(p):
        raw_count+=1
        key=tuple(r.values())
        if key in seen:
            duplicates+=1; continue
        seen.add(key)
        reason=None
        if r['customer_id'] not in customers: reason='invalid_customer'
        elif r['product_id'] not in products: reason='invalid_product'
        else:
            try: qty=int(r['quantity'])
            except ValueError: qty=0
            try: price=int(r['unit_price_cents'])
            except ValueError: price=-1
            if qty<=0: reason='invalid_quantity'
            elif price<0: reason='invalid_price'
            else:
                try:
                    d=date.fromisoformat(r['order_date'])
                    if d.year!=2025 or d.isoformat()!=r['order_date']: raise ValueError()
                except ValueError: reason='invalid_date'
                if reason is None and r['status'] not in ['completed','cancelled','refunded']: reason='invalid_status'
                if reason is None and r['currency']!='CAD': reason='invalid_currency'
        if reason:
            rejected[reason]+=1; continue
        valid_count+=1;status_counts[r['status']]+=1
        if r['status']=='completed':
            for dim,value in [('month',r['order_date'][:7]),('region',customers[r['customer_id']]['region']),('product',r['product_id'])]:
                reports[dim][value]['revenue_cents']+=qty*price
                reports[dim][value]['order_count']+=1
assert raw_count==250000 and duplicates==1000
assert sum(rejected.values())==1494 and valid_count==247506
assert all(v==249 for v in rejected.values())
assert raw_count==duplicates+sum(rejected.values())+valid_count
revenues=[sum(v['revenue_cents'] for v in report.values()) for report in reports.values()]
assert len(set(revenues))==1
result={'verification_method':'Python standard library; Spark starter not executed','raw_order_rows':raw_count,'exact_duplicates_removed':duplicates,'deduplicated_rows':len(seen),'rejected_rows':sum(rejected.values()),'rejection_counts':dict(rejected),'valid_rows':valid_count,'valid_status_counts':dict(status_counts),'completed_sales_revenue_cents':revenues[0],'summaries':{k:dict(sorted(v.items())) for k,v in reports.items()},'raw_file_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((ROOT/'data/raw').glob('*.csv'))}}
(ROOT/'checks/expected_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['summaries','raw_file_sha256']},indent=2))

#!/usr/bin/env python3
import argparse, csv

def num(row, key):
    try: return max(0.0, min(100.0, float(row.get(key, 0) or 0)))
    except ValueError: return 0.0

def main():
    p=argparse.ArgumentParser()
    p.add_argument('input_csv'); p.add_argument('output_csv')
    a=p.parse_args()
    with open(a.input_csv, newline='', encoding='utf-8-sig') as f:
        rows=list(csv.DictReader(f)); fields=list(rows[0].keys()) if rows else []
    if 'total_score' not in fields: fields.append('total_score')
    for r in rows:
        score=.35*num(r,'fit_score')+.30*num(r,'capacity_score')+.20*num(r,'intent_score')+.15*num(r,'source_quality_score')-num(r,'risk_penalty')
        r['total_score']=f'{max(0,min(100,score)):.1f}'
    with open(a.output_csv,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
if __name__=='__main__': main()

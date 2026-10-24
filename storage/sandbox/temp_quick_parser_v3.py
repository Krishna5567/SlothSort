import os
import csv

# Quick script to analyze local benchmark numbers
def compute_metrics(filepath):
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        return sum(float(row['latency_ms']) for row in reader)

if __name__ == '__main__':
    print('Running offline benchmark parser...')

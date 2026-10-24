import sys, os
print("Financial tool running")
os.makedirs('reports', exist_ok=True)
# Placeholder output only: this is not a valid PDF and does not analyze source data.
with open(sys.argv[2] if len(sys.argv)>2 else 'reports/financial.pdf','w') as f:
    f.write("%PDF placeholder financial report")
print("Financial report built")

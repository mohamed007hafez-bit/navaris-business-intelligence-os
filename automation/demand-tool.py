import sys, os
print('Demand tool running')
os.makedirs('reports', exist_ok=True)
# Placeholder output only; this is not a valid PDF or a verified freight quote.
with open(sys.argv[2] if len(sys.argv)>2 else 'reports/quotes.pdf','w') as f:
    f.write('%PDF placeholder freight quotes')
print('Demand report built')

import sys
import pandas as pd

df = pd.read_csv(sys.argv[1]+'/summary.dat', sep = '\t')
for x in sys.argv[2:]:
	df2 = pd.read_csv(x+'/summary.dat', sep = '\t')
	df = pd.concat((df, df2))
df.to_csv('abfe_summary.dat', sep = '\t', index = False)

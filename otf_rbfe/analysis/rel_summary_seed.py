import sys
import pandas as pd

df = pd.read_csv(sys.argv[1]+'/lam_seed.csv')
df['Name']=[sys.argv[1]]
for x in sys.argv[2:]:
    df2 = pd.read_csv(x+'/lam_seed.csv')
    df2['Name'] = [x]
    df = pd.concat((df, df2))
df.to_csv('rbfe_summary.dat', sep = '\t', index = False)

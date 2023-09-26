import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pic,ax=plt.subplots(figsize=(2,2))

df=pd.read_csv('output.csv')
df2=pd.read_csv('analysis/DLoutput.csv')
df["DLKcat"]=df2['Kcat value (1/s)']
df.rename(columns={'prediction':"RetKcat"},inplace=True)
df.rename(columns={'correct':"Experiment"},inplace=True)
del df['id']
df=np.log10(df)


plt.tick_params(direction='in')
plt.tick_params(which='major',length=1)
plt.tick_params(which='major',width=0.5)

palette = {"RetKcat": '#9dcee2', "Experiment": '#72d643',"DLKcat":'#f7874e'}

ax = sns.stripplot(data=df, order = ["RetKcat", "Experiment","DLKcat"], jitter=0.2,
        palette=palette, size=2, dodge=True,native_scale=True)
ax = sns.boxplot(data=df, order = ["RetKcat", "Experiment","DLKcat"],
        palette=palette, showfliers=False, linewidth=0.6, width=0.5,saturation=1)  



ax.set(xlabel=None)

P=df.corr('pearson')
print(P)

ax.set_ylabel("Predicted $k$$_\mathregular{cat}$ value [log10]", fontsize=4)

plt.yticks([-2,-1, 0, 1, 2])
plt.xticks(fontsize=4)
plt.yticks(fontsize=4)

ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)
ax.spines['top'].set_linewidth(0.5)
ax.spines['right'].set_linewidth(0.5)

pic.savefig('boxplot.png',dpi=1600)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import pearsonr
from scipy.stats import gaussian_kde

with open('output.csv','rb') as f:df=pd.read_csv(f)

yc=np.log10(2**df['correct'])
yp=np.log10(2**df['prediction'])
for i in yc:
    if np.isinf(i):
        print(i)
yc_mean=df['correct'].mean()
r2=1-sum((yc-yp)**2)/sum((yc-yc_mean)**2)


r = pearsonr(yc,yp)

print("pearson系数",r[0])
print("P-Value",r[1])
print("R2",r2)

plt.figure(figsize=(1.75,1.5))




plt.tick_params(direction='in')
plt.tick_params(which='major',length=1)
plt.tick_params(which='major',width=1)

kcat_values_vstack = np.vstack([yc,yp])
experimental_predicted = gaussian_kde(kcat_values_vstack)(kcat_values_vstack)

ax = plt.scatter(x = yc, y = yp, c=experimental_predicted, s=3, edgecolor=[])


cbar = plt.colorbar(ax)
cbar.ax.tick_params(labelsize=6)
cbar.set_label('Density', size=6)

plt.text(-6.0, 6.2, 'r = %.2f' % r[0], fontweight ="normal", fontsize=5)
plt.text(-6.0, 5.5, 'P value = 0', fontweight ="normal", fontsize=5)
plt.text(-6.0, 4.8, f'N = {len(df)}', fontweight ="normal", fontsize=5)



plt.xlabel("log$_{10}$[Experimental $k$$_\mathregular{cat}$ value]", fontdict={'weight': 'normal', 'size': 6}, fontsize=6)
plt.ylabel('log$_{10}$[Predicted $k$$_\mathregular{cat}$ value]',fontdict={'weight': 'normal', 'size': 6},fontsize=6)

plt.xticks([i-8 for i in range(0,18,2)])
plt.yticks([i-4 for i in range(0,14,2)])

plt.xticks(fontsize=6)
plt.yticks(fontsize=6)

x=np.arange(-4,8)
y=np.arange(-4,8)
plt.plot(x, y,linewidth=0.5,c='black',linestyle='--')

ax = plt.gca()
ax.spines['bottom'].set_linewidth(0.5)
ax.spines['left'].set_linewidth(0.5)
ax.spines['top'].set_linewidth(0.5)
ax.spines['right'].set_linewidth(0.5)

xpoints = np.array([-2, 6])
ypoints = np.array([-2, 6])

#plt.plot(xpoints, ypoints,linewidth=0.5,c='black',linestyle='--')

plt.savefig("Pearson.png", dpi=400, bbox_inches='tight')
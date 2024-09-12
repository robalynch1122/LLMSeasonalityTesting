# compare two distributions from two lists to see if the null huypothesis is true that the two distributions are the same

import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns

# New batch
MayLengths = []
DecemberLengths = []


# produce descriptive statistics for the two samples
from scipy.stats import describe
print('Compare May and December character lengths:')
print('May descriptive stats: ', describe(MayLengths))
print('December descriptive stats: ', describe(DecemberLengths))

# compare the two distributions with the 1-tailed t-test
from scipy.stats import ttest_ind
ttest = ttest_ind(MayLengths, DecemberLengths)
print(ttest)

# interpret via p-value
alpha = 0.05
if ttest[1] > alpha:
	print('Samples are likely drawn from the same distributions (fail to reject H0)')
else:
	print('Samples are likely drawn from different distributions (reject H0)')


# plot the two distributions
import matplotlib.pyplot as plt
plt.figure()
plt.hist(MayLengths, bins=25, alpha=0.5, label='May Character Lengths')
plt.hist(DecemberLengths, bins=25, alpha=0.5, label='December Character Lengths')
plt.legend(loc='upper right')
plt.savefig('Plot.png')

# Plot density plots
plt.figure()
sns.kdeplot(MayLengths, label='May Character Lengths', shade=True)
sns.kdeplot(DecemberLengths, label='December Character Lengths', shade=True)
plt.legend(loc='upper right')
plt.title('Density Plot of Token Lengths')

# Save the plot
plt.tight_layout()
plt.savefig('DPlot.png')
plt.show()

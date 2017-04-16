import numpy as np
from scipy import stats

N = 10000
a = np.random.normal(0, 1, N)
mean, sigma = a.mean(), a.std(ddof=1)
conf_int_a = stats.norm.interval(0.68, loc=mean, scale=sigma)

print('{:0.2%} of the single draws are in conf_int_a'
      .format(((a >= conf_int_a[0]) & (a < conf_int_a[1])).sum() / float(N)))

M = 1000
b = np.random.normal(0, 1, (N, M)).mean(axis=1)
conf_int_b = stats.norm.interval(0.68, loc=0, scale=1 / np.sqrt(M))
print('{:0.2%} of the means are in conf_int_b'
      .format(((b >= conf_int_b[0]) & (b < conf_int_b[1])).sum() / float(N))) 
        
            
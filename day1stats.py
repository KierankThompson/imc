import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress




df = pd.read_csv("round-1-island-data-bottle\prices_round_1_day_-2.csv", sep=';')
squiddf = df[df['product'] == 'SQUID_INK']
squiddf.fillna(0)
forestdf = df[df['product'] == 'RAINFOREST_RESIN']
forestdf.fillna(0)
kelpdf = df[df['product'] == 'KELP']
kelpdf.fillna(0)


pd.set_option('display.max_columns', None)
#print(forestdf)


squidReturns = squiddf['mid_price'].diff()[1:]
forestReturns = forestdf['mid_price'].diff()[1:]
kelpReturns = kelpdf['mid_price'].diff()[1:]



dataframes = [squiddf, forestdf, kelpdf]
mid_prices = np.array([df['mid_price'].values for df in dataframes])


mid_prices = mid_prices.T


product_labels = ['SQUID_INK', 'RAINFOREST_RESIN', 'KELP']

returns = np.diff(mid_prices, axis=0) / mid_prices[:-1] * 100

num_slices = 1
slice_size = len(returns) // num_slices

for i in range(num_slices):
    start_idx = i * slice_size
    end_idx = (i + 1) * slice_size if i < num_slices - 1 else len(returns)
    sliced_returns = returns[start_idx:end_idx]
    corr_matrix = np.corrcoef(sliced_returns, rowvar=False)
    print(f"Correlation Matrix for Slice {i + 1}:")
    print(pd.DataFrame(corr_matrix, index=product_labels, columns=product_labels))
    print()



"""
means = np.array([arr.mean() for arr in (squidReturns,forestReturns,kelpReturns)])
stockReturns = pd.DataFrame({
    'squid_price': squidReturns.reset_index(drop=True),
    'forest_price': forestReturns.reset_index(drop=True),
    'kelp_price': kelpReturns.reset_index(drop=True)
})
dev = stockReturns - means
v = dev.T @ dev / (stockReturns.shape[0] - 1)
inverseV = np.linalg.inv(v)
eArr = means
oneArr = np.array([1 for _ in range(3)])
a = eArr.T @ inverseV @ oneArr
b = eArr.T @ inverseV @ eArr
c = oneArr.T @ inverseV @ oneArr
d = b * c - a**2
g = (b * (inverseV @ oneArr) - a * (inverseV @ eArr)) / d
h = (c * (inverseV @ eArr) - a * (inverseV @ oneArr)) / d
def computeWeights(portReturn):
    return g + h * portReturn
def computeVariance(portReturn):
    return (1/d) * (c * portReturn**2 - 2 * a * portReturn + b)
expectedReturns = np.random.uniform(low=0,high=0.03,size=(100000,))
sdReturns = [np.sqrt(computeVariance(r)) for r in expectedReturns]
plt.plot(sdReturns, expectedReturns,'o', color="red", markersize = 3, label="Efficient Frontier")
plt.plot((1/c)**(1/2), a/c, 'o', color="blue", markersize = 8, label = "MVP")
plt.show()

print(computeWeights(0.01))
"""




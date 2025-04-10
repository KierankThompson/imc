import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress




df = pd.read_csv("day1data\prices_round_1_day_0.csv", sep=';')
squiddf = df[df['product'] == 'SQUID_INK']
squiddf.fillna(0, inplace=True)
forestdf = df[df['product'] == 'RAINFOREST_RESIN']
forestdf.fillna(0, inplace=True)
kelpdf = df[df['product'] == 'KELP']
kelpdf.fillna(0, inplace=True)


pd.set_option('display.max_columns', None)
#print(forestdf)


squidReturns = squiddf['mid_price'].diff()[1:]
forestReturns = forestdf['mid_price'].diff()[1:]
kelpReturns = kelpdf['mid_price'].diff()[1:]


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
#print(forestReturns.value_counts())

#print(forestdf['mid_price'].mean())
#print(forestdf['mid_price'].value_counts())


total_bid_value = (
    kelpdf['bid_price_1'] * kelpdf['bid_volume_1'] +
    kelpdf['bid_price_2'] * kelpdf['bid_volume_2'] +
    kelpdf['bid_price_3'] * kelpdf['bid_volume_3']
)

total_bid_volume = (
    kelpdf['bid_volume_1'] +
    kelpdf['bid_volume_2'] +
    kelpdf['bid_volume_3']
)




total_ask_value = (
    kelpdf['ask_price_1'] * kelpdf['ask_volume_1'] +
    kelpdf['ask_price_2'] * kelpdf['ask_volume_2'] +
    kelpdf['ask_price_3'] * kelpdf['ask_volume_3']
)

total_ask_volume = (
    kelpdf['ask_volume_1'] +
    kelpdf['ask_volume_2'] +
    kelpdf['ask_volume_3']
)



vwap = (total_bid_value + total_ask_value) / (total_ask_volume + total_bid_volume)



vwap_diff = vwap - kelpdf['mid_price']
print(vwap_diff.value_counts())


print(squiddf['ask_price_1'].value_counts())


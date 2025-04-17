import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint



csv_files = [
    "round-2-island-data-bottle\\prices_round_2_day_-1.csv",
    "round-2-island-data-bottle\\prices_round_2_day_0.csv",
    "round-2-island-data-bottle\\prices_round_2_day_1.csv"
]

# Combine all CSV files into one DataFrame
df = pd.concat([pd.read_csv(file, sep=';') for file in csv_files], ignore_index=True)
squiddf = df[df['product'] == 'SQUID_INK']
squiddf.fillna(0)
forestdf = df[df['product'] == 'RAINFOREST_RESIN']
forestdf.fillna(0)
kelpdf = df[df['product'] == 'KELP']
kelpdf.fillna(0)
croissantdf = df[df['product'] == 'CROISSANTS']
croissantdf.fillna(0)
jamsdf = df[df['product'] == 'JAMS']
jamsdf.fillna(0)
djembesdf = df[df['product'] == 'DJEMBES']
djembesdf.fillna(0)
picnicbasket1df = df[df['product'] == 'PICNIC_BASKET1']
picnicbasket1df.fillna(0)
picnicbasket2df = df[df['product'] == 'PICNIC_BASKET2']
picnicbasket2df.fillna(0)

for df in [squiddf, forestdf, kelpdf, croissantdf, jamsdf, djembesdf, picnicbasket1df, picnicbasket2df]:
    for i in range(1, 4):  
        
        
        df[f'weighted_ask_price_{i}'] = df[f'ask_price_{i}'] * df[f'ask_volume_{i}']
        df[f'weighted_bid_price_{i}'] = df[f'bid_price_{i}'] * df[f'bid_volume_{i}']
    
    
    df['average_price'] = (
        sum(df[f'weighted_ask_price_{i}'].fillna(0) + df[f'weighted_bid_price_{i}'].fillna(0) for i in range(1, 4)) /
        sum(df[f'ask_volume_{i}'].fillna(0) + df[f'bid_volume_{i}'].fillna(0) for i in range(1, 4))
    )
    
    
    diff_count = (abs(df['average_price'] - df['mid_price']) > 1).sum()
    total_count = len(df)
    percentage_diff = (diff_count / total_count) * 100
    
    print(f"Percentage of times average_price and mid_price differ by more than 1 for {df['product'].iloc[0]}: {percentage_diff:.2f}%")
dataframes = [squiddf, forestdf, kelpdf, croissantdf, jamsdf, djembesdf, picnicbasket1df, picnicbasket2df]
mid_prices = np.array([df['mid_price'].values for df in dataframes])


mid_prices = mid_prices.T


product_labels = ['SQUID_INK', 'RAINFOREST_RESIN', 'KELP', 'CROISSANTS', 'JAMS', 'DJEMBES', 'PICNIC_BASKET1', 'PICNIC_BASKET2']

returns = np.diff(mid_prices, axis=0) / mid_prices[:-1] * 100

num_slices = 2
slice_size = len(returns) // num_slices

for i in range(num_slices):
    start_idx = i * slice_size
    end_idx = (i + 1) * slice_size if i < num_slices - 1 else len(returns)
    sliced_returns = returns[start_idx:end_idx]
    corr_matrix = np.corrcoef(sliced_returns, rowvar=False)
    print(f"Correlation Matrix for Slice {i + 1}:")
    print(pd.DataFrame(corr_matrix, index=product_labels, columns=product_labels))
    print()

def test_stationarity(dataframes, product_labels):
    for df, label in zip(dataframes, product_labels):
        mid_prices = df['mid_price'].values
        result = adfuller(mid_prices)
        print(f"ADF Statistic for {label}: {result[0]}")
        print(f"p-value for {label}: {result[1]}")
        print("Critical Values:")
        for key, value in result[4].items():
            print(f"   {key}: {value}")
        print(f"Mean for {label}: {np.mean(mid_prices):.2f}")
        print(f"Standard Deviation for {label}: {np.std(mid_prices):.2f}")
        print(f"Skew for {label}: {pd.Series(mid_prices).skew():.2f}")
        if result[1] <= 0.05:
            print("Stationary")
        else:
            print("Not Stationary")
        print()

test_stationarity(dataframes, product_labels)


def calculate_cointegration_matrix(dataframes, product_labels):
    num_products = len(dataframes)
    coint_matrix = np.zeros((num_products, num_products))

    for i in range(num_products):
        for j in range(num_products):
            if i != j:
                _, p_value, _ = coint(dataframes[i]['mid_price'], dataframes[j]['mid_price'])
                coint_matrix[i, j] = p_value
            else:
                coint_matrix[i, j] = 1

    return coint_matrix

coint_matrix = calculate_cointegration_matrix(dataframes, product_labels)
print("Cointegration Matrix:")
print(pd.DataFrame(coint_matrix, index=product_labels, columns=product_labels))


croissant_returns = returns[:, product_labels.index('CROISSANTS')]
kelp_returns = returns[:, product_labels.index('KELP')]

croissant_skew = pd.Series(croissant_returns).skew()
kelp_skew = pd.Series(kelp_returns).skew()

croissant_avg = np.mean(croissant_returns)
kelp_avg = np.mean(kelp_returns)

print(croissant_avg*100)
print(croissant_skew)
print(kelp_avg*100)
print(kelp_skew)






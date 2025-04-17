from datamodel import Listing, Observation, Order, OrderDepth, ProsperityEncoder, Symbol, Trade, TradingState
from typing import Any, List
import string
import jsonpickle
import pickle
import numpy as np
import pandas as pd





def forestTrade(order_depth, curPos):
    meanPrice = 10000
    #vol stands for volume
    vwap = int((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0]) / 2)
    if vwap - meanPrice > 1:
        tradeVol = tradeVol = min(50, 25 + (temp:= sum(volume for price, volume in order_depth.buy_orders.items() if price >= 10002)))
        tradePrice = meanPrice + 2 #max(vwap - 1, meanPrice+1)
        return tradePrice, -tradeVol
    if vwap - meanPrice < 1:
        tradeVol = min(50, 25 + (temp:= sum(volume for price, volume in order_depth.sell_orders.items() if price <= 9998)))
        tradePrice = meanPrice - 2 #min(vwap + 1, meanPrice-1)
        return tradePrice, tradeVol
    else:
        return vwap, -curPos
        
def meanReversion(order_depth, curPos, arr, maxVol, sequenceLength, mult=1.5, add = 0):
    if len(arr) != sequenceLength:
        return 0, 0
    meanPrice = int(np.mean(arr))
    sdPrice = np.std(arr)
    total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
    total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
    vwap = int(total_value / total_volume) if total_volume > 0 else 0
    #print(f"VWAP picnic: {vwap}",end = " ")
    #print(f"mean price {meanPrice}", end = " ")
    #print(f"std: {sdPrice}", end = " ")
    if vwap > meanPrice + (sdPrice*mult):
        tradeVol = min(maxVol+curPos, add + sum(volume for price, volume in order_depth.buy_orders.items() if price >= vwap-1))
        tradePrice = vwap - 1 #max(vwap - 1, meanPrice+1)
        return tradePrice, -tradeVol
    if vwap < meanPrice - (sdPrice*mult):
        tradeVol = min(maxVol-curPos, add + sum(volume for price, volume in order_depth.sell_orders.items() if price <= vwap+1))
        tradePrice = vwap + 1 #min(vwap + 1, meanPrice-1)
        return tradePrice, tradeVol
    else:
        return 0,0
    
def momentum(order_depth, curPos, arr, maxVol, sequenceLength, add=0):
    if len(arr) < sequenceLength:
        return 0, 0
    meanReturn = (np.mean(np.diff(arr) / arr[:-1]) * 100)
    sdReturn = np.std((np.diff(arr) / arr[:-1]) * 100)
    total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
    total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
    vwap = int(total_value / total_volume) if total_volume > 0 else 0
    currentReturn = ((vwap - arr[-1]) / arr[-1]) * 100
    if currentReturn > meanReturn * (1+sdReturn):
        tradeVol =  min(maxVol+curPos, add + sum(volume for price, volume in order_depth.sell_orders.items() if price <= vwap))
        tradePrice = vwap - 1
        return tradePrice, tradeVol
    if currentReturn < meanReturn * (1-sdReturn):
        tradeVol = min(maxVol+curPos, add + sum(volume for price, volume in order_depth.buy_orders.items() if price >= vwap))
        tradePrice = vwap + 1
        return tradePrice, -tradeVol
    else:
        return vwap, -curPos
    
def short(order_depth, curPos, arr, maxVol, sequenceLength, add=0):
    if len(arr) < sequenceLength:
        return 0, 0
    meanReturn = (np.mean(np.diff(arr) / arr[:-1]) * 100)
    sdReturn = np.std((np.diff(arr) / arr[:-1]) * 100)
    total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
    total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
    vwap = int(total_value / total_volume) if total_volume > 0 else 0
    currentReturn = ((vwap - arr[-1]) / arr[-1]) * 100
    if currentReturn < meanReturn * (1-sdReturn):
        tradeVol = min(maxVol+curPos, add + sum(volume for price, volume in order_depth.buy_orders.items() if price >= vwap))
        tradePrice = vwap
        return tradePrice, -tradeVol
    else:
        return vwap, -curPos

    
    
    




        



        

        
class Trader:

    def __init__(self):
        self.length = {
            "KELP": 15,
            "RAINFOREST_RESIN": 10,
            "SQUID_INK": 5,
            "CROISSANTS": 20,
            "JAMS": 10,
            "DJEMBES": 10,
            "PICNIC_BASKET1": 10,
            "PICNIC_BASKET2": 10
        }
        dic = {key: [] for key in self.length}
        
        self.frozen = jsonpickle.encode(dic)
    def run(self, state: TradingState):
        
        #print(f"orders: {orders}", end = " ")
        #print("Observations: " + str(state.observations))
        print(f"Position: {state.position}", end = " ")
        
        result = {}
        
        productDic = jsonpickle.decode(self.frozen)
        traderData = " "
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            tradeVol = 0
            tradePrice = 0
            if product == "RAINFOREST_RESIN":
                tradePrice, tradeVol = forestTrade(order_depth, state.position.get(product, 0))
            if product == "PICNIC_BASKET1":
                tradePrice, tradeVol = meanReversion(order_depth, state.position.get(product, 0), productDic[product],60,self.length[product])
                total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
                total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
                vwap = int(total_value / total_volume) if total_volume > 0 else 0
                productDic[product].append(vwap)
                if len(productDic[product]) > self.length[product]:
                    productDic[product].pop(0)
            if product == "PICNIC_BASKET2":
                tradePrice, tradeVol = meanReversion(order_depth, state.position.get(product, 0), productDic[product],100,self.length[product],add=10)
                total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
                total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
                vwap = int(total_value / total_volume) if total_volume > 0 else 0
                productDic[product].append(vwap)
                if len(productDic[product]) > self.length[product]:
                    productDic[product].pop(0)
            if product == "SQUID_INK":
                #tradePrice, tradeVol = meanReversion(order_depth, state.position.get(product, 0), productDic[product],50,10)
                tradePrice, tradeVol = momentum(order_depth, state.position.get(product, 0), productDic[product],50,self.length[product],add = 10)
                total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
                total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
                vwap = int(total_value / total_volume) if total_volume > 0 else 0
                productDic[product].append(vwap)
                if len(productDic[product]) > self.length[product]:
                    productDic[product].pop(0)
            if product == "JAMS":
                tradePrice, tradeVol = meanReversion(order_depth, state.position.get(product, 0), productDic[product],350,self.length[product],add=25)
                total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
                total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
                vwap = int(total_value / total_volume) if total_volume > 0 else 0
                productDic[product].append(vwap)
                if len(productDic[product]) > self.length[product]:
                    productDic[product].pop(0)
            if product == "CROISSANTS":
                tradePrice, tradeVol = momentum(order_depth, state.position.get(product, 0), productDic[product],250,self.length[product])
                total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
                total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
                vwap = int(total_value / total_volume) if total_volume > 0 else 0
                productDic[product].append(vwap)
                if len(productDic[product]) > self.length[product]:
                    productDic[product].pop(0)
            if product == "KELP":
                tradePrice, tradeVol = momentum(order_depth, state.position.get(product, 0), productDic[product],250,self.length[product],30)
                total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
                total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
                vwap = int(total_value / total_volume) if total_volume > 0 else 0
                productDic[product].append(vwap)
                if len(productDic[product]) > self.length[product]:
                    productDic[product].pop(0)
            if product == "DJEMBES":
                tradePrice, tradeVol = meanReversion(order_depth, state.position.get(product, 0), productDic[product],60,self.length[product],add=10)
                total_volume = sum(abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(abs(volume) for price, volume in order_depth.buy_orders.items())
                total_value = sum(price * abs(volume) for price, volume in order_depth.sell_orders.items()) + sum(price * abs(volume) for price, volume in order_depth.buy_orders.items())
                vwap = int(total_value / total_volume) if total_volume > 0 else 0
                productDic[product].append(vwap)
                if len(productDic[product]) > self.length[product]:
                    productDic[product].pop(0)
            

            o = Order(product, tradePrice, int(tradeVol))
            orders.append(o)
            result[product] = orders
                
        self.frozen = jsonpickle.encode(productDic)
            
            
            
    
        
        
        conversions = 1
        return result, conversions, traderData

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string






def forestTrade(order_depth, curPos, pastPosition):
    meanPrice = 10000
    #vol stands for volume
    vwap = int((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0]) / 2)
    print(f"This is vwap: {vwap}",end = " ")
    if vwap - meanPrice > 0:
        tradeVol = min(50,max(13,int(list(order_depth.buy_orders.items())[0][1])*1.25))
        tradePrice = meanPrice + 2
        return tradePrice, -tradeVol, True
    if vwap - meanPrice < 0:
        tradeVol = min(50,max(int(list(order_depth.sell_orders.items())[0][1]*1.25),13))
        tradePrice = meanPrice - 2
        return tradePrice, tradeVol, True
    else:
        if pastPosition+curPos < 1:
            return 1000, -curPos, False
        else:
            return 1000, -curPos, False
def kelpTrade(order_depth,curPos, pastPosition):
    meanPrice = 2036
    #vol stands for volume
    vwap = int((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0]) / 2)
    
    if vwap - meanPrice > 0:
        tradeVol = min(50,max(10,int(list(order_depth.buy_orders.items())[0][1]*1.25)))
        tradePrice = meanPrice + 2
        return tradePrice, -tradeVol, True
    if vwap - meanPrice < 0:
        tradeVol = min(50,max(int(list(order_depth.sell_orders.items())[0][1]*1.25),10))
        tradePrice = meanPrice - 2
        return tradePrice, tradeVol, True
    else:
        if pastPosition+curPos < 1:
            return 2037, -curPos, False
        else:
            return 2037, -curPos, False
        
def squidTrade(order_depth,curPos, pastPosition):
    meanPrice = 1956
    #vol stands for volume
    vwap = int((list(order_depth.sell_orders.items())[0][0] + list(order_depth.buy_orders.items())[0][0]) / 2)
    print(f"This is vwap: {vwap}",end = " ")
    print(f"This is mean price {meanPrice}",end = "")
    if vwap - meanPrice > 1:
        tradeVol = min(50,max(10,int(list(order_depth.buy_orders.items())[0][1]*1.25)))
        tradePrice = vwap + 2
        return tradePrice, -tradeVol, True
    if vwap - meanPrice < -1:
        tradeVol = min(50,max(int(list(order_depth.sell_orders.items())[0][1]*1.25),10))
        tradePrice = vwap - 2
        return tradePrice, tradeVol, True
    else:
        if pastPosition+curPos < 1:
            return 1956, -curPos, False
        else:
            return 1956, -curPos, False



        

        
class Trader:
    def run(self, state: TradingState):
        #print("traderData: " + state.traderData)
        #print("Observations: " + str(state.observations))
        result = {}
        pos = False
        pos2 = False
        pos3 = False
        if not state.traderData:
            state.traderData = "0,0,0"
        data = state.traderData.split(",")
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            orders: List[Order] = []
            #print("Acceptable price : " + str(acceptable_price))
            #print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            if product == "RAINFOREST_RESIN":
                if product in state.position:
                    tradePrice, tradeVol, pos = forestTrade(order_depth, state.position[product], int(data[0]))
                else:
                    tradePrice, tradeVol, pos = forestTrade(order_depth, 0, int(data[0]))
                #print(f"Trade Price: {tradePrice} Trade vol: {tradeVol}", end = " ")
                #print(f"Position: {state.position}", end = " ")
                o = Order(product, tradePrice, int(tradeVol))
                
                #print(f"Order: {o}", end = " ")
                #print(f"orders: {orders}", end = " ")
                orders.append(o)
            if product == "KELP":
                if product in state.position:
                    tradePrice, tradeVol2, pos2 = kelpTrade(order_depth, state.position[product], int(data[1]))
                else:
                    tradePrice, tradeVol2, pos2 = kelpTrade(order_depth, 0, int(data[1]))
                #print(f"Trade Price: {tradePrice} Trade vol: {tradeVol}", end = " ")
                #print(f"Position: {state.position}", end = " ")
                o = Order(product, tradePrice, int(tradeVol2))
                
                #print(f"Order: {o}", end = " ")
                #print(f"orders: {orders}", end = " ")
                orders.append(o)
            if product == "SQUID_INK":
                if product in state.position:
                    tradePrice, tradeVol3, pos3 = kelpTrade(order_depth, state.position[product], int(data[2]))
                else:
                    tradePrice, tradeVol3, pos3 = kelpTrade(order_depth, 0, int(data[2]))
                #print(f"Trade Price: {tradePrice} Trade vol: {tradeVol}", end = " ")
                #print(f"Position: {state.position}", end = " ")
                o = Order(product, tradePrice, int(tradeVol3))
                
                #print(f"Order: {o}", end = " ")
                #print(f"orders: {orders}", end = " ")
                orders.append(o)
            result[product] = orders
            if pos:
                data[0] =  f"{tradeVol}"
            else:
                data[0] = f"{0}"
            if pos2:
                data[1] = f"{tradeVol2}"
            else:
                data[1] = f"{0}"
            if pos3:
                data[2] = f"{tradeVol3}"
            else:
                data[2] = f"{0}"
        traderData = ",".join(data)
    
        
        
        conversions = 1
        return result, conversions, traderData

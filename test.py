# sudo apt install python3-pip
# pip install python-okx
# pip install websockets
# nohup python3 test.py > output.log 2>&1 &

import okx.Trade as Trade
import asyncio
import json
import time

from okx.websocket.WsPrivateAsync import WsPrivateAsync
    
flag = "0"
apiKey = ""
secretKey = ""
passphrase = ""
# url = "wss://wspap.okx.com:8443/ws/v5/private?brokerId=9999"
url = "wss://ws.okx.com:8443/ws/v5/private"
arg1 = {"channel": "account", "ccy": "BTC"}
arg2 = {"channel": "orders", "instType": "ANY"}
arg3 = {"channel": "balance_and_position"}
global_startTime = 0
global_openTime = 0
global_filledTime = 0
global_orderId = 0
cost_times = []  # 用于存储每个订单的时间差
file = None
canceled = False
max_cost_time = 0
min_cost_time = 0
total_count = 60
current_count = 0

def privateCallback(message):
    global global_openTime
    global global_filledTime
    global cost_times
    global global_startTime
    global global_orderId
    global file
    global canceled
    global max_cost_time
    global min_cost_time
    global current_count
    global total_count
    print("privateCallback", message)
    try:
        data = json.loads(message)
        if data['arg']['channel'] == "orders":
            for dataItem in data['data']:
                print("state:", dataItem['state'])
                print("clOrdId:", dataItem['clOrdId'])
                if dataItem['clOrdId'] == str(global_orderId):
                    if dataItem['state'] == "live":
                        global_openTime = time.time_ns()
                        print("openTime:", global_openTime)
                        cost_time = (global_openTime - global_orderId) / 1000000
                        req_time = (global_startTime - global_orderId) / 1000000
                        cost_times.append(cost_time)  # 将每个订单的时间差添加到列表中
                        max_cost_time = max(max_cost_time, cost_time)  # 更新最大耗时
                        if min_cost_time == 0 :
                            min_cost_time = cost_time
                        else:
                            min_cost_time = min(min_cost_time, cost_time)  # 更新最小耗时
                        average_cost_time = sum(cost_times) / len(cost_times) if cost_times else 0
                        if file:
                            file.write(f"{current_count}   orderId: {global_orderId}, orderTime: {global_startTime}, openTime: {global_openTime},  reqCost:{req_time}ms, cost_time:{cost_time}ms, average:{average_cost_time}ms, min:{min_cost_time}ms, max:{max_cost_time}ms\n")
                            if current_count == total_count:
                               file.write(f"test end,   average:{average_cost_time}ms, min:{min_cost_time}ms, max:{max_cost_time}ms\n") 
                            file.flush()
                        print("-----------------------------------------cancelOrder--------------------------------------------")
                        cancelOrder(orderId=global_orderId)
                    elif dataItem['state'] == "canceled":
                        canceled = True
    
    except Exception as e:
        print(f"Error for privateCallback: {e}")
            

async def main():
    global file
    global canceled
    global total_count
    global current_count
    try:        
        file = open('order_records.txt', 'a')
        print("-----------------------------------------start ws--------------------------------------------")
        ws = WsPrivateAsync(
            apiKey=apiKey,
            passphrase=passphrase,
            secretKey=secretKey,
            url=url,
            useServerTime=False
        )
        await ws.start()
        await asyncio.sleep(5)
        print("-----------------------------------------subscribe--------------------------------------------")
        args1 = [arg2]
        await ws.subscribe(args1, callback=privateCallback)
        await asyncio.sleep(5)
        
        while current_count < total_count:
            print("-----------------------------------------placeorder--------------------------------------------")
            await placeOrder() 
            current_count += 1
            await asyncio.sleep(300)  # 每隔5分钟（300秒）下一次单
             # 检查撤单状态
            if not canceled:   
                # 撤单未成功，重新连接 WebSocket
                await ws.stop()  # 先关闭当前连接
                await ws.start()  # 重新连接
                await asyncio.sleep(5)  # 等待连接建立
                await ws.subscribe(args1, callback=privateCallback)
                await asyncio.sleep(5)  # 等待连接建立
            
        await asyncio.sleep(10)
        print("-----------------------------------------unsubscribe--------------------------------------------")
        args2 = [arg2]
        await ws.unsubscribe(args2, callback=privateCallback)
        await asyncio.sleep(10)
        if file:
            file.close()
    except Exception as e:
        print(f"Error for ws: {e}")
        
async def placeOrder():
    global global_orderId
    global global_startTime
    global_orderId = time.time_ns()
    print("orderId:", global_orderId)
    tradeAPI = Trade.TradeAPI(apiKey, secretKey, passphrase, False, flag)
    result = tradeAPI.place_order(
        instId="BTC-USDT",
        tdMode="cash",
        clOrdId=str(global_orderId),
        side="buy",
        ordType="limit",
        px="2.15",
        sz="2"
    )
    global_startTime = time.time_ns()
    print("startTime:",global_startTime)
    print(result)
    
def cancelOrder(orderId):
    tradeAPI = Trade.TradeAPI(apiKey, secretKey, passphrase, False, flag)
    result = tradeAPI.cancel_order(
        instId="BTC-USDT",
        clOrdId=orderId
    )
    print(result)


if __name__ == '__main__':
    asyncio.run(main())


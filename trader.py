#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time
<<<<<<< HEAD

=======
>>>>>>> 5492f2b1d7d23a2a0d3dc3a399b24f4cddc9bbb8
#GLOBALS

# The amount of money we have
money = 0
bond_fair = 1000
# The current state of the market
book = {}
# The buy/sell requests that are sent to the exchange
orders = []
# The stocks that we own
my_stock = {}
order_id = 1

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25001))
    return s.makefile('w+', 1)

def add(order_id, symbol, direction, price, size):
  #direction is buying / selling

  json_string = '{"type": "add", "order_id": "' + str(order_id) + '", "symbol": "' + symbol + '", "dir": "' + direction + '", "price": "' + str(price) + '", "size": "'+ str(size) +'"}'
  return json_string

    
def convert(order_id, symbol, direction, price, size):
  json_string = '{"type": "convert", "order_id": "' + str(order_id) + '", "symbol": "' + symbol + '", "dir": "' + direction + '", "size": "'+size +'"}'
  return json_string
    
def cancel(order_id):
  json_string = '{"type": "cancel", "order_id": "'+ str(order_id) + '"}'
  return json_string
    
def hello():
  json_string = '{"type": "hello", "team": "JURIEN"}'
  print(json_string, file=exchange)

# The highest price someone is willing to offer for a share    
def bestBuyPrice(symbol):
  global book
  return book[symbol]["buy"][0][0]

# The lowest someone is willing to sell out a share
def bestSellPrice(symbol):
  global book
  return book[symbol]["sell"][0][0]


# Returns the fair price of the stock assuming the market is correct
def fairPrice(symbol):
  mid = (bestSellPrice(symbol) + bestBuyPrice(symbol)) / 2  
  return mid

# Whether we have enough money to risk buying stocks
def canBuy():
  global cash
  if cash <= -40000:
    return False
  else:
    return True    
    
# Generates buy requests and adds it onto the orders list
def whatToBuy():
  global orders
  global order_id
  # Max number of bonds we buy in 1 transaction is 5
  symbol = "BOND"
  size = 1
  price = bestSellPrice(symbol)
  for j in range(50):
    if canBuy(symbol) and price > 0:
      buy_request = '{"type": "add", "order_id": ' + str(order_id) + ', "symbol": ' + symbol + ', "dir": "BUY", "price": ' + price + ', "size": ' + size + ' }'
      orders.insert(buy_request)
      order_id += 1

# Generates sell requests and adds it onto the orders list
def whatToSell():
  global orders
  global order_id  
  symbol = "BOND"
  size = 1
  order_id = getOrderId()
  for j in range(100):
    if canSell(symbol) and price > 0:
      sell_request = '{"type": "add", "order_id": ' + str(order_id) + ', "symbol": ' + symbol + ', "dir": "BUY", "price": ' + price + ', "size": ' + size + ' }'
      orders.insert(sell_request)
      order_id += 1

# Sends all the orders to the exchange
def makeTrades(exchange):
  global orders
  for item in orders:
    print(item, file=exchange)

# Processes and handles the different server responses
def processServerResponse(json_response, exchange):
  response_dict = json.loads(json_response)
  response_type = response_dict["type"]
  global my_stock
  global money
  global book
  if response_type == "hello":
    money = response_dict["cash"]

    for symbol_pair in response_dict["symbols"]:
      sym = symbol_pair["symbol"]
      pos = symbol_pair["position"]      
      
      my_stock[sym] = pos
    
  elif response_type == "open":
    #update list of open orders
    pass
  elif response_type == "close":
    pass
  elif response_type == "error":
    print(response_dict["error"])

  elif response_type == "book":
    # Update our local copy of the book
    book[response_dict["symbol"]] = {"buy": response_dict["buy"], "sell": response_dict["sell"]}
    # After each state is recorded, we make decisions on what to buy and what to sell
    # Once we have a list of 100 actions, we send the requests to the exchange and then 
    # process the results.
    whatToBuy()
    whatToSell()
    makeTrades(exchange)
    pass

  elif response_type == "trade":
    pass
  elif response_type == "ack":
    # Our order went through
    pass

  elif response_type == "reject":
    # Remove the order from out local list
    print (response_dict["order_id"], response_dict["error"])

  elif response_type == "fill":        
    print (response_dict)
    print(response_dict)
    hello()
    
    #this means that our order has been filled
    #so we should re-evaluate the state by saying hello
    
    json_string = '{"type": "hello", "team": "JURIEN"}'
    print(json_string, file=exchange)          


    pass
  elif response_type == "out":    
    pass
        
  return response_dict


def main():
  exchange = connect()
  json_string = '{"type": "hello", "team": "JURIEN"}'
  print(json_string, file=exchange)
  hello_from_exchange = json.loads(exchange.readline())
  print(hello_from_exchange)
  print(json_string, file=exchange)
 
  while 1:
    # Read everything the server says  
    try:
      message_from_exchange = json.loads(exchange.readline())
      processServerResponse(message_from_exchange, exchange)
      print(message_from_exchange)
    except:
      pass

    for i in range(1, 100):
      print(bestBuyPrice("BOND"))
      json_string = '{"type": "add", "order_id": ' + str(i) + ', "symbol": "BOND", "dir": "BUY", "price": 999, "size": 1}'
      try:
        print(json_string, file=exchange)
#	print("i am trying to buy")
      except:
        pass
      print(bestSellPrice("BOND"))
      json_string = '{"type": "add", "order_id": ' + str(i+100) + ', "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 1}'
      try:
        print(json_string, file=exchange)
#	print("i am trying to sell")
      except:
        pass
      time.sleep(0.1)
     

 

if __name__ == "__main__":
  main()

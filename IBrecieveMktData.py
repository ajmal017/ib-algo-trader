from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep

# print all message from TWS


def watcher(msg):
    print(msg)

# show Bid and Ask quotes
def my_BidAsk(msg):
    if msg.field == 1:
        print('{}:{}: bid: {}' .format(contractTuple[0], contractTuple[6], msg.price))
    elif msg.field == 2:
        print('{}:{}: ask: {}' .format(contractTuple[0], contractTuple[6], msg.price))

def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    #print('Contract Values {}, {}, {}, {}, {}, {}' .format(contractTuple))
    return newContract

if __name__ == '__main__':
    a = '55'
    con = ibConnection(port=7497, clientId=100)
    con.registerAll(watcher)
    showBidAskOnly = False   # set False to see the raw message
    if showBidAskOnly:
        con.unregister(watcher, message.tickSize, message.tickPrice, message.tickString,
                       message.tickOptionComputation)
        con.register(my_BidAsk, message.tickPrice)
    con.connect()
    sleep(1)
    tickId = 4

    # Note: Option quotes will give an error if they aren't shown in TWS

    contractTuple = ('SPY', 'STK', 'SMART', 'USD', '', 0.0, '')
    #contractTuple = ('SPY', 'OPT', 'SMART', 'USD', '20180321', 275.0, 'CALL')
    # contractTuple = ('ES', 'FUT', 'GLOBEX', 'USD', '200709', 0.0, '')
    # contractTuple = ('ES', 'FOP', 'GLOBEX', 'USD', '20070920', 1460.0, 'CALL')
    # contractTuple = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')
    stkContract = makeStkContract(contractTuple)
    print('* * * * REQUESTING MARKET DATA * * * *')
    con.reqMarketDataType(4)
    con.reqMktData(tickId, stkContract, '', False)
    sleep(1)
    print('* * * * CANCELING MARKET DATA * * * *')
    con.cancelMktData(tickId)
    sleep(1)
    con.disconnect()
    sleep(1)
    print('asdafas',a)


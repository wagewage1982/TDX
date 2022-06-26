#encoding:gbk

import pandas as pd
import numpy as np
import talib

def init(ContextInfo):
    ContextInfo.accountID = '420089000010'
    ContextInfo.accountType = 'STOCK_OPTION'
    ContextInfo.order = 1
    ContextInfo.set_commission(1, 0.0004)
    #ContextInfo.trade_code_list=['510300.SH']
    ContextInfo.trade_code_list=['10004307.SHO']
    ContextInfo.set_universe(ContextInfo.trade_code_list)
    ContextInfo.buyy = True
    ContextInfo.sell = True
    ContextInfo.last_macd={}
    ContextInfo.last_macd['L1_ON'] = 0
    ContextInfo.last_macd['H1_ON'] = 0
    ContextInfo.last_macd['L2_ON'] = 0
    ContextInfo.last_macd['H2_ON'] = 0
    ContextInfo.open_price = -1000.00
    ContextInfo.max_price = -1000.00
    ContextInfo.min_price = -1000.00
    
def handlebar(ContextInfo):
    #if not ContextInfo.is_last_bar():
    #    return
    dw = ContextInfo.get_market_data(['close'],count=100)
    dw['DIF'], dw['DEA'], dw['MACD'] = talib.MACD(np.array(dw['close']), fastperiod=12, slowperiod=26, signalperiod=9)
    #ContextInfo.paint("DEA",1.0*dw['DEA'][-1],-1,0,'yellow','noaxis')
    #ContextInfo.paint("DIF",1.0*dw['DIF'][-1],-1,0,'white','noaxis')
    #ContextInfo.paint("MACD",2.0*dw['MACD'][-1],-1,0,'yellow','noaxis')
    #x=call_vba('MACD.DIFF','510300.SH',ContextInfo)
    #print(dw['DIF'][-1],x)

    #交易策略
    #if not ContextInfo.is_last_bar():
    #    return
    ## MACD 底背离
    buyy_condition = 0
    ContextInfo.last_macd['L2_ON'] = 0
    if ContextInfo.last_macd['L1_ON'] == 0:
        if dw['MACD'][-3]>dw['MACD'][-2]<dw['MACD'][-1] and 2*dw['MACD'][-2]<-0.0030 and ContextInfo.buyy:
            ContextInfo.last_macd['L1_ON'] = 1
            #ContextInfo.last_macd['L2_ON'] = 0
            ContextInfo.last_macd['L1_MACD'] = dw['MACD'][-2]
            ContextInfo.last_macd['L1_DIF'] = dw['DIF'][-2]
            ContextInfo.last_macd['L1_DEA'] = dw['DEA'][-2]
            ContextInfo.last_macd['L1_CLOSE'] = dw['close'][-2]
            #print(dw.index[-2], '  S1:  L1:', ContextInfo.last_macd['L1_ON'], 'L2:', ContextInfo.last_macd['L2_ON'])
            #print(200*dw['MACD'][-3],200*dw['MACD'][-2],200*dw['MACD'][-1])
    elif ContextInfo.last_macd['L1_ON'] == 1:
        if dw['MACD'][-3]>0 and dw['MACD'][-2]>0 and dw['MACD'][-1]<0 and ContextInfo.buyy:
            ContextInfo.last_macd['L1_ON'] = 2
            #print(dw.index[-2], '  S2:  L1:', ContextInfo.last_macd['L1_ON'], 'L2:', ContextInfo.last_macd['L2_ON'])
    elif ContextInfo.last_macd['L1_ON'] == 2:
        if dw['MACD'][-3]>dw['MACD'][-2]<dw['MACD'][-1] and 2*dw['MACD'][-2]<-0.0008 and ContextInfo.buyy:
            ContextInfo.last_macd['L2_ON'] = 1
            ContextInfo.last_macd['L2_MACD'] = dw['MACD'][-2]
            ContextInfo.last_macd['L2_DIF'] = dw['DIF'][-2]
            ContextInfo.last_macd['L2_DEA'] = dw['DEA'][-2]
            ContextInfo.last_macd['L2_CLOSE'] = dw['close'][-2]
            if 2*dw['MACD'][-2]<-0.0030 and ContextInfo.buyy:
                ContextInfo.last_macd['L1_ON'] = 1
                ContextInfo.last_macd['L1_MACD'] = dw['MACD'][-2]
                ContextInfo.last_macd['L1_DIF'] = dw['DIF'][-2]
                ContextInfo.last_macd['L1_DEA'] = dw['DEA'][-2]
                ContextInfo.last_macd['L1_CLOSE'] = dw['close'][-2]
            else:
                ContextInfo.last_macd['L1_ON'] = 0
                if ContextInfo.last_macd['L2_ON'] == 1 and ContextInfo.last_macd['L2_CLOSE'] < ContextInfo.last_macd['L1_CLOSE']*0.999 and ContextInfo.last_macd['L2_MACD']*1.5 > ContextInfo.last_macd['L1_MACD']:
                    print(dw.index[-2], ' BUYY:  L1:', ContextInfo.last_macd['L1_ON'], 'L2:', ContextInfo.last_macd['L2_ON'])
                    buyy_condition = 1

    ## MACD 顶背离
    sell_condition = 0
    ContextInfo.last_macd['H2_ON'] = 0
    if ContextInfo.last_macd['H1_ON'] == 0:
        if dw['MACD'][-3]<dw['MACD'][-2]>dw['MACD'][-1] and 2*dw['MACD'][-2]>0.0030 and ContextInfo.sell:
            ContextInfo.last_macd['H1_ON'] = 1
            #ContextInfo.last_macd['H2_ON'] = 0
            ContextInfo.last_macd['H1_MACD'] = dw['MACD'][-2]
            ContextInfo.last_macd['H1_DIF'] = dw['DIF'][-2]
            ContextInfo.last_macd['H1_DEA'] = dw['DEA'][-2]
            ContextInfo.last_macd['H1_CLOSE'] = dw['close'][-2]
            #print(dw.index[-2], '  S1:  H1:', ContextInfo.last_macd['H1_ON'], 'H2:', ContextInfo.last_macd['H2_ON'])
            #print(200*dw['MACD'][-3],200*dw['MACD'][-2],200*dw['MACD'][-1])
    elif ContextInfo.last_macd['H1_ON'] == 1:
        if dw['MACD'][-3]<0 and dw['MACD'][-2]<0 and dw['MACD'][-1]>0 and ContextInfo.sell:
            ContextInfo.last_macd['H1_ON'] = 2
            #print(dw.index[-2], '  S2:  H1:', ContextInfo.last_macd['H1_ON'], 'H2:', ContextInfo.last_macd['H2_ON'])
    elif ContextInfo.last_macd['H1_ON'] == 2:
        if dw['MACD'][-3]<dw['MACD'][-2]>dw['MACD'][-1] and 2*dw['MACD'][-2]>0.0008 and ContextInfo.sell:
            ContextInfo.last_macd['H2_ON'] = 1
            ContextInfo.last_macd['H2_MACD'] = dw['MACD'][-2]
            ContextInfo.last_macd['H2_DIF'] = dw['DIF'][-2]
            ContextInfo.last_macd['H2_DEA'] = dw['DEA'][-2]
            ContextInfo.last_macd['H2_CLOSE'] = dw['close'][-2]
            if 2*dw['MACD'][-2]>0.0030 and ContextInfo.sell:
                ContextInfo.last_macd['H1_ON'] = 1
                ContextInfo.last_macd['H1_MACD'] = dw['MACD'][-2]
                ContextInfo.last_macd['H1_DIF'] = dw['DIF'][-2]
                ContextInfo.last_macd['H1_DEA'] = dw['DEA'][-2]
                ContextInfo.last_macd['H1_CLOSE'] = dw['close'][-2]
            else:
                ContextInfo.last_macd['H1_ON'] = 0
                if ContextInfo.last_macd['H2_ON'] == 1 and ContextInfo.last_macd['H2_CLOSE']*0.999 > ContextInfo.last_macd['H1_CLOSE'] and ContextInfo.last_macd['H2_MACD']*1.5 < ContextInfo.last_macd['H1_MACD']:
                    print(dw.index[-2], ' SELL:  H1:', ContextInfo.last_macd['H1_ON'], 'H2:', ContextInfo.last_macd['H2_ON'])
                    sell_condition = 1

    if buyy_condition:
        #ContextInfo.buyy = False
        #ContextInfo.sell = True
        for i in ContextInfo.trade_code_list:
            option_price = ContextInfo.get_full_tick([i])[i]['lastPrice']
            passorder(50, 1101, ContextInfo.accountID, i, 14, option_price+0.0001, ContextInfo.order, 'MACD', 1, '', ContextInfo)

            pass
    elif sell_condition:
        #ContextInfo.buyy = True
        #ContextInfo.sell = False
        for i in ContextInfo.trade_code_list:
            option_price = ContextInfo.get_full_tick([i])[i]['lastPrice']
            passorder(51, 1101, ContextInfo.accountID, i, 14, option_price-0.0001, ContextInfo.order, 'MACD', 1, '', ContextInfo)
            pass
            
    #可买或可卖状态
    ContextInfo.draw_text(bool(buyy_condition),float(1.0),'B') #绘制买点
    ContextInfo.draw_text(bool(sell_condition),float(1.0),'S') #绘制卖点
    #ContextInfo.paint('can_buyy',ContextInfo.buyy,-1,0,'nodraw')
    #ContextInfo.paint('can_sell',ContextInfo.sell,-1,0,'nodraw')











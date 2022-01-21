from config import Connect
from gecko import Gecko
from web3 import Web3
from db import Database
import requests
import json
import time
import sys
import subprocess
from datetime import datetime

class Main:
    def __init__(self):
        
        self.connection = Connect()
        self.db = Database()
        self.gecko = Gecko()
        self.connection.make_connection()
        bsc = "https://bsc-dataseed.binance.org/"
        self.web3 = Web3(Web3.HTTPProvider(bsc))
        #If your main.py process crashes with error, trade.py will continue on cycling through, make sure to close opened console
        subprocess.Popen('start /wait python trade.py', shell=True)
        self.menu()

    def menu(self):

        while True:

            balance = self.get_bnb_balance()
            wbnb_balance = self.get_wbnb_balance()
            print('//////////////////////////////////////////////')
            print('Current BNB balance : ',balance,' WBNB balance:',wbnb_balance,'\n')
            print('1.Create new trade 2.Show active trades 3.Change bsc address 4.quit\n')
            cmd = input('Choose comand to execute:')

            if cmd == '1':

                self.create_trade()
            
            elif cmd=='2':

                past = self.db.get_all_past_trades()
                present = self.db.get_all_trades()
                print('Currently active trades: ')
                for x in present:

                    contract = x[0]
                    amount = x[1]
                    method = x[2]
                    value = x[3]
                    id = x[4]
                    print('Name: ',id,';Contract: ',contract,';Amount(BNB): ',amount,';Method: ',method,';Value: ',value )

                print('Do you want to delete some trade?(write "0" to just exit this menu)')
                trade_num = input('number of trade to delete')
                if trade_num =='0':

                    pass

                else:

                    trade_num = int(trade_num) - 1
                    self.db.delete_trade(present[trade_num][0])
                    print('Delted trade!')

                print('Trades made in past:')
                for y in past:

                    print(y)
                    contract = y[0]
                    id = y[1]
                    ts = datetime.fromtimestamp(float(y[2]))
                    amount = y[3]
                    status = y[4]
                    method= y[5]
                    print('Name: ',id,';Contract: ',contract,';Amount(WBNB): ',amount,';Method: ',method,';Time: ',ts,';Status: ',status )

            elif cmd == '3':

                addr = input('New address: ')
                key = input('New private key')
                self.db.update_address(addr,key)

            else:

                sys.exit()

    def create_trade(self):

        sender_address = self.db.get_address()[0]
        trades_number = self.db.count_trades()[0][0]
        print('TRADES NUMBER:',trades_number)

        if trades_number>=3:

            print('Too many trades are active, pls close existing trades or w8 for them to finish')
            sys.exit()

        contract_addr = input('Contract of token to trade with: ').lower()

        try:

            coingecko_url = 'https://api.coingecko.com/api/v3/coins/binance-smart-chain/contract/'+contract_addr
            coin_info = requests.get(coingecko_url)

        except Exception as e:

            print(e)
            print("Couldn't get data from coingecko, pls try agian later...")
            sys.exit()

        coin_info = json.loads(coin_info.text)
        if 'error' in coin_info:

            print("Couldn't get data from coingecko, pls check contract address...")    
            sys.exit()

        name = coin_info['name']
        id = coin_info['id']
        bnb_price = coin_info['market_data']['current_price']['bnb']
        usd_price = coin_info['market_data']['current_price']['usd']
        print('Name: ',name,';Current price in bnb: ',bnb_price,';Current price in usd: ',usd_price,';\n')
        print('Pls choose how much wbnb to use in trade, current WBNB balance is:', self.get_wbnb_balance())
        trade_amount = input('WBNB amount to trade with: ')
        print('Choose which trade method to use:')
        trade_method = input('1. RSI less 2. RSI greater 3. Price less 4. Price greater')
        
        if trade_method == '1' or trade_method == '2':

            last_RSI = self.gecko.get_last_rsi(id,contract_addr)
            print('Current last RSI of 4 hours chart: ',last_RSI)
            trade_value = input('Choose RSI value(1-100): ')

        else:

            last_price = self.gecko.get_last_price(contract_addr)
            print('Current price of token in usd: ',last_price)
            trade_value = input('Choose a price value: ')

        self.db.store_trade(contract_addr,trade_amount,trade_method,trade_value,id)
        
        print('Trade added to db successfully! You can see active and past trades in "Active trades" menu.')
        time.sleep(3)
        

    def get_bnb_balance(self):

        balance = self.web3.eth.get_balance(self.db.get_address()[0])
        balance = self.web3.fromWei(balance,'ether')
        return balance

    def get_wbnb_balance(self):

        #wraped BNB abi
        wbnb_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'
        wbnb_contract = self.web3.eth.contract('0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c' , abi=wbnb_abi)
        wbnb_balance = self.web3.fromWei(wbnb_contract.functions.balanceOf(self.db.get_address()[0]).call(),'ether')
        return wbnb_balance
        
Main()
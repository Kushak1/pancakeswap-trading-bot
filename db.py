
import sqlite3

class Database:
    def __init__(self):
        self.db = sqlite3.connect('./server.db')
        self.sql = self.db.cursor()


        a = self.sql.execute(""" CREATE TABLE IF NOT EXISTS address (
            address TEXT,
            key TEXT,
            id INT
            )""")
        b = self.sql.execute(""" CREATE TABLE IF NOT EXISTS trades (
            contract TEXT,
            amount TEXT,
            method TEXT,    
            value TEXT,
            id TEXT
            )""")

        b = self.sql.execute(""" CREATE TABLE IF NOT EXISTS past_trades (
            contract TEXT,
            id TEXT,
            time TEXT,
            amount TEXT,
            status TEXT,
            method TEXT
            )""")
    def store_address(self,address, key):
        
        
        table = self.sql.execute("SELECT id FROM address WHERE id = 1")

        if table.fetchone() is None:
            q = "INSERT INTO address (address,key, id) VALUES (?,?,?);"
            result = self.sql.execute(q,(address,key, 1))
           

            self.db.commit()

        else:

            q = "UPDATE address SET address = ?, key = ? WHERE id = 1;"
            result = self.sql.execute(q,(address,key))

            
            self.db.commit()

        if result :


            return True
        else:
            
            return False
    def get_address(self):
        table = self.sql.execute("SELECT address FROM address WHERE id = 1")
        temp = table.fetchone()
        
        
        if temp is None:

            return False
        else:

            return temp

    def count_trades(self):
        q = "SELECT COUNT(*) FROM trades;"

        result = self.sql.execute(q)
        result = result.fetchall()
        
        return result
    def store_trade(self,contract_addr,trade_amount,trade_method,trade_value,name):
        q = "INSERT INTO trades (contract, amount, method, value, id) VALUES (?,?,?,?,?);"
        
        result = self.sql.execute(q,(contract_addr,trade_amount, trade_method, trade_value,name))
        


        self.db.commit()
        
        return result
    def get_user_data(self):
        table = self.sql.execute("SELECT address, key FROM address WHERE id = 1")
        temp = table.fetchone()
        
        
        if temp is None:

            return False
        else:

            return temp
    def get_all_trades(self):

        q = "SELECT * FROM trades"

        result = self.sql.execute(q)
        result = result.fetchall()
        
        return result
    def get_all_past_trades(self):

        q = "SELECT * FROM past_trades"

        result = self.sql.execute(q)
        result = result.fetchall()
        
        return result
    def delete_trade(self,contract):

        q = "DELETE FROM trades WHERE contract = ?;"
        result = self.sql.execute(q,(contract,))

        self.db.commit()
        return True
    def store_past_trades(self,contract_addr,id, time,trade_amount,tx_status,trade_method):
        q = "INSERT INTO past_trades (contract,id,time, amount, status, method) VALUES (?,?,?,?,?,?);"
        
        result = self.sql.execute(q,(contract_addr, id, time, trade_amount, tx_status, trade_method))
        


        self.db.commit()
        
        return result

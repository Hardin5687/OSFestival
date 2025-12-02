import sqlite3
import time

class Manager:
    def __init__(self, db_name='festival.db'):
        self.conn = sqlite3.connect(db_name )
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        #financial Metrics Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            price REAL,
            spectator_id TEXT,
            timestamp REAL
        )
        ''')
        #drug sales Metrics Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS drug_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug TEXT,,
            price REAL,
            dealer TEXT,
            spectator_id TEXT,
            timestamp REAL
        )
        ''')
        #Bathroom Usage Metrics Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS bathroom_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            spectator_id TEXT,
            wait_time REAL,
            timestamp REAL
        )
        ''')    
        #Security Metrics Table 
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS security_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            spectator_id TEXT,
            security_id TEXT,
            timestamp REAL
        )
        ''')
        #Cash Flow / Ticket Metrics Table
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS cash_flow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spectator_id TEXT,
            price REAL, 
            timestamp REAL
        )
        ''')
        self.conn.commit()

      #Function to log financial metrics
    def log_sale(self, item, price, spectator_id):
        self.cur.execute("INSERT INTO sales (item, price, spectator_id, timestamp) VALUES (?, ?, ?, ?)",
                         (item, price, spectator_id, time.time()))
        self.conn.commit()

    def log_drug_sale(self, drug, price, dealer, spectator_id):
        self.cur.execute("INSERT INTO drug_sales (drug, price, dealer, spectator_id, timestamp) VALUES (?, ?, ?, ?, ?)",
                         (drug, price, dealer, spectator_id, time.time()))
        self.conn.commit()

    def log_bathroom_wait(self, spectator_id, wait_time):
        self.cur.execute("INSERT INTO bathroom_usage (spectator_id, wait_time, timestamp) VALUES (?, ?, ?)",
                         (spectator_id, wait_time, time.time()))
        self.conn.commit()

    def log_security_event(self, event_type, spectator_id, guard_id):
        self.cur.execute("INSERT INTO security_events (event_type, spectator_id, guard_id, timestamp) VALUES (?, ?, ?, ?)",
                         (event_type, spectator_id, guard_id, time.time()))
        self.conn.commit()

    def log_ticket(self, spectator_id, price):
        self.cur.execute("INSERT INTO tickets (spectator_id, price, timestamp) VALUES (?, ?, ?)",
                         (spectator_id, price, time.time()))
        self.conn.commit()
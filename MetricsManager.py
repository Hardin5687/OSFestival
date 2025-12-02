import sqlite3
import time
import threading
import queue

class MetricsManager:
    def __init__(self, db_name='festival.db'):
        # Single writer connection
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_tables()

        # Queue for log jobs
        self.jobs = queue.Queue()

        # Start background writer thread
        self.writer_thread = threading.Thread(target=self.worker, daemon=True)
        self.writer_thread.start()

    def worker(self):
        """Writer thread that processes all DB writes sequentially."""
        while True:
            sql, values = self.jobs.get()
            try:
                self.cur.execute(sql, values)
                self.conn.commit()
            except Exception as e:
                print("DB ERROR:", e)
            self.jobs.task_done()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT,
                price REAL,
                spectator_id TEXT,
                timestamp REAL
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS drug_sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                drug TEXT,
                price REAL,
                dealer TEXT,
                spectator_id TEXT,
                timestamp REAL
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS bathroom_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spectator_id TEXT,
                wait_time REAL,
                timestamp REAL
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS security_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                spectator_id TEXT,
                guard_id TEXT,
                timestamp REAL
            )
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                spectator_id TEXT,
                price REAL,
                timestamp REAL
            )
        """)

        self.conn.commit()

    def log_sale(self, item, price, spectator_id):
        self.jobs.put((
            "INSERT INTO sales (item, price, spectator_id, timestamp) VALUES (?, ?, ?, ?)",
            (item, price, spectator_id, time.time())
        ))

    def log_drug_sale(self, drug, price, dealer, spectator_id):
        self.jobs.put((
            "INSERT INTO drug_sales (drug, price, dealer, spectator_id, timestamp) VALUES (?, ?, ?, ?, ?)",
            (drug, price, dealer, spectator_id, time.time())
        ))

    def log_bathroom_wait(self, spectator_id, wait_time):
        self.jobs.put((
            "INSERT INTO bathroom_usage (spectator_id, wait_time, timestamp) VALUES (?, ?, ?)",
            (spectator_id, wait_time, time.time())
        ))

    def log_security_event(self, event_type, spectator_id, guard_id):
        self.jobs.put((
            "INSERT INTO security_events (event_type, spectator_id, guard_id, timestamp) VALUES (?, ?, ?, ?)",
            (event_type, spectator_id, guard_id, time.time())
        ))

    def log_ticket(self, spectator_id, price):
        self.jobs.put((
            "INSERT INTO tickets (spectator_id, price, timestamp) VALUES (?, ?, ?)",
            (spectator_id, price, time.time())
        ))

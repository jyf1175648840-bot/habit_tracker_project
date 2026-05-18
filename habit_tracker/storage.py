import sqlite3
from datetime import datetime
from typing import List
from .models import Habit

DB_PATH = "habits.db"

class SQLiteStorage:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DB_PATH
        self._init_db()
    
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    periodicity TEXT NOT NULL,
                    creation_date TEXT NOT NULL,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completion_time TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits(id)
                )
            ''')
    
    def save_habit(self, habit: Habit) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if habit.id is None:
                cursor.execute('''
                    INSERT INTO habits (name, description, periodicity, creation_date,
                                      current_streak, longest_streak)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (habit.name, habit.description, habit.periodicity,
                      habit.creation_date.isoformat(), habit.current_streak,
                      habit.longest_streak))
                habit_id = cursor.lastrowid
            else:
                cursor.execute('''
                    UPDATE habits 
                    SET name=?, description=?, periodicity=?, creation_date=?,
                        current_streak=?, longest_streak=?
                    WHERE id=?
                ''', (habit.name, habit.description, habit.periodicity,
                      habit.creation_date.isoformat(), habit.current_streak,
                      habit.longest_streak, habit.id))
                habit_id = habit.id
            cursor.execute('DELETE FROM completions WHERE habit_id = ?', (habit_id,))
            for completion in habit.completions:
                cursor.execute('''
                    INSERT INTO completions (habit_id, completion_time)
                    VALUES (?, ?)
                ''', (habit_id, completion.isoformat()))
            return habit_id
    
    def load_habits(self) -> List[Habit]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM habits')
            habits = []
            for row in cursor.fetchall():
                habit = Habit(
                    id=row[0], name=row[1], description=row[2],
                    periodicity=row[3], creation_date=datetime.fromisoformat(row[4]),
                    current_streak=row[5], longest_streak=row[6]
                )
                cursor.execute('SELECT completion_time FROM completions WHERE habit_id = ? ORDER BY completion_time', (habit.id,))
                completions = cursor.fetchall()
                habit.completions = [datetime.fromisoformat(c[0]) for c in completions]
                if habit.completions:
                    habit.last_completion = habit.completions[-1]
                habits.append(habit)
            return habits

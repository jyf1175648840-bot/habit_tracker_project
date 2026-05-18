import unittest
from datetime import datetime, timedelta
from habit_tracker.models import Habit

class TestHabit(unittest.TestCase):
    def setUp(self):
        self.daily_habit = Habit(name="Test Daily", periodicity="daily")
        self.weekly_habit = Habit(name="Test Weekly", periodicity="weekly")
    
    def test_mark_complete_daily(self):
        today = datetime.now()
        self.assertTrue(self.daily_habit.mark_complete(today))
        self.assertFalse(self.daily_habit.mark_complete(today))
    
    def test_streak_calculation_daily(self):
        base = datetime(2026, 5, 1)
        for i in range(3):
            self.daily_habit.mark_complete(base + timedelta(days=i))
        self.assertEqual(self.daily_habit.current_streak, 3)
        # skip a day
        self.daily_habit.mark_complete(base + timedelta(days=5))
        self.assertEqual(self.daily_habit.current_streak, 1)
    
    def test_streak_calculation_weekly(self):
        base = datetime(2026, 5, 3)  # Sunday
        for i in range(3):
            self.weekly_habit.mark_complete(base + timedelta(weeks=i))
        self.assertEqual(self.weekly_habit.current_streak, 3)
    
    def test_broken_habit(self):
        old_habit = Habit(creation_date=datetime.now() - timedelta(days=2))
        self.assertTrue(old_habit.check_if_broken())
        self.daily_habit.mark_complete()
        self.assertFalse(self.daily_habit.check_if_broken())

if __name__ == "__main__":
    unittest.main()

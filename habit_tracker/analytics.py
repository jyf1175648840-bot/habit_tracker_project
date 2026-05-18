from typing import List, Dict, Any
from .models import Habit

def get_total_habits(habits: List[Habit]) -> int:
    return len(habits)

def get_habits_by_periodicity(habits: List[Habit], period: str) -> List[Habit]:
    return list(filter(lambda h: h.periodicity == period, habits))

def get_broken_habits(habits: List[Habit]) -> List[Habit]:
    return list(filter(lambda h: h.check_if_broken(), habits))

def get_longest_streak_all(habits: List[Habit]) -> Dict[str, Any]:
    if not habits:
        return {"name": None, "streak": 0}
    best = max(habits, key=lambda h: h.longest_streak)
    return {"name": best.name, "streak": best.longest_streak}

def get_streak_ranking(habits: List[Habit], top_n: int = 5) -> List[Dict]:
    sorted_habits = sorted(habits, key=lambda h: h.current_streak, reverse=True)
    return [{"name": h.name, "streak": h.current_streak} for h in sorted_habits[:top_n] if h.current_streak > 0]

def get_total_completions(habits: List[Habit]) -> int:
    return sum(map(lambda h: len(h.completions), habits))

def get_habit_stats(habits: List[Habit]) -> Dict:
    return {
        "total_habits": get_total_habits(habits),
        "daily_habits": len(get_habits_by_periodicity(habits, Habit.DAILY)),
        "weekly_habits": len(get_habits_by_periodicity(habits, Habit.WEEKLY)),
        "broken_habits": len(get_broken_habits(habits)),
        "total_completions": get_total_completions(habits),
        "best_streak": get_longest_streak_all(habits),
        "streak_ranking": get_streak_ranking(habits),
    }

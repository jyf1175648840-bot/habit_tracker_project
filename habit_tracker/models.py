from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional

@dataclass
class Habit:
    DAILY = "daily"
    WEEKLY = "weekly"
    
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    periodicity: str = DAILY
    creation_date: datetime = field(default_factory=datetime.now)
    current_streak: int = 0
    longest_streak: int = 0
    completions: List[datetime] = field(default_factory=list)
    last_completion: Optional[datetime] = None
    
    def __post_init__(self):
        if self.periodicity not in [self.DAILY, self.WEEKLY]:
            raise ValueError(f"period must be '{self.DAILY}' or '{self.WEEKLY}'")
    
    def mark_complete(self, completion_time: Optional[datetime] = None) -> bool:
        completion_time = completion_time or datetime.now()
        for comp in self.completions:
            if self._same_period(comp, completion_time):
                return False
        self.completions.append(completion_time)
        self.last_completion = completion_time
        self.current_streak = self.calculate_streak()
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak
        return True
    
    def calculate_streak(self) -> int:
        if not self.completions:
            return 0
        completions = sorted(self.completions)
        streak = 1
        for i in range(len(completions)-1, 0, -1):
            if self._are_consecutive(completions[i], completions[i-1]):
                streak += 1
            else:
                break
        return streak
    
    def check_if_broken(self) -> bool:
        if not self.completions:
            next_deadline = self._get_next_period_end(self.creation_date)
            return datetime.now() > next_deadline
        last_completion = self.completions[-1]
        period_end = self._get_next_period_end(last_completion)
        return datetime.now() > period_end
    
    def _same_period(self, time1: datetime, time2: datetime) -> bool:
        if self.periodicity == self.DAILY:
            return time1.date() == time2.date()
        else:
            return time1.isocalendar()[:2] == time2.isocalendar()[:2]
    
    def _are_consecutive(self, later: datetime, earlier: datetime) -> bool:
        if self.periodicity == self.DAILY:
            return (later.date() - earlier.date()).days == 1
        else:
            y1, w1 = earlier.isocalendar()[:2]
            y2, w2 = later.isocalendar()[:2]
            week_diff = (y2 - y1) * 52 + (w2 - w1)
            return week_diff == 1
    
    def _get_next_period_end(self, start_time: datetime) -> datetime:
        if self.periodicity == self.DAILY:
            next_day = start_time.date() + timedelta(days=1)
            return datetime.combine(next_day, datetime.min.time())
        else:
            days_until_sunday = 6 - start_time.weekday()
            next_sunday = start_time + timedelta(days=days_until_sunday)
            return datetime.combine(next_sunday.date(), datetime.max.time())

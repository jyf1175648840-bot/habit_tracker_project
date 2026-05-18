import click
import json
import csv
import os
import sqlite3
from datetime import datetime, timedelta
from .storage import SQLiteStorage
from .models import Habit
from . import analytics

@click.group()
def cli():
    pass

@cli.command()
@click.option('--name', required=True, help='Habit name')
@click.option('--description', default='', help='Habit description')
@click.option('--periodicity', type=click.Choice(['daily', 'weekly']), required=True, help='daily or weekly')
def create(name, description, periodicity):
    """Create a new habit"""
    storage = SQLiteStorage()
    habits = storage.load_habits()
    if any(h.name == name for h in habits):
        click.echo(f"Error: Habit '{name}' already exists")
        return
    habit = Habit(name=name, description=description, periodicity=periodicity)
    habit_id = storage.save_habit(habit)
    click.echo(f"Habit '{name}' created successfully! ID: {habit_id}")

@cli.command()
@click.option('--name', required=True, help='Habit name')
def complete(name):
    """Mark a habit as completed"""
    storage = SQLiteStorage()
    habits = storage.load_habits()
    habit = next((h for h in habits if h.name == name), None)
    if not habit:
        click.echo(f"Error: Habit '{name}' not found")
        return
    if habit.mark_complete():
        storage.save_habit(habit)
        click.echo(f"Habit '{name}' completed!")
        click.echo(f"Current streak: {habit.current_streak}")
        click.echo(f"Longest streak: {habit.longest_streak}")
    else:
        click.echo(f"Habit '{name}' already completed in this period")

@cli.command()
def list_habits():
    """List all habits with status"""
    storage = SQLiteStorage()
    habits = storage.load_habits()
    if not habits:
        click.echo("No habits yet.")
        return
    click.echo("\n" + "="*60)
    click.echo("Your habits:")
    click.echo("="*60)
    for h in habits:
        status = "✅" if not h.check_if_broken() else "❌"
        click.echo(f"{status} {h.name} ({h.periodicity})")
        click.echo(f"   Description: {h.description or 'None'}")
        click.echo(f"   Current streak: {h.current_streak}")
        click.echo(f"   Longest streak: {h.longest_streak}")
        click.echo(f"   Total completions: {len(h.completions)}")
        if h.completions:
            last = h.completions[-1].strftime("%Y-%m-%d %H:%M")
            click.echo(f"   Last completion: {last}")
        click.echo()

@cli.command()
def stats():
    """Show habit statistics"""
    storage = SQLiteStorage()
    habits = storage.load_habits()
    stats_data = analytics.get_habit_stats(habits)
    click.echo("\n📊 Habit Statistics")
    click.echo("="*40)
    click.echo(f"Total habits: {stats_data['total_habits']}")
    click.echo(f"Daily habits: {stats_data['daily_habits']}")
    click.echo(f"Weekly habits: {stats_data['weekly_habits']}")
    click.echo(f"Broken habits: {stats_data['broken_habits']}")
    click.echo(f"Total completions: {stats_data['total_completions']}")
    if stats_data['best_streak']['name']:
        click.echo(f"\n🏆 Best streak: {stats_data['best_streak']['name']} ({stats_data['best_streak']['streak']} days)")
    click.echo("\n📈 Streak ranking:")
    for i, item in enumerate(stats_data['streak_ranking'], 1):
        click.echo(f"  {i}. {item['name']}: {item['streak']} days")

@cli.command()
@click.option('--name', required=True, help='Name of habit to delete')
def delete(name):
    """Delete a habit and all its completion records"""
    storage = SQLiteStorage()
    conn = sqlite3.connect(storage.db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM habits WHERE name = ?', (name,))
    result = cursor.fetchone()
    if not result:
        click.echo(f"Error: Habit '{name}' not found")
        conn.close()
        return
    habit_id = result[0]
    cursor.execute('DELETE FROM completions WHERE habit_id = ?', (habit_id,))
    cursor.execute('DELETE FROM habits WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()
    click.echo(f"Habit '{name}' deleted successfully")

@cli.command()
@click.option('--format', type=click.Choice(['json', 'csv']), default='json', help='Export format')
@click.option('--output', default='habits_export.json', help='Output filename')
def export(format, output):
    """Export habit data to JSON or CSV"""
    storage = SQLiteStorage()
    habits = storage.load_habits()
    if format == 'json':
        data = []
        for habit in habits:
            habit_dict = {
                'name': habit.name,
                'description': habit.description,
                'periodicity': habit.periodicity,
                'creation_date': habit.creation_date.isoformat(),
                'current_streak': habit.current_streak,
                'longest_streak': habit.longest_streak,
                'completions': [c.isoformat() for c in habit.completions]
            }
            data.append(habit_dict)
        with open(output, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        click.echo(f"Data exported to {output}")
    elif format == 'csv':
        with open(output, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'description', 'periodicity', 'creation_date', 'current_streak', 'longest_streak', 'completion_count'])
            for habit in habits:
                writer.writerow([
                    habit.name,
                    habit.description,
                    habit.periodicity,
                    habit.creation_date.strftime('%Y-%m-%d'),
                    habit.current_streak,
                    habit.longest_streak,
                    len(habit.completions)
                ])
        click.echo(f"Data exported to {output}")

@cli.command()
def reminders():
    """Show habits that are about to become broken"""
    storage = SQLiteStorage()
    habits = storage.load_habits()
    now = datetime.now()
    upcoming = []
    for habit in habits:
        if habit.completions:
            deadline = habit._get_next_period_end(habit.completions[-1])
            time_left = deadline - now
            if 0 <= time_left.total_seconds() <= 7 * 24 * 3600:
                upcoming.append((habit, deadline, time_left))
    if not upcoming:
        click.echo("🎉 No upcoming deadlines! Great job!")
        return
    click.echo("\n⏰ Upcoming deadlines:")
    upcoming.sort(key=lambda x: x[2])
    for habit, deadline, time_left in upcoming:
        days = time_left.days
        hours = time_left.seconds // 3600
        if days > 0:
            time_str = f"{days} days left"
        elif hours > 0:
            time_str = f"{hours} hours left"
        else:
            time_str = "Due soon!"
        click.echo(f"📌 {habit.name} ({habit.periodicity}) - {time_str} (deadline: {deadline.strftime('%Y-%m-%d %H:%M')})")

@cli.command()
def demo():
    """Create demo habits with sample data"""
    storage = SQLiteStorage()
    demo_habits = [
        Habit(name="Morning meditation", description="10 min daily", periodicity="daily"),
        Habit(name="Evening journal", description="Write before sleep", periodicity="daily"),
        Habit(name="Weekly planning", description="Plan next week", periodicity="weekly"),
        Habit(name="Exercise", description="Workout 3x per week", periodicity="weekly"),
        Habit(name="Reading", description="30 min reading", periodicity="daily"),
    ]
    for habit in demo_habits:
        # Add some dummy completions (last 5 periods)
        for i in range(5):
            days_ago = (4 - i) * 2 if habit.periodicity == "weekly" else (4 - i)
            completion_time = datetime.now() - __import__('datetime').timedelta(days=days_ago)
            habit.mark_complete(completion_time)
        storage.save_habit(habit)
        click.echo(f"Created demo habit: {habit.name}")
    click.echo("\nDemo data created! Use 'list-habits' and 'stats' to explore.")

@cli.command()
def init():
    """Initialize the database (create tables)"""
    storage = SQLiteStorage()
    click.echo(f"Database initialized at {storage.db_path}")
    click.echo("Use 'create' to add habits or 'demo' to try sample data.")

@cli.command()
def reset():
    """Delete the database and reinitialize"""
    storage = SQLiteStorage()
    if os.path.exists(storage.db_path):
        os.remove(storage.db_path)
    storage._init_db()
    click.echo("All data has been reset.")

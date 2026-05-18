@cli.command()
def demo():
    """Create demo data"""
    storage = SQLiteStorage()
    
    demo_habits = [
        Habit(name="Morning meditation", description="Meditate for 10 minutes daily", periodicity="daily"),
        Habit(name="Evening journal", description="Write journal before sleep", periodicity="daily"),
        Habit(name="Weekly planning", description="Plan next week every Sunday", periodicity="weekly"),
        Habit(name="Exercise", description="Workout 3 times per week", periodicity="weekly"),
        Habit(name="Reading", description="Read for 30 minutes daily", periodicity="daily"),
    ]
    
    for habit in demo_habits:
        # Add some completion records
        for i in range(5):
            days_ago = (4 - i) * 2 if habit.periodicity == "weekly" else (4 - i)
            completion_time = datetime.now() - timedelta(days=days_ago)
            habit.mark_complete(completion_time)
        
        storage.save_habit(habit)
        click.echo(f"Created demo habit: {habit.name}")
    
    click.echo("\nDemo data created!")
    click.echo("Use 'list-habits' command to view all habits")
    click.echo("Use 'stats' command to view statistics")

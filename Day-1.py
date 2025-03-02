import json
import os
import datetime
import matplotlib.pyplot as plt
from collections import defaultdict

class HabitTracker:
    def __init__(self, data_file="habits.json"):
        self.data_file = data_file
        self.habits = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    self.habits = json.load(f)
            except json.JSONDecodeError:
                print("Error loading data file. Starting with empty data.")
                self.habits = {}
        else:
            self.habits = {}

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.habits, f, indent=4)

    def add_habit(self, habit_name, description=""):
        if habit_name not in self.habits:
            self.habits[habit_name] = {
                "description": description,
                "created_date": datetime.datetime.now().strftime("%Y-%m-%d"),
                "tracking": {}
            }
            self.save_data()
            print(f"Habit '{habit_name}' added successfully.")
        else:
            print(f"Habit '{habit_name}' already exists.")

    def remove_habit(self, habit_name):
        if habit_name in self.habits:
            del self.habits[habit_name]
            self.save_data()
            print(f"Habit '{habit_name}' removed successfully.")
        else:
            print(f"Habit '{habit_name}' does not exist.")

    def list_habits(self):
        if not self.habits:
            print("No habits found. Add some habits to track!")
            return

        print("\nYour Habits:")
        print("-" * 40)
        for name, data in self.habits.items():
            desc = data["description"]
            created = data["created_date"]
            completion_count = len(data["tracking"])
            print(f"• {name}")
            if desc:
                print(f"  Description: {desc}")
            print(f"  Created on: {created}")
            print(f"  Tracked {completion_count} times")
            print("-" * 40)

    def track_habit(self, habit_name, date=None, completed=True, notes=""):
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")

        if habit_name in self.habits:
            self.habits[habit_name]["tracking"][date] = {
                "completed": completed,
                "notes": notes,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.save_data()
            status = "completed" if completed else "not completed"
            print(f"Habit '{habit_name}' marked as {status} for {date}.")
        else:
            print(f"Habit '{habit_name}' does not exist.")

    def get_habit_stats(self, habit_name):
        if habit_name not in self.habits:
            print(f"Habit '{habit_name}' does not exist.")
            return None

        habit = self.habits[habit_name]
        total_days = len(habit["tracking"])
        completed_days = sum(1 for day in habit["tracking"].values() if day["completed"])
        completion_rate = 0 if total_days == 0 else (completed_days / total_days) * 100

        return {
            "name": habit_name,
            "description": habit["description"],
            "created_date": habit["created_date"],
            "total_days_tracked": total_days,
            "completed_days": completed_days,
            "completion_rate": completion_rate
        }

    def print_habit_stats(self, habit_name):
        stats = self.get_habit_stats(habit_name)
        if stats:
            print(f"\nStatistics for '{stats['name']}':")
            print("-" * 40)
            print(f"Description: {stats['description']}")
            print(f"Created on: {stats['created_date']}")
            print(f"Days tracked: {stats['total_days_tracked']}")
            print(f"Days completed: {stats['completed_days']}")
            print(f"Completion rate: {stats['completion_rate']:.2f}%")

    def plot_habit(self, habit_name):
        if habit_name not in self.habits:
            print(f"Habit '{habit_name}' does not exist.")
            return

        habit = self.habits[habit_name]
        tracking_data = habit["tracking"]

        if not tracking_data:
            print(f"No tracking data available for '{habit_name}'.")
            return

        dates = sorted(tracking_data.keys())
        completions = [1 if tracking_data[date]["completed"] else 0 for date in dates]
        dates_dt = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in dates]

        plt.figure(figsize=(10, 6))
        plt.plot(dates_dt, completions, 'o-', markersize=8)
        plt.yticks([0, 1], ['Not Done', 'Done'])
        plt.title(f"Habit Tracking: {habit_name}")
        plt.xlabel("Date")
        plt.ylabel("Completion Status")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()

    def plot_all_habits(self):
        if not self.habits:
            print("No habits found. Add some habits to track!")
            return

        habit_completion = defaultdict(list)
        all_dates = set()

        for habit_name, data in self.habits.items():
            for date, tracking in data["tracking"].items():
                habit_completion[habit_name].append((date, 1 if tracking["completed"] else 0))
                all_dates.add(date)

        if not all_dates:
            print("No tracking data available for any habit.")
            return

        all_dates = sorted(all_dates)
        dates_dt = [datetime.datetime.strptime(date, "%Y-%m-%d") for date in all_dates]

        plt.figure(figsize=(12, 6))

        for i, (habit_name, completions) in enumerate(habit_completion.items()):
            habit_data = {date: status for date, status in completions}
            y_values = []
            for date in all_dates:
                if date in habit_data:
                    y_values.append(habit_data[date] + 0.1*i)  # Offset for visibility
                else:
                    y_values.append(0)

            plt.plot(dates_dt, y_values, 'o-', label=habit_name, markersize=6)

        plt.title("All Habits Tracking")
        plt.xlabel("Date")
        plt.ylabel("Completion Status")
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(loc='best')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.show()

    def plot_completion_rates(self):
        if not self.habits:
            print("No habits found. Add some habits to track!")
            return

        habits = []
        rates = []

        for name in self.habits:
            stats = self.get_habit_stats(name)
            if stats and stats["total_days_tracked"] > 0:
                habits.append(name)
                rates.append(stats["completion_rate"])

        if not habits:
            print("No tracking data available for any habit.")
            return

        plt.figure(figsize=(10, 6))
        bars = plt.bar(habits, rates, color='skyblue')

        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.1f}%',
                     ha='center', va='bottom')

        plt.title("Completion Rates for All Habits")
        plt.xlabel("Habit")
        plt.ylabel("Completion Rate (%)")
        plt.ylim(0, 105)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45)

        plt.tight_layout()
        plt.show()

def main():
    tracker = HabitTracker()

    while True:
        print("\n===== Habit Tracker =====")
        print("1. Add a new habit")
        print("2. Remove a habit")
        print("3. List all habits")
        print("4. Track a habit")
        print("5. View habit statistics")
        print("6. Plot habit progress")
        print("7. Plot all habits")
        print("8. Plot completion rates")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            name = input("Enter habit name: ")
            desc = input("Enter description (optional): ")
            tracker.add_habit(name, desc)

        elif choice == "2":
            name = input("Enter habit name to remove: ")
            tracker.remove_habit(name)

        elif choice == "3":
            tracker.list_habits()

        elif choice == "4":
            name = input("Enter habit name: ")
            date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
            date = date if date else None
            completed_input = input("Completed? (y/n): ").lower()
            completed = completed_input.startswith('y')
            notes = input("Enter any notes (optional): ")
            tracker.track_habit(name, date, completed, notes)

        elif choice == "5":
            name = input("Enter habit name: ")
            tracker.print_habit_stats(name)

        elif choice == "6":
            name = input("Enter habit name: ")
            tracker.plot_habit(name)

        elif choice == "7":
            tracker.plot_all_habits()

        elif choice == "8":
            tracker.plot_completion_rates()

        elif choice == "0":
            print("Thank you for using Habit Tracker. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

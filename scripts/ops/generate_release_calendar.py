import csv
import datetime
import random
import argparse
from pathlib import Path

# Configuration
MAX_ARTICLES_PER_DAY = 4
TIME_SLOTS = [
    (8, 0), (9, 30),  # Morning
    (12, 0), (13, 30), # Lunch
    (17, 0), (19, 0),  # Evening
    (21, 0), (23, 0)   # Night
]

def generate_calendar(site_name, start_date_str, num_articles):
    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    current_date = start_date
    articles_scheduled = 0

    output_rows = []

    while articles_scheduled < num_articles:
        # Determine how many articles for this day (randomly 3 or 4 to vary, but max 4)
        # Actually rule says "Max 4". Let's aim for 4 to clear backlog, but sometimes 3.
        daily_count = random.choices([3, 4], weights=[0.2, 0.8])[0]
        if articles_scheduled + daily_count > num_articles:
            daily_count = num_articles - articles_scheduled

        # Select time slots
        daily_slots = random.sample(TIME_SLOTS, daily_count)
        daily_slots.sort()

        for slot_idx, (hour, minute) in enumerate(daily_slots):
            # Add jitter (minute variation)
            jitter = random.randint(-15, 15)
            slot_time = datetime.time(hour, max(0, min(59, minute + jitter)))

            article_id = f"{site_name}-{articles_scheduled + 1:04d}"

            output_rows.append({
                "Date": current_date,
                "Time": slot_time.strftime("%H:%M"),
                "Slot": slot_idx + 1,
                "Article_ID": article_id,
                "Status": "Scheduled"
            })

            articles_scheduled += 1

        current_date += datetime.timedelta(days=1)

    # Write to CSV
    output_path = Path(f"sites/{site_name}/release_plan.csv")
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Date", "Time", "Slot", "Article_ID", "Status"])
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"Generated calendar for {num_articles} articles starting {start_date_str}")
    print(f"Output: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate a release calendar.")
    parser.add_argument("site", help="Site name (e.g., site01)")
    parser.add_argument("start_date", help="YYYY-MM-DD")
    parser.add_argument("count", type=int, help="Number of articles to schedule")

    args = parser.parse_args()
    generate_calendar(args.site, args.start_date, args.count)

if __name__ == "__main__":
    main()

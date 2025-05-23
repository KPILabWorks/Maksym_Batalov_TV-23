import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pytz
import re

URL = "https://kyiv.digital/storage/air-alert/stats.html"
UA_TZ = pytz.timezone("Europe/Kiev")

time_re = re.compile(r"(\d{2}):(\d{2})\s+(\d{2})\.(\d{2})\.(\d{2})")
duration_re = re.compile(r"(?:(\d+)\s*годин[аиу]?)?\s*(?:(\d+)\s*хвилин[аиу]?)?")

response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")
rows = soup.find_all("tr")

records = []
for row in reversed(rows):
    cols = row.find_all("td")
    if len(cols) < 2:
        continue
    time_str = cols[0].text.strip()
    status = cols[1].text.strip()
    duration_text = cols[2].text.strip() if len(cols) > 2 else ""
    match = time_re.search(time_str)
    if not match:
        continue
    hour, minute, day, month, year = map(int, match.groups())
    year += 2000
    timestamp = UA_TZ.localize(datetime(year, month, day, hour, minute))
    records.append({
        "timestamp": timestamp,
        "status": status,
        "duration_text": duration_text
    })

alerts = []
pending_start = None

for rec in records:
    if "🔴" in rec["status"]:
        pending_start = rec["timestamp"]
    elif "🟢" in rec["status"] and pending_start:
        dur_match = duration_re.search(rec["duration_text"].replace("\xa0", " "))
        if dur_match:
            hours = int(dur_match.group(1)) if dur_match.group(1) else 0
            minutes = int(dur_match.group(2)) if dur_match.group(2) else 0
            duration = hours * 60 + minutes  # duration in minutes
        else:
            duration_td = rec["timestamp"] - pending_start
            duration = int(duration_td.total_seconds() // 60)  # duration in minutes
        start_date = pending_start.date()
        weekday = start_date.isoweekday()
        is_weekend = 1 if weekday in (6, 7) else 0
        day_of_year = start_date.timetuple().tm_yday
        # Determine season: 1=autumn, 2=winter, 3=spring, 4=summer
        month = start_date.month
        if month in (9, 10, 11):
            season = 1  # autumn
        elif month in (12, 1, 2):
            season = 2  # winter
        elif month in (3, 4, 5):
            season = 3  # spring
        else:
            season = 4  # summer
        if duration < 30:
            alert_duration_category = 1
        elif duration <= 90:
            alert_duration_category = 2
        else:
            alert_duration_category = 3
        alerts.append({
            "start": pending_start.strftime("%H:%M"),
            "end": rec["timestamp"].strftime("%H:%M"),
            "date": start_date,
            "duration": duration,
            "weekday": weekday,
            "is_weekend": is_weekend,
            "day_of_year": day_of_year,
            "alert_duration_category": alert_duration_category,
            "season": season,
        })
        pending_start = None

# Save to CSV
df = pd.DataFrame(alerts)
df.to_csv("air_alerts.csv", index=False)
print("Saved to air_alerts.csv")

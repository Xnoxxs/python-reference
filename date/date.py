
from datetime import datetime, timedelta

# Add one more day to a date
date = datetime.now()
new_date = date + timedelta(days=1)

print(new_date)
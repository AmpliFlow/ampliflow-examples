
import json
import requests
from datetime import datetime
import collections

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("MAILERLITE_API_KEY")

# Base URL for the MailerLite API v2
BASE_URL = 'https://api.mailerlite.com/api/v2'

# Headers for authentication
headers = {
    'Content-Type': 'application/json',
    'X-MailerLite-ApiKey': api_key
}

def get_subscriber_counts_by_month(group_id):
    url = f'{BASE_URL}/groups/{group_id}/subscribers'
    params = {
        'limit': 1000,  # Adjust as needed (MailerLite allows up to 1000)
        'page': 1
    }
    subscribers = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        if not data:
            break
        
        subscribers.extend(data)
        
        if len(data) < params['limit']:
            break
        else:
            params['page'] += 1

    # Count subscribers by month
    counts_by_month = collections.Counter()
    
    for subscriber in subscribers:
        date_subscribed = subscriber['date_subscribe']
        # Convert to datetime object
        date_obj = datetime.strptime(date_subscribed, '%Y-%m-%d %H:%M:%S')
        # Format as Year-Month
        month_str = date_obj.strftime('%Y-%m')
        counts_by_month[month_str] += 1

    return counts_by_month

group_id = 107336803539748582

counts_by_month = get_subscriber_counts_by_month(group_id)

print("Subscriber counts by month:")
counts_as_json = json.dumps(counts_by_month)
print(counts_as_json)
# Print the counts sorted by month
for month in sorted(counts_by_month.keys()):
    print(f"{month}: {counts_by_month[month]} subscribers")


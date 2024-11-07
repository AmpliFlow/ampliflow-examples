import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
username = os.environ.get("WINT_USERNAME")
password = os.environ.get("WINT_PASSWORD")

def get_monthly_revenue_report(start_year, start_month, end_year, end_month):
    """
    Fetches the monthly result report for the specified start and end month,
    and returns a JSON object with entries for each month, showing the revenue amount for each.
    """
    # Base URL for the API endpoint
    base_url = 'https://superkollapi.wint.se/api/FinancialReports/MonthlyResultReport'

    # Prepare the request payload
    payload = {
        'startMonth': {
            'year': start_year,
            'month': start_month
        },
        'endMonth': {
            'year': end_year,
            'month': end_month
        }
    }

    # Make the POST request with basic authentication
    response = requests.post(
        base_url,
        json=payload,
        auth=(username, password),
        headers={'accept': 'application/json'}
    )

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Initialize the results list
        values = []

        # Extract the revenue row
        rows = data.get('Rows', [])

        for row in rows:
            if row.get('Id') == 'Revenue':
                columns = row.get('Columns', [])

                # Initialize the current date
                current_date = datetime(start_year, start_month, 1)

                for column in columns:
                    amount = abs(column.get('Amount', 0.0))  # Convert to positive

                    # Format the date as the first day of the month in ISO format
                    date_str = current_date.strftime('%Y-%m-%dT00:00:00.000Z')

                    # Append to the list
                    values.append({
                        'date': date_str,
                        'value': round(amount / 1000)
                    })

                    # Move to the next month
                    if current_date.month == 12:
                        current_date = datetime(current_date.year + 1, 1, 1)
                    else:
                        current_date = current_date.replace(month=current_date.month + 1)

        return {'values': values}
    else:
        # Handle errors
        print(f'Error: API request failed with status code {response.status_code}')
        print(f'Response: {response.text}')
        return None
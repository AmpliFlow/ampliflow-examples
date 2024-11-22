import os
import sys
import json
import requests
from datetime import datetime
import collections
import logging
from dotenv import load_dotenv

load_dotenv()

mailerlite_api_key = os.environ.get("MAILERLITE_API_KEY")
mailerlite_group_id = os.environ.get("MAILERLITE_GROUP_ID")

af_base_url = os.environ.get("AF_BASE_URL")
af_api_key = os.environ.get("AF_API_KEY")


if not all([mailerlite_api_key, af_base_url, af_api_key]):
    print("Missing required environment variables. Please ensure MAILERLITE_API_KEY, AF_BASE_URL, and AF_API_KEY are set.")
    sys.exit(1)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

# MailerLite API Base URL and headers
MAILER_BASE_URL = 'https://api.mailerlite.com/api/v2'
mail_headers = {
    'Content-Type': 'application/json',
    'X-MailerLite-ApiKey': mailerlite_api_key
}

def get_subscriber_counts_by_month(group_id):
    url = f'{MAILER_BASE_URL}/groups/{group_id}/subscribers'
    params = {
        'limit': 1000,  # MailerLite allows up to 1000
        'page': 1
    }
    subscribers = []

    while True:
        response = requests.get(url, headers=mail_headers, params=params)
        if response.status_code != 200:
            logging.error(f"Failed to get subscribers: {response.status_code}")
            logging.error('Response: %s', response.text)
            sys.exit(1)
        data = response.json()

        if not data:
            break

        subscribers.extend(data)

        if len(data) < params['limit']:
            break
        else:
            params['page'] += 1

    counts_by_month = collections.Counter()

    for subscriber in subscribers:
        date_subscribed = subscriber['date_subscribe']

        date_obj = datetime.strptime(date_subscribed, '%Y-%m-%d %H:%M:%S')

        # Format as Year-Month
        month_str = date_obj.strftime('%Y-%m')
        counts_by_month[month_str] += 1

    return counts_by_month

def transform_counts_to_values(counts_by_month):
    transformed_values = []
    for month_str, count in counts_by_month.items():

        # Split the 'YYYY-MM' string into year and month integers
        year, month = map(int, month_str.split('-'))
        transformed_values.append({
            'year': year,
            'month': month,
            'value': count
        })
    return transformed_values

def get_kpis():
    url = f'{af_base_url}/api/Exec/kpis/{af_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        logging.info('KPIs fetched successfully.')
        kpis = response.json()
        return kpis
    else:
        logging.error(f'Error fetching KPIs: {response.status_code}')
        logging.error('Response: %s', response.text)
        sys.exit(1)

def find_kpi_by_name(kpis, name):
    for kpi in kpis:
        if kpi.get('name') == name:
            logging.info(f'FOUND: KPI "{name}"')
            return kpi
    logging.error(f'KPI "{name}" not found.')
    return None

def get_manual_data_sources(kpi_id):
    url = f'{af_base_url}/api/Exec/kpi/manual-data-sources/{kpi_id}/{af_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        logging.info(f'Manual data sources for KPI {kpi_id} fetched successfully.')
        data_sources = response.json()
        return data_sources
    else:
        logging.error(f'Error fetching manual data sources: {response.status_code}')
        logging.error('Response: %s', response.text)
        sys.exit(1)

def update_manual_data_source(data_source_id, values_payload):
    url = f'{af_base_url}/api/Exec/kpi/manual-data-sources/{af_api_key}'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'id': data_source_id,
        'values': values_payload
    }
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 204:
        logging.info('Manual data source updated successfully.')
    else:
        logging.error(f'Error updating manual data source: {response.status_code}')
        logging.error('Response: %s', response.text)
        sys.exit(1)

def main():

    # Step 1: Fetch subscriber counts
    counts_by_month = get_subscriber_counts_by_month(mailerlite_group_id)

    # Transform the counts into the desired format
    transformed_values = transform_counts_to_values(counts_by_month)

    # Step 2: Get all KPIs from Ampliflow
    kpis = get_kpis()

    # Step 3: Find the KPI by name (Replace with your actual KPI name)
    kpi_name = 'Subscribers'
    kpi = find_kpi_by_name(kpis, kpi_name)
    if not kpi:
        logging.error(f'KPI "{kpi_name}" not found.')
        sys.exit(1)
    kpi_id = kpi['id']

    # Step 4: Get manual data sources for the KPI
    data_sources = get_manual_data_sources(kpi_id)
    if not data_sources:
        logging.error(f'No manual data sources found for KPI {kpi_id}.')
        sys.exit(1)

    # Assuming we need to update the first manual data source
    data_source = data_sources[0]
    data_source_id = data_source['id']

    # Step 5: Update the manual data source with transformed_values
    logging.info('Updating manual data source with values: %s', json.dumps(transformed_values, indent=4))
    update_manual_data_source(data_source_id, transformed_values)

if __name__ == '__main__':
    main()
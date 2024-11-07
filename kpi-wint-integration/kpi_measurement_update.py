import json
from pathlib import Path
import requests
import sys
import logging
from datetime import datetime
from dotenv import load_dotenv

from wint_get_invoiced import get_monthly_revenue_report

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]  # Log to stdout
)

load_dotenv()
base_url = os.environ.get("AF_BASE_URL")
api_key = os.environ.get("AF_API_KEY")

def get_kpis():
    url = f'{base_url}/api/Exec/kpis/{api_key}'
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
    return None

def get_manual_data_sources(kpi_id):
    url = f'{base_url}/api/Exec/kpi/manual-data-sources/{kpi_id}/{api_key}'
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
    url = f'{base_url}/api/Exec/kpi/manual-data-sources/{api_key}'
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

def transform_values_payload(values):
    transformed_values = []
    for entry in values:
        date = datetime.fromisoformat(entry['date'].replace('Z', '+00:00'))
        transformed_values.append({
            'year': date.year,
            'month': date.month,
            'value': entry['value']
        })
    return transformed_values

def main():
    # Step 1: Get all KPIs
    kpis = get_kpis()

    # Step 2: Find the KPI with name "Revenue"
    kpi = find_kpi_by_name(kpis, 'Revenue')
    if not kpi:
        logging.error('KPI "Revenue" not found.')
        sys.exit(1)
    kpi_id = kpi['id']

    # Step 3: Get manual data sources for the KPI
    data_sources = get_manual_data_sources(kpi_id)
    if not data_sources:
        logging.error(f'No manual data sources found for KPI {kpi_id}.')
        sys.exit(1)

    # Assuming we need to update the first manual data source
    data_source = data_sources[0]
    data_source_id = data_source['id']

    # Step 4: Fetch revenue data from wint_get_invoiced.py
    start_year = 2024
    start_month = 4

    # Get current year and month
    current_date = datetime.now()
    end_year = current_date.year
    end_month = current_date.month

    monthly_revenue = get_monthly_revenue_report(start_year, start_month, end_year, end_month)
    if not monthly_revenue:
        logging.error('Failed to fetch monthly revenue data.')
        sys.exit(1)

    # Transform the values payload to the expected format
    values_payload = transform_values_payload(monthly_revenue.get('values', []))

    logging.info('Updating manual data source with values: %s', values_payload)

    # Step 5: Update the manual data source
    update_manual_data_source(data_source_id, values_payload)

if __name__ == '__main__':
    main()
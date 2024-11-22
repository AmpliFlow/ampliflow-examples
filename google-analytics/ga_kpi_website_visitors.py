import os
import sys
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]  # Log to stdout
)

# Load environment variables from .env file
load_dotenv()

# Retrieve Ampliflow credentials
base_url = os.environ.get("AF_BASE_URL")
api_key = os.environ.get("AF_API_KEY")

# Retrieve environment variables for Google Analytics
property_id = os.getenv('GA4_PROPERTY_ID')
service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Set the path to the service account key for Google API authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path

# Debug prints
print("Property ID:", property_id)
print("Service Account Path:", service_account_path)

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

def update_ampliflow_kpi(final_data):
    # Step 1: Get all KPIs
    kpis = get_kpis()

    # Step 2: Find the KPI with name "Total website visitors"
    kpi_name = 'Total website visitors'
    kpi = find_kpi_by_name(kpis, kpi_name)
    if not kpi:
        logging.error(f'KPI "{kpi_name}" not found.')
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

    # Step 4: Prepare the values payload
    values_payload = final_data

    # Step 5: Update the manual data source
    logging.info('Updating manual data source with values: %s', values_payload)
    update_manual_data_source(data_source_id, values_payload)

def run_report():
    client = BetaAnalyticsDataClient()

    today = datetime.today().strftime('%Y-%m-%d')

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name='year'),
            Dimension(name='month'),
        ],
        metrics=[
            Metric(name='activeUsers'),
        ],
        date_ranges=[
            DateRange(start_date='2023-01-01', end_date=today),
        ],
    )

    try:
        response = client.run_report(request)
        # Create the data structure
        data = {}
        if not response.rows:
            print("No data found for the specified request.")
        else:
            for row in response.rows:
                year = int(row.dimension_values[0].value)
                month = int(row.dimension_values[1].value)
                active_users = int(row.metric_values[0].value)

                key = (year, month)
                if key in data:
                    data[key] += active_users
                else:
                    data[key] = active_users

        # Convert data to desired format
        final_data = []
        for (year, month), value in sorted(data.items()):
            final_data.append({
                'year': year,
                'month': month,
                'value': value
            })

        # Print the final data
        print("Final Data:", final_data)

        # Update the Ampliflow KPI with the data
        update_ampliflow_kpi(final_data)

    except Exception as e:
        print("An error occurred while running the report:", str(e))

if __name__ == '__main__':
    run_report()
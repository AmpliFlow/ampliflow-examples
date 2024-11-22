import os
from dotenv import load_dotenv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    FilterExpression,
    Filter,
)

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
property_id = os.getenv('GA4_PROPERTY_ID')
service_account_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
conversion_events = os.getenv('CONVERSION_EVENTS', '').split(',')

# Set the path to the service account key for Google API authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_path

def run_report():
    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[
            Dimension(name='month'),                # To aggregate data by month
        ],
        metrics=[
            Metric(name='sessions'),               # Website visits
        ],
        date_ranges=[
            DateRange(start_date='2023-01-01', end_date='2024-12-31'),
        ],
        dimension_filter=FilterExpression(
            filter=Filter(
                field_name='eventName',
                in_list_filter=Filter.InListFilter(
                    values=conversion_events  # Use conversion events from environment variables
                )
            )
        ),
    )

    response = client.run_report(request)
    print(response)

    # Print the results
    print(f"{'Month':<10}{'Channel Group':<25}{'Conversion Type':<30}{'Sessions':<15}{'Conversions':<15}")
    for row in response.rows:
        month = row.dimension_values[0].value
        channel_group = row.dimension_values[1].value
        conversion_type = row.dimension_values[2].value
        sessions = row.metric_values[0].value
        conversions = row.metric_values[1].value
        print(f"{month:<10}{channel_group:<25}{conversion_type:<30}{sessions:<15}{conversions:<15}")

if __name__ == '__main__':
    run_report()
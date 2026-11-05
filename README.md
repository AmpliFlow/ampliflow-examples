# AmpliFlow Examples

This repository provides developer examples demonstrating how to integrate with [AmpliFlow](https://www.ampliflow.se) using [APIs (Swagger definition here)](https://app.ampliflow.com/swagger/index.html) and solutions. The examples are written in Python and cover common use cases such as interacting with the Custom List API and updating KPI measurements.

It includes an example of a simple data integration script that integrates with [Wint](https://www.wint.se/) to show an example of how to get financial data into KPI measurements in AmpliFlow.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Custom List API Example](#custom-list-api-example)
  - [Update KPI Measurement API Example (Wint)](#update-kpi-measurement-api-example-wint)
  - [Google Analytics Example](#google-analytics-example)
  - [MailerLite Example](#mailerlite-example)
  - [Control Set Export Example](#control-set-export-example)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- [pip](https://pip.pypa.io/en/stable/) package installer
- An AmpliFlow administrator account
- (Optional) A virtual environment tool like `venv` or `conda`

### Installation

1. **Clone the repository**

   ```bash
   git clone git@github.com:AmpliFlow/ampliflow-examples.git
   cd ampliflow-examples
   ```

2. **Create a virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **Copy the example environment file**

   ```bash
   cp .env.example .env
   ```

2. **Update the `.env` file**

   Open the `.env` file in a text editor and replace the placeholders with your actual credentials:

   ```ini
   AF_BASE_URL='https://yourtenant.ampliflow.com'
   AF_API_KEY='your_ampliflow_api_key'
   
   WINT_USERNAME='your_username'
   WINT_PASSWORD='your_password_or_api_key'
   ```

   - **AF_BASE_URL**: Replace `yourtenant` with your AmpliFlow tenant name.
   - **AF_API_KEY**: Generate an API key from your AmpliFlow account settings at `https://yourtenant.ampliflow.com/api-keys`.
   - **WINT_USERNAME** and **WINT_PASSWORD**: Credentials required for authentication if applicable.

## Usage

The repository includes example scripts demonstrating how to use different AmpliFlow APIs. Each property in the exec endpoints is accompanied by a detailed description in the Swagger documentation to assist with implementation.

### Custom List API Example

The custom list API example shows how to interact with custom lists in AmpliFlow.

- **Script**: `custom-lists/custom-list-example.py`

**Running the Example**

```bash
python custom-lists/custom-list-example.py
```

**Features Demonstrated**

- Authenticating with the AmpliFlow API using an API key
- Retrieving custom lists
- Adding items to a custom list
- Updating existing items in a custom list
- Error handling for API requests

### Update KPI Measurement API Example (Wint)

This example demonstrates how to update KPI measurements using the AmpliFlow API, pulling monthly revenue data from [Wint](https://www.wint.se/).

- **Script**: `kpi-wint-integration/kpi_measurement_update.py` (fetches data via `kpi-wint-integration/wint_get_invoiced.py`)

**Running the Example**

```bash
python kpi-wint-integration/kpi_measurement_update.py
```

**Features Demonstrated**

- Authenticating with the AmpliFlow API using an API key
- Submitting new KPI measurements
- Validating API responses
- Handling errors and exceptions

### Google Analytics Example

This example pulls website data from Google Analytics 4 into KPI manual data sources in AmpliFlow. See `google-analytics/README.md` for setup instructions (GA4 service account and property id required).

- **Script**: `google-analytics/ga_kpi_website_visitors.py` (active users)
- **Script**: `google-analytics/ga_kpi_update.py` (conversion events)

### MailerLite Example

This example pulls newsletter subscriber counts per month from MailerLite into a KPI manual data source in AmpliFlow.

- **Script**: `mailerlite/mailerlite.py` (requires `MAILERLITE_API_KEY` and `MAILERLITE_GROUP_ID` in `.env`)

### Control Set Export Example

This example logs in with your tenant, username and password and exports every live (non-archived/deleted) control set as machine-readable, LLM-friendly YAML — every API field of every control, with display values inlined for id fields — plus reference-data for the dropdown sources (users, teams, roles, processes, risks, pages, legislation, equipment). Exports are written to a gitignored `output/` folder. See `control-set-export/README.md`.

- **Script**: `control-set-export/control_set_export.py` (requires `AF_TENANT`, `AF_USERNAME` and `AF_PASSWORD` in `control-set-export/.env`)

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear commit messages.
4. Push your changes to your fork.
5. Submit a pull request explaining your changes.

Please ensure your code adheres to the existing style and includes appropriate documentation and tests.

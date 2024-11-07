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
  - [Update KPI Measurement API Example](#update-kpi-measurement-api-example)
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

- **Script**: `custom_list_example.py`

**Running the Example**

```bash
python custom_list_example.py
```

**Features Demonstrated**

- Authenticating with the AmpliFlow API using an API key
- Retrieving custom lists
- Adding items to a custom list
- Updating existing items in a custom list
- Error handling for API requests

### Update KPI Measurement API Example

This example demonstrates how to update KPI measurements using the AmpliFlow API.

- **Script**: `update_kpi_measurement.py`

**Running the Example**

```bash
python update_kpi_measurement.py
```

**Features Demonstrated**

- Authenticating with the AmpliFlow API using an API key
- Submitting new KPI measurements
- Validating API responses
- Handling errors and exceptions

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear commit messages.
4. Push your changes to your fork.
5. Submit a pull request explaining your changes.

Please ensure your code adheres to the existing style and includes appropriate documentation and tests.

# ConnectLife API Python Client

A simple Python script to connect to the ConnectLife API and fetch appliance data.

## Features

- Authenticates with ConnectLife using a multi-step OAuth2 process.
- Fetches a list of connected appliances and their data.

## Prerequisites

- Python 3.x
- The `requests` library

## Installation

1.  Clone this repository or download the `connectlife_api.py` script.
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Important:** Open `connectlife_api.py` and replace the placeholder `USERNAME` and `PASSWORD` with your actual ConnectLife account credentials.
    ```python
    # Replace with your actual ConnectLife credentials
    USERNAME = "your-email@example.com"
    PASSWORD = "your-password"
    ```
2.  Run the script from your terminal:
    ```bash
    python connectlife_api.py
    ```

The script will print the list of your connected appliances in JSON format.

## Community Project

For a more detailed and community-managed solution with more features, please check out the following project:

- **[oyvindwe/connectlife](https://github.com/oyvindwe/connectlife)**

This project is actively maintained and offers a more robust implementation.

## Disclaimer

This is an unofficial script and is not affiliated with or supported by ConnectLife, Hisense, or Gorenje. Use it at your own risk.

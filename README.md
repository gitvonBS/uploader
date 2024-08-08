# Uploader

A simple Python application to upload files to a specified server.

## Features

- Uploads files to a server
- Supports various file types
- Configurable server settings

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/gitvonBS/uploader.git
    ```

2. Navigate to the project directory:

    ```bash
    cd uploader
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure your server settings are configured in the `config.json` file.
2. Run the uploader script:

    ```bash
    python uploader.py
    ```

## Configuration

Edit the `config.json` file to configure the server settings:

```json
{
    "server_url": "http://example.com/upload",
    "api_key": "your_api_key",
    "timeout": 30
}
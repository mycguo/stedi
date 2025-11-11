# Stedi Healthcare API Sample Request Generator

This repository contains a Python script to generate sample requests from the Stedi Healthcare OpenAPI specification.

API Key: https://portal.stedi.com/app/settings/api-keys?account=6a97ba34-1d98-4102-8954-ca02f253dcbc

test_JFyME6G.VSSis3ZG4m1iFPds82ndIc8m

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script to generate sample requests:

```bash
python3 generate_sample_requests.py
```

This will:
1. Download the OpenAPI specification from the Stedi GitHub repository
2. Generate sample requests for all endpoints
3. Create two output files:
   - `sample_requests.json` - JSON file containing all sample requests
   - `sample_requests.py` - Python script with executable request functions

## Output Files

### sample_requests.json
Contains all sample requests in JSON format with:
- HTTP method
- Path
- URL
- Headers (including API key placeholder)
- Query parameters
- Request body (if applicable)

### sample_requests.py
A Python script with individual functions for each endpoint. Each function:
- Uses the `requests` library
- Includes proper headers
- Has sample payloads based on the OpenAPI schema
- Returns the response object

#### Running as a Program

The `sample_requests.py` script can be run directly as a command-line program:

```bash
# List all available requests
python3 sample_requests.py --list
# or
./sample_requests.py --list

# Show details about a specific request
python3 sample_requests.py --info 1

# Run a specific request
python3 sample_requests.py --run 19

# Run with verbose output (shows headers)
python3 sample_requests.py --run 19 --verbose

# Dry run (see what would be executed without making the request)
python3 sample_requests.py --run 19 --dry-run

# Override API key
python3 sample_requests.py --run 19 --api-key "your-api-key-here"
```

#### Using as a Python Module

You can also import and use the functions directly:

```python
from sample_requests import request_1, API_KEY

# Set your API key
import sample_requests
sample_requests.API_KEY = "your-actual-api-key"

# Make a request
response = request_1()
print(response.json())
```

## Customization

You can modify `generate_sample_requests.py` to:
- Change the OpenAPI spec URL
- Customize sample value generation
- Add different output formats (cURL, etc.)
- Filter specific endpoints

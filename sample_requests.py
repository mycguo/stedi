#!/usr/bin/env python3
"""
Sample requests for Stedi Healthcare API
Generated from OpenAPI specification
"""

import requests
import json
import argparse
import sys
import os
from typing import Dict, Callable, Any, Optional

BASE_URL = "https://healthcare.us.stedi.com/2024-04-01"

# Global variable to store API key (set by Streamlit or CLI)
_api_key: Optional[str] = None

def get_api_key() -> str:
    """Get API key from Streamlit secrets, environment variable, or global variable."""
    global _api_key
    
    # Try Streamlit secrets first (when running in Streamlit)
    try:
        import streamlit as st
        if "STEDI_API_KEY" in st.secrets:
            return st.secrets["STEDI_API_KEY"]
    except (ImportError, RuntimeError):
        pass  # Not running in Streamlit
    
    # Try environment variable
    env_key = os.getenv("STEDI_API_KEY")
    if env_key:
        return env_key
    
    # Use global variable if set
    if _api_key:
        return _api_key
    
    # Fallback for CLI usage
    raise ValueError("API key not found. Set STEDI_API_KEY environment variable or use --api-key flag.")

# Registry of all available requests
REQUESTS: Dict[int, Dict[str, Any]] = {
    1: {"func": None, "method": "POST", "path": "/change/medicalnetwork/claimstatus/v2", "description": "Submit a 276/277 real-time claim status check in JSON format"},
    2: {"func": None, "method": "POST", "path": "/change/medicalnetwork/claimstatus/v2/raw-x12", "description": "Submit a 276/277 real-time claim status check in raw X12 EDI format"},
    3: {"func": None, "method": "POST", "path": "/change/medicalnetwork/eligibility/v3", "description": "Submit a real-time 270/271 eligibility check in JSON format"},
    4: {"func": None, "method": "POST", "path": "/change/medicalnetwork/eligibility/v3/raw-x12", "description": "Submit a real-time 270/271 eligibility check in raw X12 EDI format"},
    5: {"func": None, "method": "POST", "path": "/change/medicalnetwork/institutionalclaims/v1/raw-x12-submission", "description": "Submit an 837I institutional claim in raw X12 EDI format"},
    6: {"func": None, "method": "POST", "path": "/change/medicalnetwork/institutionalclaims/v1/submission", "description": "Submit an 837I institutional claim in JSON format"},
    7: {"func": None, "method": "POST", "path": "/change/medicalnetwork/professionalclaims/v3/raw-x12-submission", "description": "Submit an 837P professional claim in raw X12 EDI format"},
    8: {"func": None, "method": "POST", "path": "/change/medicalnetwork/professionalclaims/v3/submission", "description": "Submit an 837P professional claim in JSON format"},
    9: {"func": None, "method": "GET", "path": "/change/medicalnetwork/reports/v2/{eligibilitySearchId}/277", "description": "Get 277 claim status report"},
    10: {"func": None, "method": "GET", "path": "/change/medicalnetwork/reports/v2/{eligibilitySearchId}/835", "description": "Get 835 payment report"},
    11: {"func": None, "method": "POST", "path": "/coordination-of-benefits", "description": "Submit coordination of benefits check"},
    12: {"func": None, "method": "POST", "path": "/dental-claims/raw-x12-submission", "description": "Submit dental claim in raw X12 EDI format"},
    13: {"func": None, "method": "POST", "path": "/dental-claims/submission", "description": "Submit dental claim in JSON format"},
    14: {"func": None, "method": "GET", "path": "/export/pdf", "description": "Export PDF"},
    15: {"func": None, "method": "GET", "path": "/export/{claimId}/1500/pdf", "description": "Export 1500 form PDF"},
    16: {"func": None, "method": "POST", "path": "/insurance-discovery/check/v1", "description": "Submit insurance discovery check"},
    17: {"func": None, "method": "GET", "path": "/insurance-discovery/check/v1/{checkId}", "description": "Get insurance discovery check result"},
    18: {"func": None, "method": "GET", "path": "/payer/{payerId}", "description": "Get payer information"},
    19: {"func": None, "method": "GET", "path": "/payers", "description": "List all payers"},
    20: {"func": None, "method": "GET", "path": "/payers/csv", "description": "Export payers as CSV"},
    21: {"func": None, "method": "GET", "path": "/payers/search", "description": "Search payers"},
}


# Request 1: POST /change/medicalnetwork/claimstatus/v2
def request_1():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/claimstatus/v2"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "providers": [
                {
                        "providerType": "BillingProvider"
                }
        ],
        "subscriber": {
                "firstName": "EXAMPLE",
                "lastName": "EXAMPLE",
                "memberId": "123456789"
        },
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 2: POST /change/medicalnetwork/claimstatus/v2/raw-x12
def request_2():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/claimstatus/v2/raw-x12"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "x12": "example"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 3: POST /change/medicalnetwork/eligibility/v3
def request_3():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/eligibility/v3"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "provider": {
                "npi": "87726",
                "organizationName": "UnitedHealthcare"
        },
        "subscriber": {
                "firstName": "JOHN",
                "lastName": "DOE",
                "memberId": "123456789",
                "dateOfBirth": "19800101"
        },
        "tradingPartnerServiceId": "10379"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 4: POST /change/medicalnetwork/eligibility/v3/raw-x12
def request_4():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/eligibility/v3/raw-x12"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "x12": "example"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 5: POST /change/medicalnetwork/institutionalclaims/v1/raw-x12-submission
def request_5():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/institutionalclaims/v1/raw-x12-submission"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "x12": "example"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 6: POST /change/medicalnetwork/institutionalclaims/v1/submission
def request_6():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/institutionalclaims/v1/submission"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "claimInformation": {
                "benefitsAssignmentCertificationIndicator": "N",
                "claimChargeAmount": "example",
                "claimCodeInformation": {
                        "admissionTypeCode": "e",
                        "patientStatusCode": "ex"
                },
                "claimDateInformation": {
                        "statementBeginDate": "20240101",
                        "statementEndDate": "20240101"
                },
                "claimFilingCode": "11",
                "claimFrequencyCode": "e",
                "patientControlNumber": "123456",
                "placeOfServiceCode": "ex",
                "planParticipationCode": "A",
                "principalDiagnosis": {
                        "principalDiagnosisCode": "example",
                        "qualifierCode": "ABK"
                },
                "releaseInformationCode": "I",
                "serviceLines": [
                        {
                                "institutionalService": {
                                        "lineItemChargeAmount": "example",
                                        "measurementUnit": "DA",
                                        "serviceLineRevenueCode": "example",
                                        "serviceUnitCount": "example"
                                }
                        }
                ]
        },
        "receiver": {
                "organizationName": "EXAMPLE"
        },
        "submitter": {
                "contactInformation": {},
                "organizationName": "EXAMPLE",
                "taxId": "123456789"
        },
        "subscriber": {
                "firstName": "EXAMPLE",
                "lastName": "EXAMPLE",
                "paymentResponsibilityLevelCode": "A"
        },
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 7: POST /change/medicalnetwork/professionalclaims/v3/raw-x12-submission
def request_7():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/professionalclaims/v3/raw-x12-submission"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "x12": "example"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 8: POST /change/medicalnetwork/professionalclaims/v3/submission
def request_8():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/professionalclaims/v3/submission"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "billing": {},
        "claimInformation": {
                "benefitsAssignmentCertificationIndicator": "N",
                "claimChargeAmount": "example",
                "claimFilingCode": "11",
                "claimFrequencyCode": "1",
                "healthCareCodeInformation": [
                        {
                                "diagnosisCode": "example",
                                "diagnosisTypeCode": "BK"
                        }
                ],
                "patientControlNumber": "123456",
                "placeOfServiceCode": "01",
                "planParticipationCode": "A",
                "releaseInformationCode": "I",
                "serviceLines": [
                        {
                                "professionalService": {
                                        "compositeDiagnosisCodePointers": {
                                                "diagnosisCodePointers": [
                                                        "example"
                                                ]
                                        },
                                        "lineItemChargeAmount": "example",
                                        "measurementUnit": "MJ",
                                        "procedureCode": "example",
                                        "procedureIdentifier": "ER",
                                        "serviceUnitCount": "example"
                                },
                                "serviceDate": "20240101"
                        }
                ],
                "signatureIndicator": "N"
        },
        "receiver": {
                "organizationName": "EXAMPLE"
        },
        "submitter": {
                "contactInformation": {}
        },
        "subscriber": {
                "firstName": "JOHN",
                "lastName": "DOE",
                "memberId": "123456789"
        },
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 9: GET /change/medicalnetwork/reports/v2/123456789/277
def request_9():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/reports/v2/123456789/277"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 10: GET /change/medicalnetwork/reports/v2/123456789/835
def request_10():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/reports/v2/123456789/835"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 11: POST /coordination-of-benefits
def request_11():
    """"""
    url = f"{BASE_URL}/coordination-of-benefits"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "encounter": {},
        "provider": {
                "npi": "example"
        },
        "subscriber": {
                "dateOfBirth": "20240101",
                "firstName": "EXAMPLE",
                "lastName": "EXAMPLE"
        },
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 12: POST /dental-claims/raw-x12-submission
def request_12():
    """"""
    url = f"{BASE_URL}/dental-claims/raw-x12-submission"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "x12": "example"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 13: POST /dental-claims/submission
def request_13():
    """"""
    url = f"{BASE_URL}/dental-claims/submission"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "billing": {},
        "claimInformation": {
                "benefitsAssignmentCertificationIndicator": "N",
                "claimChargeAmount": "example",
                "claimFrequencyCode": "1",
                "patientControlNumber": "123456",
                "placeOfServiceCode": "01",
                "releaseInformationCode": "I",
                "serviceLines": [
                        {
                                "dentalService": {
                                        "lineItemChargeAmount": "example",
                                        "procedureCode": "example"
                                }
                        }
                ],
                "signatureIndicator": "N"
        },
        "receiver": {
                "organizationName": "EXAMPLE"
        },
        "submitter": {
                "contactInformation": {}
        },
        "subscriber": {
                "firstName": "JOHN",
                "lastName": "DOE",
                "memberId": "123456789"
        },
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 14: GET /export/pdf
def request_14():
    """"""
    url = f"{BASE_URL}/export/pdf"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    params = {
        "businessId": "123456789"
}
    response = requests.get(url, headers=headers, params=params)
    return response


# Request 15: GET /export/123456789/1500/pdf
def request_15():
    """"""
    url = f"{BASE_URL}/export/123456789/1500/pdf"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 16: POST /insurance-discovery/check/v1
def request_16():
    """"""
    url = f"{BASE_URL}/insurance-discovery/check/v1"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    payload = {
        "provider": {
                "npi": "example"
        },
        "subscriber": {
                "firstName": "EXAMPLE",
                "lastName": "EXAMPLE"
        }
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 17: GET /insurance-discovery/check/v1/123456789
def request_17():
    """"""
    url = f"{BASE_URL}/insurance-discovery/check/v1/123456789"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 18: GET /payer/123456789
def request_18():
    """"""
    url = f"{BASE_URL}/payer/123456789"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 19: GET /payers
def request_19():
    """"""
    url = f"{BASE_URL}/payers"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 20: GET /payers/csv
def request_20():
    """"""
    url = f"{BASE_URL}/payers/csv"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 21: GET /payers/search
def request_21():
    """"""
    url = f"{BASE_URL}/payers/search"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


def print_response(response: requests.Response, verbose: bool = False) -> None:
    """Print formatted response."""
    print(f"\n{'='*80}")
    print(f"Status Code: {response.status_code} {response.reason}")
    print(f"{'='*80}")
    
    if verbose:
        print("\nHeaders:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
    
    print("\nResponse Body:")
    try:
        response_json = response.json()
        print(json.dumps(response_json, indent=2))
    except json.JSONDecodeError:
        print(response.text[:1000])  # Print first 1000 chars if not JSON
        if len(response.text) > 1000:
            print(f"\n... (truncated, total length: {len(response.text)} chars)")


def list_requests() -> None:
    """List all available requests."""
    print("\nAvailable Requests:")
    print("="*80)
    for req_id, req_info in REQUESTS.items():
        print(f"{req_id:2d}. {req_info['method']:6s} {req_info['path']}")
        if req_info.get('description'):
            print(f"    {req_info['description']}")
        print()


def get_request_info(request_id: int) -> None:
    """Show detailed information about a specific request."""
    if request_id not in REQUESTS:
        print(f"Error: Request {request_id} not found. Use --list to see all requests.")
        return
    
    req_info = REQUESTS[request_id]
    func = req_info['func']
    
    print(f"\nRequest {request_id}: {req_info['method']} {req_info['path']}")
    print("="*80)
    if req_info.get('description'):
        print(f"Description: {req_info['description']}")
    print(f"Full URL: {BASE_URL}{req_info['path']}")
    
    if func:
        # Try to get payload info by calling the function (but don't actually make request)
        import inspect
        source = inspect.getsource(func)
        # Extract payload if it exists
        if 'payload' in source:
            print("\nSample Payload:")
            # This is a simplified extraction - in practice, you'd parse the function better
            print("  (See function definition for full payload)")
    
    print()


def run_request(request_id: int, verbose: bool = False, dry_run: bool = False) -> None:
    """Run a specific request."""
    if request_id not in REQUESTS:
        print(f"Error: Request {request_id} not found. Use --list to see all requests.")
        sys.exit(1)
    
    req_info = REQUESTS[request_id]
    func = req_info['func']
    
    if not func:
        print(f"Error: Request function {request_id} not initialized.")
        sys.exit(1)
    
    print(f"\nRunning Request {request_id}: {req_info['method']} {req_info['path']}")
    print(f"Description: {req_info.get('description', 'N/A')}")
    
    if dry_run:
        print("\n[DRY RUN] Would execute:")
        print(f"  Function: {func.__name__}")
        print(f"  URL: {BASE_URL}{req_info['path']}")
        return
    
    try:
        response = func()
        print_response(response, verbose)
    except requests.exceptions.RequestException as e:
        print(f"\nError making request: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Stedi Healthcare API Sample Request Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                    # List all available requests
  %(prog)s --info 1                  # Show details about request 1
  %(prog)s --run 1                   # Run request 1
  %(prog)s --run 1 --verbose         # Run request 1 with verbose output
  %(prog)s --run 1 --dry-run         # Show what would be executed without making request
        """
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List all available requests"
    )
    
    parser.add_argument(
        "--info", "-i",
        type=int,
        metavar="ID",
        help="Show detailed information about a specific request"
    )
    
    parser.add_argument(
        "--run", "-r",
        type=int,
        metavar="ID",
        help="Run a specific request by ID"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output including response headers"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be executed without making the actual request"
    )
    
    parser.add_argument(
        "--api-key",
        help="Override API key (default: uses STEDI_API_KEY environment variable or st.secrets)"
    )
    
    args = parser.parse_args()
    
    # Override API key if provided
    global _api_key
    if args.api_key:
        _api_key = args.api_key
    
    # Initialize request functions
    for req_id in REQUESTS:
        func_name = f"request_{req_id}"
        REQUESTS[req_id]["func"] = globals().get(func_name)
    
    # Handle commands
    if args.list:
        list_requests()
    elif args.info:
        get_request_info(args.info)
    elif args.run:
        run_request(args.run, verbose=args.verbose, dry_run=args.dry_run)
    else:
        # Default: show help and list requests
        parser.print_help()
        print("\n")
        list_requests()


if __name__ == "__main__":
    main()


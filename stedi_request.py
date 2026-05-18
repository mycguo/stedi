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

API_REFERENCE_URL = "https://www.stedi.com/docs/healthcare/api-reference"
HEALTHCARE_OPENAPI_URL = "https://raw.githubusercontent.com/Stedi/openApi/main/healthcare.json"
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

_usage_indicator: str = "T"

def set_usage_indicator(value: str):
    """Set the global usage indicator (T for test, P for production)."""
    global _usage_indicator
    if value in ["T", "P"]:
        _usage_indicator = value

def get_usage_indicator() -> str:
    """Get the current usage indicator."""
    return _usage_indicator

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
    9: {"func": None, "method": "GET", "path": "/change/medicalnetwork/reports/v2/{transactionId}/277", "description": "Get 277 claim acknowledgment report"},
    10: {"func": None, "method": "GET", "path": "/change/medicalnetwork/reports/v2/{transactionId}/835", "description": "Get 835 ERA report"},
    11: {"func": None, "method": "POST", "path": "/coordination-of-benefits", "description": "Submit coordination of benefits check"},
    12: {"func": None, "method": "POST", "path": "/dental-claims/raw-x12-submission", "description": "Submit dental claim in raw X12 EDI format"},
    13: {"func": None, "method": "POST", "path": "/dental-claims/submission", "description": "Submit dental claim in JSON format"},
    14: {"func": None, "method": "GET", "path": "/export/pdf", "description": "Export PDF"},
    15: {"func": None, "method": "GET", "path": "/export/{transactionId}/1500/pdf", "description": "Export 1500 form PDF"},
    16: {"func": None, "method": "POST", "path": "/insurance-discovery/check/v1", "description": "Submit insurance discovery check"},
    17: {"func": None, "method": "GET", "path": "/insurance-discovery/check/v1/{discoveryId}", "description": "Get insurance discovery check result"},
    18: {"func": None, "method": "GET", "path": "/payer/{stediId}", "description": "Get payer information"},
    19: {"func": None, "method": "GET", "path": "/payers", "description": "List all payers"},
    20: {"func": None, "method": "GET", "path": "/payers/csv", "description": "Export payers as CSV"},
    21: {"func": None, "method": "GET", "path": "/payers/search", "description": "Search payers"},
    22: {"func": None, "method": "GET", "path": "/electronic-remittance-advice/{transactionId}/pdf", "description": "Get 835 ERA PDF"},
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
        "encounter": {
                "beginningDateOfService": "20250630",
                "endDateOfService": "20250702"
        },
        "providers": [
                {
                        "providerType": "BillingProvider",
                        "npi": "1999999984",
                        "organizationName": "Provider Name"
                }
        ],
        "subscriber": {
                "dateOfBirth": "19710101",
                "firstName": "Jane",
                "lastName": "Doe",
                "memberId": "UHC123456"
        },
        "tradingPartnerServiceId": "87726"
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
    # X12 276 Health Care Claim Status Request from the current Stedi spec.
    x12_content = """ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *250916*2048*^*00501*000000001*0*T*>~
GS*HR*SENDERGS*RECEIVERGS*20250916*204811*1*X*005010X212~
ST*276*0001*005010X212~
BHT*0010*13*ABC276XXX*20250915*1425~
HL*1**20*1~
NM1*PR*2*UNITEDHEALTHCARE*****PI*87726~
HL*2*1*21*1~
NM1*41*2*PROVIDER NAME*****46*123456789~
HL*3*2*19*1~
NM1*1P*2*PROVIDER NAME*****XX*1999999984~
HL*4*3*22*0~
DMG*D8*19710101~
NM1*IL*1*DOE*JANE****MI*UHC123456~
TRN*1*123456789~
DTP*472*RD8*20250630-20250702~
SE*14*0001~
GE*1*1~
IEA*1*000000001~"""
    
    payload = {
        "x12": x12_content
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
        "encounter": {
                "serviceTypeCodes": [
                        "MH"
                ]
        },
        "externalPatientId": "UAA111222333",
        "provider": {
                "npi": "1999999984",
                "organizationName": "ACME Health Services"
        },
        "subscriber": {
                "dateOfBirth": "19000101",
                "firstName": "Jane",
                "lastName": "Doe",
                "memberId": "123456789",
        },
        "tradingPartnerServiceId": "AHS"
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
    # X12 270 Health Care Eligibility Benefit Inquiry from the current Stedi spec.
    x12_content = """ISA*00*          *00*          *ZZ*SENDER         *ZZ*RECEIVER       *231106*1406*^*00501*000000001*0*T*>~
GS*HS*SENDERGS*RECEIVERGS*20231106*140631*000000001*X*005010X279A1~
ST*270*1234*005010X279A1~
BHT*0022*13*10001234*20240321*1319~
HL*1**20*1~
NM1*PR*2*ABCDE*****PI*11122~
HL*2*1*21*1~
NM1*1P*2*ACME HEALTH SERVICES*****SV*1999999984~
HL*3*2*22*0~
TRN*1*11122-12345*1234567890~
NM1*IL*1*JANE*DOE****MI*123456789~
DMG*D8*19000101~
DTP*291*D8*20240108~
EQ*MH~
SE*13*1234~
GE*1*000000001~
IEA*1*000000001~"""
    
    payload = {
        "x12": x12_content
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
    # Basic X12 837I Institutional Claim
    x12_content = """ISA*00*          *00*          *ZZ*STEDI          *01*123456789      *250101*1200*^*00501*000000001*0*P*:~
GS*HC*STEDI*123456789*20250101*1200*1*X*005010X223A2~
ST*837*0001*005010X223A2~
BHT*0019*00*TEST123456*20250101*1200*CH~
NM1*41*2*EXAMPLE RECEIVER*****46*10379~
PER*IC*CONTACT*TE*5551234567~
NM1*40*2*EXAMPLE SUBMITTER*****46*123456789~
HL*1**20*1~
PRV*BI*PXC*207Q00000X~
NM1*85*2*EXAMPLE BILLING PROVIDER*****XX*1234567890~
N3*123 MAIN ST~
N4*CITY*ST*12345~
REF*EI*123456789~
HL*2*1*22*0~
SBR*P*18*GROUP123*ACME INSURANCE*****CI~
NM1*IL*1*DOE*JOHN****MI*123456789~
N3*456 PATIENT ST~
N4*CITY*ST*12345~
DMG*D8*19800101*M~
NM1*PR*2*10379*****PI*10379~
CLM*123456*100.00***11:A:1**A*Y*Y~
DTP*434*RD8*20250101-20250101~
DTP*435*D8*20250101~
CL1*1*1*01~
REF*D9*123456~
HI*BK:Z0000~
LX*1~
SV2*0450*HC:99213*100.00*UN*1~
DTP*472*D8*20250101~
SE*28*0001~
GE*1*1~
IEA*1*000000001~"""
    
    payload = {
        "x12": x12_content
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
        "usageIndicator": get_usage_indicator(),
        "tradingPartnerName": "EXAMPLE PAYER",
        "tradingPartnerServiceId": "10379",
        "submitter": {
                "organizationName": "EXAMPLE",
                "contactInformation": {
                        "name": "EXAMPLE CONTACT",
                        "phoneNumber": "5551234567"
                },
                "taxId": "123456789"
        },
        "receiver": {
                "organizationName": "EXAMPLE"
        },
        "subscriber": {
                "memberId": "123456789",
                "paymentResponsibilityLevelCode": "P",
                "firstName": "EXAMPLE",
                "lastName": "EXAMPLE",
                "gender": "M",
                "dateOfBirth": "19800101",
                "address": {
                        "address1": "123 MAIN ST",
                        "city": "ANYTOWN",
                        "state": "NY",
                        "postalCode": "100011234"
                }
        },
        "claimInformation": {
                "claimFilingCode": "ZZ",
                "patientControlNumber": "123456",
                "claimChargeAmount": "100.00",
                "placeOfServiceCode": "11",
                "claimFrequencyCode": "0",
                "planParticipationCode": "C",
                "benefitsAssignmentCertificationIndicator": "Y",
                "releaseInformationCode": "Y",
                "principalDiagnosis": {
                        "qualifierCode": "ABK",
                        "principalDiagnosisCode": "Z0000"
                },
                "serviceLines": [
                        {
                                "assignedNumber": "0",
                                "serviceDate": "20240101",
                                "serviceDateEnd": "20240101",
                                "lineItemControlNumber": "111222333",
                                "institutionalService": {
                                        "serviceLineRevenueCode": "0450",
                                        "lineItemChargeAmount": "100.00",
                                        "measurementUnit": "UN",
                                        "serviceUnitCount": "1",
                                        "procedureIdentifier": "HC",
                                        "procedureCode": "99213"
                                }
                        }
                ],
                "claimCodeInformation": {
                        "admissionTypeCode": "1",
                        "admissionSourceCode": "7",
                        "patientStatusCode": "01"
                },
                "claimDateInformation": {
                        "admissionDateAndHour": "202401010800",
                        "statementBeginDate": "20240101",
                        "statementEndDate": "20240101"
                }
        },
        "providers": [
                {
                        "providerType": "BillingProvider",
                        "npi": "1932808896",
                        "employerId": "123456789",
                        "organizationName": "EXAMPLE BILLING PROVIDER",
                        "address": {
                                "address1": "123 BILLING ST",
                                "city": "ANYTOWN",
                                "state": "NY",
                                "postalCode": "100011234"
                        },
                        "contactInformation": {
                                "name": "EXAMPLE BILLING PROVIDER",
                                "phoneNumber": "5551234567"
                        }
                },
                {
                        "providerType": "AttendingProvider",
                        "npi": "1003000126",
                        "firstName": "JANE",
                        "lastName": "DOE",
                        "contactInformation": {
                                "name": "JANE DOE"
                        }
                }
        ]
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
    x12_content = """ISA*00*          *00*          *ZZ*574183004559   *ZZ*STEDITEST      *260213*2039*^*00501*000000039*0*T*>~
GS*HC*574183004559*STEDITEST*20260213*203918*39*X*005010X222A1~
ST*837*0001*005010X222A1~
BHT*0019*00*01KHCBK84E40QQYJVXA5VVXG54*20260213*2038*CH~
NM1*41*2*Test Data Health Services, Inc.*****46*123435~
PER*IC**TE*5552223333~
NM1*40*2*Cigna*****46*6400~
HL*1**20*1~
PRV*BI*PXC*2084P0800X~
NM1*85*2*Therapy Associates*****XX*1999999984~
N3*123 Some St*Floor 1~
N4*A City*NY*123450000~
REF*EI*123456789~
PER*IC*Test Data Health Services, Inc.*TE*5553334444~
HL*2*1*22*0~
SBR*P*18*3335555******CI~
NM1*IL*1*Anon*John****MI*U7777788888~
N3*2222 Random St~
N4*A City*NY*123450000~
DMG*D8*20000101*M~
NM1*PR*2*Cigna*****PI*6400~
CLM*123456789*109.2***02>B>1*Y*A*Y*Y~
HI*ABK>F1111~
NM1*77*2*Smith Associates~
N3*1234 Other St~
N4*A City*NY*123450000~
LX*1~
SV1*HC>90837>95*109.2*UN*1***1~
DTP*472*D8*20240101~
REF*6R*111222333~
SE*29*0001~
GE*1*39~
IEA*1*000000039~"""
    payload = {
        "x12": x12_content
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
        "billing": {
                "npi": "1932808896",
                "organizationName": "EXAMPLE BILLING PROVIDER",
                "employerId": "123456789",
                "address": {
                        "address1": "123 BILLING ST",
                        "city": "ANYTOWN",
                        "state": "NY",
                        "postalCode": "10001"
                }
        },
        "claimInformation": {
                "benefitsAssignmentCertificationIndicator": "N",
                "claimChargeAmount": "100.00",
                "claimFilingCode": "11",
                "claimFrequencyCode": "1",
                "healthCareCodeInformation": [
                        {
                                "diagnosisCode": "Z0000",
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
                                                        "1"
                                                ]
                                        },
                                        "lineItemChargeAmount": "100.00",
                                        "measurementUnit": "UN",
                                        "procedureCode": "99213",
                                        "procedureIdentifier": "ER",
                                        "serviceUnitCount": "1"
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
                "organizationName": "EXAMPLE SUBMITTER",
                "contactInformation": {
                        "name": "EXAMPLE CONTACT",
                        "phoneNumber": "5551234567"
                }
        },
        "subscriber": {
                "firstName": "JOHN",
                "lastName": "DOE",
                "memberId": "123456789",
                "dateOfBirth": "19800101",
                "gender": "M",
                "address": {
                        "address1": "123 MAIN ST",
                        "city": "ANYTOWN",
                        "state": "NY",
                        "postalCode": "10001"
                }
        },
        "tradingPartnerServiceId": "10379",
        "usageIndicator": get_usage_indicator()
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 9: GET /change/medicalnetwork/reports/v2/{transactionId}/277
def request_9():
    """"""
    # Replace this with the processed 277 transactionId from Stedi.
    transaction_id = "d567c2ae-f073-4725-8b8c-06c473b738a6"
    url = f"{BASE_URL}/change/medicalnetwork/reports/v2/{transaction_id}/277"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 10: GET /change/medicalnetwork/reports/v2/{transactionId}/835
def request_10():
    """"""
    # Replace this with the processed 835 transactionId from Stedi.
    transaction_id = "d567c2ae-f073-4725-8b8c-06c473b738a6"
    url = f"{BASE_URL}/change/medicalnetwork/reports/v2/{transaction_id}/835"
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
        "dependent": {
                "dateOfBirth": "2002-12-31",
                "firstName": "Jordan",
                "lastName": "Doe"
        },
        "encounter": {
                "dateOfService": "2024-08-02",
                "serviceTypeCode": "30"
        },
        "provider": {
                "npi": "1932808896",
                "organizationName": "ACME Health Services"
        },
        "subscriber": {
                "dateOfBirth": "1985-05-27",
                "firstName": "John",
                "lastName": "Doe",
                "memberId": "W000000000"
        },
        "tradingPartnerServiceId": "SOMEID"
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
    x12_content = """ISA*00*          *00*          *ZZ*574183004559   *ZZ*STEDITEST      *260213*2050*^*00501*000000042*0*T*>~
GS*HC*574183004559*STEDITEST*20260213*205048*42*X*005010X224A2~
ST*837*0001*005010X224A2~
BHT*0019*00*01KHCCA4V6K00NFPX588G859SJ*20260213*2050*CH~
NM1*41*2*ABA Inc*****46*1234567~
PER*IC*BILLING DEPARTMENT*TE*3131234567~
NM1*40*2*United HealthCare Dental*****46*52133~
HL*1**20*1~
PRV*BI*PXC*106S00000X~
NM1*85*2*ABA Inc*****XX*1999999992~
N3*ABA Inc 123 Some St~
N4*Denver*CO*802383000~
REF*EI*123456789~
PER*IC*ABA Inc*TE*3134893157~
HL*2*1*22*0~
SBR*P*18*1234567890******FI~
NM1*IL*1*Doe*John****MI*123412345~
N3*1234 Some St~
N4*Buckeye*AZ*85326~
DMG*D8*20180615*F~
NM1*PR*2*United HealthCare Dental*****PI*52133~
N3*PO Box 7000~
N4*Camden*SC*29000~
CLM*12345*832***12>B>1*Y*A*Y*Y~
DN2*3*E****JP~
REF*G1*20231010012345678~
HI*ABK>K081~
NM1*82*1*Doe*Jane****XX*1999999992~
PRV*PE*PXC*106S00000X~
LX*1~
SV3*AD>D7140*832**1>2*I*2*****1~
TOO*JP*3*M>O~
DTP*472*D8*20230428~
REF*6R*a0UDo000000dd2dMAA~
NM1*82*1*Doe*Jane****XX*1999999992~
PRV*PE*PXC*122300000X~
SE*35*0001~
GE*1*42~
IEA*1*000000042~"""
    payload = {
        "x12": x12_content
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
        "tradingPartnerServiceId": "10379"
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


# Request 15: GET /export/{transactionId}/1500/pdf
def request_15():
    """"""
    # Replace this with the processed professional claim transactionId from Stedi.
    transaction_id = "a10b1111-7233-484c-8dee-b240c590c767"
    url = f"{BASE_URL}/export/{transaction_id}/1500/pdf"
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
        "encounter": {
                "beginningDateOfService": "20240326",
                "endDateOfService": "20240326"
        },
        "provider": {
                "npi": "1999999984"
        },
        "subscriber": {
                "address": {
                        "address1": "123 Main St",
                        "city": "Springfield",
                        "postalCode": "62701",
                        "state": "IL"
                },
                "dateOfBirth": "19800101",
                "firstName": "John",
                "gender": "M",
                "lastName": "Smith",
                "middleName": "Robert",
                "ssn": "123456789"
        }
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 17: GET /insurance-discovery/check/v1/{discoveryId}
def request_17():
    """"""
    discovery_id = "12345678-abcd-4321-efgh-987654321abc"
    url = f"{BASE_URL}/insurance-discovery/check/v1/{discovery_id}"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 18: GET /payer/{stediId}
def request_18():
    """"""
    stedi_id = "QDTRP"
    url = f"{BASE_URL}/payer/{stedi_id}"
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


# Request 22: GET /electronic-remittance-advice/{transactionId}/pdf
def request_22():
    """"""
    # Replace this with the processed 835 ERA transactionId from Stedi.
    transaction_id = "b12a1241-3312-a3dc-aed2-1a30ca50cd63"
    url = f"{BASE_URL}/electronic-remittance-advice/{transaction_id}/pdf"
    headers = {
        "Authorization": get_api_key(),
        "Content-Type": "application/json"
    }
    params = {
        "logo": True
}
    response = requests.get(url, headers=headers, params=params)
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

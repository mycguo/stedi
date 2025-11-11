#!/usr/bin/env python3
"""
Sample requests for Stedi Healthcare API
Generated from OpenAPI specification
"""

import requests
import json

API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://healthcare.us.stedi.com/2024-04-01"


# Request 1: POST /change/medicalnetwork/claimstatus/v2
def request_1():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/claimstatus/v2"
    headers = {
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "provider": {},
        "subscriber": {},
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 4: POST /change/medicalnetwork/eligibility/v3/raw-x12
def request_4():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/eligibility/v3/raw-x12"
    headers = {
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
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
        "subscriber": {},
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 9: GET /change/medicalnetwork/reports/v2/123456789/277
def request_9():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/reports/v2/123456789/277"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 10: GET /change/medicalnetwork/reports/v2/123456789/835
def request_10():
    """"""
    url = f"{BASE_URL}/change/medicalnetwork/reports/v2/123456789/835"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 11: POST /coordination-of-benefits
def request_11():
    """"""
    url = f"{BASE_URL}/coordination-of-benefits"
    headers = {
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
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
        "subscriber": {},
        "tradingPartnerServiceId": "123456789"
}
    response = requests.post(url, headers=headers, json=payload)
    return response


# Request 14: GET /export/pdf
def request_14():
    """"""
    url = f"{BASE_URL}/export/pdf"
    headers = {
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 16: POST /insurance-discovery/check/v1
def request_16():
    """"""
    url = f"{BASE_URL}/insurance-discovery/check/v1"
    headers = {
        "X-API-Key": API_KEY,
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
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 18: GET /payer/123456789
def request_18():
    """"""
    url = f"{BASE_URL}/payer/123456789"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 19: GET /payers
def request_19():
    """"""
    url = f"{BASE_URL}/payers"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 20: GET /payers/csv
def request_20():
    """"""
    url = f"{BASE_URL}/payers/csv"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


# Request 21: GET /payers/search
def request_21():
    """"""
    url = f"{BASE_URL}/payers/search"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response


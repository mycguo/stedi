#!/usr/bin/env python3
"""Local verification for the Stedi request runner migration."""

from unittest.mock import MagicMock

import requests

import stedi_request


EXPECTED_REQUESTS = {
    1: ("POST", "/change/medicalnetwork/claimstatus/v2"),
    2: ("POST", "/change/medicalnetwork/claimstatus/v2/raw-x12"),
    3: ("POST", "/change/medicalnetwork/eligibility/v3"),
    4: ("POST", "/change/medicalnetwork/eligibility/v3/raw-x12"),
    5: ("POST", "/change/medicalnetwork/institutionalclaims/v1/raw-x12-submission"),
    6: ("POST", "/change/medicalnetwork/institutionalclaims/v1/submission"),
    7: ("POST", "/change/medicalnetwork/professionalclaims/v3/raw-x12-submission"),
    8: ("POST", "/change/medicalnetwork/professionalclaims/v3/submission"),
    9: ("GET", "/change/medicalnetwork/reports/v2/{transactionId}/277"),
    10: ("GET", "/change/medicalnetwork/reports/v2/{transactionId}/835"),
    11: ("POST", "/coordination-of-benefits"),
    12: ("POST", "/dental-claims/raw-x12-submission"),
    13: ("POST", "/dental-claims/submission"),
    14: ("GET", "/export/pdf"),
    15: ("GET", "/export/{transactionId}/1500/pdf"),
    16: ("POST", "/insurance-discovery/check/v1"),
    17: ("GET", "/insurance-discovery/check/v1/{discoveryId}"),
    18: ("GET", "/payer/{stediId}"),
    19: ("GET", "/payers"),
    20: ("GET", "/payers/csv"),
    21: ("GET", "/payers/search"),
    22: ("GET", "/electronic-remittance-advice/{transactionId}/pdf"),
}


def assert_request_registry() -> None:
    actual = {
        request_id: (request["method"], request["path"])
        for request_id, request in stedi_request.REQUESTS.items()
    }
    assert actual == EXPECTED_REQUESTS, f"REQUESTS drifted:\nactual={actual}"


def assert_all_request_functions_execute() -> None:
    requests.get = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    requests.post = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    stedi_request.get_api_key = MagicMock(return_value="test_key")

    for request_id, (method, _) in EXPECTED_REQUESTS.items():
        func = getattr(stedi_request, f"request_{request_id}")
        func()
        if method == "GET":
            assert requests.get.called, f"request_{request_id} did not call requests.get"
            requests.get.reset_mock()
        else:
            assert requests.post.called, f"request_{request_id} did not call requests.post"
            _, kwargs = requests.post.call_args
            assert kwargs.get("json"), f"request_{request_id} did not send a JSON payload"
            requests.post.reset_mock()


def assert_migrated_examples() -> None:
    requests.post = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    stedi_request.get_api_key = MagicMock(return_value="test_key")

    stedi_request.request_3()
    _, kwargs = requests.post.call_args
    eligibility_payload = kwargs["json"]
    assert eligibility_payload["provider"]["npi"] == "1999999984"
    assert eligibility_payload["provider"]["organizationName"] == "ACME Health Services"
    assert eligibility_payload["tradingPartnerServiceId"] == "AHS"

    requests.get = MagicMock(return_value=MagicMock(status_code=200, json=lambda: {}))
    stedi_request.request_22()
    args, kwargs = requests.get.call_args
    assert "/electronic-remittance-advice/" in args[0]
    assert kwargs["params"] == {"logo": True}


def main() -> None:
    assert_request_registry()
    assert_all_request_functions_execute()
    assert_migrated_examples()
    print("Verification passed: request registry, request functions, and migrated examples are current.")


if __name__ == "__main__":
    main()

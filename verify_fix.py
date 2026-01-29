
import requests
from unittest.mock import MagicMock

# Mock requests.post
requests.post = MagicMock()

# Import the code to test
import stedi_request
# Mock get_api_key
stedi_request.get_api_key = MagicMock(return_value="test_key")
from stedi_request import request_6, request_8

def verify_fix():
    print("Verifying Request 6 fix...")
    
    # Run the request function
    try:
        request_6()
    except Exception as e:
        print(f"Error running request_6: {e}")
        return

    # Check if requests.post was called
    if not requests.post.called:
        print("Error: requests.post was not called")
        return

    # Get the arguments passed to requests.post
    args, kwargs = requests.post.call_args
    payload = kwargs.get('json')

    if not payload:
        print("Error: No JSON payload found in requests.post call")
        return

    # Check for subscriber fields
    subscriber = payload.get('subscriber')
    if not subscriber:
        print("Error: 'subscriber' object missing in payload")
        return

    expected_fields = ['dateOfBirth', 'gender', 'address']
    missing_fields = [field for field in expected_fields if field not in subscriber]

    if missing_fields:
        print(f"Error: Missing fields in subscriber: {missing_fields}")
    else:
        print("Success: Subscriber contains dateOfBirth, gender, and address.")

    # Check address fields
    address = subscriber.get('address')
    if address:
        expected_addr_fields = ['address1', 'city', 'state', 'postalCode']
        missing_addr_fields = [field for field in expected_addr_fields if field not in address]
        if missing_addr_fields:
            print(f"Error: Missing fields in subscriber address: {missing_addr_fields}")
        else:
            print("Success: Subscriber address contains all required fields.")
            
    # Check for billing fields (Request 6 Internal Error Fix)
    billing = payload.get('billing')
    if not billing:
        print("Error: 'billing' object missing in payload")
    else:
        if billing.get('employerId'):
            print("Success: Billing object contains employerId.")
        else:
            print("Error: 'employerId' missing in billing")
            
        if billing.get('address'):
            print("Success: Billing object contains address.")
        else:
             print("Error: 'address' missing in billing")
    
    # Check for submitter contactInformation (Request 6 Internal Error Fix)
    submitter = payload.get('submitter')
    if submitter:
        contact_info = submitter.get('contactInformation')
        if contact_info:
            if contact_info.get('name'):
                print("Success: Submitter contactInformation contains name.")
            else:
                print("Error: 'name' missing in submitter contactInformation")
        else:
            print("Error: 'contactInformation' missing in submitter")
    else:
        print("Error: 'submitter' object missing in payload")

    print("\nPayload verification complete.")

    print("\n" + "="*50 + "\n")
    print("Verifying Request 8 fix...")
    
    # Reset mock
    requests.post.reset_mock()
    
    # Run request 8
    try:
        request_8()
    except Exception as e:
        print(f"Error running request_8: {e}")
        return

    # Check if requests.post was called
    if not requests.post.called:
        print("Error: requests.post was not called for request_8")
        return

    # Get the arguments passed to requests.post
    args, kwargs = requests.post.call_args
    payload = kwargs.get('json')

    if not payload:
        print("Error: No JSON payload found in requests.post call for request_8")
        return

    # Check for billing fields
    billing = payload.get('billing')
    if not billing:
        print("Error: 'billing' object missing in payload for request_8")
        return

    if billing.get('npi') and billing.get('organizationName'):
        print("Success: Billing object contains npi and organizationName.")
    else:
        print(f"Error: Missing fields in billing: {billing}")

    print("\nRequest 8 verification complete.")

    print("\n" + "="*50 + "\n")
    print("Verifying Request 8 contact info...")

    # Check for submitter contact info
    submitter = payload.get('submitter')
    if not submitter:
        print("Error: 'submitter' object missing in payload for request_8")
        return

    contact_info = submitter.get('contactInformation')
    if not contact_info:
        print("Error: 'contactInformation' object missing in submitter for request_8")
        return

    expected_contact_fields = ['name', 'phoneNumber']
    missing_contact_fields = [field for field in expected_contact_fields if field not in contact_info]

    if missing_contact_fields:
        print(f"Error: Missing fields in submitter.contactInformation: {missing_contact_fields}")
    else:
        print("Success: Submitter contact info contains name and phoneNumber.")

    print("\nRequest 8 contact info verification complete.")

    print("\n" + "="*50 + "\n")
    print("Verifying Request 8 billing address...")

    # Check for billing address
    billing = payload.get('billing')
    # Billing object existence already checked in previous step, but safe to re-get
    
    billing_address = billing.get('address')
    if not billing_address:
        print("Error: 'address' object missing in billing for request_8")
        return

    expected_addr_fields = ['address1', 'city', 'state', 'postalCode']
    missing_addr_fields = [field for field in expected_addr_fields if field not in billing_address]

    if missing_addr_fields:
        print(f"Error: Missing fields in billing.address: {missing_addr_fields}")
    else:
        print("Success: Billing address contains all required fields.")

    print("\nRequest 8 billing address verification complete.")

    print("\n" + "="*50 + "\n")
    print("Verifying Request 8 billing tax ID...")

    if billing.get('employerId'):
        print("Success: Billing object contains employerId.")
    else:
        print("Error: 'employerId' missing in billing for request_8")

    print("\nRequest 8 billing tax ID verification complete.")

    print("\n" + "="*50 + "\n")
    print("Verifying Request 8 submitter name...")

    if submitter.get('organizationName'):
        print("Success: Submitter object contains organizationName.")
    else:
        print("Error: 'organizationName' missing in submitter for request_8")

    print("\nRequest 8 submitter name verification complete.")

    print("\n" + "="*50 + "\n")
    print("Verifying Request 8 additional fixes (MeasurementUnit + Subscriber)...")

    # Check Measurement Unit
    claim_info = payload.get('claimInformation', {})
    service_lines = claim_info.get('serviceLines', [])
    if service_lines:
        prof_service = service_lines[0].get('professionalService', {})
        unit = prof_service.get('measurementUnit')
        if unit == 'UN':
            print("Success: MeasurementUnit is 'UN'.")
        else:
            print(f"Error: MeasurementUnit is '{unit}', expected 'UN'.")
    else:
        print("Error: No serviceLines found in claimInformation.")

    # Check Subscriber details
    subscriber = payload.get('subscriber', {})
    expected_sub_fields = ['dateOfBirth', 'gender', 'address']
    missing_sub_fields = [field for field in expected_sub_fields if field not in subscriber]
    
    if missing_sub_fields:
        print(f"Error: Missing fields in subscriber: {missing_sub_fields}")
    else:
         print("Success: Subscriber contains dateOfBirth, gender, and address.")

    print("\nRequest 8 additional fixes verification complete.")

if __name__ == "__main__":
    verify_fix()

#!/usr/bin/env python3
"""
Script to generate sample requests from Stedi Healthcare OpenAPI specifications.
"""

import argparse
import json
from typing import Dict, Any, List, Optional
from urllib.request import urlopen
from urllib.parse import urljoin

API_REFERENCE_URL = "https://www.stedi.com/docs/healthcare/api-reference"

OPENAPI_SPECS = {
    "healthcare": "https://raw.githubusercontent.com/Stedi/openApi/main/healthcare.json",
    "claim-attachments": "https://raw.githubusercontent.com/Stedi/openApi/main/claims.json",
    "batch-eligibility": "https://raw.githubusercontent.com/Stedi/openApi/main/manager.json",
    "transaction-enrollment": "https://raw.githubusercontent.com/Stedi/openApi/main/enrollment.json",
    "payers": "https://raw.githubusercontent.com/Stedi/openApi/main/payers.json",
    "event-destinations": "https://raw.githubusercontent.com/Stedi/openApi/main/event-destinations.json",
}


class SampleRequestGenerator:
    def __init__(
        self,
        openapi_url: str = OPENAPI_SPECS["healthcare"],
        spec_name: str = "healthcare",
    ):
        self.openapi_url = openapi_url
        self.spec_name = spec_name
        self.spec: Dict[str, Any] = {}
        self.base_url = ""
        self.schemas: Dict[str, Any] = {}
        
    def load_spec(self) -> None:
        """Load the OpenAPI specification from the URL."""
        print(f"Loading OpenAPI spec from {self.openapi_url}...")
        with urlopen(self.openapi_url, timeout=30) as response:
            self.spec = json.load(response)
        
        # Extract base URL
        if "servers" in self.spec and len(self.spec["servers"]) > 0:
            self.base_url = self.spec["servers"][0]["url"]
        
        # Extract schemas
        if "components" in self.spec and "schemas" in self.spec["components"]:
            self.schemas = self.spec["components"]["schemas"]
        
        print(f"Loaded spec with {len(self.spec.get('paths', {}))} paths")

    def get_example_value(self, source: Dict[str, Any]) -> Optional[Any]:
        """Return an OpenAPI example value from an object, if one is available."""
        if "example" in source:
            return source["example"]

        examples = source.get("examples")
        if isinstance(examples, dict):
            for example in examples.values():
                if isinstance(example, dict) and "value" in example:
                    return example["value"]

        return None
    
    def generate_sample_value(self, schema: Dict[str, Any], prop_name: str = "") -> Any:
        """Generate a sample value based on schema definition."""
        example_value = self.get_example_value(schema)
        if example_value is not None:
            return example_value

        if "type" not in schema:
            # Check for $ref
            if "$ref" in schema:
                ref_path = schema["$ref"].split("/")[-1]
                if ref_path in self.schemas:
                    return self.generate_sample_value(self.schemas[ref_path], prop_name)
            return None
        
        schema_type = schema["type"]
        
        if schema_type == "string":
            # Check for enum
            if "enum" in schema:
                return schema["enum"][0]
            
            # Check for format
            format_type = schema.get("format", "")
            if format_type == "date":
                return "2024-01-01"
            elif format_type == "date-time":
                return "2024-01-01T00:00:00Z"
            elif format_type == "email":
                return "example@example.com"
            elif format_type == "uri":
                return "https://example.com"
            
            # Use example if available
            if "example" in schema:
                return schema["example"]
            
            # Generate based on property name
            if "date" in prop_name.lower():
                return "20240101"
            elif "id" in prop_name.lower():
                return "123456789"
            elif "name" in prop_name.lower():
                return "EXAMPLE"
            elif "number" in prop_name.lower():
                return "123456"
            else:
                max_len = schema.get("maxLength", 10)
                return "example"[:max_len]
        
        elif schema_type == "integer":
            if "example" in schema:
                return schema["example"]
            return schema.get("minimum", 0)
        
        elif schema_type == "number":
            if "example" in schema:
                return schema["example"]
            return float(schema.get("minimum", 0.0))
        
        elif schema_type == "boolean":
            return True
        
        elif schema_type == "array":
            items_schema = schema.get("items", {})
            return [self.generate_sample_value(items_schema, prop_name)]
        
        elif schema_type == "object":
            result = {}
            properties = schema.get("properties", {})
            required = schema.get("required", [])
            
            # Include required properties
            for prop_name, prop_schema in properties.items():
                if prop_name in required:
                    result[prop_name] = self.generate_sample_value(prop_schema, prop_name)
            
            return result
        
        return None
    
    def generate_request_body(self, request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate sample request body from requestBody schema."""
        content = request_body.get("content", {})
        
        # Look for application/json content
        if "application/json" in content:
            media_type = content["application/json"]
            example_value = self.get_example_value(media_type)
            if example_value is not None:
                return example_value

            schema = media_type.get("schema", {})
            return self.generate_sample_value(schema)

        return None
    
    def generate_path_params(self, path: str, parameters: List[Dict[str, Any]]) -> Dict[str, str]:
        """Generate sample path parameters."""
        params = {}
        for param in parameters:
            if param.get("in") == "path":
                param_name = param["name"]
                param_schema = param.get("schema", {})
                params[param_name] = (
                    self.get_example_value(param)
                    or self.generate_sample_value(param_schema, param_name)
                )
        return params
    
    def generate_query_params(self, parameters: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate sample query parameters."""
        params = {}
        for param in parameters:
            if param.get("in") == "query":
                param_name = param["name"]
                param_schema = param.get("schema", {})
                required = param.get("required", False)
                if required:
                    params[param_name] = (
                        self.get_example_value(param)
                        or self.generate_sample_value(param_schema, param_name)
                    )
        return params
    
    def format_path(self, path_template: str, path_params: Dict[str, str]) -> str:
        """Format path template with parameters."""
        result = path_template
        for key, value in path_params.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result
    
    def generate_sample_request(self, path: str, method: str, operation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a sample request for a given path and method."""
        request_info = {
            "spec": self.spec_name,
            "method": method.upper(),
            "path": path,
            "summary": operation.get("summary", ""),
            "description": operation.get("description", ""),
            "base_url": self.base_url,
            "url": "",
            "headers": {},
            "query_params": {},
            "path_params": {},
            "body": None,
        }
        
        # Extract parameters
        parameters = operation.get("parameters", [])
        path_params = self.generate_path_params(path, parameters)
        query_params = self.generate_query_params(parameters)
        
        request_info["path_params"] = path_params
        request_info["query_params"] = query_params
        
        # Format path
        formatted_path = self.format_path(path, path_params)
        request_info["path"] = formatted_path
        
        # Build URL
        if self.base_url:
            request_info["url"] = urljoin(
                self.base_url.rstrip("/") + "/",
                formatted_path.lstrip("/"),
            )
        
        # Generate request body
        request_body = operation.get("requestBody")
        if request_body:
            body = self.generate_request_body(request_body)
            request_info["body"] = body
        
        # Add authentication header
        request_info["headers"]["Authorization"] = "YOUR_API_KEY_HERE"
        request_info["headers"]["Content-Type"] = "application/json"
        
        return request_info
    
    def generate_all_requests(self) -> List[Dict[str, Any]]:
        """Generate sample requests for all endpoints."""
        requests_list = []
        
        if "paths" not in self.spec:
            return requests_list
        
        for path, path_item in self.spec["paths"].items():
            for method in ["get", "post", "put", "patch", "delete"]:
                if method in path_item:
                    operation = path_item[method]
                    sample_request = self.generate_sample_request(path, method, operation)
                    requests_list.append(sample_request)
        
        return requests_list
    
    def print_request(self, request_info: Dict[str, Any], format_type: str = "python") -> None:
        """Print a formatted request."""
        print("\n" + "="*80)
        print(f"{request_info['method']} {request_info['path']}")
        if request_info.get("summary"):
            print(f"Summary: {request_info['summary']}")
        print("="*80)
        
        if format_type == "python":
            print("\n# Python request:")
            print("import requests")
            print()
            print(f"url = \"{request_info['url']}\"")
            print(f"headers = {json.dumps(request_info['headers'], indent=2)}")
            
            if request_info['query_params']:
                print(f"params = {json.dumps(request_info['query_params'], indent=2)}")
            
            if request_info['body']:
                print(f"payload = {json.dumps(request_info['body'], indent=2)}")
                print()
                print(f"response = requests.{request_info['method'].lower()}(url, headers=headers, json=payload)")
            elif request_info['query_params']:
                print()
                print(f"response = requests.{request_info['method'].lower()}(url, headers=headers, params=params)")
            else:
                print()
                print(f"response = requests.{request_info['method'].lower()}(url, headers=headers)")
        
        elif format_type == "curl":
            print("\n# cURL command:")
            curl_cmd = f"curl -X {request_info['method']}"
            
            for key, value in request_info['headers'].items():
                curl_cmd += f" -H \"{key}: {value}\""
            
            if request_info['query_params']:
                query_string = "&".join([f"{k}={v}" for k, v in request_info['query_params'].items()])
                curl_cmd += f" \"{request_info['url']}?{query_string}\""
            else:
                curl_cmd += f" \"{request_info['url']}\""
            
            if request_info['body']:
                body_json = json.dumps(request_info['body'])
                curl_cmd += f" -d '{body_json}'"
            
            print(curl_cmd)
        
        elif format_type == "json":
            print("\n# JSON representation:")
            print(json.dumps(request_info, indent=2))
    
    def save_to_file(self, requests_list: List[Dict[str, Any]], filename: str = "sample_requests.json") -> None:
        """Save all requests to a JSON file."""
        with open(filename, "w") as f:
            json.dump(requests_list, f, indent=2)
        print(f"\nSaved {len(requests_list)} sample requests to {filename}")
    
    def generate_python_script(self, requests_list: List[Dict[str, Any]], filename: str = "sample_requests.py") -> None:
        """Generate a Python script with all sample requests."""
        with open(filename, "w") as f:
            f.write('#!/usr/bin/env python3\n')
            f.write('"""\n')
            f.write('Sample requests for Stedi Healthcare API\n')
            f.write('Generated from OpenAPI specification\n')
            f.write('"""\n\n')
            f.write('import requests\n')
            f.write('import json\n\n')
            f.write('API_KEY = "YOUR_API_KEY_HERE"\n')
            f.write(f'API_REFERENCE_URL = "{API_REFERENCE_URL}"\n\n')
            
            for i, req in enumerate(requests_list):
                f.write(f'\n# Request {i+1}: {req["method"]} {req["path"]}\n')
                if req.get("summary"):
                    f.write(f'# {req["summary"]}\n')
                
                f.write(f'def request_{i+1}():\n')
                f.write(f'    """{req.get("summary", "Sample request")}"""\n')
                f.write(f'    url = "{req["url"]}"\n')
                f.write(f'    headers = {{\n')
                f.write(f'        "Authorization": API_KEY,\n')
                f.write(f'        "Content-Type": "application/json"\n')
                f.write(f'    }}\n')
                
                if req['query_params']:
                    f.write(f'    params = {json.dumps(req["query_params"], indent=8)}\n')
                
                if req['body']:
                    f.write(f'    payload = {json.dumps(req["body"], indent=8)}\n')
                    f.write(f'    response = requests.{req["method"].lower()}(url, headers=headers, json=payload)\n')
                elif req['query_params']:
                    f.write(f'    response = requests.{req["method"].lower()}(url, headers=headers, params=params)\n')
                else:
                    f.write(f'    response = requests.{req["method"].lower()}(url, headers=headers)\n')
                
                f.write(f'    return response\n\n')
        
        print(f"Generated Python script with {len(requests_list)} sample requests: {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate sample requests from the current Stedi Healthcare API reference."
    )
    parser.add_argument(
        "--spec",
        choices=[*OPENAPI_SPECS.keys(), "all"],
        default="healthcare",
        help="OpenAPI spec to load from the Stedi API reference. Default: healthcare.",
    )
    parser.add_argument(
        "--openapi-url",
        help="Override the OpenAPI URL. Cannot be used with --spec all.",
    )
    parser.add_argument(
        "--output-json",
        default="sample_requests.json",
        help="JSON output file. Default: sample_requests.json.",
    )
    parser.add_argument(
        "--output-python",
        default="sample_requests.py",
        help="Generated Python output file. Default: sample_requests.py.",
    )
    parser.add_argument(
        "--skip-python",
        action="store_true",
        help="Only write the JSON output file.",
    )
    parser.add_argument(
        "--list-specs",
        action="store_true",
        help="List known Stedi OpenAPI specs from the API reference and exit.",
    )
    args = parser.parse_args()

    if args.list_specs:
        print(f"API reference: {API_REFERENCE_URL}")
        for name, url in OPENAPI_SPECS.items():
            print(f"{name}: {url}")
        return

    if args.openapi_url and args.spec == "all":
        parser.error("--openapi-url cannot be used with --spec all")

    selected_specs = (
        OPENAPI_SPECS.items()
        if args.spec == "all"
        else [(args.spec, args.openapi_url or OPENAPI_SPECS[args.spec])]
    )
    requests_list: List[Dict[str, Any]] = []

    try:
        for spec_name, spec_url in selected_specs:
            generator = SampleRequestGenerator(spec_url, spec_name=spec_name)

            # Load the OpenAPI spec
            generator.load_spec()

            # Generate all sample requests
            print(f"\nGenerating sample requests for {spec_name}...")
            requests_list.extend(generator.generate_all_requests())

        print(f"\nGenerated {len(requests_list)} sample requests")
        
        # Print first few requests as examples
        print("\n" + "="*80)
        print("SAMPLE REQUESTS (showing first 3)")
        print("="*80)
        
        for req in requests_list[:3]:
            generator.print_request(req, format_type="python")
        
        if len(requests_list) > 3:
            print(f"\n... and {len(requests_list) - 3} more requests")
        
        # Save to files
        generator.save_to_file(requests_list, args.output_json)
        if not args.skip_python:
            generator.generate_python_script(requests_list, args.output_python)
        
        print("\nDone!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

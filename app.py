#!/usr/bin/env python3
"""
Streamlit app for running Stedi Healthcare API requests
"""

import streamlit as st
import requests
import json
import time
import inspect
import ast
import re
from stedi_request import REQUESTS, BASE_URL, get_api_key
import stedi_request

# Initialize request functions
for req_id in REQUESTS:
    func_name = f"request_{req_id}"
    REQUESTS[req_id]["func"] = getattr(stedi_request, func_name, None)

def extract_payload_from_function(func):
    """Extract payload from a request function."""
    if not func:
        return None
    
    try:
        source = inspect.getsource(func)
        
        # Find payload assignment
        if 'payload = {' not in source:
            return None
        
        # Extract the payload dictionary
        lines = source.split('\n')
        payload_start_idx = None
        
        for i, line in enumerate(lines):
            if 'payload = {' in line:
                payload_start_idx = i
                break
        
        if payload_start_idx is None:
            return None
        
        # Find the end of the payload dict by counting braces
        payload_lines = []
        brace_count = 0
        in_payload = False
        
        for i in range(payload_start_idx, len(lines)):
            line = lines[i]
            if 'payload = {' in line:
                in_payload = True
                # Extract just the dict part
                dict_start = line.find('{')
                payload_lines.append(line[dict_start:])
                brace_count = line[dict_start:].count('{') - line[dict_start:].count('}')
            elif in_payload:
                payload_lines.append(line)
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    break
        
        if not payload_lines:
            return None
        
        # Reconstruct payload code
        payload_code = '\n'.join(payload_lines)
        
        # Try to evaluate it safely
        try:
            # Create a minimal context
            context = {
                'BASE_URL': BASE_URL,
                'get_api_key': get_api_key,
            }
            local_vars = {}
            exec(f"payload = {payload_code}", context, local_vars)
            return local_vars.get('payload')
        except Exception as e:
            # Fallback: try to parse as JSON-like structure
            try:
                # Replace Python None with null, True/False with true/false
                json_str = payload_code.replace('None', 'null').replace('True', 'true').replace('False', 'false')
                # Remove trailing comma issues
                json_str = json_str.replace(',\n}', '\n}').replace(',\n]', '\n]')
                return json.loads(json_str)
            except:
                return None
    except Exception as e:
        return None

def execute_request_with_payload(req_id, payload, headers, url, method):
    """Execute a request with custom payload."""
    if method == "GET":
        return requests.get(url, headers=headers)
    elif method == "POST":
        return requests.post(url, headers=headers, json=payload)
    elif method == "PUT":
        return requests.put(url, headers=headers, json=payload)
    elif method == "PATCH":
        return requests.patch(url, headers=headers, json=payload)
    elif method == "DELETE":
        return requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")

# Page configuration
st.set_page_config(
    page_title="Stedi Healthcare API Request Runner",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'request_results' not in st.session_state:
    st.session_state.request_results = {}
if 'edited_payloads' not in st.session_state:
    st.session_state.edited_payloads = {}

# Title
st.title("🏥 Stedi Healthcare API Request Runner")
st.markdown("---")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Base URL
    st.text_input("Base URL", value=BASE_URL, disabled=True)
    
    st.markdown("---")
    
    # Request selection mode
    st.header("📋 Request Selection")
    run_mode = st.radio(
        "Run Mode",
        ["Single Request", "All Requests"],
        help="Choose to run a single request or all requests at once"
    )

# Main content area
if run_mode == "Single Request":
    st.header("Select a Request")
    
    # Create a selectbox with request details
    request_options = {
        f"{req_id}. {req_info['method']} {req_info['path']}": req_id
        for req_id, req_info in REQUESTS.items()
    }
    
    selected_request = st.selectbox(
        "Choose a request to run:",
        options=list(request_options.keys()),
        help="Select a request from the list"
    )
    
    selected_id = request_options[selected_request]
    req_info = REQUESTS[selected_id]
    
    # Show request details
    with st.expander("📄 Request Details", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Method:** {req_info['method']}")
            st.write(f"**Path:** {req_info['path']}")
        with col2:
            st.write(f"**ID:** {selected_id}")
            st.write(f"**Full URL:** {BASE_URL}{req_info['path']}")
        
        if req_info.get('description'):
            st.write(f"**Description:** {req_info['description']}")
        
        # Extract and display payload
        func = req_info['func']
        default_payload = None
        
        if func and req_info['method'] in ['POST', 'PUT', 'PATCH']:
            # Try to extract payload from function
            default_payload = extract_payload_from_function(func)
        
        # Initialize edited payload in session state if not exists
        payload_key = f"payload_{selected_id}"
        refresh_key = f"refresh_{selected_id}"
        
        # Check if refresh button was clicked
        if refresh_key not in st.session_state:
            st.session_state[refresh_key] = False
        
        if payload_key not in st.session_state.edited_payloads:
            st.session_state.edited_payloads[payload_key] = default_payload
        
        # Display editable payload
        if default_payload is not None:
            st.markdown("---")
            st.subheader("📝 Request Payload (Editable)")
            
            # Add refresh button
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button("🔄 Refresh from Code", key=f"refresh_btn_{selected_id}", help="Reload payload from function source code"):
                    st.session_state.edited_payloads[payload_key] = default_payload
                    st.session_state[refresh_key] = True
                    st.rerun()
            
            # Use text area for editing (more reliable than json_editor)
            payload_json = json.dumps(st.session_state.edited_payloads[payload_key], indent=2)
            edited_json = st.text_area(
                "Edit Payload (JSON):",
                value=payload_json,
                height=300,
                key=f"payload_text_{selected_id}",
                help="Modify the JSON payload below. Changes will be used when you click 'Run Request'."
            )
            try:
                parsed_payload = json.loads(edited_json)
                st.session_state.edited_payloads[payload_key] = parsed_payload
                st.success("✓ Valid JSON")
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {str(e)}")
                # Keep the previous valid payload
                if st.session_state.edited_payloads[payload_key] is None:
                    st.session_state.edited_payloads[payload_key] = default_payload
    
    # Run button
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        run_button = st.button("🚀 Run Request", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear Results", use_container_width=True)
    
    if clear_button:
        if selected_id in st.session_state.request_results:
            del st.session_state.request_results[selected_id]
        st.rerun()
    
    if run_button:
        with st.spinner(f"Running request {selected_id}..."):
            try:
                func = req_info['func']
                if not func:
                    st.error(f"Request function {selected_id} not found!")
                else:
                    # Get URL and headers from function
                    source = inspect.getsource(func)
                    url = BASE_URL + req_info['path']
                    headers = {
                        "Authorization": get_api_key(),
                        "Content-Type": "application/json"
                    }
                    
                    # Try to extract actual URL from function (handles path parameters)
                    try:
                        # Look for URL assignment in function source
                        for line in source.split('\n'):
                            if 'url = f"' in line:
                                # Extract f-string and evaluate it
                                # Find the f-string content
                                start_idx = line.find('f"') + 2
                                end_idx = line.rfind('"')
                                if end_idx > start_idx:
                                    url_template = line[start_idx:end_idx]
                                    # Replace {BASE_URL} with actual BASE_URL
                                    url_template = url_template.replace('{BASE_URL}', BASE_URL)
                                    
                                    # Extract any variables from the f-string
                                    # Look for variable references like {variable_name}
                                    var_pattern = r'\{(\w+)\}'
                                    variables = re.findall(var_pattern, url_template)
                                    
                                    # Try to get variable values from function source
                                    for var_name in variables:
                                        if var_name == 'BASE_URL':
                                            continue
                                        # Look for variable assignment
                                        for func_line in source.split('\n'):
                                            if f'{var_name} = ' in func_line:
                                                try:
                                                    var_value = func_line.split('=')[1].strip().strip('"').strip("'")
                                                    url_template = url_template.replace(f'{{{var_name}}}', var_value)
                                                except:
                                                    pass
                                    
                                    url = url_template
                                    break
                            elif 'url = "' in line and BASE_URL in line:
                                # Simple string URL
                                url_match = re.search(r'url = "([^"]+)"', line)
                                if url_match:
                                    url = url_match.group(1).replace('{BASE_URL}', BASE_URL)
                                    break
                    except Exception as e:
                        # Fallback to default URL construction
                        pass
                    
                    # Get edited payload or use default
                    payload_key = f"payload_{selected_id}"
                    payload = st.session_state.edited_payloads.get(payload_key)
                    
                    # If no edited payload, try to extract from function
                    if payload is None:
                        payload = extract_payload_from_function(func)
                    
                    start_time = time.time()
                    
                    # Execute request with payload
                    if req_info['method'] == 'GET':
                        response = requests.get(url, headers=headers)
                    elif req_info['method'] == 'POST':
                        response = requests.post(url, headers=headers, json=payload)
                    elif req_info['method'] == 'PUT':
                        response = requests.put(url, headers=headers, json=payload)
                    elif req_info['method'] == 'PATCH':
                        response = requests.patch(url, headers=headers, json=payload)
                    elif req_info['method'] == 'DELETE':
                        response = requests.delete(url, headers=headers)
                    else:
                        st.error(f"Unsupported method: {req_info['method']}")
                        st.stop()
                    
                    elapsed_time = time.time() - start_time
                    
                    # Store result
                    result = {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "elapsed_time": elapsed_time,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    try:
                        result["body"] = response.json()
                        result["body_type"] = "json"
                    except:
                        result["body"] = response.text
                        result["body_type"] = "text"
                    
                    st.session_state.request_results[selected_id] = result
                    st.success(f"Request completed in {elapsed_time:.2f}s")
                    st.rerun()
            except Exception as e:
                st.error(f"Error running request: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    # Display results
    if selected_id in st.session_state.request_results:
        result = st.session_state.request_results[selected_id]
        st.markdown("---")
        st.header("📊 Response")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            status_color = "🟢" if 200 <= result["status_code"] < 300 else "🔴" if result["status_code"] >= 400 else "🟡"
            st.metric("Status Code", f"{status_color} {result['status_code']}")
        with col2:
            st.metric("Response Time", f"{result['elapsed_time']:.2f}s")
        with col3:
            st.metric("Timestamp", result["timestamp"])
        
        # Response body
        st.subheader("Response Body")
        if result["body_type"] == "json":
            st.json(result["body"])
        else:
            st.code(result["body"], language="text")
        
        # Headers (collapsible)
        with st.expander("📋 Response Headers"):
            st.json(result["headers"])

else:  # All Requests mode
    st.header("Run All Requests")
    st.warning("⚠️ This will execute all 21 requests sequentially. This may take a while.")
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        run_all_button = st.button("🚀 Run All Requests", type="primary", use_container_width=True)
    with col2:
        clear_all_button = st.button("🗑️ Clear All Results", use_container_width=True)
    
    if clear_all_button:
        st.session_state.request_results = {}
        st.rerun()
    
    if run_all_button:
        progress_bar = st.progress(0)
        status_text = st.empty()
        results_container = st.container()
        
        total_requests = len(REQUESTS)
        completed = 0
        results_summary = []
        
        for req_id, req_info in REQUESTS.items():
            status_text.text(f"Running request {req_id}/{total_requests}: {req_info['method']} {req_info['path']}")
            
            try:
                func = req_info['func']
                if not func:
                    result = {
                        "id": req_id,
                        "status": "error",
                        "message": "Function not found",
                        "status_code": None,
                        "elapsed_time": 0
                    }
                else:
                    start_time = time.time()
                    response = func()
                    elapsed_time = time.time() - start_time
                    
                    try:
                        body = response.json()
                        body_type = "json"
                    except:
                        body = response.text[:500]  # Truncate long text
                        body_type = "text"
                    
                    result = {
                        "id": req_id,
                        "status": "success" if 200 <= response.status_code < 300 else "error",
                        "status_code": response.status_code,
                        "elapsed_time": elapsed_time,
                        "body_preview": body if body_type == "json" else body[:200],
                        "body_type": body_type
                    }
                    
                    # Store full result
                    st.session_state.request_results[req_id] = {
                        "status_code": response.status_code,
                        "headers": dict(response.headers),
                        "elapsed_time": elapsed_time,
                        "body": body if body_type == "json" else response.text,
                        "body_type": body_type,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                
                results_summary.append(result)
            except Exception as e:
                results_summary.append({
                    "id": req_id,
                    "status": "error",
                    "message": str(e),
                    "status_code": None,
                    "elapsed_time": 0
                })
            
            completed += 1
            progress_bar.progress(completed / total_requests)
        
        status_text.text("✅ All requests completed!")
        progress_bar.empty()
        status_text.empty()
        
        # Display summary
        st.markdown("---")
        st.header("📊 Results Summary")
        
        # Summary statistics
        success_count = sum(1 for r in results_summary if r.get("status") == "success")
        error_count = sum(1 for r in results_summary if r.get("status") == "error")
        total_time = sum(r.get("elapsed_time", 0) for r in results_summary)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Requests", total_requests)
        with col2:
            st.metric("✅ Successful", success_count, delta=f"{success_count/total_requests*100:.1f}%")
        with col3:
            st.metric("❌ Errors", error_count)
        with col4:
            st.metric("⏱️ Total Time", f"{total_time:.2f}s")
        
        # Results table
        st.subheader("Detailed Results")
        
        for result in results_summary:
            req_info = REQUESTS[result["id"]]
            with st.expander(
                f"{result['id']}. {req_info['method']} {req_info['path']} - "
                f"Status: {result.get('status_code', 'N/A')} "
                f"({result.get('elapsed_time', 0):.2f}s)",
                expanded=False
            ):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Status:** {result.get('status', 'unknown')}")
                    st.write(f"**Status Code:** {result.get('status_code', 'N/A')}")
                with col2:
                    st.write(f"**Elapsed Time:** {result.get('elapsed_time', 0):.2f}s")
                    if result["id"] in st.session_state.request_results:
                        st.write(f"**Timestamp:** {st.session_state.request_results[result['id']].get('timestamp', 'N/A')}")
                
                if result.get("body_preview"):
                    st.write("**Response Preview:**")
                    if result.get("body_type") == "json":
                        st.json(result["body_preview"])
                    else:
                        st.code(result["body_preview"], language="text")
                
                if result.get("message"):
                    st.error(f"Error: {result['message']}")
                
                # Link to full result
                if result["id"] in st.session_state.request_results:
                    st.write("**Full Response:**")
                    full_result = st.session_state.request_results[result["id"]]
                    if full_result.get("body_type") == "json":
                        st.json(full_result["body"])
                    else:
                        st.code(full_result["body"], language="text")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "Stedi Healthcare API Request Runner | "
    f"Base URL: {BASE_URL}"
    "</div>",
    unsafe_allow_html=True
)


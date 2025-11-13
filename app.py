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
import logging
from stedi_request import REQUESTS, BASE_URL, get_api_key
import stedi_request

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize request functions
for req_id in REQUESTS:
    func_name = f"request_{req_id}"
    REQUESTS[req_id]["func"] = getattr(stedi_request, func_name, None)

def extract_payload_from_function(func):
    """Extract payload from a request function."""
    logger.debug(f"extract_payload_from_function called for {func.__name__ if func else 'None'}")
    if not func:
        logger.debug("Function is None, returning None")
        return None
    
    try:
        source = inspect.getsource(func)
        logger.debug(f"Got source code, length: {len(source)}")
        
        # Find payload assignment - check for both 'payload = {' and 'payload={' patterns
        if 'payload = {' not in source and 'payload={' not in source:
            logger.debug("No 'payload = {' or 'payload={' found in source")
            return None
        logger.debug("Found payload assignment in source")
        
        # Extract the payload dictionary
        lines = source.split('\n')
        payload_start_idx = None
        
        for i, line in enumerate(lines):
            if 'payload = {' in line or 'payload={' in line:
                payload_start_idx = i
                break
        
        if payload_start_idx is None:
            logger.debug("payload_start_idx is None")
            return None
        logger.debug(f"Found payload at line {payload_start_idx + 1}")
        
        # Find the end of the payload dict by counting braces
        # Handle multiline strings (triple quotes) and nested structures
        payload_lines = []
        brace_count = 0
        in_payload = False
        in_triple_quote = False
        quote_char = None
        
        for i in range(payload_start_idx, len(lines)):
            line = lines[i]
            if 'payload = {' in line or 'payload={' in line:
                in_payload = True
                # Extract just the dict part
                dict_start = max(line.find('payload = {'), line.find('payload={'))
                if dict_start == -1:
                    dict_start = line.find('{')
                else:
                    dict_start = line.find('{', dict_start)
                payload_lines.append(line[dict_start:])
                brace_count = line[dict_start:].count('{') - line[dict_start:].count('}')
            elif in_payload:
                # Check for triple quotes (multiline strings)
                stripped = line.strip()
                if '"""' in stripped or "'''" in stripped:
                    # Count triple quotes
                    triple_double = stripped.count('"""')
                    triple_single = stripped.count("'''")
                    if triple_double % 2 == 1:
                        in_triple_quote = not in_triple_quote
                        quote_char = '"""'
                    elif triple_single % 2 == 1:
                        in_triple_quote = not in_triple_quote
                        quote_char = "'''"
                
                # Don't count braces inside triple-quoted strings
                if not in_triple_quote:
                    brace_count += line.count('{') - line.count('}')
                
                payload_lines.append(line)
                
                if brace_count == 0 and not in_triple_quote:
                    break
        
        if not payload_lines:
            logger.debug("No payload_lines extracted")
            return None
        logger.debug(f"Extracted {len(payload_lines)} lines of payload code")
        
        # Reconstruct payload code (with indentation) for variable detection
        payload_code_with_indent = '\n'.join(payload_lines)
        
        # Extract variable definitions that might be used in payload (like x12_content)
        # Look for variable assignments before payload, especially multiline strings
        variable_definitions = []
        i = 0
        while i < payload_start_idx:
            line = lines[i]
            stripped = line.strip()
            
            # Skip comments and empty lines
            if stripped.startswith('#') or not stripped:
                i += 1
                continue
            
            # Look for variable assignments with triple-quoted strings (multiline)
            if '=' in stripped and ('"""' in stripped or "'''" in stripped):
                var_parts = stripped.split('=', 1)
                if len(var_parts) == 2:
                    var_name = var_parts[0].strip()
                    # Check if variable name is valid and might be used in payload
                    if var_name and var_name.replace('_', '').isalnum():
                        # Check if this variable is referenced in payload_code
                        if var_name in payload_code_with_indent:
                            logger.debug(f"Found variable used in payload: {var_name}")
                            # Extract the full multiline string
                            var_lines = [line]
                            quote_type = '"""' if '"""' in stripped else "'''"
                            quote_count = stripped.count(quote_type)
                            
                            # If quotes are not closed on this line, find closing
                            if quote_count % 2 == 1:
                                i += 1
                                while i < payload_start_idx:
                                    var_lines.append(lines[i])
                                    if quote_type in lines[i]:
                                        break
                                    i += 1
                            variable_definitions.extend(var_lines)
                            logger.debug(f"Extracted {len(var_lines)} lines for variable {var_name}")
            i += 1
        
        # Strip leading indentation from payload lines (they're indented in the function)
        # Find the minimum indentation level
        if payload_lines:
            min_indent = min(len(line) - len(line.lstrip()) for line in payload_lines if line.strip())
            payload_lines_stripped = [line[min_indent:] if len(line) > min_indent else line for line in payload_lines]
            payload_code = '\n'.join(payload_lines_stripped)
        
        # Strip indentation from variable definitions
        # For multiline strings, Python preserves content exactly, so we can strip all indentation
        if variable_definitions:
            logger.debug(f"Processing {len(variable_definitions)} variable definition lines")
            # Find minimum indentation to strip
            var_min_indent = min(len(line) - len(line.lstrip()) for line in variable_definitions if line.strip())
            logger.debug(f"Variable min indent: {var_min_indent}")
            
            # Strip the minimum indentation from all lines
            variable_definitions_stripped = []
            for line in variable_definitions:
                if line.strip():
                    # Strip the minimum indent amount
                    if len(line) > var_min_indent:
                        variable_definitions_stripped.append(line[var_min_indent:])
                    else:
                        variable_definitions_stripped.append(line.lstrip())
                else:
                    variable_definitions_stripped.append('')
            
            # Combine variable definitions and payload
            full_code = '\n'.join(variable_definitions_stripped + payload_lines_stripped)
            logger.debug(f"Full code length: {len(full_code)} characters")
            logger.debug(f"First 500 chars:\n{full_code[:500]}")
            logger.debug(f"Last 200 chars:\n{full_code[-200:]}")
        else:
            full_code = payload_code
            logger.debug("No variable definitions found")
            logger.debug(f"Payload code (first 300 chars):\n{payload_code[:300]}")
        
        # Try to evaluate it safely
        context = {
            'BASE_URL': BASE_URL,
            'get_api_key': get_api_key,
        }
        
        # Try multiple approaches
        attempts = [
            (full_code, "full code with variables"),
            (payload_code, "payload code only"),
        ]
        
        for code_to_exec, description in attempts:
            try:
                logger.debug(f"Trying to exec: {description}")
                logger.debug(f"Code preview (first 300 chars):\n{code_to_exec[:300]}")
                local_vars = {}
                # Execute the code
                exec(code_to_exec, context, local_vars)
                logger.debug(f"Variables after exec: {list(local_vars.keys())}")
                result = local_vars.get('payload')
                logger.debug(f"Exec completed. Result: {result is not None}, type: {type(result)}")
                if result is not None:
                    logger.debug(f"Result keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
                if result is not None and isinstance(result, dict):
                    logger.debug(f"SUCCESS: Extracted payload with {len(result)} keys")
                    return result
                # Fallback: if x12_content exists but payload doesn't, create it manually
                if 'x12_content' in local_vars and result is None:
                    logger.debug("x12_content exists but payload doesn't, creating manually")
                    try:
                        manual_payload = {"x12": local_vars['x12_content']}
                        logger.debug(f"Created manual payload with {len(manual_payload)} keys")
                        return manual_payload
                    except Exception as e:
                        logger.debug(f"Failed to create manual payload: {e}")
            except SyntaxError as e:
                logger.debug(f"SyntaxError with {description}: {e}")
                logger.debug(f"Code that failed (first 300 chars):\n{code_to_exec[:300]}")
                # Try fixing indentation - remove ALL leading whitespace from each line
                try:
                    fixed_lines = []
                    for line in code_to_exec.split('\n'):
                        if line.strip():
                            # Remove all leading whitespace
                            fixed_lines.append(line.lstrip())
                        else:
                            fixed_lines.append('')
                    fixed_code = '\n'.join(fixed_lines)
                    logger.debug(f"Trying fixed code (first 500 chars):\n{fixed_code[:500]}")
                    logger.debug(f"Fixed code (last 200 chars):\n{fixed_code[-200:]}")
                    local_vars = {}
                    exec(fixed_code, context, local_vars)
                    logger.debug(f"Variables after exec: {list(local_vars.keys())}")
                    result = local_vars.get('payload')
                    logger.debug(f"Fixed code exec completed. Result: {result is not None}, type: {type(result)}")
                    if result is not None:
                        logger.debug(f"Fixed result keys: {list(result.keys()) if isinstance(result, dict) else 'N/A'}")
                    if result is not None and isinstance(result, dict):
                        logger.debug(f"SUCCESS: Fixed code worked, payload has {len(result)} keys")
                        return result
                    else:
                        # Check what variables were created and their values
                        logger.debug(f"Variables created: {list(local_vars.keys())}")
                        if 'x12_content' in local_vars:
                            logger.debug(f"x12_content exists, length: {len(local_vars['x12_content']) if isinstance(local_vars['x12_content'], str) else 'N/A'}")
                        # Try to manually create payload if x12_content exists
                        if 'x12_content' in local_vars and 'payload' not in local_vars:
                            logger.debug("x12_content exists but payload doesn't, trying to create it manually")
                            try:
                                manual_payload = {"x12": local_vars['x12_content']}
                                logger.debug(f"Created manual payload with {len(manual_payload)} keys")
                                return manual_payload
                            except Exception as e:
                                logger.debug(f"Failed to create manual payload: {e}")
                except Exception as fix_error:
                    logger.debug(f"Fixed code also failed: {type(fix_error).__name__}: {fix_error}")
                    import traceback
                    logger.debug(f"Traceback: {traceback.format_exc()}")
                    pass
            except Exception as e:
                # Continue to next attempt
                logger.debug(f"Exception with {description}: {type(e).__name__}: {e}")
                import traceback
                logger.debug(f"Traceback: {traceback.format_exc()}")
                pass
        
        # Fallback: try to parse as JSON-like structure (won't work for multiline strings)
        try:
            # Replace Python None with null, True/False with true/false
            json_str = payload_code.replace('None', 'null').replace('True', 'true').replace('False', 'false')
            # Remove trailing comma issues
            json_str = json_str.replace(',\n}', '\n}').replace(',\n]', '\n]')
            return json.loads(json_str)
        except:
            # Last resort: try to actually call the function and extract payload
            # But this won't work if function requires API key, so we'll return None
            return None
    except Exception as e:
        # If all else fails, return None
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
            # Show extraction debug info
            if default_payload is None:
                with st.expander("⚠️ Payload Extraction Debug", expanded=False):
                    st.warning("Payload extraction failed. Debug info:")
                    try:
                        source = inspect.getsource(func)
                        has_payload = 'payload = {' in source or 'payload={' in source
                        st.write(f"- Function: {func.__name__}")
                        st.write(f"- Has 'payload = {{': {has_payload}")
                        st.write(f"- Source length: {len(source)} characters")
                        if has_payload:
                            # Show where payload is
                            lines = source.split('\n')
                            for i, line in enumerate(lines):
                                if 'payload = {' in line or 'payload={' in line:
                                    st.write(f"- Payload found at line {i+1}")
                                    st.code(line[:100] + "..." if len(line) > 100 else line)
                                    break
                    except Exception as e:
                        st.write(f"- Error getting source: {e}")
        
        # Initialize edited payload in session state if not exists
        payload_key = f"payload_{selected_id}"
        refresh_key = f"refresh_{selected_id}"
        
        # Check if refresh button was clicked
        if refresh_key not in st.session_state:
            st.session_state[refresh_key] = False
        
        if payload_key not in st.session_state.edited_payloads:
            # Use default_payload if available, otherwise use empty dict
            st.session_state.edited_payloads[payload_key] = default_payload if default_payload is not None else {}
        
        # Display editable payload (always show for POST/PUT/PATCH requests)
        if req_info['method'] in ['POST', 'PUT', 'PATCH']:
            st.markdown("---")
            # Put refresh button on same line as header
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader("📝 Request Payload (Editable)")
            with col2:
                if st.button("🔄 Refresh from Code", key=f"refresh_btn_{selected_id}", help="Reload payload from function source code", use_container_width=True):
                    # Try to extract payload again
                    refreshed_payload = extract_payload_from_function(func)
                    if refreshed_payload is not None:
                        st.session_state.edited_payloads[payload_key] = refreshed_payload
                    elif default_payload is not None:
                        st.session_state.edited_payloads[payload_key] = default_payload
                    else:
                        st.session_state.edited_payloads[payload_key] = {}
                    st.session_state[refresh_key] = True
                    st.rerun()
            
            # Use text area for editing (more reliable than json_editor)
            current_payload = st.session_state.edited_payloads[payload_key]
            if current_payload is not None and len(current_payload) > 0:
                payload_json = json.dumps(current_payload, indent=2)
            else:
                # Show a helpful message if payload is empty
                if default_payload is None:
                    payload_json = "{}"
                else:
                    payload_json = json.dumps(default_payload, indent=2) if default_payload else "{}"
            
            edited_json = st.text_area(
                "Edit Payload (JSON):",
                value=payload_json,
                height=300,
                key=f"payload_text_{selected_id}",
                help="Modify the JSON payload below. Changes will be used when you click 'Run Request'."
            )
            try:
                # Strip whitespace and check if empty
                edited_json_stripped = edited_json.strip()
                
                if not edited_json_stripped or edited_json_stripped == "{}":
                    if default_payload is not None:
                        st.warning("⚠️ Payload is empty. Using default payload.")
                        parsed_payload = default_payload
                    else:
                        st.warning("⚠️ Payload is empty. Please enter a valid JSON payload.")
                        parsed_payload = {}
                else:
                    parsed_payload = json.loads(edited_json_stripped)
                    if not isinstance(parsed_payload, dict):
                        st.error("Payload must be a JSON object (dict), not an array or primitive value.")
                        parsed_payload = current_payload if current_payload is not None and len(current_payload) > 0 else (default_payload if default_payload is not None else {})
                    else:
                        st.session_state.edited_payloads[payload_key] = parsed_payload
                        st.success("✓ Valid JSON")
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON format: {str(e)}")
                # Keep the previous valid payload
                if current_payload is None or len(current_payload) == 0:
                    st.session_state.edited_payloads[payload_key] = default_payload if default_payload is not None else {}
    
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
                    logger.debug(f"Initial payload from session: {payload is not None}, type: {type(payload) if payload is not None else None}")
                    
                    # If no edited payload, try to extract from function
                    if payload is None or (isinstance(payload, dict) and len(payload) == 0):
                        logger.debug("Payload is None or empty, attempting extraction")
                        payload = extract_payload_from_function(func)
                        logger.debug(f"After extraction: {payload is not None}, type: {type(payload) if payload is not None else None}")
                        # If extraction failed, try to get default from the payload editor
                        if payload is None or (isinstance(payload, dict) and len(payload) == 0):
                            logger.debug(f"Extraction failed, trying default_payload: {default_payload is not None}")
                            # Check if there's a default payload that was extracted earlier
                            if default_payload is not None:
                                payload = default_payload
                                st.session_state.edited_payloads[payload_key] = payload
                                logger.debug(f"Using default_payload: {len(payload)} keys")
                    
                    # Validate payload for POST/PUT/PATCH requests
                    if req_info['method'] in ['POST', 'PUT', 'PATCH']:
                        logger.debug(f"Validating payload for {req_info['method']} request")
                        logger.debug(f"Payload: {payload}, type: {type(payload)}, is_empty: {isinstance(payload, dict) and len(payload) == 0 if isinstance(payload, dict) else 'N/A'}")
                        if payload is None or (isinstance(payload, dict) and len(payload) == 0):
                            st.error("⚠️ Error: No payload found or payload is empty.")
                            st.info("💡 **Solution:** Click the '🔄 Refresh from Code' button above to reload the payload from the function, or manually enter/edit the JSON payload in the text area below.")
                            # Log debug info
                            with st.expander("🔍 Debug Information"):
                                st.code(f"Payload: {payload}\nType: {type(payload)}\nDefault payload available: {default_payload is not None}\nFunction: {func.__name__ if func else 'None'}")
                            st.stop()
                        # Ensure payload is a valid dict/object (not empty string or None)
                        if not isinstance(payload, dict):
                            st.error(f"Error: Invalid payload type. Expected dict, got {type(payload)}")
                            st.info("💡 **Solution:** Make sure the payload in the text area is a valid JSON object.")
                            st.stop()
                    
                    start_time = time.time()
                    
                    # Log the request details
                    logger.debug(f"Making {req_info['method']} request to {url}")
                    logger.debug(f"Payload keys: {list(payload.keys()) if isinstance(payload, dict) else 'N/A'}")
                    logger.debug(f"Payload preview: {json.dumps(payload, indent=2)[:500]}...")
                    
                    # Show debug info in UI (collapsible)
                    with st.expander("🔍 Request Debug Info", expanded=False):
                        st.write("**URL:**", url)
                        st.write("**Method:**", req_info['method'])
                        st.write("**Payload Type:**", type(payload).__name__)
                        st.write("**Payload Keys:**", list(payload.keys()) if isinstance(payload, dict) else "N/A")
                        st.write("**Payload Size:**", len(json.dumps(payload)) if payload else 0, "bytes")
                        st.json(payload)
                    
                    # Execute request with payload
                    if req_info['method'] == 'GET':
                        response = requests.get(url, headers=headers)
                    elif req_info['method'] == 'POST':
                        # Only send json if payload exists and is not empty
                        if payload:
                            logger.debug("Sending POST request with JSON payload")
                            response = requests.post(url, headers=headers, json=payload)
                        else:
                            logger.debug("Sending POST request without payload")
                            response = requests.post(url, headers=headers)
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


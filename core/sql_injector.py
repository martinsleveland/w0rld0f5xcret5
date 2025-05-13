import requests
from urllib.parse import urlparse, parse_qs, urlencode

# Basic payloads to test for sql injection
payloads = ["'", 
            "--",
            "' OR '1='1",
            "' AND SLEEP(3)--",
            "\" OR \"\"=\""
            ]

error_signatures = [
    "you have an error in your sql syntax",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "mysql_fetch",
    "ORA-",
    "SQLite",
    "syntax error"
]

def scan_sql_injection(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if not query:
        return "[!] No query parameters found to test!"
    
    results = []

    for param in query:
        original = query[param][0]
        for payload in payloads:
            test_query = query.copy()
            test_query[param] = original + payload
            full_url = f"[parsed.scheme]://{parsed.netloc}{parsed.path}?"

            try:
                res = requests.get(full_url, timeout=5)
                for err in error_signatures:
                    if err.lower() in res.text.lower():
                        results.append(f"[+] Potential SQLi in '{param}' with payload: {payload}")
                        break
            except requests.RequestException as e:
                results.append(f"[!] Request failed: {e}")

    if not results:
        return "[!] No potential SQL injections found!"
    return "\n".join(results)
import requests

def subdomain_enum(domain: str) -> str:
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    output = f"[*] Getting subdomains for {domain}...\n"

    try:
        res = requests.get(url, timeout=10)
        if res.status_code != 200:
            return f"[!] Error: {res.status_code} - {res.reason}"

        data = res.json()
        subdomains = set()

        for entry in data:
            name = entry.get("name_value")
            if name:
                for sub in name.split('\n'):
                    if sub.endswith(domain):
                        subdomains.add(sub.strip())

        if subdomains:
            for sub in sorted(subdomains):
                output += f"[+] {sub}\n"
        else:
            output += "[!] No subdomains found.\n"

        return output

    except Exception as e:
        return f"[!] Error: {e}"

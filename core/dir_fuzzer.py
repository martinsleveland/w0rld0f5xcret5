import os
import httpx
import asyncio

extensions = ["", ".php", ".bak", ".html", ".zip", ".old", ".asp", ".aspx", ".txt"]

async def fetch_url(client, url):
    try:
        response = await client.get(url, follow_redirects=True)
        status = response.status_code

        if status in [200, 301, 302, 403]:
            return f"[+] {status} → {url}"
    except httpx.RequestError:
        return None

async def dir_fuzzer(base_url: str, wordlist_path: str) -> str:
    output = f"[*] Starting fuzz on {base_url} using wordlist {wordlist_path}...\n"

    wordlist_path = os.path.expanduser(wordlist_path)
    if not os.path.isfile(wordlist_path):
        return f"[!] Error: Wordlist not found at {wordlist_path}"

    try:
        with open(wordlist_path, 'r') as f:
            paths = [line.strip() for line in f if line.strip()]
    except Exception as e:
        return f"[!] Error reading wordlist: {e}"

    if not base_url.endswith('/'):
        base_url += '/'

    async with httpx.AsyncClient(timeout=5.0) as client:
        tasks = []
        for path in paths:
            for ext in extensions:
                full_path = f"{path}{ext}"
                url = base_url + full_path
                tasks.append(fetch_url(client, url))

        results = await asyncio.gather(*tasks)

    for result in results:
        if result:
            output += result + "\n"

    return output if "[+]" in output else "[!] No valid directories found."

def fuzz_directories(target_url: str, wordlist_path: str) -> str:
    try:
        return asyncio.run(dir_fuzzer(target_url, wordlist_path))
    except Exception as e:
        return f"[!] Async error: {e}"

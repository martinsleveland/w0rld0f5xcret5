import os
import httpx
import asyncio
from rich.console import Console

def fuzz_directories():
    extensions = ["", ".php", ".bak", ".hmtl", ".zip", ".old", ".asp", ".aspx", ".txt"]
    
    console = Console()
    
    async def fetch_url(client, url):
        try:
            response = await client.get(url, follow_redirects=True)
            status = response.status_code
    
            if status in [200, 301, 302, 403]:
                console.print(f"[bold green]{status} {url}[/bold green]")
            return url, status
        
        except httpx.RequestError as e:
            return url, None
        
    async def dir_fuzzer(base_url: str, wordlist_path: str):
        console.print(f"[bold blue] Starting fuzz on {base_url} using wordlist {wordlist_path}...[/bold blue]")
    
        try:
            wordlist_path = os.path.expanduser(wordlist_path)
            if not os.path.isfile(wordlist_path):
                console.print(f"[bold red]Error: Wordlist not found at {wordlist_path}[/bold red]")
                return
            with open(wordlist_path, 'r') as f:
                paths = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            console.print(f"[bold red]Error: Wordlist not found at {wordlist_path}[/bold red]")
            return
        if not base_url.endswith('/'):
            base_url += '/'
    
        async with httpx.AsyncClient(timeout=5.0) as client:
            tasks = []
            for path in paths:
                for ext in extensions:
                    full_path = f"{path}{ext}"
                    url = base_url + full_path
                    tasks.append(fetch_url(client, url))
    
            await asyncio.gather(*tasks)
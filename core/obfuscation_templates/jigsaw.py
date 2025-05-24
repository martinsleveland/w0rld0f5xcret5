import os
import random

def jigsaw_obfuscation(input_path, output_path, chunk_size=64):
    try:
        with open(input_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"[!] Input file not found: {input_path}")

    if not data:
        raise ValueError("[!] Input file is empty!")

    # Split into chunks
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    indexes = list(range(len(chunks)))
    random.shuffle(indexes)

    obfuscated_chunks = [chunks[i] for i in indexes]

    metadata = {
        "order": indexes,
        "chunk_size": chunk_size,
        "total_chunks": len(chunks)
    }

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write chunks to output file
    with open(output_path, 'wb') as f:
        for chunk in obfuscated_chunks:
            f.write(chunk)

    # Save metadata (or return it)
    metadata_path = output_path + ".meta"
    with open(metadata_path, 'w') as meta:
        meta.write(f"{metadata}")

    return f"[+] Jigsaw obfuscation complete.\nOutput: {output_path}\nMetadata: {metadata_path}"

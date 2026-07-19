import os

search_dirs = [
    r"C:\Users\HP\.gemini\antigravity\brain\71e7b1d1-f50b-477e-a713-942e8319b97d",
    r"c:\Users\HP\OneDrive\Documents\AG2OSINTNEOMAXX"
]

print("Checking for Google API credentials or local email archives...")

for s_dir in search_dirs:
    if not os.path.exists(s_dir):
        continue
    for root, dirs, files in os.walk(s_dir):
        for file in files:
            # Check for credential files or email archives
            if file in ['credentials.json', 'token.json', 'service_account.json'] or file.lower().endswith(('.eml', '.mbox', '.pst', '.msg')):
                print(f"FOUND: {os.path.join(root, file)}")

print("Done checking.")

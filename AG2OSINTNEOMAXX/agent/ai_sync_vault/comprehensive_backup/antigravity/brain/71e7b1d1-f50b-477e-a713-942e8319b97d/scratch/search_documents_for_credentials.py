import os

documents_dir = r"C:\Users\HP\OneDrive\Documents"

print(f"Scanning Documents folder for Google credentials: {documents_dir}")
found = False
if os.path.exists(documents_dir):
    for root, dirs, files in os.walk(documents_dir):
        # limit depth if needed, but we can do a quick search
        for file in files:
            if file in ['credentials.json', 'token.json']:
                print(f"FOUND CREDENTIALS: {os.path.join(root, file)}")
                found = True
else:
    print("Documents directory does not exist.")

if not found:
    print("No credentials found in Documents.")

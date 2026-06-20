import os
import zipfile

def zip_folder(folder_path, output_path):
    # Directories to exclude
    exclude_dirs = {'venv', '__pycache__', 'tiles_temp', '.git'}
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                file_path = os.path.join(root, file)
                # Ensure we don't zip the output zip itself
                if file_path == output_path:
                    continue
                # Determine the relative path inside the zip file
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
                print(f"Added {arcname}")

if __name__ == "__main__":
    source = r"C:\Users\HP\.gemini\antigravity-ide\scratch\osint-agent"
    output = r"C:\Users\HP\.gemini\antigravity-ide\scratch\OSINT_VAULT_BACKUP.zip"
    print(f"Zipping {source} to {output} (excluding venv, .git, etc.)...")
    zip_folder(source, output)
    print("Zip complete.")

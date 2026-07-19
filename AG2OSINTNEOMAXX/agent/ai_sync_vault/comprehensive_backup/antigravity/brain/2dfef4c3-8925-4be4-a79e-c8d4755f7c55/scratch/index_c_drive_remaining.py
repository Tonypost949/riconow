import os
import csv
import datetime

# Root path
root_drive = "C:\\"

# Root folders to exclude
exclude_roots = {
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users",
    "C:\\System Volume Information",
    "C:\\$Recycle.Bin",
    "C:\\$WinREAgent",
    "C:\\Config.Msi",
    "C:\\Recovery",
    "C:\\Documents and Settings"
}

# CSV output path
output_csv = r"C:\Users\HP\.gemini\antigravity\brain\2dfef4c3-8925-4be4-a79e-c8d4755f7c55\scratch\remaining_c_files.csv"

print("[*] Starting C: drive scan (excluding system, program, and user folders)...")

csv_columns = ["drive_letter", "file_path", "file_name", "extension", "size_kb", "last_modified"]

with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(csv_columns)
    
    # 1. Scan files directly in C:\ root
    try:
        for entry in os.scandir(root_drive):
            if entry.is_file():
                try:
                    stat = entry.stat()
                    size_kb = round(stat.st_size / 1024, 2)
                    last_mod = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                    name, ext = os.path.splitext(entry.name)
                    writer.writerow(["C", entry.path, entry.name, ext, size_kb, last_mod])
                except Exception as e:
                    pass
    except Exception as e:
        print(f"[!] Error scanning C:\\ root files: {e}")

    # 2. Scan subdirectories in C:\ that are not excluded
    try:
        for entry in os.scandir(root_drive):
            if entry.is_dir():
                # Check if it starts with any of the excluded roots
                normalized_path = os.path.abspath(entry.path)
                should_exclude = False
                for exclude in exclude_roots:
                    if normalized_path.lower() == exclude.lower() or normalized_path.lower().startswith(exclude.lower() + os.sep):
                        should_exclude = True
                        break
                
                if should_exclude:
                    continue
                
                print(f"[*] Scanning folder: {normalized_path}")
                for root, dirs, files in os.walk(normalized_path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        try:
                            stat = os.stat(full_path)
                            size_kb = round(stat.st_size / 1024, 2)
                            last_mod = datetime.datetime.fromtimestamp(stat.st_mtime, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                            name, ext = os.path.splitext(file)
                            writer.writerow(["C", full_path, file, ext, size_kb, last_mod])
                        except Exception as e:
                            pass
    except Exception as e:
        print(f"[!] Error during directory walk: {e}")

print(f"[+] Scan complete. Output written to: {output_csv}")

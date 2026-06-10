import os
import csv
from pathlib import Path

def create_log_file():
    # Define directory and file path
    data_dir = Path("data")
    file_path = data_dir / "sample_execution_logs.csv"
    
    # Ensure the directory exists
    data_dir.mkdir(exist_ok=True)
    
    # Define header and sample data
    header = ["timestamp", "log_level", "module", "execution_time_ms", "status"]
    sample_data = [
        ["2026-06-10 07:30:00", "INFO", "data_ingestion", 145, "SUCCESS"],
        ["2026-06-10 07:30:05", "INFO", "calculation_engine", 89, "SUCCESS"]
    ]
    
    # Write to the CSV file
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(sample_data)
        print(f"Successfully created: {file_path}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    create_log_file()
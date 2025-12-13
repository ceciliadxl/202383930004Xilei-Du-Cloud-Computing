# Streaming Data Processing

## Introduction

This experiment demonstrates how to use streaming for large data processing:
1. Database streaming processing: Process large datasets using streaming
2. S3 data download and streaming processing: Download large files from Amazon S3 and process incrementally



## Files

### 1. `database_streaming.py`
Process data using database streaming.

**Features:**
- Connect to PostgreSQL database
- Use `fetchone()` to read data row by row
- Use `fetchmany()` to read data in batches
- Statistics for processing time and speed

**Usage:**
```python
db_config = {
    'dbname': 'your_db',
    'user': 'your_user',
    'password': 'your_password',
    'host': 'your_host',
    'port': 5432
}

python database_streaming.py
```

### 2. `s3_streaming.py`
Download data from Amazon S3 and process using streaming method.

**Features:**
- Download large files from S3
- Process file line by line
- Process file in chunks (memory-friendly)
- Show download and processing progress

**Usage:**
```python
s3_config = {
    'bucket_name': 'my-bucket',
    'file_name': 'large-data-file.csv',
    'local_path': '/tmp/large-data-file.csv',
    'region_name': 'us-east-1'
}

python s3_streaming.py
```

### 3. `requirements.txt`
Project dependencies.

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## Environment Setup

### 1. Python Environment
- Python 3.7 or higher

### 2. Database Configuration (database_streaming.py)
- Install PostgreSQL
- Create database and tables
- Update database connection info in code

### 3. AWS Configuration (s3_streaming.py)

**Method 1: AWS credentials file**
```bash
aws configure
```

**Method 2: Environment variables**
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

**Method 3: Specify in code**
```python
s3_client = create_s3_client(
    aws_access_key_id='your_access_key',
    aws_secret_access_key='your_secret_key',
    region_name='us-east-1'
)
```

## Performance Comparison

### Database Streaming Methods

| Method | Memory Usage | Processing Speed | Use Case |
|--------|--------------|------------------|----------|
| Load all | High | Fast (small data) | Small datasets (< 1GB) |
| fetchmany() | Medium | Medium | Medium datasets (1-10GB) |
| fetchone() | Low | Slow | Large datasets (> 10GB) |

### File Processing Methods

| Method | Memory Usage | Processing Speed | Use Case |
|--------|--------------|------------------|----------|
| Load all | High | Fast (small file) | Small files (< 100MB) |
| Chunk reading | Medium | Medium | Medium files (100MB-1GB) |
| Line by line | Low | Slow | Large files (> 1GB) |

## Getting Started

### Step 1: Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### Step 2: Configure Database (database_streaming.py)
1. Install and start PostgreSQL
2. Create test database and tables
3. Insert test data
4. Update connection info in code

### Step 3: Configure AWS S3 (s3_streaming.py)
1. Create AWS account
2. Create S3 bucket
3. Upload test file
4. Configure AWS credentials

### Step 4: Run Experiment
```bash
python database_streaming.py
python s3_streaming.py
```

## Notes

1. **Database connection**: Ensure database service is running and connection info is correct
2. **AWS credentials**: Ensure AWS credentials are configured correctly with S3 access permission
3. **File paths**: Ensure local file paths exist and are writable
4. **Memory management**: For very large files, use line-by-line processing
5. **Error handling**: Code includes basic error handling, can be extended as needed

## FAQ

**Q: How to process CSV files?**
A: Use Python's `csv` module:
```python
import csv

with open(file_path, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        process_row(row)
```

**Q: How to process in parallel?**
A: Use `multiprocessing` or `concurrent.futures`:
```python
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=4) as executor:
    executor.map(process_row, rows)
```

**Q: How to process JSON files?**
A: Use `ijson` library for streaming JSON parsing:
```python
import ijson

with open(file_path, 'rb') as f:
    parser = ijson.items(f, 'item')
    for item in parser:
        process_item(item)
```

## References

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Python File I/O](https://docs.python.org/3/tutorial/inputoutput.html)

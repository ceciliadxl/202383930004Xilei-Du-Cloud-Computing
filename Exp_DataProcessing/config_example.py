"""
Configuration file example
Copy this file as config.py and fill in actual configuration
Do not commit config.py with real credentials to version control
"""

DATABASE_CONFIG = {
    'dbname': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'port': 5432
}

S3_CONFIG = {
    'bucket_name': 'your-bucket-name',
    'region_name': 'us-east-1',
}

FILE_CONFIG = {
    's3_file_path': 'data/large-data-file.csv',
    'local_file_path': '/tmp/downloaded-file.csv',
}

PROCESSING_CONFIG = {
    'db_batch_size': 1000,
    'file_chunk_size': 8192,
    'processing_method': 'line_by_line',
}

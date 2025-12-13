"""
S3 data download and streaming processing
Download large files from Amazon S3 and process them incrementally
"""
import boto3
import time
import os
from botocore.exceptions import ClientError


def create_s3_client(aws_access_key_id=None, aws_secret_access_key=None, region_name='us-east-1'):
    """Create S3 client"""
    try:
        if aws_access_key_id and aws_secret_access_key:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                region_name=region_name
            )
        else:
            s3_client = boto3.client('s3', region_name=region_name)
        
        print(f"S3 client created successfully (region: {region_name})")
        return s3_client
    except Exception as e:
        print(f"Error creating S3 client: {e}")
        return None


def download_file_from_s3(s3_client, bucket_name, file_name, local_path):
    """Download file from S3"""
    start_time = time.time()
    
    try:
        print(f"Downloading {file_name} from bucket {bucket_name}...")
        
        with open(local_path, 'wb') as f:
            s3_client.download_fileobj(bucket_name, file_name, f)
        
        if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            file_size = os.path.getsize(local_path)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            print(f"File downloaded successfully!")
            print(f"File size: {file_size / (1024*1024):.2f} MB")
            print(f"Download time: {elapsed_time:.2f} seconds")
            print(f"Download speed: {file_size / (1024*1024) / elapsed_time:.2f} MB/s")
            return True
        else:
            print("Download failed: file is empty or does not exist")
            return False
            
    except ClientError as e:
        print(f"Error downloading file from S3: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def process_line(line):
    """
    Process a single line of data
    
    Args:
        line: A string containing one line of data from file
    """
    # Example: Extract and process line data
    # You can add your specific processing logic here
    # For example: parse CSV, extract fields, calculate statistics, etc.
    
    # Example processing: count words in line
    # words = line.strip().split()
    # return len(words)
    pass


def process_file_in_chunks(file_path, chunk_size=8192):
    """Process file in chunks"""
    start_time = time.time()
    
    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist")
            return
        
        file_size = os.path.getsize(file_path)
        print(f"Processing file: {file_path}")
        print(f"File size: {file_size / (1024*1024):.2f} MB")
        print(f"Reading in chunks of {chunk_size} bytes...")
        
        processed_bytes = 0
        processed_lines = 0
        buffer = ""
        
        with open(file_path, 'r', encoding='utf-8') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    if buffer:
                        process_line(buffer)
                        processed_lines += 1
                    break
                
                buffer += chunk
                processed_bytes += len(chunk)
                
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    process_line(line)
                    processed_lines += 1
                
                if processed_bytes % (1024 * 1024) == 0:
                    progress = (processed_bytes / file_size) * 100
                    print(f"Progress: {progress:.1f}% ({processed_bytes / (1024*1024):.1f} MB processed)", end='\r')
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nFile processing completed!")
        print(f"Total lines processed: {processed_lines}")
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Processing speed: {processed_lines/elapsed_time:.2f} lines/second")
        
    except Exception as e:
        print(f"Error processing file: {e}")


def process_file_line_by_line(file_path):
    """Process file line by line"""
    start_time = time.time()
    
    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist")
            return
        
        file_size = os.path.getsize(file_path)
        print(f"Processing file: {file_path}")
        print(f"File size: {file_size / (1024*1024):.2f} MB")
        print("Reading line by line...")
        
        processed_lines = 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                process_line(line)
                processed_lines += 1
                
                if processed_lines % 10000 == 0:
                    print(f"Processed {processed_lines} lines...", end='\r')
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nFile processing completed!")
        print(f"Total lines processed: {processed_lines}")
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Processing speed: {processed_lines/elapsed_time:.2f} lines/second")
        
    except Exception as e:
        print(f"Error processing file: {e}")


def download_and_process_s3_data(s3_client, bucket_name, file_name, local_path, process_method='line_by_line'):
    """Download and process S3 data"""
    print("="*60)
    print("Step 1: Downloading file from S3")
    print("="*60)
    
    if not download_file_from_s3(s3_client, bucket_name, file_name, local_path):
        print("Download failed. Exiting...")
        return
    
    print("\n" + "="*60)
    print("Step 2: Processing downloaded file")
    print("="*60)
    
    if process_method == 'line_by_line':
        process_file_line_by_line(local_path)
    elif process_method == 'chunk':
        process_file_in_chunks(local_path, chunk_size=8192)
    else:
        print(f"Unknown process method: {process_method}")
        return


def main():
    """Main function"""
    s3_config = {
        'bucket_name': 'my-bucket',
        'file_name': 'large-data-file.csv',
        'local_path': '/tmp/large-data-file.csv',
        'region_name': 'us-east-1'
    }
    
    s3_client = create_s3_client(region_name=s3_config['region_name'])
    
    if s3_client is None:
        print("Failed to create S3 client. Exiting...")
        return
    
    try:
        print("\n" + "="*60)
        print("Method 1: Line-by-line processing")
        print("="*60)
        download_and_process_s3_data(
            s3_client,
            s3_config['bucket_name'],
            s3_config['file_name'],
            s3_config['local_path'],
            process_method='line_by_line'
        )
        
        print("\n" + "="*60)
        print("Method 2: Chunk-based processing")
        print("="*60)
        download_and_process_s3_data(
            s3_client,
            s3_config['bucket_name'],
            s3_config['file_name'],
            s3_config['local_path'],
            process_method='chunk'
        )
        
    except Exception as e:
        print(f"Error in main execution: {e}")


if __name__ == "__main__":
    main()

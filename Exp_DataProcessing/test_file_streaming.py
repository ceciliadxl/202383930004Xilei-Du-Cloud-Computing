"""
Simplified file streaming test
Test file streaming processing without database or S3
"""
import os
import time


def process_line(line):
    """
    Process a single line of data
    
    Args:
        line: A string containing one line of data
    """
    # Add your processing logic here
    # For example: extract data, calculate statistics, etc.
    # 
    # Example: Simple word count
    # words = line.strip().split()
    # return len(words)
    pass


def process_file_line_by_line(file_path):
    """Process file line by line (streaming)"""
    import sys
    start_time = time.time()
    
    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist")
            return
        
        file_size = os.path.getsize(file_path)
        print(f"Processing file: {file_path}")
        print(f"File size: {file_size / (1024*1024):.2f} MB")
        print("Reading line by line (streaming)...")
        sys.stdout.flush()
        
        processed_lines = 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                process_line(line)
                processed_lines += 1
                
                if processed_lines % 10000 == 0:
                    print(f"Processed {processed_lines:,} lines...", end='\r')
                    sys.stdout.flush()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nFile processing completed!")
        print(f"Total lines: {processed_lines:,}")
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Processing speed: {processed_lines/elapsed_time:.2f} lines/second")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"Error processing file: {e}")


def process_file_in_chunks(file_path, chunk_size=8192):
    """Process file in chunks (streaming)"""
    import sys
    start_time = time.time()
    
    try:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist")
            return
        
        file_size = os.path.getsize(file_path)
        print(f"Processing file: {file_path}")
        print(f"File size: {file_size / (1024*1024):.2f} MB")
        print(f"Reading in chunks of {chunk_size} bytes...")
        sys.stdout.flush()
        
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
                    sys.stdout.flush()
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"\nFile processing completed!")
        print(f"Total lines: {processed_lines:,}")
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Processing speed: {processed_lines/elapsed_time:.2f} lines/second")
        sys.stdout.flush()
        
    except Exception as e:
        print(f"Error processing file: {e}")


def compare_methods(file_path):
    """Compare different processing methods"""
    print("=" * 60)
    print("Method 1: Line-by-line processing")
    print("=" * 60)
    process_file_line_by_line(file_path)
    
    print("\n" + "=" * 60)
    print("Method 2: Chunk-based processing")
    print("=" * 60)
    process_file_in_chunks(file_path, chunk_size=8192)


if __name__ == "__main__":
    import sys
    test_file = "test_data.txt"
    
    print("=" * 60)
    print("File Streaming Processing Test")
    print("=" * 60)
    sys.stdout.flush()
    
    # Check if test file exists
    if not os.path.exists(test_file):
        print(f"Test file '{test_file}' not found!")
        print("Please run 'python create_test_file.py' first to create test data.")
        sys.stdout.flush()
        exit(1)
    
    # Compare different methods
    compare_methods(test_file)


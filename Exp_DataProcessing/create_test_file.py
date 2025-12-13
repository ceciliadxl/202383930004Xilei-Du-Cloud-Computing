"""
Create test file for streaming processing experiment
Generate a large text file to test file streaming methods
"""
import os

def create_test_file(filename='test_data.txt', num_lines=100000):
    """Create a test file with specified number of lines"""
    import sys
    print(f"Creating test file: {filename}")
    print(f"Number of lines: {num_lines:,}")
    sys.stdout.flush()
    
    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(num_lines):
            f.write(f"Line {i}: This is test data number {i}, value = {i * 2}\n")
            if (i + 1) % 10000 == 0:
                print(f"Progress: {i + 1:,} / {num_lines:,} lines written...", end='\r')
                sys.stdout.flush()
    
    file_size = os.path.getsize(filename)
    print(f"\nFile created successfully!")
    print(f"File size: {file_size / (1024*1024):.2f} MB")
    sys.stdout.flush()

if __name__ == "__main__":
    # Create a test file with 100,000 lines
    create_test_file('test_data.txt', 100000)
    
    # Uncomment to create a larger file
    # create_test_file('test_data_large.txt', 1000000)


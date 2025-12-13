"""
Database streaming processing example
Process large datasets using streaming
"""
import psycopg2
import time


def connect_to_database(dbname, user, password, host, port=5432):
    """Connect to PostgreSQL database"""
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        print(f"Successfully connected to database: {dbname}")
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def process_row(row):
    """
    Process a single row of data
    
    Args:
        row: A tuple containing row data from database query
    """
    # Example: Extract and process row data
    # You can add your specific processing logic here
    # For example: calculate statistics, transform data, save to file, etc.
    
    # Example processing: calculate sum of numeric values
    # if len(row) > 1 and isinstance(row[1], (int, float)):
    #     return row[1]
    pass


def process_data_in_batches(connection, query, batch_size=1000):
    """Process large dataset in batches"""
    start_time = time.time()
    
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        print(f"Query executed. Fetching data in batches of {batch_size}...")
        
        processed_rows = 0
        
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            
            for row in rows:
                process_row(row)
                processed_rows += 1
            
            print(f"Processed {processed_rows} rows...", end='\r')
        
        print(f"\nTotal rows processed: {processed_rows}")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Processing speed: {processed_rows/elapsed_time:.2f} rows/second")
        
        cursor.close()
        
    except psycopg2.Error as e:
        print(f"Error processing data: {e}")


def process_data_one_by_one(connection, query):
    """Process data row by row"""
    start_time = time.time()
    
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        
        print("Query executed. Processing data row by row...")
        
        processed_rows = 0
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            
            process_row(row)
            processed_rows += 1
            
            if processed_rows % 1000 == 0:
                print(f"Processed {processed_rows} rows...", end='\r')
        
        print(f"\nTotal rows processed: {processed_rows}")
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Total time: {elapsed_time:.2f} seconds")
        print(f"Processing speed: {processed_rows/elapsed_time:.2f} rows/second")
        
        cursor.close()
        
    except psycopg2.Error as e:
        print(f"Error processing data: {e}")


def main():
    """Main function"""
    db_config = {
        'dbname': 'your_db',
        'user': 'your_user',
        'password': 'your_password',
        'host': 'your_host',
        'port': 5432
    }
    
    connection = connect_to_database(**db_config)
    
    if connection is None:
        print("Failed to connect to database. Exiting...")
        return
    
    try:
        query_with_limit = "SELECT * FROM your_table LIMIT 10000;"
        query_all = "SELECT * FROM your_table;"
        
        print("\n" + "="*60)
        print("Method 1: Processing data in batches")
        print("="*60)
        process_data_in_batches(connection, query_with_limit, batch_size=1000)
        
        print("\n" + "="*60)
        print("Method 2: Processing data one by one")
        print("="*60)
        process_data_one_by_one(connection, query_with_limit)
        
    finally:
        connection.close()
        print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()

import pandas as pd

# Load the Excel file
file_path = 'Furniture.xlsx'  # Update this with the correct file path
try:
    excel_data = pd.ExcelFile(file_path)
except FileNotFoundError:
    print(f"Error: The file '{file_path}' could not be found.")
    exit(1)

# Load the data from the first sheet (assuming that's where the data is)
try:
    df = pd.read_excel(excel_data, sheet_name=0)
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit(1)

# Display the first few rows of the dataframe to understand its structure
print(df.head())

# Generate SQL insert statements
insert_statements = []

for index, row in df.iterrows():
    product_name = row['Product Name']
    category_id = row['Category name']
    status_id = row['Status name']
    buy_date = row['Buy Date']
    buy_price = row['Buy Price']
    buy_platform_id = row['Buy Platform']
    sell_date = row['Sell Date']
    sell_price = row['Sell Price']
    sell_platform_id = row['Sell Platform']
    fees = row['Fees']
    image_name = row['product image']
    
    # Assuming you have proper handling of NULL values or empty strings for your database
    insert_statement = f"INSERT INTO products (product_name, category_id, status_id, buy_date, buy_price, buy_platform_id, sell_date, sell_price, sell_platform_id, fees, image_name) VALUES ('{product_name}', {category_id}, {status_id}, '{buy_date}', {buy_price}, {buy_platform_id}, '{sell_date}', {sell_price}, {sell_platform_id}, {fees}, '{image_name}');"
    insert_statements.append(insert_statement)

# Save the insert statements to a file
output_file = 'insert_statements.sql'
try:
    with open(output_file, 'w') as file:
        for statement in insert_statements:
            file.write(statement + '\n')
    print(f"SQL insert statements have been generated and saved to {output_file}")
except Exception as e:
    print(f"Error saving SQL insert statements: {e}")

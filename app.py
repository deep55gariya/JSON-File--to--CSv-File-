import streamlit as st
import json
import csv
import io

# Function to clean and format multiline fields or lists
def clean_multiline_field(text):
    if isinstance(text, list):
        # If the text is a list, join the list items into a single string separated by commas
        text = ', '.join(text)
    # Replace newlines with " | " if any multiline text is present
    return text.replace("\n", " | ") if text else ""

# Function to replace empty fields with 0
def replace_blank_with_zero(value):
    return value if value else "0"

# Function to decode Unicode escape sequences
def decode_unicode(text):
    if text is None:
        return ""
    return text.encode('utf-8').decode('unicode_escape')

# Function to convert JSON data to CSV rows
def json_to_csv_rows(json_data, columns):
    # Prepare a row with values in the order of the columns specified
    csv_row = []
    for column in columns:
        # Extract the value for each column, and handle multiline or list data
        value = json_data.get(column, "")
        value = clean_multiline_field(value)
        value = decode_unicode(value)
        value = replace_blank_with_zero(value)
        csv_row.append(value)
    
    return csv_row

# Function to convert multiple JSON files to a single CSV
def convert_multiple_json_to_csv(json_files, columns):
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)
    
    # Write the header
    writer.writerow(columns)
    
    for json_file in json_files:
        try:
            # Decode the file and load JSON data
            json_data = json.load(io.TextIOWrapper(json_file, encoding='utf-8'))
            csv_rows = json_to_csv_rows(json_data, columns)
            writer.writerow(csv_rows)
        except (json.JSONDecodeError, TypeError) as e:
            st.error(f"Error processing file {json_file.name}: {e}")
    
    # Get the CSV content as bytes
    csv_output.seek(0)
    return csv_output.getvalue().encode('utf-8')

# Streamlit App
st.title("Dynamic JSON to CSV Converter")

# Step 1: Input number of columns
num_columns = st.number_input("Enter the number of columns", min_value=1, step=1)

# Step 2: Input the column names based on the number of columns specified
columns = []
for i in range(num_columns):
    column_name = st.text_input(f"Enter name for column {i + 1}")
    if column_name:
        columns.append(column_name)

# Step 3: Upload JSON files
uploaded_files = st.file_uploader("Choose JSON files", type="json", accept_multiple_files=True)

if uploaded_files and columns:
    # Convert multiple JSON files to CSV
    csv_output = convert_multiple_json_to_csv(uploaded_files, columns)
    
    # Provide download link for CSV file
    st.download_button(
        label="Download CSV",
        data=csv_output,
        file_name="combined_file.csv",
        mime="text/csv"
    )

st.write("Enter the number of columns, specify their names, and upload JSON files to combine them into a single CSV file.")

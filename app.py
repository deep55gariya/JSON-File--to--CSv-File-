import streamlit as st
import json
import csv
import io

def clean_multiline_field(text):
    if isinstance(text, list):
        text = ', '.join(text)
    return text.replace("\n", " | ") if text else ""

def json_to_csv_rows(json_data, columns):
    csv_row = []
    for column in columns:
        value = json_data.get(column, "")
        value = clean_multiline_field(value)
        csv_row.append(value)
    return csv_row

def convert_multiple_json_to_csv(json_files):
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)

    headers = []
    json_data_list = []

    # Load JSON data and determine headers based on the first JSON file
    for idx, json_file in enumerate(json_files):
        try:
            json_data = json.load(io.TextIOWrapper(json_file, encoding='utf-8'))
            json_data_list.append(json_data)
            if idx == 0:
                # Use the headers from the first JSON file
                headers = list(json_data.keys())
        except (json.JSONDecodeError, TypeError) as e:
            st.error(f"Error processing file {json_file.name}: {e}")

    writer.writerow(headers)

    # Write CSV rows
    for json_data in json_data_list:
        csv_rows = json_to_csv_rows(json_data, headers)
        writer.writerow(csv_rows)

    csv_output.seek(0)
    return csv_output.getvalue().encode('utf-8')

st.title("Dynamic JSON to CSV Converter")

uploaded_files = st.file_uploader("Choose JSON files", type="json", accept_multiple_files=True)

if uploaded_files:
    csv_output = convert_multiple_json_to_csv(uploaded_files)
    st.download_button(
        label="Download CSV",
        data=csv_output,
        file_name="combined_file.csv",
        mime="text/csv"
    )

st.write("Upload JSON files, and they will be automatically converted into a CSV file with headers arranged as per the first file.")

import streamlit as st
import json
import csv
import io

# Function to clean and format multiline fields
def clean_multiline_field(text):
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
def json_to_csv_rows(json_data):
    # Extract and clean multiline fields
    others = json_data.get("Others", [""])
    role = ""
    for item in others:
        if item.startswith("Role: "):
            role = clean_multiline_field(item)
    
    education_details = clean_multiline_field(', '.join(json_data.get("Education details", [])))
    skills = clean_multiline_field(', '.join(json_data.get("Skills", [])))

    # Extract the years from the JSON data
    years = replace_blank_with_zero(decode_unicode(json_data.get("Years", "")))

    # Prepare data row
    csv_row = [
        replace_blank_with_zero(decode_unicode(json_data.get("Title", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Company name", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Job location", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Work experience", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Portal link", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("job listing link", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Company's Rating", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("No. of openings", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Applicants", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Job_posting_date", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Minimum salary", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Maximum salary", ""))),
        replace_blank_with_zero(decode_unicode(json_data.get("Average salary", ""))),
        replace_blank_with_zero(decode_unicode(', '.join(json_data.get("Benefits", [])))),
        replace_blank_with_zero(decode_unicode(role)),
        replace_blank_with_zero(decode_unicode(education_details)),
        replace_blank_with_zero(decode_unicode(skills)),
        replace_blank_with_zero(decode_unicode(clean_multiline_field(json_data.get("About company", "")).replace("About company\n", ""))),
        years  # Add years to the CSV row
    ]
    
    return csv_row

# Function to convert multiple JSON files to a single CSV
def convert_multiple_json_to_csv(json_files, columns):
    csv_output = io.StringIO()
    writer = csv.writer(csv_output)
    
    # Write the header
    writer.writerow(columns)
    
    for json_file in json_files:
        json_data = json.load(json_file)
        csv_rows = json_to_csv_rows(json_data)
        writer.writerow(csv_rows)
    
    # Get the CSV content as bytes
    csv_output.seek(0)
    return csv_output.getvalue().encode('utf-8')

# Streamlit App
st.title("JSON to CSV Converter")

# Multiple file upload
uploaded_files = st.file_uploader("Choose JSON files", type="json", accept_multiple_files=True)

# Column names
columns = [
    "Title", "Company name", "Job location", "Work experience", "Portal link", 
    "job listing link", "Company's Rating", "No. of openings", "Applicants", 
    "Job_posting_date", "Minimum salary", "Maximum salary", "Average salary", 
    "Benefits", "Role", "Education details", "Skills", "About company", "Years"
]

if uploaded_files:
    # Convert multiple JSON files to CSV
    csv_output = convert_multiple_json_to_csv(uploaded_files, columns)
    
    # Provide download link for CSV file
    st.download_button(
        label="Download CSV",
        data=csv_output,
        file_name="combined_file.csv",
        mime="text/csv"
    )

st.write("Upload multiple JSON files to combine them into a single CSV file.")

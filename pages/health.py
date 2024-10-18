import streamlit as st
import os
import json
import pdfplumber
import regex

from clarifai.client.model import Model

SYS_PROMPT = '''
You are a text entity extraction specialist. Given some text, your task is to extract the values of the following entities:

{
  "overall_health": [{
    "perception": "string",
    "rurality_definition_1": {
      "non_rural": "integer",
      "rural": "integer"
    },
    "rurality_definition_2": {
      "non_rural": "integer",
      "rural": "integer"
    },
    "rurality_definition_3": {
      "non_rural": "integer",
      "rural": "integer"
    }
  }],
  "physical_health": [{
    "aggregate": "string",
    "rurality_definition_1": {
      "non_rural": "integer",
      "rural": "integer"
    },
    "rurality_definition_2": {
      "non_rural": "integer",
      "rural": "integer"
    },
    "rurality_definition_3": {
      "non_rural": "integer",
      "rural": "integer"
    }
  }],
  "mental_health": [{
    "aggregate": "string",
    "rurality_definition_1": {
      "non_rural": "integer",
      "rural": "integer"
    },
    "rurality_definition_2": {
      "non_rural": "integer",
      "rural": "integer"
    },
    "rurality_definition_3": {
      "non_rural": "integer",
      "rural": "integer"
    }
  }]
}

The JSON schema must be followed during the extraction.
The values must only include text found in the document
Do not normalize any entity value.
If an entity is not found in the document, set the entity value to null.
'''

inference_params = dict(temperature=0.2, system_prompt=SYS_PROMPT)

def extract_json(text):
  # Define a regular expression pattern to match the JSON structure
  pattern = regex.compile(r'\{(?:[^{}]|(?R))*\}')
  
  # Find all matches of the JSON pattern in the input text
  matches = pattern.findall(text)
  
  # Assuming there is only one JSON structure in the input text
  json_string = matches[0] if matches else None
  
  # Parse the JSON string into a Python dictionary
  if json_string:
      try:
          json_data = json.loads(json_string)
          return json_data
      except json.JSONDecodeError as e:
          # Error decoding JSON
          return None
  else:
      # No JSON structure found
      return None

# Function to validate and load JSON string
def validate_and_load_json(json_string):
    try:
        # Attempt to parse the JSON string
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        st.error(f"Invalid JSON format: {e}")
    return None

def json_to_html(data):
    # Start HTML table
    html = """
    <table border="1" cellpadding="5" cellspacing="0">
        <thead>
            <tr>
                <th>Category</th>
                <th colspan="2">Rurality Definition 1</th>
                <th colspan="2">Rurality Definition 2</th>
                <th colspan="2">Rurality Definition 3</th>
            </tr>
            <tr>
                <th></th>
                <th>Non-Rural</th>
                <th>Rural</th>
                <th>Non-Rural</th>
                <th>Rural</th>
                <th>Non-Rural</th>
                <th>Rural</th>
            </tr>
        </thead>
        <tbody>
    """
    
    # Define categories to iterate over
    categories = ["overall_health", "physical_health", "mental_health"]
    
    # Iterate through each category in the JSON data
    for category in categories:
        if category in json_data and isinstance(json_data[category], list):
            for item in json_data[category]:
                html += f"<tr><td>{category.replace('_', ' ').capitalize()}</td>"
                
                # Safely get values for rurality definitions
                for i in range(1, 4):
                    def_key = f"rurality_definition_{i}"
                    non_rural = item.get(def_key, {}).get("non_rural", "N/A")
                    rural = item.get(def_key, {}).get("rural", "N/A")
                    
                    # Add non-rural and rural values to the row
                    html += f"<td>{non_rural}</td><td>{rural}</td>"
                
                html += "</tr>"
    
    # Close the table
    html += "</tbody></table>"
    return html
   
# Function to update HTML table based on changes in the JSON textarea
def update_table():
    try:
        # Get the modified JSON data
        json_data = json.loads(st.session_state["json_key"])

        # Generate the updated HTML table
        html_table = json_to_html(json_data)

        # Update the HTML content on the page
        st.session_state["html_table"] = html_table
    except json.JSONDecodeError:
        st.error("The JSON data is invalid. Please correct it.")
        st.session_state["html_table"] = ""

@st.fragment
def show_codes():
    st.text_area(
      "Edit the JSON here:",
      value=st.session_state['json_key'],
      height=300,
      key="json_key")
    
    # Update the table only when the button is clicked
    if st.button("Update HTML"):
      update_table()

    # Show the generated HTML table
    st.subheader("Generated HTML")
    
    html_table = st.session_state["html_table"]
    st.markdown("### HTML Table Output")
    st.markdown(html_table, unsafe_allow_html=True) 
      
    st.markdown("### HTML Code")
    st.code(html_table, language='html')
  
def main():
    col1, mid, col2 = st.columns([1,1,20])
    with col1:
      st.image("https://raw.githubusercontent.com/datjandra/Team-Pu-u-Kukui/refs/heads/main/logo.png", width=60)
    with col2:
      st.title("Health Data Extractor")

    
    # File uploader for PDF files
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        # Save the uploaded file
        st.success(f"Uploaded {uploaded_file.name}")
        
        # Input for page number or page range (e.g., "7" or "7-8")
        page_input = st.text_input("Enter the page number or range (e.g., 7 or 7-8)")

        json_data = None
      
        if st.button("Extract Table from Page"):
            with pdfplumber.open(uploaded_file) as pdf:
              pages = pdf.pages
              # Get the total number of pages in the PDF
              total_pages = len(pages)

              # Initialize the variable to store all extracted text
              extracted_text = []
  
              try:
                  # Check if the input is a range
                  if '-' in page_input:
                      # Extract the start and end of the range
                      start_page, end_page = page_input.split('-')
                      start_page = int(start_page) - 1  # Convert to zero-indexed
                      end_page = int(end_page) - 1  # Convert to zero-indexed
  
                      # Ensure the page range is valid
                      if start_page < 0 or end_page >= total_pages or start_page > end_page:
                          st.error("Invalid page range")
                      else:
                          # Loop through the page range and extract text
                          for page_num in range(start_page, end_page + 1):
                              extracted_text += pdf.pages[page_num].extract_table() + "\n"
  
                  else:
                      # Single page input
                      single_page = int(page_input) - 1  # Convert to zero-indexed
  
                      # Ensure the page number is valid
                      if single_page < 0 or single_page >= total_pages:
                          st.error("Invalid page number")
                      else:
                          extracted_text.append(pdf.pages[single_page].extract_table())
  
              except ValueError:
                  st.error("Please enter a valid page number or range.")
            
              if extracted_text:
                # prompt = f"Extract JSON from table in text: {extracted_text}"

                # Model Predict
                with st.spinner("Extracting data, please wait..."):
                  # model_prediction = Model("https://clarifai.com/openai/chat-completion/models/gpt-4-turbo").predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
                # json_data = extract_json(model_prediction.outputs[0].data.text.raw)
                  json_data = json.loads('{"hello": "world"}')

                  st.markdown('\n\n'.join(extracted_text))
                  
                  
        
        if json_data:
          # Store JSON in session_state to persist across reruns
          if 'json_key' not in st.session_state:
            st.session_state['json_key'] = json.dumps(json_data, indent=2)
          if 'html_table' not in st.session_state:
            st.session_state['html_table'] = ""  # Empty until first update
          
          show_codes()
                    
if __name__ == "__main__":
    main()

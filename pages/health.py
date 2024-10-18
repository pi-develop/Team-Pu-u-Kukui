import streamlit as st
import os
import json
import pdfplumber
import regex

from clarifai.client.model import Model

SYS_PROMPT = '''
You are a text entity extraction specialist. Given a table embedded in some text, your task is to extract the table values into the following entities:

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
Table starts when columns "Rurality Definition 1", "Rurality Definition 2", or "Rurality Definition 3" are encountered.
Table ends when phrase "Table 2" is encountered.
Ignore other text that are not part of the table.
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
    # Start the HTML table
    html_table = """
    <table border="1" cellpadding="5" cellspacing="0">
      <thead>
        <tr>
          <th></th>
          <th colspan="2">Rurality Definition 1</th>
          <th colspan="2">Rurality Definition 2</th>
          <th colspan="2">Rurality Definition 3</th>
        </tr>
        <tr>
          <th>Category</th>
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

    # Helper function to handle missing values
    def get_value(d, key, sub_key):
        return d.get(key, {}).get(sub_key, 'N/A')

    # Process overall_health section
    if 'overall_health' in data:
        # Add the "Overall Health Perception" section
        html_table += """
        <tr>
          <td colspan="7" style="text-align:center; font-weight:bold;">Overall Health Perception</td>
        </tr>
        """
      
        for entry in data['overall_health']:
            perception = entry.get('perception', 'N/A')
            row = f"""
            <tr>
              <td>{perception}</td>
              <td>{get_value(entry, 'rurality_definition_1', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_1', 'rural')}</td>
              <td>{get_value(entry, 'rurality_definition_2', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_2', 'rural')}</td>
              <td>{get_value(entry, 'rurality_definition_3', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_3', 'rural')}</td>
            </tr>
            """
            html_table += row

        # Add a section separator row
        html_table += """
        <tr>
          <td colspan="7" style="text-align:center; font-weight:bold;">Physical Health</td>
        </tr>
        """

    # Process physical_health section
    if 'physical_health' in data:
        for entry in data['physical_health']:
            aggregate = entry.get('aggregate', 'N/A')
            row = f"""
            <tr>
              <td>{aggregate}</td>
              <td>{get_value(entry, 'rurality_definition_1', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_1', 'rural')}</td>
              <td>{get_value(entry, 'rurality_definition_2', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_2', 'rural')}</td>
              <td>{get_value(entry, 'rurality_definition_3', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_3', 'rural')}</td>
            </tr>
            """
            html_table += row

        # Add a section separator row
        html_table += """
        <tr>
          <td colspan="7" style="text-align:center; font-weight:bold;">Mental Health</td>
        </tr>
        """

    # Process mental_health section
    if 'mental_health' in data:
        for entry in data['mental_health']:
            aggregate = entry.get('aggregate', 'N/A')
            row = f"""
            <tr>
              <td>{aggregate}</td>
              <td>{get_value(entry, 'rurality_definition_1', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_1', 'rural')}</td>
              <td>{get_value(entry, 'rurality_definition_2', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_2', 'rural')}</td>
              <td>{get_value(entry, 'rurality_definition_3', 'non_rural')}</td>
              <td>{get_value(entry, 'rurality_definition_3', 'rural')}</td>
            </tr>
            """
            html_table += row

    # End the table
    html_table += """
      </tbody>
    </table>
    """

    return html_table
   
# Function to update HTML table based on changes in the JSON textarea
def update_table():
    try:
        # Get the modified JSON data
        json_data = json.loads(st.session_state['json_key'])
      
        if json_data:
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
    html_table = st.session_state["html_table"]
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
              extracted_text = ''
  
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
                              extracted_text += pdf.pages[page_num].extract_text() + "\n"
  
                  else:
                      # Single page input
                      single_page = int(page_input) - 1  # Convert to zero-indexed
  
                      # Ensure the page number is valid
                      if single_page < 0 or single_page >= total_pages:
                          st.error("Invalid page number")
                      else:
                          extracted_text += pdf.pages[single_page].extract_text()
  
              except ValueError:
                  st.error("Please enter a valid page number or range.")
            
              if extracted_text:
                prompt = f"Extract JSON from table in text: {extracted_text}"

                # Model Predict
                with st.spinner("Extracting data, please wait..."):
                  model_prediction = Model("https://clarifai.com/openai/chat-completion/models/gpt-4-turbo").predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
                json_data = extract_json(model_prediction.outputs[0].data.text.raw)
                  
        if json_data:
          # Store JSON in session_state to persist across reruns
          if 'json_key' not in st.session_state:
            st.session_state['json_key'] = json.dumps(json_data, indent=2)
          if 'html_table' not in st.session_state:
            st.session_state['html_table'] = ""  # Empty until first update
          
          show_codes()
                    
if __name__ == "__main__":
    main()

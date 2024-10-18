import streamlit as st
import os
import json
import pdfplumber
import regex

from clarifai.client.model import Model

SYS_PROMPT = '''
You are a text entity extraction specialist. Given some text, your task is to extract the values of the following entities:

{
  "total_population": {
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
    }
  },
  "county_distribution": [{
    "county": "string",
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
    }
  }],
  "gender_identity": [{
    "gender": "string",
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
    }
  }],
  "race_ethnicity": [{
    "race": "string",
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
    }
  }],
  "income": [{
    "income_level": "string",
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
    }
  }],
  "education": [{
    "education_level": "string",
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
    }
  }],
  "disability": [{
    "disability_level": "string",
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
    }
  }],
  "age_continuous": [{
    "age": "string",
    "non_rural": {
      "sample": "integer",
      "state_population": "integer"
    },
    "rural": {
     "sample": "integer",
      "state_population": "integer"
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
    # Start the HTML table
    html = '''
    <table border="1">
        <thead>
            <tr>
                <th>Category</th> <!-- Updated header -->
                <th colspan="2">Non-rural</th>
                <th colspan="2">Rural</th>
            </tr>
            <tr>
                <th></th>
                <th>Sample</th>
                <th>State Population</th>
                <th>Sample</th>
                <th>State Population</th>
            </tr>
        </thead>
        <tbody>
    '''
    
    # Helper function to add rows
    def add_row(label, non_rural, rural):
        html_row = f'<tr><td>{label}</td>'
        for key in ['sample', 'state_population']:
            html_row += f'<td>{non_rural.get(key) if non_rural and key in non_rural else ""}</td>'
        for key in ['sample', 'state_population']:
            html_row += f'<td>{rural.get(key) if rural and key in rural else ""}</td>'
        html_row += '</tr>\n'  # Add newline for readability
        return html_row

    # Add total population
    total_population = data.get("total_population", {})
    html += add_row("Total Population", total_population.get("non_rural"), total_population.get("rural"))
    
    # Add a divider row
    html += '<tr><td colspan="5" style="height: 10px;"></td></tr>\n'

    # Add county distribution
    html += '<tr><td colspan="5"><strong>County</strong></td></tr>\n'
    for county_data in data.get("county_distribution", []):
        html += add_row(county_data['county'], county_data.get("non_rural"), county_data.get("rural"))

    # Add a divider row
    html += '<tr><td colspan="5" style="height: 10px;"></td></tr>\n'

    # Add gender identity
    html += '<tr><td colspan="5"><strong>Gender Identity</strong></td></tr>\n'
    for gender_data in data.get("gender_identity", []):
        html += add_row(gender_data['gender'], gender_data.get("non_rural"), gender_data.get("rural"))

    # Add a divider row
    html += '<tr><td colspan="5" style="height: 10px;"></td></tr>\n'

    # Add race and ethnicity
    html += '<tr><td colspan="5"><strong>Race and Ethnicity</strong></td></tr>\n'
    for race_data in data.get("race_ethnicity", []):
        html += add_row(race_data['race'], race_data.get("non_rural"), race_data.get("rural"))

    # Add a divider row
    html += '<tr><td colspan="5" style="height: 10px;"></td></tr>\n'

    # Add income
    html += '<tr><td colspan="5"><strong>Income</strong></td></tr>\n'
    for income_data in data.get("income", []):
        html += add_row(income_data['income_level'], income_data.get("non_rural"), income_data.get("rural"))

    # Add a divider row
    html += '<tr><td colspan="5" style="height: 10px;"></td></tr>\n'

    # Add education
    html += '<tr><td colspan="5"><strong>Education</strong></td></tr>\n'
    for education_data in data.get("education", []):
        html += add_row(education_data['education_level'], education_data.get("non_rural"), education_data.get("rural"))

    # Add a divider row
    html += '<tr><td colspan="5" style="height: 10px;"></td></tr>\n'

    # Add disability
    html += '<tr><td colspan="5"><strong>Disability</strong></td></tr>\n'
    for disability_data in data.get("disability", []):
        html += add_row(disability_data['disability_level'], disability_data.get("non_rural"), disability_data.get("rural"))

    # Add a divider row
    html += '<tr><td colspan="5" style="height: 10px;"></td></tr>\n'

    # Add age continuous
    html += '<tr><td colspan="5"><strong>Age (continuous)</strong></td></tr>\n'
    for age_data in data.get("age_continuous", []):
        html += add_row(age_data['age'], age_data.get("non_rural"), age_data.get("rural"))

    # Close the table
    html += '''
        </tbody>
    </table>
    '''
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
      st.title("Demographics Data Extractor")

    
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
              extracted_text = ""
  
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

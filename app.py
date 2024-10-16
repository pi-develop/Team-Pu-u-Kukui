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
    html = "<table border='1'>\n"

    # Create the header row
    html += "  <tr>\n"
    html += "    <th>Section</th>\n"
    html += "    <th colspan='2'>Non-Rural</th>\n"
    html += "    <th colspan='2'>Rural</th>\n"
    html += "  </tr>\n"
    html += "  <tr>\n"
    html += "    <th></th>\n"
    html += "    <th>Sample</th>\n"
    html += "    <th>State Population</th>\n"
    html += "    <th>Sample</th>\n"
    html += "    <th>State Population</th>\n"
    html += "  </tr>\n"

    if "sample_data" in data:
        sample_data = data["sample_data"]

        # Total Population Section
        if "total_population" in sample_data:
            html += "  <tr><td>Total Population</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["total_population"].get("non_rural", "N/A"))
            html += "    <td>N/A</td>\n"  # No State Population for Total Population
            html += "    <td>{}</td>\n".format(sample_data["total_population"].get("rural", "N/A"))
            html += "    <td>N/A</td>\n"
            html += "  </tr>\n"

        # County Distribution Section
        if "county_distribution" in sample_data:
            for county in sample_data["county_distribution"]:
                html += "  <tr><td>County: {}</td>\n".format(county["county"])
                html += "    <td>{}</td>\n".format(county["sample"].get("non_rural", "N/A"))
                html += "    <td>{}</td>\n".format(county["state_population"].get("non_rural", "N/A"))
                html += "    <td>{}</td>\n".format(county["sample"].get("rural", "N/A"))
                html += "    <td>{}</td>\n".format(county["state_population"].get("rural", "N/A"))
                html += "  </tr>\n"

        # Gender Identity Section
        if "gender_identity" in sample_data:
            html += "  <tr><td>Gender Identity: Women</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["non_rural"]["women"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["non_rural"]["women"]["percentage"])
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["rural"]["women"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["rural"]["women"]["percentage"])
            html += "  </tr>\n"

            html += "  <tr><td>Gender Identity: Men</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["non_rural"]["men"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["non_rural"]["men"]["percentage"])
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["rural"]["men"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["gender_identity"]["rural"]["men"]["percentage"])
            html += "  </tr>\n"

        # Race and Ethnicity Section
        if "race_ethnicity" in sample_data:
            html += "  <tr><td>Race/Ethnicity: Asian</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["race_ethnicity"]["non_rural"].get("asian", "N/A"))
            html += "    <td>N/A</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["race_ethnicity"]["rural"].get("asian", "N/A"))
            html += "    <td>N/A</td>\n"
            html += "  </tr>\n"

            html += "  <tr><td>Race/Ethnicity: NHPI</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["race_ethnicity"]["non_rural"].get("nhpi", "N/A"))
            html += "    <td>N/A</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["race_ethnicity"]["rural"].get("nhpi", "N/A"))
            html += "    <td>N/A</td>\n"
            html += "  </tr>\n"

            html += "  <tr><td>Race/Ethnicity: White</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["race_ethnicity"]["non_rural"].get("white", "N/A"))
            html += "    <td>N/A</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["race_ethnicity"]["rural"].get("white", "N/A"))
            html += "    <td>N/A</td>\n"
            html += "  </tr>\n"

        # Income Section
        if "income" in sample_data:
            html += "  <tr><td>Income: Below Poverty</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["income"]["non_rural"]["below_poverty"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["income"]["non_rural"]["below_poverty"]["percentage"])
            html += "    <td>{}</td>\n".format(sample_data["income"]["rural"]["below_poverty"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["income"]["rural"]["below_poverty"]["percentage"])
            html += "  </tr>\n"

            html += "  <tr><td>Income: Above Poverty</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["income"]["non_rural"]["above_poverty"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["income"]["non_rural"]["above_poverty"]["percentage"])
            html += "    <td>{}</td>\n".format(sample_data["income"]["rural"]["above_poverty"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["income"]["rural"]["above_poverty"]["percentage"])
            html += "  </tr>\n"

        # Education Section
        if "education" in sample_data:
            html += "  <tr><td>Education: High School or Below</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["education"]["non_rural"]["high_school_or_below"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["education"]["non_rural"]["high_school_or_below"]["percentage"])
            html += "    <td>{}</td>\n".format(sample_data["education"]["rural"]["high_school_or_below"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["education"]["rural"]["high_school_or_below"]["percentage"])
            html += "  </tr>\n"

            html += "  <tr><td>Education: Postsecondary</td>\n"
            html += "    <td>{}</td>\n".format(sample_data["education"]["non_rural"]["postsecondary"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["education"]["non_rural"]["postsecondary"]["percentage"])
            html += "    <td>{}</td>\n".format(sample_data["education"]["rural"]["postsecondary"]["count"])
            html += "    <td>{}</td>\n".format(sample_data["education"]["rural"]["postsecondary"]["percentage"])
            html += "  </tr>\n"

    html += "</table>\n"
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

def main():
    st.title("Health Data Extractor")
    
    # File uploader for PDF files
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file is not None:
        # Save the uploaded file
        st.success(f"Uploaded {uploaded_file.name}")
        
        # Input for page number or page range (e.g., "7" or "7-8")
        page_input = st.text_input("Enter the page number or range (e.g., 7 or 7-8)")

        json_data = None
      
        if st.button("Extract from Page"):
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
                model_prediction = Model("https://clarifai.com/openai/chat-completion/models/gpt-4-turbo").predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
                json_data = extract_json(model_prediction.outputs[0].data.text.raw)

        if json_data:
          # Store JSON in session_state to persist across reruns
          if 'json_key' not in st.session_state:
            st.session_state['json_key'] = json.dumps(json_data, indent=2)
          if 'html_table' not in st.session_state:
            st.session_state['html_table'] = ""  # Empty until first update
          
          st.text_area(
              "Edit the JSON here:",
              value=st.session_state['json_key'],
              height=300,
              key="json_key"
          )
  
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
      
if __name__ == "__main__":
    main()

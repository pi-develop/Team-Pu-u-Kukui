import streamlit as st

from streamlit_extras.switch_page_button import switch_page

def apply_custom_style():
  st.set_page_config(layout="wide")
    
  # Define the HTML and CSS
  html_content = """
  <style>
  @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');

  /* Set Montserrat as the default font */
  body {
      font-family: 'Montserrat', sans-serif;
  }
  .e1_15 { 
      color:rgba(255, 255, 255, 1);
      width:727px;
      height:52px;
      font-family:Montserrat;
      text-align:left;
      font-size:45.37845230102539px;
      letter-spacing:0;
      line-height:52px; /* Adjusted to give line height a specific value */
  }
  .e2_21 { 
      background-image:linear-gradient(0deg, rgba(4.999259691685438, 96.68749898672104, 180.9985300898552, 1) 0%, rgba(2.1819744911044836, 42.20017835497856, 78.99852856993675, 1) 100%);
      width:100%; /* Set width to 100% for responsiveness */
      height:256px;
      display: flex;
      flex-direction: row;
      justify-content: center;
      align-items: center;
      align-items: flex-start;
      padding-left: 20px;
  }
  .e2_22 { 
      color:rgba(255, 255, 255, 1);
      width:177px;
      height:52px;
      font-family:Montserrat;
      text-align:left;
      font-size:45.37845230102539px;
      letter-spacing:0;
      line-height:52px; /* Adjusted for consistency */
  }
  .e2_23 { 
      transform: rotate(-2.4848083448933725e-17deg);
      width:281.00177001953125px;
      height:0px;
      border:2px solid rgba(255, 255, 255, 1);
  }
  
  .stButton > button {
      background-image: linear-gradient(0deg, rgba(4, 65, 121, 1) 0%, rgba(7, 119, 223, 1) 100%);
      color: rgba(255, 255, 255, 1);
      width: 200px;  /* Set a maximum width */
      height: 60px;  /* Set height */
      border-radius: 23px;  /* Rounded corners */
      font-family: 'Montserrat', sans-serif;
      font-size: 16px;  /* Font size */
      text-align: center;
      line-height: 60px;  /* Center text vertically */
      border: none;  /* No border */
      cursor: pointer;  /* Change cursor on hover */
      transition: opacity 0.3s ease;  /* Smooth transition for hover effect */
      overflow-wrap: break-word;  /* Allow text to wrap */
      word-wrap: break-word;  /* For compatibility */
      hyphens: auto;  /* Hyphenate words if needed */
  }

  /* Hover effect */
  .stButton > button:hover {
      opacity: 0.9;  /* Slightly transparent on hover */
  }

  .header-image {
      height: 100px; /* Set image height */
      width: auto; /* Maintain aspect ratio */
      padding-right: 20px;
  }
  </style>
  
  <div class="e2_21">
    <div>
      <span class="e1_15">DIGITAL EQUITY DASHBOARD</span>
      <div class="e2_23"></div>
      <span class="e2_22">HAWAII</span>
    </div>
    <img src="https://raw.githubusercontent.com/datjandra/Team-Pu-u-Kukui/refs/heads/main/logo.png" alt="Hawaii Map" class="header-image">
  </div>
  """
  
  # Insert the HTML and CSS into the Streamlit app
  st.markdown(html_content, unsafe_allow_html=True)
  
  st.header("Bridging Hawaii's Digital Divide")
  
  st.markdown(
      """
      Welcome to Hawaii's Digital Equity Dashboard, where we track technology and internet access across our islands. 
      This tool maps the digital divide in our communities, showing where support is needed most.
      """
  )

  # Create 3 columns
  col1, spacer1, col2, spacer2, col3 = st.columns([1, 0.2, 1, 0.2, 1])

  # First row of buttons
  with col1:
      st.button("Digital\nLiteracy")
          
  with col2:
      st.button("Device Access")
          
  with col3:
      if st.button("Broadband Connectivity"):
          switch_page("app")
        
  # Second row of buttons
  with col1:
      if st.button("Open Data"):
          switch_page("open_data")
          
  with col2:
      st.button("Initiatives Impact")
          
  with col3:
      st.button("User Feedback")

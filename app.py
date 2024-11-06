import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import matplotlib.pyplot as plt

def main():
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
      flex-direction: column;
      justify-content: center;
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
    .e1_8 { 
        width:281px;
        height:281px;
        position: absolute;
      right: 20px;
    }
    .e1_9 { 
        width:259.046875px;
        height:166.84375px;
        position:absolute;
        left:10.9765625px;
        top:57.078125px;
    }
    .header-img {
      max-width: 140px;
      max-height: 140px;
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
    </style>
    
    <div class="e2_21">
    <span class="e1_15">DIGITAL EQUITY DASHBOARD</span>
    <div class="e2_23"></div>
    <span class="e2_22">HAWAII</span>
    <div class="e1_8">
      <div class="e1_9">
      </div>
    </div>
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

    # Set up a blue header style for the card
    header_style = """
        <style>
            .card-header {
                background-image:linear-gradient(0deg, rgba(4.999259691685438, 96.68749898672104, 180.9985300898552, 1) 0%, rgba(2.1819744911044836, 42.20017835497856, 78.99852856993675, 1) 100%);
                color: white;
                padding: 10px;
                font-size: 1.2rem;
                font-weight: bold;
                border-radius: 0.5rem 0.5rem 0 0;
                text-align: left;
            }
            .card {
                border: 1px solid #d3d3d3;
                border-radius: 0.5rem;
                box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            /* Footer container styling */
            .card-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                background-color: #f1f1f1;
                border-top: 1px solid #ddd;
            }
        
            /* Text styling for "Read more about it" */
            .card-footer-text {
                font-size: 16px;
                color: #333;
            }
        
            /* Button styling */
            .card-footer-button {
                padding: 8px 16px;
                font-size: 16px;
                color: #fff;
                background-color: #007BFF;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                text-decoration: none;
            }
        
            /* Button hover effect */
            .card-footer-button:hover {
                background-color: #0056b3;
            }
        </style>
    """
    
    # Display the custom styles in Streamlit
    st.markdown(header_style, unsafe_allow_html=True)
    
    # Create a card layout with a blue header
    st.markdown("""
        <div class="card">
            <div class="card-header">Broadband Connectivity</div>
            <div>
    """, unsafe_allow_html=True)

    st.subheader("State of Hawaii Broadband Connectivity Map")
    
    # Create a Leaflet map centered at an example location
    m = leafmap.Map(location=[37.7749, -122.4194], zoom_start=10)  # Centered on San Francisco, for example
    
    # Display the map in Streamlit
    m.to_streamlit(height=500)
    
    # Close the card div
    # Add the footer with "Read more about it" and a button
    st.markdown("""
            </div>
            <div class="card-footer">
                <span class="card-footer-text">Read more about it</span>
                <a href="#" class="card-footer-button">Read More</a>
    """, unsafe_allow_html=True)
    
    # Close the card footer and card div
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

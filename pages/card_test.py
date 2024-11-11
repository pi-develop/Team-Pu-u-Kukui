import streamlit as st
import streamlit_shadcn_ui as ui

from style_helper import apply_custom_style

def get_header_style():
    # Define the style for the card and header
    header_style = """
        <style>
            .card-header {
                background-image: linear-gradient(0deg, rgba(5, 96.7, 181, 1) 0%, rgba(2.2, 42.2, 1) 100%);
                color: white;
                padding: 10px 20px;
                font-size: 1.2rem;
                font-weight: bold;
                border-radius: 0.5rem 0.5rem 0 0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .card-header .card-header-image img {
                height: 25px;
                width: auto;
            }
            .card {
                border: 1px solid #d3d3d3;
                border-radius: 0.5rem;
                box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
                margin-bottom: 20px;
            }
            .card-footer {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px 20px;
                border-top: 1px solid #ddd;
            }
            .card-footer-text {
                font-size: 16px;
                color: #333;
            }
            .card-footer-button {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 50px;
                height: 50px;
                font-size: 16px;
                color: #fff;
                background-color: #007BFF;
                border: none;
                border-radius: 50%;
                cursor: pointer;
                text-decoration: none;
            }
            .card-footer-button:hover {
                background-color: #0056b3;
            }
        </style>
    """
    return header_style

def create_card_header(title, image_link):
    st.markdown(f"""
        <div class="card">
            <div class="card-header">
                <div>{title}</div>
                <div class="card-header-image">
                    <img src="{image_link}" alt="Card Header Image">
                </div>
            </div>
            <div>
    """, unsafe_allow_html=True)

with ui.card(key="card1"):
  # Set up a blue header style for the card
  header_style = get_header_style()

  # Display the custom styles in Streamlit
  st.markdown(header_style, unsafe_allow_html=True)

  # Create a card layout with a blue header
  st.markdown("""
    <div class="card">
        <div class="card-header">
            <div>Geographical Breakdown</div>
        </div>
        <div>
  """, unsafe_allow_html=True)
    
  st.write("Somethig here")
    
  # Close the card div
  # Add the footer with "Read more about it" and a button
  st.markdown("""
        </div>
        <div class="card-footer">
            <span class="card-footer-text">Read more about it</span>
            <a href="https://app.powerbi.com/view?r=eyJrIjoiM2JmM2QxZjEtYWEzZi00MDI5LThlZDMtODMzMjhkZTY2Y2Q2IiwidCI6ImMxMzZlZWMwLWZlOTItNDVlMC1iZWFlLTQ2OTg0OTczZTIzMiIsImMiOjF9" target="_blank" class="card-footer-button">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                    <path d="M24 12l-12-9v5h-12v8h12v5l12-9z" fill="white"/>
                </svg>
            </a>
  """, unsafe_allow_html=True)

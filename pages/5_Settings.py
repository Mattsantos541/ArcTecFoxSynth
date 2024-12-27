import streamlit as st
import os
from PIL import Image
from utils.auth import check_authentication

def main():
    if not check_authentication():
        return
        
    st.title("Platform Settings")
    
    st.subheader("Logo Upload")
    uploaded_logo = st.file_uploader(
        "Upload your logo (PNG, JPG)",
        type=['png', 'jpg', 'jpeg'],
        help="Upload your company logo to customize the platform"
    )
    
    if uploaded_logo is not None:
        # Save the uploaded logo
        image = Image.open(uploaded_logo)
        logo_path = "static/uploaded_logo.png"
        os.makedirs("static", exist_ok=True)
        image.save(logo_path)
        st.success("Logo uploaded successfully!")
        
        # Display preview
        st.subheader("Logo Preview")
        st.image(image, width=200)
    
    st.subheader("Color Theme")
    primary_color = st.color_picker(
        "Primary Color",
        "#2196F3",
        help="Choose your primary brand color"
    )
    
    if st.button("Save Theme"):
        # Update the config.toml file with new colors
        config_path = ".streamlit/config.toml"
        with open(config_path, "r") as f:
            config = f.read()
        
        # Update primary color
        config = config.replace(
            'primaryColor = "#2196F3"',
            f'primaryColor = "{primary_color}"'
        )
        
        with open(config_path, "w") as f:
            f.write(config)
            
        st.success("Theme updated! Please refresh the page to see changes.")

if __name__ == "__main__":
    main()

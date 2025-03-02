import streamlit as st
import random
import string

def generate_password(length, use_uppercase, use_lowercase, use_digits, use_special, exclude_similar):
    """Generate a random password based on the specified criteria."""
    # Define character sets
    uppercase_chars = string.ascii_uppercase
    lowercase_chars = string.ascii_lowercase
    digit_chars = string.digits
    special_chars = string.punctuation
    
    # Remove similar characters if requested
    if exclude_similar:
        similar_chars = "Il1O0"
        uppercase_chars = ''.join(c for c in uppercase_chars if c not in similar_chars)
        lowercase_chars = ''.join(c for c in lowercase_chars if c not in similar_chars)
        digit_chars = ''.join(c for c in digit_chars if c not in similar_chars)
    
    # Combine selected character sets
    all_chars = ""
    if use_uppercase:
        all_chars += uppercase_chars
    if use_lowercase:
        all_chars += lowercase_chars
    if use_digits:
        all_chars += digit_chars
    if use_special:
        all_chars += special_chars
    
    if not all_chars:
        return "Please select at least one character type"
    
    # Generate password
    password = ''.join(random.choice(all_chars) for _ in range(length))
    return password

def main():
    st.set_page_config(page_title="Password Generator", page_icon="🔒")
    
    st.title("🔒 Secure Password Generator")
    st.write("Create strong, customized passwords for your accounts")
    
    # Password options
    st.subheader("Password Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        length = st.slider("Password Length", min_value=6, max_value=32, value=12)
        use_uppercase = st.checkbox("Include Uppercase Letters (A-Z)", value=True)
        use_lowercase = st.checkbox("Include Lowercase Letters (a-z)", value=True)
    
    with col2:
        use_digits = st.checkbox("Include Numbers (0-9)", value=True)
        use_special = st.checkbox("Include Special Characters (!@#$...)", value=True)
        exclude_similar = st.checkbox("Exclude Similar Characters (Il1O0)", value=False)
    
    # Generate password button
    if st.button("Generate Password", type="primary"):
        password = generate_password(
            length, 
            use_uppercase, 
            use_lowercase, 
            use_digits, 
            use_special, 
            exclude_similar
        )
        
        st.session_state.password = password
    
    # Display generated password
    if 'password' in st.session_state:
        st.subheader("Your Generated Password:")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.code(st.session_state.password, language=None)
        with col2:
            if st.button("Copy to Clipboard"):
                st.write("Password copied!")
                # Note: In a real Streamlit app, we'd use JavaScript for clipboard functionality
                # For this demo, we're just showing the UI element
    
    # Password strength indicator
    if 'password' in st.session_state and len(st.session_state.password) > 5:
        password = st.session_state.password
        strength = 0
        
        # Simple strength calculation
        if len(password) >= 12:
            strength += 1
        if any(c.isupper() for c in password):
            strength += 1
        if any(c.islower() for c in password):
            strength += 1
        if any(c.isdigit() for c in password):
            strength += 1
        if any(c in string.punctuation for c in password):
            strength += 1
        
        strength_labels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
        strength_colors = ["#FF0000", "#FF8000", "#FFFF00", "#80FF00", "#00FF00"]
        
        st.write("Password Strength:")
        st.progress(strength / 5)
        st.markdown(f"<span style='color:{strength_colors[strength]}'>{strength_labels[strength]}</span>", unsafe_allow_html=True)
    
    # Password tips
    with st.expander("Password Security Tips"):
        st.markdown("""
        - Use a different password for each account
        - Change your passwords regularly
        - Never share your passwords with others
        - Consider using a password manager
        - Enable two-factor authentication when available
        """)

if __name__ == "__main__":
    main()

# To run this app:
# 1. Save this code to a file named password_generator.py
# 2. Install Streamlit: pip install streamlit
# 3. Run the app: streamlit run password_generator.py
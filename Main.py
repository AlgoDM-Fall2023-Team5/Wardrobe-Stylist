import streamlit as st

def main():
    # Title and tag line with styling
    st.title(" 🌟 Personal Wardrobe Stylist 🌟 ")
    st.write("Let Your Event Speak Your Style! 💃🕺")

    # Overview text with emphasis on keywords

    st.header("👕 Your Style, Your Way")
    st.write("Embarking on a revolutionary journey in fashion technology, our Personal Wardrobe Stylist Application redefines how customers explore and embrace style. Seamlessly blending cutting-edge AI technology with an extensive product inventory, our mission is to simplify the daunting task of selecting the perfect outfit for every occasion. The interface serves as a gateway to this transformative experience, offering an intuitive platform where users effortlessly input event details, initiating a personalized fashion voyage. Through Streamlit's streamlined interface, users engage in a sophisticated yet user-friendly space, triggering AI-powered algorithms to craft bespoke fashion recommendations. This amalgamation of technology promises a refined, convenient, and engaging fashion exploration for our users.")
   
    #Video with a stylish frame
    st.header("🎥 Feature Highlight")
    st.video("https://youtu.be/TG9C7n1HXBAS", format="video/mp4")

    # User Guide with a call-to-action button
    st.header("📖 User Guide")
    st.write("Unlock the full potential of our application. Access the User Guide here:")
    user_guide_url = "https://codelabs-preview.appspot.com/?file_id=1rK05tYKUVYfXsGXxTgk34mNUvEnJMNN64T21XHXgxAM#0"
    st.markdown(f"[User Guide]({user_guide_url})")

    # Developer Guide with a call-to-action button
    st.header("🛠️ Developer Guide")
    st.write("Ready to dive into the technical details? Access the Developer Guide here:")
    developer_guide_url = "https://codelabs-preview.appspot.com/?file_id=1GLvJAY5Ad_vSvI_1TGS0YKVMwm8oBR0tY2SlN_XIitk#0"
    st.markdown(f"[User Guide]({developer_guide_url})")

if __name__ == "__main__":
    main()

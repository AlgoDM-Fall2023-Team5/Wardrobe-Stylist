import streamlit as st

def main():
    # Title and tag line with styling
    st.title(" Personal Wardrobe Stylist ")
    st.write("Let Your Event Speak Your Style! 💃🕺")

    # Overview text with emphasis on keywords
    st.header("🚀 Revolutionary Fashion Technology")
    st.write("Embark on a transformative journey with our Personal Wardrobe Stylist Application. "
             "Redefine how you explore and embrace style, blending cutting-edge AI technology with an extensive product inventory. "
             "Our mission is to simplify the daunting task of selecting the perfect outfit for every occasion.")

    st.subheader("🌈 Your Style, Your Way")
    st.write("The interface serves as a gateway to this transformative experience, offering an intuitive platform where users effortlessly input event details, initiating a personalized fashion voyage. "
             "Through Streamlit's streamlined interface, engage in a sophisticated yet user-friendly space, triggering AI-powered algorithms to craft bespoke fashion recommendations.")

    st.subheader("✨ Refined, Convenient, Engaging")
    st.write("This amalgamation of technology promises a refined, convenient, and engaging fashion exploration for our users.")

    # Video with a stylish frame
    st.header("🎥 Feature Highlight")
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", format="video/mp4")

    # User Guide with a call-to-action button
    st.header("📖 User Guide")
    st.write("Unlock the full potential of our application. Access the User Guide here:")
    user_guide_url = "https://codelabs-preview.appspot.com/?file_id=1rK05tYKUVYfXsGXxTgk34mNUvEnJMNN64T21XHXgxAM#0"
    st.button("📘 Open User Guide", on_click=lambda: st.markdown(f"[User Guide]({user_guide_url})"))

    # Developer Guide with a call-to-action button
    st.header("🛠️ Developer Guide")
    st.write("Ready to dive into the technical details? Access the Developer Guide here:")
    developer_guide_url = "https://codelabs-preview.appspot.com/?file_id=1GLvJAY5Ad_vSvI_1TGS0YKVMwm8oBR0tY2SlN_XIitk#0"
    st.button("👩‍💻 Open Developer Guide", on_click=lambda: st.markdown(f"[Developer Guide]({developer_guide_url})"))

if __name__ == "__main__":
    main()

import streamlit as st

def main():
    st.title(':robot_face: TIP AI-assisted Claims') 
    st.subheader('AI Models Testing System v0.1 (Internal Only)')
    st.divider()
    st.write("\n")
    st.write("\n")
    st.subheader('MODEL 1: Ceiling Material Detection')
    st.text('Please upload an image of ceiling to detect the material')

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="ceiling_01") 
    if uploaded_file is not None:
        img_data = uploaded_file.read()
        st.image(img_data)

    model_01_result = "Wooden Ceiling"
    st.text('Ceiling Material Detected: ')
    st.success('The ceiling material is: {}'.format(model_01_result))
    st.write("\n")
    st.write("\n")
    st.divider()
    st.write("\n")
    st.write("\n")
    st.subheader('MODEL 2: Percentage of Damage Detection')
    st.write("\n")
    st.text("Pease provide the following information for damage calculation:")
    st.divider()
    st.markdown("<h4 style='text-align: center; color: white;'>Image No. 1: Wall with Reference Object</h4>", unsafe_allow_html=True)
    st.write("\n")
    uploaded_file_damaged_01 = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="damaged_01")
    damage_result = 50
    if uploaded_file_damaged_01 is not None:
        img_damaged_01 = uploaded_file_damaged_01.read()
        st.image(img_damaged_01)
    ref_width = st.number_input('Reference Object Width in Image No. 1 (cm)', value=0, format="%d", step=1, key="width")
    ref_height = st.number_input('Reference Object Height in Image No. 1 (cm)', value=0, format="%d", step=1, key="height")
    st.divider()
    st.markdown("<h4 style='text-align: center; color: white;'>Image No. 2: Damaged Ceiling with Reference Object</h4>", unsafe_allow_html=True)
    st.text('Please upload an image of damaged ceiling for testing')

    uploaded_file_damaged_02 = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="damaged_02")
    if uploaded_file_damaged_02 is not None:
        img_damaged_02 = uploaded_file_damaged_02.read()
        st.image(img_damaged_02)

    check_camera_distance = st.checkbox("I have made sure that the camera-to-reference distance matches the reference height.", key="check")

    if check_camera_distance:
        st.success("You have checked the distance.")
    else:
        st.warning("Check your camera distance!")

    ref_distance = st.number_input('Distance Measured on the Ground from the Point under the Damage to Your Current Position (cm)', value=0, format="%d", step=1, key="distance")
    
    st.divider()
    st.text('Damage Percentage Calculated:')
    st.success('The damage percentage is {} %'.format(damage_result))

if __name__ == "__main__":
    main()
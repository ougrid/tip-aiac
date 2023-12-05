import streamlit as st
import tensorflow as tf
import cv2
import numpy as np
import PIL
from streamlit_drawable_canvas import st_canvas


def load_ceiling_type_model_and_labels():
    model = tf.keras.models.load_model("model.savedmodel")
    class_names = open("labels.txt", "r").readlines()
    return model, class_names


def process_ceiling_type_image(uploaded_file):
    img_data = PIL.Image.open(uploaded_file)
    image = cv2.cvtColor(np.array(img_data), cv2.COLOR_RGB2BGR)
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1
    return image


def make_ceiling_type_prediction(model, image, class_names):
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return class_name, confidence_score


def main():
    canvas_config = {
        "stroke_width": 3,
        "stroke_color": "#FF0000",
        "drawing_mode": "rect",
        # "line_color": "#00FF00",
        # "line_width": 3,
        "background_image": None,
    }
    damage_result = 50

    model, class_names = load_ceiling_type_model_and_labels()

    st.title(":robot_face: TIP AI-assisted Claims")
    st.subheader("AI Models Testing System v0.1 (Internal Only)")
    st.divider()
    st.write("\n")
    st.write("\n")
    st.subheader("MODEL 1: Ceiling Type Detection")
    st.text("Please upload an image of ceiling to detect the material")

    uploaded_file = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"], key="ceiling_01"
    )
    if uploaded_file is not None:
        image = process_ceiling_type_image(uploaded_file)
        class_name, confidence_score = make_ceiling_type_prediction(
            model, image, class_names
        )
        model_01_class_result = class_name[2:].strip()
        model_01_confidence_result = str(np.round(confidence_score * 100))[:-2]
    else:
        model_01_class_result = "-"
        model_01_confidence_result = "0"

    st.text("Ceiling Type Detected: ")
    st.success(model_01_class_result)
    st.text("(Predicted Class: {})".format(model_01_class_result))
    st.text("(Confidence Score: {}%)".format(model_01_confidence_result))
    st.write("\n")
    st.write("\n")
    st.divider()
    st.write("\n")
    st.write("\n")
    st.subheader("MODEL 2: Percentage of Damage Detection")
    st.text("Pease provide the following information for damage calculation:")
    st.divider()
    st.markdown(
        "<h4 style='text-align: center; color: white;'>Image No. 1: Wall with Reference Object</h4>",
        unsafe_allow_html=True,
    )
    st.write("\n")
    uploaded_file_damaged_01 = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"], key="damaged_01"
    )
    if uploaded_file_damaged_01 is not None:
        img_damaged_01 = uploaded_file_damaged_01.read()
        st.image(img_damaged_01)

    if uploaded_file_damaged_01 is not None:
        canvas_config["background_image"] = PIL.Image.open(uploaded_file_damaged_01)

        # Allow users to choose between drawing a rectangle and a line
        draw_mode = st.radio("Drawing tool:", ("Rectangle", "Line"))

        if draw_mode == "Rectangle":
            canvas_config["drawing_mode"] = "rect"
            canvas_config["stroke_color"] = "#FF0000"  # Red for rectangle
        else:
            canvas_config["drawing_mode"] = "line"
            canvas_config["stroke_color"] = "#00FF00"  # Green for line

        # Create the canvas
        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)", key="canvas", **canvas_config
        )
        # Process the canvas data
        if canvas_result.json_data is not None:
            # Extract rectangle and line data from canvas_result.json_data here
            pass

    ref_width = st.number_input(
        "Reference Object Width in Image No. 1 (cm)",
        value=0,
        format="%d",
        step=1,
        key="width",
        min_value=0,
    )
    ref_height = st.number_input(
        "Reference Object Height in Image No. 1 (cm)",
        value=0,
        format="%d",
        step=1,
        key="height",
        min_value=0,
    )
    st.divider()
    st.markdown(
        "<h4 style='text-align: center; color: white;'>Image No. 2: Damaged Ceiling with Reference Object</h4>",
        unsafe_allow_html=True,
    )
    st.text("Please upload an image of damaged ceiling for testing")

    uploaded_file_damaged_02 = st.file_uploader(
        "Choose an image...", type=["jpg", "jpeg", "png"], key="damaged_02"
    )
    if uploaded_file_damaged_02 is not None:
        img_damaged_02 = uploaded_file_damaged_02.read()
        st.image(img_damaged_02)

    check_camera_distance = st.checkbox(
        "I have made sure that the camera-to-reference distance matches the reference height. ฉันได้ตรวจสอบระยะห่างของกล้องกับวัตถุอ้างอิงแล้วว่าเท่ากับความสูงของวัตถุอ้างอิง",
        key="check",
    )

    if check_camera_distance:
        st.success("You have checked the distance. คุณได้ตรวจสอบระยะห่างแล้ว")
    else:
        st.warning(
            "Check your camera distance to the reference! กรุณาตรวจสอบระยะห่างของกล้องกับวัตถุอ้างอิง"
        )

    st.write("\n")
    st.write("\n")
    st.text("ระยะทางบนพื้นวัดจากจุดใต้บริเวณที่เสียหายถึงจุดที่คุณถ่ายภาพ (cm)")
    ref_distance = st.number_input(
        "Distance Measured on the Ground from the Point under the Damage to Your Current Position (cm)",
        value=0,
        format="%d",
        step=1,
        key="distance",
        min_value=0,
    )

    st.divider()
    st.text("Damage Percentage Calculated:")
    st.success("The damage percentage is {} %".format(damage_result))


if __name__ == "__main__":
    main()

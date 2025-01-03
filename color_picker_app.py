# Author: SP

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from PIL import Image, ImageDraw
import io

def rgb_to_hex(r, g, b):
    """Convert RGB values to a HEX color code."""
    return f"#{r:02X}{g:02X}{b:02X}"

def apply_background_color(image, color):
    """Apply a background color to the image."""
    background = Image.new("RGB", image.size, color)
    background.paste(image, mask=image.split()[3] if image.mode == "RGBA" else None)
    return background

# Streamlit app
st.title("3D RGB Color Picker with Photo Upload")

# Color Picker
default_color = st.color_picker("Pick a color", "#808080")
r, g, b = tuple(int(default_color[i:i+2], 16) for i in (1, 3, 5))

# RGB sliders
st.subheader("Adjust RGB Values")
r = st.slider("Red", 0, 255, r)
g = st.slider("Green", 0, 255, g)
b = st.slider("Blue", 0, 255, b)

# Show the selected color
hex_color = rgb_to_hex(r, g, b)
st.markdown("### Selected Color")
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 15px;">
        <div style="width: 75px; height: 75px; background-color: {hex_color}; border: 1px solid #000;"></div>
        <div>
            <b>RGB:</b> ({r}, {g}, {b})<br>
            <b>HEX:</b> {hex_color}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Photo Upload
uploaded_file = st.file_uploader("Upload a photo (JPEG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Load the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Apply the selected color as the background
    st.markdown("### Image with Selected Background Color")
    updated_image = apply_background_color(image, (r, g, b))
    st.image(updated_image, caption="Updated Image", use_container_width=True)

    # Save and Download Option
    buffer = io.BytesIO()
    updated_image.save(buffer, format="JPEG")
    buffer.seek(0)
    st.download_button(
        label="Download Image",
        data=buffer,
        file_name="updated_image.jpg",
        mime="image/jpeg"
    )

# Generate the 3D color cube
x, y, z = np.meshgrid(np.linspace(0, 255, 20), np.linspace(0, 255, 20), np.linspace(0, 255, 20))
colors = np.array([x.flatten() / 255, y.flatten() / 255, z.flatten() / 255]).T

fig = go.Figure()

# Add the color cube
fig.add_trace(go.Scatter3d(
    x=x.flatten(),
    y=y.flatten(),
    z=z.flatten(),
    mode="markers",
    marker=dict(
        size=4,
        color=colors,
        opacity=0.8
    )
))

# Highlight the selected point
fig.add_trace(go.Scatter3d(
    x=[r],
    y=[g],
    z=[b],
    mode="markers",
    marker=dict(
        size=10,
        color=f"rgb({r},{g},{b})"
    )
))

fig.update_layout(
    scene=dict(
        xaxis_title="Red",
        yaxis_title="Green",
        zaxis_title="Blue"
    )
)

# Display the 3D cube
st.plotly_chart(fig)

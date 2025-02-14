import streamlit as st
import PyPDF2
from io import BytesIO
from pdf2image import convert_from_bytes

def rotate_pdf(file_bytes, rotation_angle):
    pdfReader = PyPDF2.PdfReader(BytesIO(file_bytes))
    pdfWriter = PyPDF2.PdfWriter()
    
    for page in pdfReader.pages:
        page.rotate(rotation_angle)
        pdfWriter.add_page(page)
    
    output_stream = BytesIO()
    pdfWriter.write(output_stream)
    output_stream.seek(0)
    return output_stream

def display_pdf_page(file_bytes):
    images = convert_from_bytes(file_bytes, first_page=1, last_page=1)
    return images[0] if images else None

st.title("PDF Rotator")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    
    st.subheader("Select Rotation Angle")
    rotation_angle = st.radio("Rotate PDF by:", [0, 90, 180, 270], index=1)
    
    rotated_pdf = rotate_pdf(file_bytes, rotation_angle)
    
    st.subheader("Preview After Rotation (First Page)")
    rotated_image = display_pdf_page(rotated_pdf.getvalue())
    if rotated_image:
        st.image(rotated_image, caption=f"After {rotation_angle}° Rotation", use_container_width=True)
    
    st.download_button("Download Rotated PDF", rotated_pdf, file_name=f"{uploaded_file}_R{rotation_angle}.pdf", mime="application/pdf")

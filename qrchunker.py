import streamlit as st
import segno
from io import StringIO

st.title('QR Chunker')
IMAGE_SCALE=st.number_input('Set Image Scale:',1,10,10,1)
QR_CHUNK_SIZE = st.slider('Set QR Data Chunk Size:',100,5000,500,100,help="The amount of data included in a single QR Image")

tab_text , tab_file = st.tabs(["Text Chunker", "File Chunker"])

def qr_generator(datablob):
    QR_PNGS = []
    if len(datablob) > QR_CHUNK_SIZE:
        parts = [datablob[i:i+QR_CHUNK_SIZE] for i in range(0, len(datablob), QR_CHUNK_SIZE)]
        for part in parts:
            part = segno.make_qr(part)
            QR_PNGS.append(part.png_data_uri(scale=IMAGE_SCALE))
    else:
        qrcode = segno.make_qr(datablob)
        QR_PNGS.append(qrcode.png_data_uri(scale=IMAGE_SCALE))      
    
    return QR_PNGS


with tab_text:

    txt = st.text_area('Text to QRify', '''''')

    if st.button('Generate QR'):
        st.write(f"text size: {len(txt)}")
        if len(txt) > 0: 
            for images in qr_generator(txt):
                st.image(images)

with tab_file:
    uploaded_file = st.file_uploader("Choose a file to transform into QR Chunks")
    if uploaded_file is not None:
        # To read file as string:
        string_data = uploaded_file.getvalue().decode("utf-8")
        for images in qr_generator(string_data):
                st.image(images)
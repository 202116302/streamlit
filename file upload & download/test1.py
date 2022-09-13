import os.path
import pandas as pd

import streamlit as st


#
# # 디렉토리에 파일 저장
def save_uploaded_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file.name), "wb") as f:
        f.write(file.getbuffer())
    return st.success("Saved file :{} in {}".format(file.name, directory))


data_files = st.file_uploader("file upload")
if data_files is not None:
    st.write(type(data_files))
    save_uploaded_file('text', data_files)
    st.download_button(
        label="download",
        data=data_files,
        file_name='sample.xlsx',
        mime='text/xlsx',
    )







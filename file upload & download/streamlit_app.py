import os.path

import pandas as pd
from io import BytesIO
from pyproj import Transformer
import streamlit as st


#
# # 디렉토리에 파일 저장
def save_uploaded_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file.name), "wb") as f:
        f.write(file.getbuffer())
    return
    # return st.success("Saved file :{} in {}".format(file.name, directory))


def latlon2tm(lat, lon):
    transformer = Transformer.from_crs("epsg:4326", "epsg:5179")
    return transformer.transform(lat, lon)


def tm2grid(x, y, resolution=10):
    x = int(x)
    y = int(y)
    GRID_NAME = "가나다라마바사아"
    grid_name_x = GRID_NAME[x // 100000 - 7]
    grid_name_y = GRID_NAME[y // 100000 - 13]
    if resolution == 100:
        xloc = (x % 100000) // 100
        yloc = (y % 100000) // 100
    elif resolution == 1000:
        xloc = (x % 100000) // 1000
        yloc = (y % 100000) // 1000
    else:  # 10m resolution
        xloc = (x % 100000) // 10
        yloc = (y % 100000) // 10

    return f"{grid_name_x}{grid_name_y} {xloc}{yloc}"


def latlon2grid(lat, lon, resolution=10):
    y, x = latlon2tm(lat, lon)
    return tm2grid(x, y, resolution)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'})
    worksheet.set_column('A:A', None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data

data_file = st.file_uploader("file upload")
if data_file is not None:
    # st.write(type(data_file))
    save_uploaded_file('uploads', data_file)

    if data_file.name.endswith("csv"):
        df = pd.read_csv(os.path.join('uploads', data_file.name), encoding="cp949")
        grid_names = []
        for i, row in df.iterrows():
            grid_names.append(latlon2grid(row["위도"], row["경도"]))
        df["국가격자지점"] = grid_names
        output_filename = data_file.name.replace(".csv", "_변환완료.csv")
        st.download_button(
            label="download",
            data=df.to_csv().encode('utf-8-sig'),
            file_name=output_filename,
            mime='text/csv',
        )
    elif data_file.name.endswith("xlsx") or data_file.name.endswith("xls"):
        df = pd.read_excel(os.path.join('uploads', data_file.name))
        grid_names = []
        for i, row in df.iterrows():
            grid_names.append(latlon2grid(row["위도"], row["경도"]))
        df["국가격자지점"] = grid_names
        output_filename = data_file.name.replace(".xls", "_변환완료.xls")

        st.download_button(
            label="download",
            data=to_excel(df),
            file_name=output_filename,
            mime='application/vnd.ms-excel',
        )
    else:
        st.write("지원하지 않는 파일 포맷입니다. 지원하는 파일포맷은 csv, xlsx, xls입니다.")








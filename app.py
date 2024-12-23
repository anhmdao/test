import streamlit as st
import pandas as pd
from datetime import datetime
from config import QUERIES
from redash_api import redash_query

# Cấu hình trang Streamlit
st.set_page_config(page_title="Redash Query Tool", layout="wide")
st.title("Redash Query Tool")

# Chọn query
selected_query_id = st.selectbox("Chọn Query", options=list(QUERIES.keys()), format_func=lambda x: QUERIES[x])

# Tạo layout cho form nhập liệu
with st.form("query_form"):
    if selected_query_id == 1004:
        col1, col2 = st.columns(2)

        with col1:
            selected_date = st.date_input(
                "Chọn ngày",
                datetime.now(),
                format="YYYY-MM-DD"
            )

        with col2:
            shipper_id = st.number_input("Nhập Shipper ID", min_value=0, value=10804361, format="%d")
    else:
        tracking_id = st.text_input("Nhập Tracking ID", value="NJVN00529551309")

    submit_button = st.form_submit_button("Truy vấn dữ liệu")

if submit_button:
    # Chuẩn bị tham số
    if selected_query_id == 1004:
        params = {
            "date": selected_date.strftime("%Y-%m-%d"),
            "shipper_id": str(shipper_id)
        }
    else:
        params = {"tracking_id": f"'{tracking_id}'"}

    # Thực hiện truy vấn
    result_df = redash_query(selected_query_id, params)

    # Hiển thị kết quả
    if result_df is not None and not result_df.empty:
        st.success("Truy vấn thành công!")
        st.dataframe(result_df)

        # Tải xuống CSV
        csv = result_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Tải về dạng CSV",
            data=csv,
            file_name=f"query_{selected_query_id}_result.csv",
            mime="text/csv",
        )
    else:
        st.warning("Không có dữ liệu trả về.")
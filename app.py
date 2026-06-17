import pandas as pd
import streamlit as st

try:
    import folium
    from streamlit.components.v1 import html
except ImportError:
    folium = None
    html = None

st.set_page_config(page_title="주말 인기 대여점 지도", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("weekendpopular.csv", encoding="utf-8-sig")


df = load_data()
required_columns = ["대여 대여소명", "대여점위도", "대여점경도"]

if not all(col in df.columns for col in required_columns):
    st.error(f"CSV에 필요한 컬럼이 없습니다: {required_columns}")
    st.stop()

weekendpopular = df.dropna(subset=["대여점위도", "대여점경도"]).copy()

lat = weekendpopular["대여점위도"].mean()
lon = weekendpopular["대여점경도"].mean()

st.title("주말 인기 대여점 지도")
st.caption(f"중심 좌표: {lat:.6f}, {lon:.6f}")

if folium is not None and html is not None:
    map3 = folium.Map(location=[lat, lon], zoom_start=11, tiles="CartoDB positron")

    for _, row in weekendpopular.iterrows():
        folium.Marker(
            location=[row["대여점위도"], row["대여점경도"]],
            popup=row["대여 대여소명"],
            icon=folium.Icon(color="red", icon="star"),
        ).add_to(map3)

    html(map3.get_root().render(), height=650, scrolling=False)
else:
    st.warning("folium이 설치되지 않아 기본 Streamlit 지도로 표시합니다.")
    st.map(weekendpopular[["대여점위도", "대여점경도"]])

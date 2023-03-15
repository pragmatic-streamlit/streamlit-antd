import os
import streamlit as st
import streamlit.components.v1 as components

_DEVELOP_MODE = os.getenv('DEVELOP_MODE') or os.getenv('ST_ANTD_DEVELOP_MODE')

if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_tag",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_tag", path=build_dir)


def st_antd_tag():
    component_value = _component_func()
    return component_value


if _DEVELOP_MODE or os.getenv('SHOW_TAG_DEMO'):
    import streamlit as st
    st.set_page_config(layout="wide")

    event = st_antd_tag()
    print("event:", event)


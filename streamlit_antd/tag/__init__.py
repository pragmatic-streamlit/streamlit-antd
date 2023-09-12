import os
import streamlit as st
import streamlit.components.v1 as components
from typing import Union, Dict, List, Tuple

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'

if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_tag",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_tag", path=build_dir)


def st_antd_tag(tag_list: Tuple[str] = (), removable_start_idx: int = 0, log_tag_threshold: int = 20, new_tag_name='New Tag', key=None) -> List[str]:
    component_value = _component_func(tag_list=list(tag_list), removable_start_idx=removable_start_idx, log_tag_threshold=log_tag_threshold, new_tag_name=new_tag_name, key=key)
    return list(tag_list) if component_value is None else component_value


if _DEVELOP_MODE or os.getenv('SHOW_TAG_DEMO'):
    import streamlit as st
    st.set_page_config(layout="wide")

    event = st_antd_tag(key='demo1')
    print("event:", event)
    
    event = st_antd_tag(['tag1', 'tag2', 'tag3'], 2, 'new', key='demo2')
    print("event:", event)
    
    event = st_antd_tag(['tag1', 'tag2', 'tag3tag3tag3tag3tag3tag3tag3tag3tag3tag3tag3'], 2, 50, 'new', key='demo3')
    print("event:", event)


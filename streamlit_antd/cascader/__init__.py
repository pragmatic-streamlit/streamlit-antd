import os
import streamlit as st
import streamlit.components.v1 as components
from typing import Any

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_cascader",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_cascader", path=build_dir)


def set_session_value(key: str, value: Any):
    st.session_state[key] = value
    
def get_session_value(key):
    if key not in st.session_state:
        return None
    return st.session_state[key]

def st_antd_cascader(options, multiple=False, key=None, **kwargs):
    on_change = kwargs.get("on_change", None)
    value_key = f"{key}_value"
    if on_change:
        del kwargs["on_change"]
    prev_value = get_session_value(value_key) if on_change else None
    component_value = _component_func(options=options, multiple=multiple, key=key, default=None, **kwargs)
    if component_value != prev_value:
        set_session_value(value_key, component_value)
        on_change and on_change()
    return component_value


if _DEVELOP_MODE:
    import streamlit as st
    options = [
        {
            "value": 'zhejiang',
            "label": 'Zhejiang',
            "children": [
            {
                "value": 'hangzhou',
                "label": 'Hangzhou',
                "children": [
                    {
                        "value": 'xihu',
                        "label": 'West Lake',
                    },
                             {
                        "value": 'tt',
                        "label": 'TTT',
                    },
                    {
                        "value": 'xiasha',
                        "label": 'Xia Sha',
                        "disabled": True,
                    },
                ],
            },
            ],
        },
        {
            "value": 'jiangsu',
            "label": 'Jiangsu',
            "children": [
            {
                "value": 'nanjing',
                "label": 'Nanjing',
                "children": [
                {
                    "value": 'zhonghuamen',
                    "label": 'Zhong Hua men',
                },
                ],
            },
            ],
        },
    ]
    st.write('Options:')
    st.code(options)
    multiple = st.checkbox('Multiple')
    selected = st_antd_cascader(options, multiple=multiple, key="abc", **{ "defaultValue": "zhonghuamen" })
    st.write("Selected return: ")
    st.write(selected)

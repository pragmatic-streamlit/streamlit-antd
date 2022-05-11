import os
import streamlit.components.v1 as components

_DEVELOP_MODE = os.getenv('DEVELOP_MODE')


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_cascader",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_cascader", path=build_dir)


def st_antd_cascader(options, multiple=False, key=None):
    component_value = _component_func(options=options, multiple=multiple, key=key, default=None)
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
    selected = st_antd_cascader(options, multiple=multiple, key="abc")
    st.write("Selected return: ")
    st.write(selected)

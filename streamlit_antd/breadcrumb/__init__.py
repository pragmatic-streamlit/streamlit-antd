import os
import streamlit.components.v1 as components

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_breadcrumb",
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_breadcrumb", path=build_dir)


def st_antd_breadcrumb(items, key=None):
    component_value = _component_func(items=items, key=key, default=None)
    return component_value


if _DEVELOP_MODE:
    import streamlit as st
    items = [{"Label": "Home", "Other": "OtherValue"}, {"Label": "Application Center"}, {"Label": "Application List"}, {"Label": "An Application"}]
    st.write('Items:')
    st.code(items)
    clicked_event = st_antd_breadcrumb(items)
    st.write("Click return: ")
    st.write(clicked_event)

import os
import streamlit.components.v1 as components
from dataclasses import dataclass, asdict, field
from typing import List

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_result",
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_result", path=build_dir)

@dataclass
class Action:
    name: str
    title: str
    primary: bool = field(default=False)


def st_antd_result(
        title: str,
        sub_title: str,
        actions: List[Action], *,
        status='success', key=None):
    actions = [asdict(i) for i in actions] if actions else []
    component_value = _component_func(
        title=title,
        sub_title=sub_title,
        status=status,
        actions=actions,
        key=key, default=None)
    return component_value


if _DEVELOP_MODE or os.getenv('DEBUG_ANTD_DEMO'):
    import streamlit as st
    st.set_page_config(layout="wide")
    title = 'Successfully Purchased Cloud Server ECS!'
    sub_title = 'Order number: 2017182818828182881 Cloud server configuration takes 1-5 minutes, please wait.'
    actions = [
        Action('back', 'Go Console', primary=True),
        Action('buy', 'Buy Again'),
    ]
    clicked_event = st_antd_result(title, sub_title, actions)
    st.write("Click return: ", clicked_event)

    clicked_event = st_antd_result(title, sub_title, actions, status='error')
    st.write("Click return: ", clicked_event)
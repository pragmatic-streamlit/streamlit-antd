import os
from hashlib import md5
import streamlit.components.v1 as components
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Optional, Dict, Tuple

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_cards",
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_cards", path=build_dir)

@dataclass
class Action:

    action: str
    icon: str

@dataclass
class Item:

    id: str
    title: str
    description: str
    email: Optional[str] = field(repr=False, default=None)
    cover: Optional[str] = field(repr=False, default=None)
    avatar: Optional[str] = field(repr=False, default=None)
    actions: Optional[List[Action]] = field(repr=False, default=None)

def _get_avatar_url(email):
    if isinstance(email, str):
        email = email.encode('utf-8')
    hash = md5(email).hexdigest()
    return f'https://cdn.v2ex.com/gravatar/{hash}'

    
def st_antd_cards(items: List[Item], *,
                desc_max_len=64,
                width=240,
                height=160,
                margin='15px',
                video_volume=0.3,
                show_search=False,
                search_text=None,
                key=None):
    for item in items:
        item.actions = item.actions or []
        if item.email and not item.avatar:
            item.avatar = _get_avatar_url(item.email)
    component_value = _component_func(
        width=width,
        video_volume=video_volume,
        height=height,
        margin=margin,
        items=[asdict(item) for item in items],
        desc_max_len=desc_max_len,
        show_search=show_search,
        search_text=search_text or '',
        key=key, default=None)
    return component_value


if _DEVELOP_MODE or os.getenv('DEBUG_ANTD_DEMO'):
    import streamlit as st
    st.set_page_config(layout="wide")
    width = st.number_input('Card Width', value=240)
    height = st.number_input('Card Width', value=160)
    items = [
        Item(
            str(i),
            "Docking",
            """
            Molecular Docking is the computational modeling of the structure of complexes formed by two or more interacting molecules. The goal of molecular docking is the prediction of the three dimensional structures of interest. Docking itself only produces plausible candidate structures. These candidates are ranked using methods such as scoring functions to identify structures that are most likely to occur in nature. The state of the art of various computational aspects of molecular docking based virtual screening of database of small molecules is presented. This review encompasses molecular docking approaches, different search algorithms and the scoring functions used in docking methods and their applications to protein and nucleic acid drug targets. Limitations of current technologies as well as future prospects are also presented.
            """,
            cover="http://localhost:8000/tutorial.mp4",
            avatar="https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50.png",
            actions=[
                Action(**{'action': 'detail', 'icon': 'BarsOutlined'}),
                Action(**{'action': 'edit', 'icon': 'EditOutlined'}),
                Action(**{'action': 'setting', 'icon': 'SettingOutlined'}),
                Action(**{'action': 'delete', 'icon': 'DeleteOutlined'}),
             ]
        ) if i % 2 else 
        Item(
            str(i),
            "Docking",
            """
            Molecular Docking is the computational modeling of the structure of complexes formed by two or more interacting molecules. The goal of molecular docking is the prediction of the three dimensional structures of interest. Docking itself only produces plausible candidate structures. These candidates are ranked using methods such as scoring functions to identify structures that are most likely to occur in nature. The state of the art of various computational aspects of molecular docking based virtual screening of database of small molecules is presented. This review encompasses molecular docking approaches, different search algorithms and the scoring functions used in docking methods and their applications to protein and nucleic acid drug targets. Limitations of current technologies as well as future prospects are also presented.
            """,
            cover="https://openfiles.mlops.dp.tech/projects/launching/231a934b9ea0422ab49ed6b1ec0bc112/42.jpeg",
            email="mapix.me@gmail.com",
            actions=[
                Action(**{'action': 'detail', 'icon': 'BarsOutlined'}),
                Action(**{'action': 'edit', 'icon': 'EditOutlined'}),
                Action(**{'action': 'setting', 'icon': 'SettingOutlined'}),
                Action(**{'action': 'delete', 'icon': 'DeleteOutlined'}),
             ]
        ) 
        for i in range(10)
    ]
    clicked_event = st_antd_cards(items, width=width, height=height, show_search=True,
                                  search_text='Docking',
                                   key='demo')
    st.write("Click return: ")
    st.write(clicked_event)

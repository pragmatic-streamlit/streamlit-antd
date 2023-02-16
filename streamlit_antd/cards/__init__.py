import os
from hashlib import md5
import streamlit.components.v1 as components
from dataclasses import dataclass, asdict, field
from typing import Optional, List

_DEVELOP_MODE = os.getenv('DEVELOP_MODE')


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
class Item:

    id: str
    title: str
    description: str
    email: Optional[str] = field(repr=False, default=None)
    cover: Optional[str] = field(repr=False, default=None)
    avatar: Optional[str] = field(repr=False, default=None)

def _get_avatar_url(email):
    if isinstance(email, str):
        email = email.encode('utf-8')
    hash = md5(email).hexdigest()
    return f"https://www.gravatar.com/avatar/{hash}"


def st_antd_cards(items: List[Item], *,
                 show_edit_action: bool=True,
                 show_setting_action: bool=True,
                 show_open_action: bool=True,
                 show_delete_action: bool =True,
                 desc_max_len=64,
                 key=None):
    for item in items:
        if item.email and not item.avatar:
            item.avatar = _get_avatar_url(item.email)
    component_value = _component_func(
        items=[asdict(item) for item in items],
        show_edit_action=show_edit_action,
        show_setting_action=show_setting_action,
        show_open_action=show_open_action,
        show_delete_action=show_delete_action,
        desc_max_len=desc_max_len,
        key=key, default=None)
    return component_value


if _DEVELOP_MODE or os.getenv('DEBUG_ANTD_DEMO'):
    import streamlit as st
    st.set_page_config(layout="wide")
    items = [
        Item(
            str(i),
            "Docking",
            """
            Molecular Docking is the computational modeling of the structure of complexes formed by two or more interacting molecules. The goal of molecular docking is the prediction of the three dimensional structures of interest. Docking itself only produces plausible candidate structures. These candidates are ranked using methods such as scoring functions to identify structures that are most likely to occur in nature. The state of the art of various computational aspects of molecular docking based virtual screening of database of small molecules is presented. This review encompasses molecular docking approaches, different search algorithms and the scoring functions used in docking methods and their applications to protein and nucleic acid drug targets. Limitations of current technologies as well as future prospects are also presented.
            """,
            cover="https://www.researchgate.net/profile/Monika-Gaba/publication/279179780/figure/fig1/AS:391991113338883@1470469372538/Figure-Molecular-docking-of-ligand-to-a-protein-receptor-to-produce-a-complex.png",
            avatar="https://www.gravatar.com/avatar/205e460b479e2e5b48aec07710c08d50.jpg"
        ) if i % 2 else 
        Item(
            str(i),
            "Docking",
            """
            Molecular Docking is the computational modeling of the structure of complexes formed by two or more interacting molecules. The goal of molecular docking is the prediction of the three dimensional structures of interest. Docking itself only produces plausible candidate structures. These candidates are ranked using methods such as scoring functions to identify structures that are most likely to occur in nature. The state of the art of various computational aspects of molecular docking based virtual screening of database of small molecules is presented. This review encompasses molecular docking approaches, different search algorithms and the scoring functions used in docking methods and their applications to protein and nucleic acid drug targets. Limitations of current technologies as well as future prospects are also presented.
            """,
            cover="http://localhost:1024/artifacts/covers/9775dee02577400b8886f24659f6090c.jpeg",
            email="mapix.me@gmail.com"
        ) 
        for i in range(10)
    ]
    st.write('Items:')
    st.code(items)
    clicked_event = st_antd_cards(items)
    st.write("Click return: ")
    st.write(clicked_event)

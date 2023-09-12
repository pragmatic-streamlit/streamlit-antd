import os
from typing import List, Optional
from dataclasses import dataclass, field, asdict
import streamlit.components.v1 as components

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_steps",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_steps", path=build_dir)

@dataclass
class Item:

    title :str
    description: str
    subTitle: Optional[str] = field(default=None)


def st_antd_steps(items: List[Item], current: int, *, process: bool=False, error: bool=False, direction="horizontal", label_placement="horizontal", key=None):
    items = [asdict(item) for item in items]
    component_value = _component_func(
        items=items, 
        current=current,
        process=process,
        direction=direction,
        error=error,
        label_placement=label_placement,
        key=key, default=None)
    return component_value


if _DEVELOP_MODE or os.getenv('DEBUG_ANTD_DEMO'):
    from collections import defaultdict
    import streamlit as st
    st.set_page_config(page_title='Demo',
                    layout='wide',
                    initial_sidebar_state='expanded')

    st.subheader('Step Form demo')
    items = [
          Item('Inputs', 'This is a description.'),
          Item('Options', 'This is a description.'),
          Item('Review', 'This is a description.'),
        ]
    
    if not hasattr(st.session_state, 'current_step'):
        st.session_state.params = defaultdict(dict)
    params = st.session_state.params

    def render_step(step: int):
        if step < 2:
            param = st.text_input(f"Step {step}", value=params.get(step, {}).get('param', ''), key=f"{step}")
            if not param:
                st.error("Param required")
                return False
            params[step]['param'] = param
        else:
            st.json(params)
        return True
    
    if not hasattr(st.session_state, 'current_step'):
        st.session_state.current_step = 0
    elif 0 not in params:
        st.session_state.current_step = 0
    container = st.container()
    ok_next = render_step(st.session_state.current_step)
    prev_btn, next_btn = st.columns(2)
    done = False
    if st.session_state.current_step < len(items) - 1:
        if next_btn.button("Next", use_container_width=True, type="primary", disabled=not ok_next):
            st.session_state.current_step += 1
            st.experimental_rerun()
    elif st.session_state.current_step == len(items) - 1:
        done = next_btn.button("Done", use_container_width=True, type="primary", disabled=not ok_next)
    if st.session_state.current_step > 0:
        if prev_btn.button("Prev", use_container_width=True):
            st.session_state.current_step -= 1
            st.experimental_rerun()
    with container:
        st_antd_steps(items, st.session_state.current_step, key="abc")


    st.write('Current Step', st.session_state.current_step)
    st.write('Done? :', done)
    if done:
        st.write(params)

    st.subheader('Progress Demo')
    items = [
          Item('Inputs', 'This is a description.' * 10),
          Item('Options', 'This is a description.' * 10 ),
          Item('Review', 'This is a description.' * 10),
        ]
    st_antd_steps(items, 0, process=False, key="a")
    st_antd_steps(items, 1, process=True, key="b")
    st_antd_steps(items, 2, process=False, key="c")
    st_antd_steps(items, 1, process=False, error=True, key="d")
    st_antd_steps(items, 1, process=True, direction="vertical", key="e")
    st_antd_steps(items, 1, process=False, error=True, direction="vertical", key="g")
    st_antd_steps(items, 1, process=True, label_placement="vertical", key="f")
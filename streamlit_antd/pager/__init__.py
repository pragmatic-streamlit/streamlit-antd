import os
import streamlit.components.v1 as components


_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_pager",
        url="http://localhost:3000",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_pager", path=build_dir)


def st_pager(loader, total, *, page_size=10, state=None, args=None, kwargs=None, key=None):
    import streamlit as st
    state = state if state else st.session_state

    kwargs = {} if kwargs is None else kwargs
    pager_state_key = f'{key}-pager-state'
    page_info = state.get(pager_state_key, {})

    page = page_info.get('page', 1)
    page_size = page_info.get('page_size', page_size)
    elements = loader(page, page_size, *(args or []), **(kwargs or {}))
    event = _component_func(
        page=page,
        page_size=page_size,
        total=total,
        key=key, default=None)
    action_id = event and event.get('id')
    if action_id:
        session_key = f'components/streamlit-antd/pager/state/{key}/last_action_id'
        if session_key not in st.session_state:
            st.session_state[session_key] = action_id
        else:
            if action_id == st.session_state[session_key]:
                event = None
            else:
                st.session_state[session_key] = action_id
    if event and event['payload']['action'] == 'pager':
        state[pager_state_key] = event['payload']
        st.experimental_rerun()
    return elements


if _DEVELOP_MODE or os.getenv('DEBUG_ANTD_DEMO'):
    import streamlit as st
    st.set_page_config(layout="wide")
    elements = list(range(100))

    def get_paged_elements(page, size):
        st.write(elements[(page -1) * size:page * size])
    
    content = st.container()
    sub_elements = st_pager(get_paged_elements, len(elements), key='aa')
    with content:
        st.write(sub_elements)

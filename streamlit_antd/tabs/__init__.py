import os
import streamlit as st
import streamlit.components.v1 as components

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_tabs",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_tabs", path=build_dir)


def st_antd_tabs(items, *, default_active=None, session_state=None, key=None):
    component_value = _component_func(items=items, key=key, default_active=default_active, default=None)
    if default_active:
        session_state = session_state if session_state is not None else st.session_state
        key = f'streamlit-tabs-{key}-state'
        state = session_state.get(key, None)
        if state != default_active:
            session_state[key] = default_active
            return [i for i in items if i['Label'] == default_active][0]
        elif component_value is None and state:
            return [i for i in items if i['Label'] == state][0]
    return component_value


if _DEVELOP_MODE:
    import streamlit as st
    items = [{"Label": "Home", "Other": "OtherValue"}, {"Label": "Application Center"}, {"Label": "Application List"}, {"Label": "An Application"}]
    st.write('Items:')
    st.code(items)
    clicked_event = st_antd_tabs(items)
    st.write("Click return: ")
    st.write(clicked_event)

    from streamlit_router import StreamlitRouter
    router = StreamlitRouter(default_path='/')

    def show_index(tab=None):
        items = [{"Label": "1", "Other": "OtherValue"}, {"Label": "2"}, {"Label": "3"}, {"Label": "4"}]
        clicked_event = st_antd_tabs(items, default_active=tab, session_state=router.get_request_state(), key='2')
        st.write("Click return: ")
        st.write(clicked_event)
    
    
    router.register(show_index, "/", methods=['GET'])
    router.register(show_index, "/<string:tab>", methods=['GET'], endpoint='show_index_tab')
    router.serve()

    if st.button('show_tab 1'):
        router.redirect(*router.build('show_index_tab', {'tab': "1"}))
    if st.button('show_tab 2'):
        router.redirect(*router.build('show_index_tab', {'tab': "2"}))
    if st.button('show_tab 3'):
        router.redirect(*router.build('show_index_tab', {'tab': "3"}))


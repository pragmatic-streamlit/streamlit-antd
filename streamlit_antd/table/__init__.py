import os
import streamlit as st
import streamlit.components.v1 as components

_DEVELOP_MODE = os.getenv('DEVELOP_MODE')


if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_breadcrumb",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_table", path=build_dir)


def st_antd_table(df, row_key=None,
        columns=None,
        hidden_columns=None,
        fixed_left_columns=None, 
        fixed_right_columns=None,
        custom_columns_width=None,
        default_column_width=140,
        tags_columns=None,
        sorter_columns=None,
        actions=None,
        action_width=200,
        min_height=200,
        key=None):
    sorter_columns = sorter_columns or list(df.columns) 
    tags_columns = tags_columns or ['tags']
    if 'id' not in list(df.columns) and not row_key:
        df = df.reset_index()
        df = df.rename(columns={"index":"id"})
        df['id'] = df.index + 1
        row_key = 'id'
        hidden_columns = (hidden_columns or [])+ ['id']
    data = df.to_dict(orient='records')
    if not columns:
        columns = []
        for name in list(df.columns):
            if hidden_columns and name in hidden_columns:
                continue
            fixed = False
            if fixed_left_columns and name in fixed_left_columns:
                fixed = 'left'
            if fixed_right_columns and name in fixed_right_columns:
                fixed = 'right'
            column = {  
                'title': name.capitalize(),
                'width': custom_columns_width.get(name, default_column_width) if custom_columns_width else default_column_width,
                'dataIndex': name,
                'key': name,
                'fixed': fixed,
            }
            columns.append(column)
    component_value = _component_func(data=data, columns=columns, actions=actions, 
        row_key=row_key, min_height=min_height, tags_columns=tags_columns, sorter_columns=sorter_columns,
        action_width=action_width, key=key, default=None)
    action_id = component_value and component_value.get('action_id')
    if action_id:
        session_key = 'components/streamlit-antd/table/state'
        if session_key not in st.session_state:
            st.session_state[session_key] = {}
        if action_id in st.session_state[session_key]:
            del component_value['action']
            del component_value['action_records']
            del component_value['action_id']
        else:
            st.session_state[session_key][action_id] = True
    return component_value


if _DEVELOP_MODE:
    import streamlit as st
    st.set_page_config(layout="wide")
    import pandas as pd

    if 'deleted' not in st.session_state:
        st.session_state.deleted = set()
        
    data = [{
        "a": i,
        "name": f"Mapix {i}",
        "age": 10 + i,
        "tags": "Apple, Aibee",
        "address": f"Beijing no. {i}",
        "address1": f"Beijing no. {i}",
        "address2": f"Beijing no. {i}",
        "address3": f"Beijing no. {i}",
        "address4": f"Beijing no. {i}",
        "address5": f"Beijing no. {i}",
        "address6": f"Beijing no. {i}",
        "address7": f"Beijing no. {i}",
        "address8": f"Beijing no. {i}",
        "address9": f"Beijing no. {i}",
        "address10": f"Beijing no. {i}",
        "createdAt": f"2012-222-{i}",
    } for i in range(100)]
    data = [i for i in data if i['name'] not in st.session_state.deleted]
    data = pd.DataFrame(data)

    r = st_antd_table(data, 
        hidden_columns=['a'],
        fixed_left_columns=['name'],
        fixed_right_columns=['createdAt'],
        custom_columns_width={'name': 150, 'tags': 200},
        actions=['Delete', 'Edit'],
        key='addd')
    st.write(r)
    if r and r.get('action') == 'Delete':
        print('delete event found')

        st.session_state.deleted.add(r['action_records'][0]['name'])
        st.experimental_rerun()
  

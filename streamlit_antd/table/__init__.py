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
        searchable_columns=None,
        iframes_mapper=None,
        actions=None,
        actions_mapper=None,
        iframe_height=300,
        default_expand_all_rows=None,
        batch_actions=None,
        linkable_columns=None,
        revoke_height_step=0,
        expand_column=None,
        action_width=200,
        min_height=200,
        key=None):
    sorter_columns = sorter_columns or list(df.columns) 
    searchable_columns = searchable_columns or list(df.columns)
    tags_columns = tags_columns or ['tags']
    if 'id' not in list(df.columns) and not row_key:
        df = df.reset_index()
        df = df.rename(columns={"index":"id"})
        df['id'] = df.index + 1
        row_key = 'id'
        hidden_columns = (hidden_columns or [])+ ['id']
    data = df.to_dict(orient='records')
    if callable(actions_mapper):
        for item in data:
            item['_antd_table_actions'] = actions_mapper(item)
    if callable(iframes_mapper):
        for item in data:
            item['_antd_table_iframes'] = iframes_mapper(item)
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
    event = _component_func(data=data, columns=columns, actions=actions or None, 
        row_key=row_key, min_height=min_height, tags_columns=tags_columns or None, sorter_columns=sorter_columns or None,
        linkable_columns=linkable_columns or [], batch_actions=batch_actions or None, revoke_height_step=revoke_height_step,
        searchable_columns=searchable_columns or None, actions_in_row=bool(actions_mapper), iframe_height=iframe_height,
        expand_column=expand_column, default_expand_all_rows=default_expand_all_rows, iframes_in_row=bool(iframes_mapper),
        action_width=action_width, key=key, default=None)
    action_id = event and event.get('id')
    if action_id:
        session_key = f'components/streamlit-antd/table/state/{key}/last_action_id'
        if session_key not in st.session_state:
            st.session_state[session_key] = action_id
        else:
            if action_id == st.session_state[session_key]:
                event = None
            else:
                st.session_state[session_key] = action_id
    return event


if _DEVELOP_MODE:
    import streamlit as st
    st.set_page_config(layout="wide")
    from datetime import datetime
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
        "address10": f"Beijing no. {i} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "description": "Specify the width of columns if header and cell do not align properly. If specified width is not working or have gutter between columns, please try to leave one column at least without width to fit fluid layout, or make sure no long word to break table layout.",
        "createdAt": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    } for i in range(100)]
    data = [i for i in data if i['name'] not in st.session_state.deleted]
    data = pd.DataFrame(data)

    
    event = st_antd_table(data, 
        hidden_columns=['a'],
        fixed_left_columns=['name'],
        linkable_columns=['name'],
        fixed_right_columns=['createdAt'],
        custom_columns_width={'name': 150, 'tags': 200},
        revoke_height_step=300,
        iframe_height=300,
        expand_column="description",
        batch_actions=['Batch Delete', 'Batch Mark'],
        iframes_mapper=lambda x: ['//grafana.data-exchange.aibee.cn/d-solo/nginx/nginx-ingress-controller?orgId=1&refresh=5s&panelId=86&theme=light&var-namespace=All&var-controller_class=All&var-controller=All&var-ingress=customer-flow-postgrest'] * 4,
        actions_mapper=lambda x: ['Delete', 'Edit'] if x['age'] % 2==0 else ['View'], key='abc')
    st.write(event)
    if event and event['payload']['action'] in ('Delete', 'Batch Delete'):
        print('delete event found')
        for i in event['payload']['records']:
            st.session_state.deleted.add(i['name'])
        st.experimental_rerun()
  

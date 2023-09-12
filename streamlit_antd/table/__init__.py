import os
import streamlit as st
import streamlit.components.v1 as components

_DEVELOP_MODE = os.getenv('STREAMLIT_ANTD_DEVELOP_MODE') == 'true'

if _DEVELOP_MODE:
    _component_func = components.declare_component(
        "streamlit_antd_table",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_antd_table", path=build_dir)


def st_antd_table(df, *, row_key=None,
        columns=None,
        hidden_columns=None,
        fixed_left_columns=None,
        fixed_right_columns=None,
        custom_columns_width=None,
        default_column_width=None,
        tags_columns=None,
        sorter_columns=None,
        searchable_columns=None,
        ellipsis_column_configs=None,
        iframes_mapper=None,
        actions=None,
        actions_mapper=None,
        iframe_height=300,
        default_expand_all_rows=None,
        batch_actions=None,
        linkable_columns=None,
        expand_column=None,
        expand_json=False,
        action_width=None,
        compact_layout=False,
        show_pager=True,
        color_backgroud='#f0f0f0',
        rows_per_page=20,
        min_height=200,
        enable_dynamic_pager=False,
        dynamic_pager_total=0,
        dynamic_pager_page=0,
        unsafe_html_columns=None,
        sticky=False,
        ellipsis_config=None,
        scroll={ 'x': True },
        key=None):
    if columns:
        df = df[columns]
    sorter_columns = sorter_columns or [column for column in df.columns if df.dtypes[column].kind == 'O']
    searchable_columns = searchable_columns or [column for column in df.columns if df.dtypes[column].kind == 'O']
    tags_columns = tags_columns or []
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
        linkable_columns=linkable_columns or [], batch_actions=batch_actions or None,
        searchable_columns=searchable_columns or None, actions_in_row=bool(actions_mapper), iframe_height=iframe_height,
        expand_column=expand_column, default_expand_all_rows=default_expand_all_rows, iframes_in_row=bool(iframes_mapper),
        ellipsis_column_configs=ellipsis_column_configs,
        rows_per_page=rows_per_page,
        compact_layout=compact_layout,
        expand_json=expand_json,
        dynamic_pager_page=dynamic_pager_page,
        enable_dynamic_pager=enable_dynamic_pager,
        dynamic_pager_total=dynamic_pager_total,
        show_pager=show_pager,
        color_backgroud=color_backgroud,
        scroll=scroll,
        ellipsis_config=ellipsis_config,
        action_width=action_width, unsafe_html_columns=unsafe_html_columns, sticky=sticky, key=key, default=None)
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


def st_antd_dynamic_table(key, df_loader, total, page_size=10, state=None, **kwargs):
    kwargs['key'] = key
    pager_key = f'{key}-pager'
    kwargs['show_pager'] = True
    kwargs['enable_dynamic_pager'] = True
    state = state if state else st.session_state
    page_info = state.get(pager_key, {})
    page = page_info.get('page', 1)
    page_size = page_info.get('page_size', page_size)
    kwargs['dynamic_pager_page'] = page
    kwargs['rows_per_page'] = page_size
    kwargs['dynamic_pager_total'] = total
    df = df_loader(page, page_size)
    event = st_antd_table(df, **kwargs)
    if event and event['payload']['action'] == 'pager':
        state[pager_key] = event['payload']['records'][0]
        st.experimental_rerun()
    return event


if _DEVELOP_MODE or os.getenv('SHOW_TABLE_DEMO'):
    import streamlit as st
    st.set_page_config(layout="wide")
    import json
    from datetime import datetime
    import pandas as pd

    if 'deleted' not in st.session_state:
        st.session_state.deleted = set()

    func = st.selectbox('Demo', ['Table', 'Dynamic Table'])
    expand_json = st.checkbox('Expand Json')
    
    show_pager = st.checkbox('Show Pager', True)
    desc = "Specify the width of columns if header and cell do not align properly. If specified width is not working or have gutter between columns, please try to leave one column at least without width to fit fluid layout, or make sure no long word to break table layout."
    data = [{
        "a": i,
        "name": f"Mapix {i}",
        "avatar": f"<img width=\"100\" height=\"100\" src=\"https://openfiles.mlops.dp.tech/projects/launching/a12d15ff7b76432994d2cb81df28983a/home-3.png\" />",
        "age": 10 + i,
        "tags": "Apple, Google",
        "address": f"Beijing no. {i} aaaaaaa",
        "address1": f"Beijing no. {i} bbbbbbbb",
        "address2": f"Beijing no. {i} ccccccc",
        "address3": f"Beijing no. {i} ddddddd",
        "address4": f"Beijing no. {i}",
        "address5": f"Beijing no. {i}",
        "address6": f"Beijing no. {i}",
        "address7": f"Beijing no. {i}",
        "address8": f"Beijing no. {i}",
        "address9": f"Beijing no. {i}",
        "address10": f"Beijing no. {i} xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "description": json.dumps({'desc': desc}) if expand_json else desc,
        "createdAt": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    } for i in range(100)]
    data = [i for i in data if i['name'] not in st.session_state.deleted]
    data = pd.DataFrame(data)

    if func == 'Dynamic Table':
        event = st_antd_dynamic_table('demo-dynamic', lambda page, size: data.iloc[(page - 1)*size:page*size], len(data.index), unsafe_html_columns=['avatar'])
        st.write(event)
    else:
        event = st_antd_table(data,
            hidden_columns=['a'],
            row_key='a',
            sticky=False,
            unsafe_html_columns=['avatar'],
            tags_columns=['tags'],
            fixed_left_columns=['name'],
            linkable_columns=['name'],
            expand_column="description",
            expand_json=expand_json,
            show_pager=show_pager,
            batch_actions=['Batch Delete', 'Batch Mark'],
            ellipsis_config={ 'address': 10, 'address1': 15, 'address2': 20, 'address3': 25 },
            actions_mapper=lambda x: ['Delete', 'Edit'] if x['age'] % 2==0 else ['View'], key='abc')
        st.write(event)
        if event and event['payload']['action'] in ('Delete', 'Batch Delete'):
            print('delete event found')
            for i in event['payload']['records']:
                st.session_state.deleted.add(i['name'])
            st.experimental_rerun()


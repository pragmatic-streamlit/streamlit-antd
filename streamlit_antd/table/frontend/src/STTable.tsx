import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Table, Tag, Space} from 'antd';
import { ColumnProps, ColumnsType, ColumnType } from "antd/lib/table";
import { v4 as uuidv4 } from 'uuid';


interface IExtra {
  action: string
}

interface State {
  pagination: any
  filters: any 
  sorter: any 
  action: string 
  action_records: any[]
  action_id: string
}

class STTable extends StreamlitComponentBase<State> {

  private handleAction(action: string, record: object) {
    const that = this;
    return function(e:  React.MouseEvent<HTMLElement>) {
      e.stopPropagation();
      that.setState({ 
          action: action, 
          action_records: [record],
          action_id: uuidv4(),
        },
        () => Streamlit.setComponentValue(that.state)
      )
    }
  }

  private handleReAction(pagination: any, filters: any, sorter: any, extra: IExtra) {
    Streamlit.setFrameHeight(100);
    setTimeout(Streamlit.setFrameHeight, 1);
    console.log(sorter);
    /* this.setState({ 
        pagination,
        filters,
        sorter,
        action: extra.action,
        action_id: uuidv4(),
      },
      () => Streamlit.setComponentValue(this.state)
    ) */
  }

  componentDidMount() {
    setTimeout(Streamlit.setFrameHeight, 1);
  }

  componentDidUpdate() {
    setTimeout(Streamlit.setFrameHeight, 1);
  }

  public render = (): ReactNode => {
    const data = this.props.args.data;
    let columns : ColumnType<object>[] = this.props.args.columns;
    const {actions, row_key, tags_columns, sorter_columns} = this.props.args;
    const that = this;
    if (actions) {
      columns = columns.concat(
        {
          title: 'Action',
          key: 'operation',
          fixed: 'right', 
          width: this.props.args.action_width,
          render: (text, record: any) => (
            <Space size="middle">
              {actions.map(function(action: string, i: Number){
                const key = record[row_key];
                return <a href="#" key={key + action} onClick={that.handleAction(action, record).bind(that)}>{action}</a>
              })}
            </Space>
          )
        }
      );
    }


    if (sorter_columns) {
      columns.map((column: ColumnType<object>) => {
        if((sorter_columns as string[]).includes((column.key as string))){
          column.defaultSortOrder = 'descend'
          if (! column.sorter){
            column.sorter = (a: any, b: any) => {
              const aa = a[(column.key as string)];
              const bb = b[(column.key as string)];
              if (typeof(aa) === 'number') {
                return aa - bb
              }
              if (/^\d+$/.test(aa) && /^\d+$/.test(bb)) {
                return Number.parseFloat(aa) - Number.parseFloat(bb)
              }
              return aa.localeCompare(bb)
            }
          }
        }
      })
    }
    if (tags_columns) {
      columns.map((column: ColumnType<object>) => {
        if((tags_columns as string[]).includes((column.key as string))){
          column.render = (tags: string, record: any, index: Number ) => {
            return <>
              {tags.split(',').map(tag => (
                <Tag color="blue" key={'tags/' + tag + '/' + index}>
                  {tag}
                </Tag>
              ))}
            </>
          }
        }
      })
    }
    return (
       <Table
          onChange={this.handleReAction.bind(this)}
          rowKey={row_key}
          columns={columns}
          dataSource={data}
          scroll={{ x: 1500 }}
          sticky
        />
    )
  }
}

export default withStreamlitConnection(STTable);

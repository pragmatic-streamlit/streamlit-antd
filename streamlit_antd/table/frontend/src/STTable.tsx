import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Table, Input, Button, Tag, Space, InputRef, Tooltip} from 'antd';
import { ColumnProps, ColumnsType, ColumnType } from "antd/lib/table";
import { v4 as uuidv4 } from 'uuid';
import Highlighter from 'react-highlight-words';
import { SearchOutlined } from '@ant-design/icons';


interface IExtra {
  action: string
}

interface State {
  pagination?: any
  filters?: any 
  sorter?: any 
  action?: string 
  action_records?: any[]
  action_id?: string
  searchText?: string
  searchedColumn?: string
}

export interface FilterConfirmProps {
  closeDropdown: boolean;
}
export interface ColumnFilterItem {
 text: React.ReactNode;
 value: string | number | boolean;
 children?: ColumnFilterItem[];
}
export interface FilterDropdownProps {
 prefixCls: string;
 setSelectedKeys: (selectedKeys: React.Key[]) => void;
 selectedKeys: React.Key[];
 confirm: (param?: FilterConfirmProps) => void;
 clearFilters: () => void;
 filters?: ColumnFilterItem[];
 visible: boolean;
}

class STTable extends StreamlitComponentBase<State>{

  constructor(props: any){
    super(props)
    this.state = {
      searchedColumn: ""
    }
  }

  searchInput?: InputRef;

  getColumnSearchProps = (dataIndex: string) => ({
    filterDropdown: ({ setSelectedKeys, selectedKeys, confirm, clearFilters }: FilterDropdownProps) => (
      <div style={{ padding: 8 }}>
        <Input
          ref={(node: InputRef) => {
            this.searchInput = node
          }}
          placeholder={`Search ${dataIndex}`}
          value={selectedKeys[0]}
          onChange={e => setSelectedKeys(e.target.value ? [e.target.value] : [])}
          onPressEnter={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
          style={{ marginBottom: 8, display: 'block' }}
        />
        <Space>
          <Button
            type="primary"
            onClick={() => this.handleSearch(selectedKeys, confirm, dataIndex)}
            icon={<SearchOutlined />}
            size="small"
            style={{ width: 90 }}
          >
            Search
          </Button>
          <Button onClick={() => this.handleReset(clearFilters)} size="small" style={{ width: 90 }}>
            Reset
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => {
              confirm({ closeDropdown: false });
              this.setState({
                searchText: (selectedKeys[0] as string),
                searchedColumn: dataIndex,
              });
            }}
          >
            Filter
          </Button>
        </Space>
      </div>
    ),
    filterIcon: (filtered: boolean)=> <SearchOutlined style={{ color: filtered ? '#1890ff' : undefined }} />,
    onFilter: (value: string, record: any) =>
      record[dataIndex]
        ? record[dataIndex].toString().toLowerCase().includes(value.toLowerCase())
        : '',
    onFilterDropdownVisibleChange: (visible: boolean)=> {
      if (visible) {
        setTimeout(() => this.searchInput && this.searchInput.select(), 100);
      }
    },
    render: (text: string) =>
      this.state.searchedColumn === dataIndex ? (
        <Highlighter
          highlightStyle={{ backgroundColor: '#ffc069', padding: 0 }}
          searchWords={[this.state.searchText]}
          autoEscape
          textToHighlight={text ? text.toString() : ''}
        />
      ) : (<Tooltip placement="topLeft" title={text}> 
        {text}</Tooltip>
      ),
  });

  handleSearch = (selectedKeys: React.Key[], confirm: () => void, dataIndex: string) => {
    confirm();
    this.setState({
      searchText: (selectedKeys[0] as string),
      searchedColumn: dataIndex,
    });
  };

  handleReset = (clearFilters: () => void) => {
    clearFilters();
    this.setState({ searchText: '' });
  };

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
    const {actions, row_key, tags_columns, sorter_columns, searchable_columns} = this.props.args;
    const that = this;
    columns.map((column: ColumnType<object>) => {
      column.ellipsis = {
        showTitle: false,
      };
    })
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
    if (searchable_columns) {
      columns.map((column: ColumnType<object>) => {
        if((searchable_columns as string[]).includes((column.key as string))){
         Object.assign(column, this.getColumnSearchProps((column.dataIndex as string)));
        }
      })
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

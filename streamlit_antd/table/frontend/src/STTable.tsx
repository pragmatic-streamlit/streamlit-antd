import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import {
  Table,
  Input,
  Button,
  Tag,
  Space,
  InputRef,
  Tooltip,
  Popconfirm,
  ConfigProvider,
  theme,
} from "antd"
import { TableToken } from "antd/lib/table/style"
import { ColumnType } from "antd/lib/table"
import { v4 as uuidv4 } from "uuid"
import Highlighter from "react-highlight-words"
import { SearchOutlined } from "@ant-design/icons"
import JSONPretty from "react-json-pretty"

interface IExtra {
  action: string
}

interface EventPayload {
  action: string
  records?: any[]
  column?: string
}

interface Event {
  id: string
  payload: EventPayload
}

interface State {
  //pagination?: any
  filters?: any
  sorter?: any
  searchText?: string
  searchedColumn?: string
  selectedRowKeys?: React.Key[]
}

interface FilterConfirmProps {
  closeDropdown: boolean
}

interface ColumnFilterItem {
  text: React.ReactNode
  value: string | number | boolean
  children?: ColumnFilterItem[]
}

interface FilterDropdownProps {
  prefixCls: string
  setSelectedKeys: (selectedKeys: React.Key[]) => void
  selectedKeys: React.Key[]
  confirm: (param?: FilterConfirmProps) => void
  clearFilters: () => void
  filters?: ColumnFilterItem[]
  visible: boolean
}

function isDate(dateStr: string) {
  return !isNaN(new Date(dateStr).getDate())
}

function isFloat(floatStr: string) {
  return !isNaN(parseFloat(floatStr))
}

class STTable extends StreamlitComponentBase<State> {
  constructor(props: any) {
    super(props)
    this.state = {
      searchedColumn: "",
    }
  }

  searchInput?: InputRef

  getColumnSearchProps = (dataIndex: string, linkable: boolean) => ({
    filterDropdown: ({
      setSelectedKeys,
      selectedKeys,
      confirm,
      clearFilters,
    }: FilterDropdownProps) => (
      <div style={{ padding: 8 }}>
        <Input
          ref={(node: InputRef) => {
            this.searchInput = node
          }}
          placeholder={`Search ${dataIndex}`}
          value={selectedKeys[0]}
          onChange={(e) =>
            setSelectedKeys(e.target.value ? [e.target.value] : [])
          }
          onPressEnter={() =>
            this.handleSearch(selectedKeys, confirm, dataIndex)
          }
          style={{ marginBottom: 8, display: "block" }}
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
          <Button
            onClick={() => this.handleReset(clearFilters)}
            size="small"
            style={{ width: 90 }}
          >
            Reset
          </Button>
          <Button
            type="link"
            size="small"
            onClick={() => {
              confirm({ closeDropdown: false })
              this.setState({
                searchText: selectedKeys[0] as string,
                searchedColumn: dataIndex,
              })
            }}
          >
            Filter
          </Button>
        </Space>
      </div>
    ),
    filterIcon: (filtered: boolean) => (
      <SearchOutlined style={{ color: filtered ? "#1890ff" : undefined }} />
    ),
    onFilter: (value: string, record: any) =>
      record[dataIndex]
        ? record[dataIndex]
            .toString()
            .toLowerCase()
            .includes(value.toLowerCase())
        : "",
    onFilterDropdownOpenChange: (visible: boolean) => {
      if (visible) {
        setTimeout(() => this.searchInput && this.searchInput.select(), 100)
      }
    },
    render: (text: string, record: any) => {
      let x =
        this.state.searchedColumn && this.state.searchedColumn === dataIndex ? (
          <Highlighter
            highlightStyle={{ backgroundColor: "#ffc069", padding: 0 }}
            searchWords={[this.state.searchText]}
            autoEscape
            textToHighlight={text ? text.toString() : ""}
          />
        ) : (
          <Tooltip placement="topLeft" title={text}>
            {text}
          </Tooltip>
        )
      if (linkable) {
        // eslint-disable-next-line
        x = (
          <a
            href="#"
            onClick={this.handleAction("ClickLink", [record], dataIndex).bind(
              this
            )}
          >
            {x}
          </a>
        )
      }
      return x
    },
  })

  handleSearch = (
    selectedKeys: React.Key[],
    confirm: () => void,
    dataIndex: string
  ) => {
    confirm()
    this.setState({
      searchText: selectedKeys[0] as string,
      searchedColumn: dataIndex,
    })
  }

  handleReset = (clearFilters: () => void) => {
    clearFilters()
    this.setState({ searchText: "" })
  }

  private handleAction(action: string, records: object[], column?: string) {
    const that = this
    return function (e: React.MouseEvent<HTMLElement>) {
      e.stopPropagation()
      const event: Event = {
        id: uuidv4(),
        payload: {
          action,
          records,
          column,
        },
      }
      Streamlit.setComponentValue(event)
      that.setState({ selectedRowKeys: [] })
    }
  }

  ajustHeight() {
    setTimeout(() => {
      Streamlit.setFrameHeight()
    }, 300)
  }

  componentDidMount() {
    this.ajustHeight()
  }

  componentDidUpdate() {
    this.ajustHeight()
  }

  onPagerChange = (page: Number, pageSize: Number) => {
    const event: Event = {
      id: uuidv4(),
      payload: {
        action: "pager",
        records: [{"page": page, "page_size": pageSize}],
        column: undefined,
      },
    }
    Streamlit.setComponentValue(event)
  }

  onSelectChange = (selectedRowKeys: React.Key[]) => {
    this.setState({ selectedRowKeys })
  }

  public render = (): ReactNode => {
    const data = this.props.args.data
    let columns: ColumnType<object>[] = this.props.args.columns
    const {
      row_key,
      actions_in_row,
      tags_columns,
      batch_actions,
      linkable_columns,
      sorter_columns,
      searchable_columns,
      expand_column,
      default_expand_all_rows,
      iframes_in_row,
      iframe_height,
      rows_per_page,
      show_pager,
      expand_json,
      dynamic_pager_page,
      enable_dynamic_pager,
      dynamic_pager_total,
      unsafe_html_columns,
    } = this.props.args
    let actions = this.props.args.actions
    const that = this

    // console.log(8989898, columns)

    const { selectedRowKeys } = this.state
    const rowSelection = {
      selectedRowKeys,
      onChange: this.onSelectChange,
      selections: [
        Table.SELECTION_ALL,
        Table.SELECTION_INVERT,
        Table.SELECTION_NONE,
      ],
    }

    // eslint-disable-next-line
    columns.map((column: ColumnType<object>) => {
      column.ellipsis = {
        showTitle: false,
      }
      if (linkable_columns.includes(column.key as string)) {
        column.render = (text: string, record: any) => {
          // eslint-disable-next-line
          return (
            <a
              href="#"
              onClick={that
                .handleAction("ClickLink", [record], column.key?.toString())
                .bind(that)}
            >
              {text}
            </a>
          )
        }
      }
    })
    if (actions || actions_in_row) {
      columns = columns.concat({
        title: "Action",
        key: "operation",
        width: this.props.args.action_width,
        render: (text, record: any) => {
          if (record["_antd_table_actions"]) {
            actions = record["_antd_table_actions"]
          }
          return (
            <Space size="middle">
              {actions.map(function (action: string, i: Number) {
                // eslint-disable-next-line
                return (
                  <a
                    href="#"
                    key={action}
                    onClick={that.handleAction(action, [record]).bind(that)}
                  >
                    {action}
                  </a>
                )
              })}
            </Space>
          )
        },
      })
    }
    if (searchable_columns) {
      // eslint-disable-next-line
      columns.map((column: ColumnType<object>) => {
        if ((searchable_columns as string[]).includes(column.key as string)) {
          Object.assign(
            column,
            this.getColumnSearchProps(
              column.dataIndex as string,
              linkable_columns.includes(column.key as string)
            )
          )
        }
      })
    }
    if (sorter_columns) {
      // eslint-disable-next-line
      columns.map((column: ColumnType<object>) => {
        if ((sorter_columns as string[]).includes(column.key as string)) {
          column.defaultSortOrder = "descend"
          if (!column.sorter) {
            column.sorter = (a: any, b: any) => {
              const aa = a[column.key as string]
              const bb = b[column.key as string]
              if (typeof aa === "number") {
                return aa - bb
              } else if (isDate(aa) && isDate(bb)) {
                return new Date(aa).getTime() - new Date(bb).getTime()
              } else if (isFloat(aa) && isFloat(bb)) {
                return Number.parseFloat(aa) - Number.parseFloat(bb)
              }
              return aa.localeCompare(bb)
            }
          }
        }
      })
    }
    if (tags_columns) {
      // eslint-disable-next-line
      columns.map((column: ColumnType<object>) => {
        if ((tags_columns as string[]).includes(column.key as string)) {
          column.render = (tags: string, record: any, index: Number) => {
            return (
              <>
                {tags.split(",").map((tag) => (
                  <Tag color="blue" key={"tags/" + tag + "/" + index}>
                    {tag}
                  </Tag>
                ))}
              </>
            )
          }
        }
      })
    }

    columns = unsafe_html_columns ? columns.map(
      column => unsafe_html_columns.includes(column.key) ? { ...column, render: text => (<div dangerouslySetInnerHTML={{ __html: text }} />) } : column
    ) : columns

    const compact_layout = this.props.args.compact_layout
    const color_backgroud = this.props.args.color_backgroud
    let pager : any = false
    if (show_pager) {
      pager = { pageSize: rows_per_page, showQuickJumper: true }
      if (enable_dynamic_pager){
        pager.total = dynamic_pager_total
        pager.current = dynamic_pager_page
        pager.onChange = this.onPagerChange.bind(this)
      }
    }
    return (
      <ConfigProvider
        theme={{
          token: {},
          components: {
            Table: {
              colorBgContainer: color_backgroud,
            } as TableToken,
          },
          algorithm: compact_layout
            ? theme.compactAlgorithm
            : theme.defaultAlgorithm,
        }}
      >
        <Table
          pagination={pager}
          rowSelection={batch_actions ? rowSelection : undefined}
          rowKey={row_key}
          size={"large"}
          columns={columns}
          dataSource={data}
          scroll={{ x: true }}
          sticky
          expandable={
            expand_column || iframes_in_row
              ? {
                  defaultExpandAllRows: default_expand_all_rows,
                  onExpand: (expanded: boolean, record: any) => {
                    this.ajustHeight()
                  },
                  expandedRowRender: function (
                    record: any,
                    index,
                    indent,
                    expanded
                  ) {
                    const root = document.getElementById("root")
                    let width = 0
                    if (root) {
                      width = root.clientWidth
                    }
                    return (
                      <>
                        {expand_column &&
                          (expand_json ? (
                            <JSONPretty
                              id="json-pretty"
                              data={record[expand_column as string]}
                            ></JSONPretty>
                          ) : (
                            <p style={{ margin: 0 }}>
                              {record[expand_column as string]}
                            </p>
                          ))}
                        {record["_antd_table_iframes"] &&
                          record["_antd_table_iframes"].map(
                            (link: string, index: number) => {
                              // eslint-disable-next-line
                              return (
                                <iframe
                                  style={{ marginRight: "3px" }}
                                  frameBorder="0"
                                  key={index.toString()}
                                  src={link}
                                  width={
                                    width /
                                      record["_antd_table_iframes"].length -
                                    12
                                  }
                                  height={iframe_height}
                                >
                                  Browser not compatible.
                                </iframe>
                              )
                            }
                          )}
                      </>
                    )
                  },
                }
              : undefined
          }
          summary={(pageData) => {
            return batch_actions ? (
              <Table.Summary fixed="bottom">
                <Table.Summary.Row>
                  <Table.Summary.Cell index={0} colSpan={columns.length}>
                    <Space size="middle">
                      {batch_actions.map(function (action: string, i: Number) {
                        const selectedKeys: string[] = (
                          that.state.selectedRowKeys || []
                        ).map((key: React.Key) => key.toString())
                        const records: object[] = (data as object[]).filter(
                          (item: any) =>
                            selectedKeys.includes(item[row_key].toString())
                        )
                        return (
                          <Popconfirm
                            title="Are you sure to delete this task?"
                            //onConfirm={confirm}
                            okText="Yes"
                            cancelText="No"
                            key={`${i}`}
                          >
                            <Button
                              key={`${i}`}
                              onClick={that
                                .handleAction(action, records)
                                .bind(that)}
                            >
                              {action}
                            </Button>
                          </Popconfirm>
                        )
                      })}
                    </Space>
                  </Table.Summary.Cell>
                </Table.Summary.Row>
              </Table.Summary>
            ) : (
              <></>
            )
          }}
        />
      </ConfigProvider>
    )
  }
}

export default withStreamlitConnection(STTable)

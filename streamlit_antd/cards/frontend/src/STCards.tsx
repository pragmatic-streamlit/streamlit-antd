import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import {
  EditOutlined,
  DoubleRightOutlined,
  SettingOutlined,
  DeleteOutlined,
} from "@ant-design/icons"
import { Avatar, Card } from "antd"
const { Meta } = Card

const truncate = (input: string, maxlen: number) =>
  input.length > maxlen ? `${input.substring(0, maxlen)}...` : input

interface Item {
  id: string
  title: string
  description: string
  cover: string
  cover_alt: string
  avatar: string
}

class STCards extends StreamlitComponentBase {

  private onClick(item: Item, event: string) {
    Streamlit.setComponentValue({
      action: event,
      payload: item,
    })
  }

  public render = (): ReactNode => {
    const items: Item[] = this.props.args.items
    const rows: ReactNode[] = []
    let that = this
    items.forEach((item: Item, index: number) => {
      const actions: ReactNode[] = []
      if (this.props.args.show_delete_action) {
        actions.push(<DeleteOutlined key="delete" onClick={()=>that.onClick(item, "delete")}/>)
      }
      if (this.props.args.show_setting_action) {
        actions.push(<SettingOutlined key="setting" onClick={()=>that.onClick(item, "setting")}/>)
      }
      if (this.props.args.show_edit_action) {
        actions.push(<EditOutlined key="edit" onClick={()=>that.onClick(item, "edit")}/>)
      }
      if (this.props.args.show_open_action) {
        actions.push(<DoubleRightOutlined key="open" onClick={()=>that.onClick(item, "open")}/>)
      }
      rows.push(
        <Card
          key={`card-${item.id}`}
          hoverable
          style={{ width: 240, margin: "15px" }}
          cover={
            item.cover ? (
              <div style={{border: "1px solid #f0f0f0", borderBottom: "none"}}>
              <img alt={item.cover} src={item.cover} width={238} height={160} onClick={()=>that.onClick(item, "click")}/>
              </div>
            ) : null
          }
          actions={actions}
        >
          <Meta
            avatar={item.avatar ? <Avatar src={item.avatar} /> : null}
            title={item.title}
            description={truncate(
              item.description,
              this.props.args.desc_max_len
            )}
          />
        </Card>
      )
    })
    return <div style={{ display: "flex", flexWrap: "wrap" }}>{rows}</div>
  }
}

export default withStreamlitConnection(STCards)

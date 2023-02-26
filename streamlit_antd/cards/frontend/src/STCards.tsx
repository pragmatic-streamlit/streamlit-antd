import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Avatar, Card } from "antd"
import DynamicIcon from "./DynamicIcon"

const { Meta } = Card

const truncate = (input: string, maxlen: number) =>
  input.length > maxlen ? `${input.substring(0, maxlen)}...` : input

interface Item {
  id: string
  title: string
  description: string
  email: string
  cover: string
  cover_alt: string
  avatar: string
  actions: any
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
      const actions: ReactNode[] = item.actions.map(
        (action: any) => {
          const TPL = DynamicIcon()
          return <TPL
            type={action.icon}
            key={action.action}
            onClick={() => that.onClick(item, action.action)}
          />
      })
      rows.push(
        <Card
          key={`card-${item.id}`}
          hoverable
          style={{ width: 240, margin: "15px" }}
          cover={
            item.cover ? (
              <div
                style={{ border: "1px solid #f0f0f0", borderBottom: "none" }}
              >
                <img
                  alt={item.cover}
                  src={item.cover}
                  width={238}
                  height={160}
                  onClick={() => that.onClick(item, "click")}
                />
              </div>
            ) : null
          }
          actions={actions}
        >
          <Meta
            avatar={
              item.avatar ? <Avatar src={item.avatar} alt={item.email} /> : null
            }
            title={item.title}
            description={truncate(
              item.description,
              this.props.args.desc_max_len
            )}
          />
        </Card>
      )
    })
    return <div style={{ display: "flex", flexWrap: "wrap", paddingBottom: "35px" }}>{rows}</div>
  }
}

export default withStreamlitConnection(STCards)

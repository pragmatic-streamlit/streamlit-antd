import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Avatar, Card } from "antd"
import { Input, Space } from 'antd'
import DynamicIcon from "./DynamicIcon"
import ReactPlayer from 'react-player'

const { Meta } = Card
const { Search } = Input

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

const isImage = ['gif','jpg','jpeg','png', 'webp']
const isVideo =['mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'mp4', 'avi'] 

class STCards extends StreamlitComponentBase {
  private onClick(event: React.MouseEvent, item: Item, action: string) {
    event.stopPropagation();
    Streamlit.setComponentValue({
      action: action,
      payload: item,
    })
  }

  componentDidMount(): void {
    setTimeout(() => {
      Streamlit.setFrameHeight()
    }, 300)
  }
  
  componentDidUpdate(): void {
    setTimeout(() => {
      Streamlit.setFrameHeight()
    }, 300)
  }

  onSearch = (value: string) => {
    Streamlit.setComponentValue({
      action: "search",
      payload: value,
    })
  }

  public render = (): ReactNode => {
    const items: Item[] = this.props.args.items
    const rows: ReactNode[] = []
    let that = this
    items.forEach((item: Item, index: number) => {
      const actions: ReactNode[] = item.actions.map((action: any) => {
        const TPL = DynamicIcon()
        return (
          <TPL
            type={action.icon}
            key={action.action}
            onClick={(event: React.MouseEvent) => that.onClick(event, item, action.action)}
          />
        )
      })
      rows.push(
        <Card
          key={`card-${item.id}`}
          hoverable
          style={{ width: this.props.args.width, margin: this.props.args.margin }}
          cover={
            item.cover ? (
              <div
                style={{ border: "1px solid #f0f0f0", borderBottom: "none" }}
              >
                {isImage?.includes(item.cover.split('.').pop() as string) &&
                  <img
                    alt={item.cover}
                    src={item.cover}
                    width={this.props.args.width - 2}
                    height={this.props.args.height}
                  />
                 }{isVideo?.includes(item.cover.split('.')?.pop() as string) &&
                  <ReactPlayer url={item.cover}
                    height={this.props.args.height}
                    width={this.props.args.width - 2}
                    pip={false}
                    volume={this.props.args.video_volume}
                    controls/>
                 }
              </div>
            ) : null
          }
          actions={actions}
          onClick={(event: React.MouseEvent) => that.onClick(event, item, "click")}
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
          {item.email? <p style={{marginBottom: "-20px", marginTop: "1rem", color: "gray", textAlign: "center"}}>© {item.email}</p>:null}
        </Card>
      )
    })
    return <>
        {this.props.args.show_search? <Search placeholder="input search text"
         allowClear onSearch={this.onSearch} style={{ width: "100%",  paddingTop: "1rem", paddingBottom: "1rem"}}
         defaultValue={this.props.args.search_text}
          size="large" />:null}
        <div style={{ display: "flex", flexWrap: "wrap" }}>{rows}</div>
    </>;
  }
}

export default withStreamlitConnection(STCards)

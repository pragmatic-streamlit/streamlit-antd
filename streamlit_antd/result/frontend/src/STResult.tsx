import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Button, Result } from "antd"

interface Action {
  name: string
  title: string
  primary: boolean
}

class STResult extends StreamlitComponentBase {
  private onClick(event: string) {
    Streamlit.setComponentValue({
      action: event,
    })
  }

  public render = (): ReactNode => {
    const { status, title, sub_title, actions } = this.props.args
    const btns: ReactNode[] = []
    actions.forEach((action: Action) => {
      btns.push(
        <Button
          type={action.primary ? "primary" : "default"}
          key={action.name}
          onClick={() => this.onClick(action.name)}
        >
          {action.title}
        </Button>
      )
    })
    return (
      <Result status={status} title={title} subTitle={sub_title} extra={btns} />
    )
  }
}

export default withStreamlitConnection(STResult)

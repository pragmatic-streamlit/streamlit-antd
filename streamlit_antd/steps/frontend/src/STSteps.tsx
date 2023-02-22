import {
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Steps } from "antd"
import {
  SyncOutlined,
} from "@ant-design/icons"

interface State {}

class STSteps extends StreamlitComponentBase<State> {
  public render = (): ReactNode => {
    const current = this.props.args.current
    this.props.args.items.forEach((element: any, index: number) => {
      if (index === current && this.props.args.process){
        element.icon = <SyncOutlined spin/>
      }
      if (index === current && this.props.args.error){
        element.status = "error"
      }
    }) 
    return (
      <Steps
        direction={this.props.args.direction}
        labelPlacement={this.props.args.label_placement}
        current={this.props.args.current}
        responsive
        items={this.props.args.items}
      />
    )
  }
}

export default withStreamlitConnection(STSteps)

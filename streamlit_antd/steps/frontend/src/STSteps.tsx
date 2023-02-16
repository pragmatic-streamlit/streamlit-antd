import {
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Steps } from "antd"

interface State {}

class STSteps extends StreamlitComponentBase<State> {
  public render = (): ReactNode => {
    return (
      <Steps
        direction={this.props.args.direction}
        labelPlacement={this.props.args.label_placement}
        current={this.props.args.current}
        percent={this.props.args.percent}
        responsive
        items={this.props.args.items}
      />
    )
  }
}

export default withStreamlitConnection(STSteps)

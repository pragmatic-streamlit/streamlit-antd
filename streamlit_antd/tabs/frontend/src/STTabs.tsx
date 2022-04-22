import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Tabs } from 'antd';
const { TabPane } = Tabs;

interface Item {
  Label: string
}

interface State {
  clickedItem?: Item
}

class STTabs extends StreamlitComponentBase<State> {

  public render = (): ReactNode => {
    const items = this.props.args.items;
    const that = this;
    return (
      <Tabs  onChange={that.onClick.bind(that)}>
        {items.map(function(object: Item, i: any){
          return <TabPane key={object.Label} tab={object.Label}></TabPane>
        })}
    </Tabs>
    )
  }

  private onClick(key: string) {
    let item = this.props.args.items.find((i: Item) => i.Label === key);
    this.setState(
      prevState => ({ clickedItem: item}),
      () => Streamlit.setComponentValue(item)
    )
  }
}

export default withStreamlitConnection(STTabs);

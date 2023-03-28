import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Pagination } from 'antd'
import { v4 as uuidv4 } from "uuid"


class STPager extends StreamlitComponentBase {

  componentDidMount(): void {
    setTimeout(() => {
      Streamlit.setFrameHeight()
    }, 30)
    var elements = document.getElementsByClassName('ant-pagination-options-size-changer');
    for(var i = 0; i < elements.length; i++) {
        var element: any = elements[i];
        element.onclick = function() {
          setTimeout(() => {
            Streamlit.setFrameHeight()
          }, 100)
        }
    }
  }
  
  componentDidUpdate(): void {
    Streamlit.setFrameHeight()
    setTimeout(() => {
      Streamlit.setFrameHeight()
    }, 30)
  }

  onPagerChange = (page: Number, pageSize: Number) => {
    const event: any = {
      id: uuidv4(),
      payload: {
        action: "pager",
        page: page,
        page_size: pageSize
      },
    }
    Streamlit.setComponentValue(event)
  }

  public render = (): ReactNode => {
    const { total, page, page_size } = this.props.args
    console.log(this.props.args)
    return <Pagination
          className="streamlit-antd-pager"
          total={total}
          pageSize={page_size}
          current={page}
          onChange={this.onPagerChange}
          showSizeChanger={true}
          showQuickJumper
          showTotal={(total) => `Total ${total} items`}
        />    
  }
}

export default withStreamlitConnection(STPager)

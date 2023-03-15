import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from 'react';
import { PlusOutlined } from '@ant-design/icons';
// import type { InputRef } from 'antd';
import { Space, Input, Tag, Tooltip } from 'antd';


class STTag extends StreamlitComponentBase {
  state = {
    tags: ['Unremovable', 'Tag 2', 'Tag 3'],
    inputVisible: false,
    inputValue: "",
    editInputIndex: -1,
    editInputValue: "",
    inputRef: null,
    editInputRef: null,
  }

  ajustHeight() {
    setTimeout(() => {
        Streamlit.setFrameHeight();
    }, 0)
  }

  componentDidMount() {
    this.ajustHeight()
  }

  componentDidUpdate() {
    this.ajustHeight()
  }

  public render = (): ReactNode => {
  
    const handleClose = (removedTag: string) => {
      const newTags = this.state.tags.filter((tag) => tag !== removedTag);
      console.log(newTags);
      this.setState({tags: newTags})
    };
  
    const showInput = () => {
      this.setState({inputVisible: true})
    };
  
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      this.setState({inputValue: e.target.value})
    };
  
    const handleInputConfirm = () => {
      if (this.state.inputValue && this.state.tags.indexOf(this.state.inputValue) === -1) {
        this.setState({tags: [...this.state.tags, this.state.inputValue]})
      }
      this.setState({inputVisible: false, inputValue: ""})
    };
  
    const handleEditInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      this.setState({editInputValue: e.target.value})
    };
  
    const handleEditInputConfirm = () => {
      const newTags = [...this.state.tags];
      newTags[this.state.editInputIndex] = this.state.editInputValue;
      this.setState({tags: newTags, editInputIndex: -1, editInputValue: ""})
    };
  
    const tagInputStyle: React.CSSProperties = {
      width: 78,
      verticalAlign: 'top',
    };
  
    const tagPlusStyle: React.CSSProperties = {
      // background: token.colorBgContainer,
      borderStyle: 'dashed',
    };

    // Streamlit.setComponentValue("return");
  
    return (
      <Space size={[0, 8]} wrap>
        <Space size={[0, 8]} wrap>
          {this.state.tags.map((tag, index) => {
            if (this.state.editInputIndex === index) {
              return (
                <Input
                  ref={this.state.editInputRef}
                  key={tag}
                  size="small"
                  style={tagInputStyle}
                  value={this.state.editInputValue}
                  onChange={handleEditInputChange}
                  onBlur={handleEditInputConfirm}
                  onPressEnter={handleEditInputConfirm}
                />
              );
            }
            const isLongTag = tag.length > 20;
            const tagElem = (
              <Tag
                key={tag}
                closable={index !== 0}
                style={{ userSelect: 'none' }}
                onClose={() => handleClose(tag)}
              >
                <span
                  onDoubleClick={(e) => {
                    if (index !== 0) {
                      this.setState({editInputIndex: index, editInputValue: tag})
                      e.preventDefault();
                    }
                  }}
                >
                  {isLongTag ? `${tag.slice(0, 20)}...` : tag}
                </span>
              </Tag>
            );
            return isLongTag ? (
              <Tooltip title={tag} key={tag}>
                {tagElem}
              </Tooltip>
            ) : (
              tagElem
            );
          })}
        </Space>
        {this.state.inputVisible ? (
          <Input
            ref={this.state.inputRef}
            type="text"
            size="small"
            style={tagInputStyle}
            value={this.state.inputValue}
            onChange={handleInputChange}
            onBlur={handleInputConfirm}
            onPressEnter={handleInputConfirm}
          />
        ) : (
          <Tag style={tagPlusStyle} onClick={showInput}>
            <PlusOutlined /> New Tag
          </Tag>
        )}
      </Space>
    );
  };

}

export default withStreamlitConnection(STTag);
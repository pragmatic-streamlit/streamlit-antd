import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import { Cascader } from 'antd';
import { DefaultOptionType, FieldNames, SingleValueType } from "rc-cascader/lib/Cascader";


interface State {
}

function ajustHeight(open: boolean) {
  const root = document.getElementById('root');
  const droparea = document.getElementsByClassName('ant-select-dropdown')[0];
  if (open) {
    if (root) {
      const height = Math.max(droparea?droparea.clientHeight + root.clientHeight:0, document.body.clientHeight, root.clientHeight, root.scrollHeight, root.offsetHeight);
      Streamlit.setFrameHeight(height);
    }
  } else {
    Streamlit.setFrameHeight(root?root.clientHeight:undefined);
  }
}

function onVisibleChange(open: boolean) {
  setTimeout(() => {
    ajustHeight(open)
  }, 0);
}

function onChange(value: SingleValueType, selectOptions: DefaultOptionType[])  {
  const values = [value];
  console.log(values);
  console.log(selectOptions);
  Streamlit.setComponentValue({values, selectOptions})
}

function onMultiplyChange(values: SingleValueType[], selectOptions: DefaultOptionType[][])  {
  console.log(values);
  console.log(selectOptions);
  Streamlit.setComponentValue({values, selectOptions})
}

function filter(inputValue: string, options: DefaultOptionType[], fieldNames: FieldNames) : boolean {
  return options.some(option => option.label && option.label.toString().toLowerCase().indexOf(inputValue.toLowerCase()) > -1);
}


class STCascader extends StreamlitComponentBase<State> {

  public render = (): ReactNode => {
    const options = this.props.args.options;
    console.log(options);
    const multiple: boolean = this.props.args.multiple;
    const x = multiple?
        <Cascader
        //allowClear={true}
        options={options}
        onChange={ onMultiplyChange }
        style={{width: "100%"}}
        multiple={true}
        onDropdownVisibleChange={onVisibleChange}
        maxTagCount="responsive"

        //showSearch={{ filter }}
      />:<Cascader
        allowClear={true}
        options={options}
        onChange={ onChange }
        style={{width: "100%"}}
        multiple={false}
        onDropdownVisibleChange={onVisibleChange}
        showSearch={{ filter }}
      />
    return x
  }
}

export default withStreamlitConnection(STCascader);

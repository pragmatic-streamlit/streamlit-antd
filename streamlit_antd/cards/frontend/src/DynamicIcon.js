import loadable from "@loadable/component";

function DynamicIcon(){
    return loadable(props => {
        console.log(props.type)
        return import(`@ant-design/icons/es/icons/${props.type}.js`)
        .catch(err => import(`@ant-design/icons/es/icons/WarningOutlined.js`))
    })
}

export default DynamicIcon;
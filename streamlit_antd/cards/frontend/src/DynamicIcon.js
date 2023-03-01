import loadable from "@loadable/component";

function DynamicIcon(){
    return loadable(props => {
        return import(`@ant-design/icons/es/icons/${props.type}.js`).then(
                (res) => {

                    return res
                }
        )
        .catch(err => import(`@ant-design/icons/es/icons/WarningOutlined.js`))
    })
}

export default DynamicIcon;
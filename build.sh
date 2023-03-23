set -ex
export NODE_OPTIONS="--openssl-legacy-provider"
export BROWSER=none
(cd streamlit_antd/tabs/frontend && npm i --legacy-peer-deps && npm run build)
(cd streamlit_antd/table/frontend && npm i --legacy-peer-deps && npm run build)
(cd streamlit_antd/cards/frontend && npm i --legacy-peer-deps && npm run build)
(cd streamlit_antd/cascader/frontend && npm i --legacy-peer-deps && npm run build)
(cd streamlit_antd/breadcrumb/frontend && npm i --legacy-peer-deps && npm run build)
(cd streamlit_antd/steps/frontend && npm i --legacy-peer-deps && npm run build)
(cd streamlit_antd/result/frontend && npm i --legacy-peer-deps && npm run build)
(cd streamlit_antd/tag/frontend && npm i --legacy-peer-deps && npm run build)

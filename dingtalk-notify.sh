#!/bin/bash
# 钉钉消息推送脚本
# 用法: ./dingtalk-notify.sh "消息内容"

# 加载环境变量
if [ -f ~/.openclaw/env ]; then
  source ~/.openclaw/env
fi

# 检查必要参数
if [ -z "$DINGTALK_APPKEY" ] || [ -z "$DINGTALK_APPSECRET" ] || [ -z "$DINGTALK_AGENTID" ]; then
  echo "错误: 未配置钉钉凭证，请设置 DINGTALK_APPKEY/DINGTALK_APPSECRET/DINGTALK_AGENTID"
  exit 1
fi

if [ -z "$1" ]; then
  echo "用法: $0 \"消息内容\""
  exit 1
fi

# 获取 AccessToken
ACCESS_TOKEN=$(curl -s "https://oapi.dingtalk.com/gettoken?appkey=$DINGTALK_APPKEY&appsecret=$DINGTALK_APPSECRET" | jq -r .access_token)

if [ "$ACCESS_TOKEN" == "null" ]; then
  echo "错误: 获取 AccessToken 失败"
  exit 1
fi

# 发送消息 (默认发送给当前用户)
USER_ID="1458302740827526"  # 替换为实际接收人 UserID
MSG_CONTENT="$1"

curl -s 'https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2?access_token='$ACCESS_TOKEN \
-H 'Content-Type: application/json' \
-d '{
  "agent_id": "'$DINGTALK_AGENTID'",
  "userid_list": "'$USER_ID'",
  "msg": {
    "msgtype": "text",
    "text": {"content": "'$MSG_CONTENT'"}
  }
}' | jq -r '.errmsg'
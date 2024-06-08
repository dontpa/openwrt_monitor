#!/bin/sh

HEARTBEAT_URL="http://192.168.5.192:8000/heartbeat/"

# 获取过去15分钟的 load average
LOAD_AVERAGE=$(uptime | awk -F'load average: ' '{ print $2 }' | awk '{ print $3 }' | sed 's/,//')

# 输出 load average
echo "Load average (15 min): $LOAD_AVERAGE"

# 获取内存使用率
MEM_TOTAL=$(free | grep Mem | awk '{print $2}')
echo "Memory Total: $MEM_TOTAL"

MEM_USED=$(free | grep Mem | awk '{print $3}')
echo "Memory Used: $MEM_USED"

MEM_USAGE=$(awk "BEGIN {print ($MEM_USED/$MEM_TOTAL)*100}")
echo "Memory Usage: $MEM_USAGE"

# 获取温度信息（假设温度信息在此路径，可以根据实际情况调整）
TEMPERATURE_RAW=$(cat /sys/class/thermal/thermal_zone0/temp)
TEMPERATURE=$(awk "BEGIN {print $TEMPERATURE_RAW/1000}")
echo "Temperature: $TEMPERATURE"

# VPN_STATUS 状态
HTTP_STATUS=$(curl -s --head https://www.google.com | head -n 1 | awk '{print $2}')
if [ "$HTTP_STATUS" = "200" ]; then
    VPN_STATUS="true"
else
    VPN_STATUS="false"
fi
echo "VPN Status: $VPN_STATUS"


# 构建 JSON 数据
JSON_DATA=$(printf '{"cpu_usage": %.2f, "mem_usage": %.2f, "temperature": %.2f, "vpn_status": %s}' "$LOAD_AVERAGE" "$MEM_USAGE" "$TEMPERATURE" "$VPN_STATUS")
echo "JSON Data: $JSON_DATA"

# 发送心跳信号
curl -X POST -H "Content-Type: application/json" -d "$JSON_DATA" $HEARTBEAT_URL

import os
import logging
from JoycontrolPlugin import JoycontrolPlugin

# Slack関連
import urllib.request, urllib.parse

logger = logging.getLogger(__name__)

class CustomCommon(JoycontrolPlugin):
    def __init__(self, controller_state, options):
        super().__init__(controller_state, options)

    async def button_ctl(self, *buttons, p_sec=0.1, w_sec=0.1):
        # ボタンの押下時間と解放後待機時間を指定する
        await self.button_press(*buttons)
        await self.wait(p_sec)
        await self.button_release(*buttons)
        await self.wait(w_sec)

    async def send_slack_message(self, msg):
        # Slackでメッセージ送信
        URL = 'https://slack.com/api/chat.postMessage'
        headers = {
                'Authorization': 'Bearer ' + os.environ.get('POST_SLACK_TOKEN_ID')
        }
        message = {
                'text' : msg,
                'channel' : os.environ.get('POST_SLACK_CHANNEL_ID')
        }
        data = urllib.parse.urlencode(message).encode("utf-8")
        req = urllib.request.Request(URL,data=data,headers=headers,method='POST')
        urllib.request.urlopen(req)

import requests
import json
from slacker import Slacker
from glocal.secret import safe_get

def opererror_slack(text=None, channel='#glocalportal', username='errorreport',attachments=None):
   token = safe_get('slack_key')
   slack = Slacker(token)
   slack.chat.post_message(text=text,channel=channel,username=username,attachments=attachments)
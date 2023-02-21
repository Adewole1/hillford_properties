from typing import List, Optional

import requests

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from sms.backends.base import BaseSmsBackend
from sms.message import Message


class SMSBackend(BaseSmsBackend):

    def __init__(self, fail_silently: bool = False, **kwargs) -> None:
        super().__init__(fail_silently=fail_silently, **kwargs)
        
        api_token: Optional[str] = getattr(settings, "API_TOKEN")

        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        self.url = 'https://www.bulksmsnigeria.com/api/v2/sms/create'

        self.payload = {
            "api_token": api_token
        }

        if not api_token and not self.fail_silently:
            raise ImproperlyConfigured(
                "Check that there is the right api_token for your backend"
            )
    
    def send_messages(self, messages: List[Message]) -> int:
        
        msg_count: int = 0
        for message in messages:
            for recipient in message.recipients:
                try:
                    params = {
                        'to': recipient,
                        'from': message.originator,
                        'body': message.body,
                        'gateway': '0',
                        'append_sender': '0',
                    }

                    response = requests.request('POST', self.url, headers=self.headers, json=self.payload, params=params)
                    res = response.json()
                    assert res['data']['status']=='success'
                
                except Exception as exc:
                    if not self.fail_silently:
                        raise exc
                
                msg_count += 1
        
        return msg_count
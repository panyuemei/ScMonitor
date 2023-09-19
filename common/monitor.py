import json
import time
import hmac
import hashlib
import urllib.parse
import base64
from typing import TYPE_CHECKING
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import logging
from websocket import create_connection
if TYPE_CHECKING:
    from requests import Response
from utils.common import build_url


class BaseMonitor:
    title: str = ''
    default_ding_title: str = None
    base_url: str = None
    default_api_timeout: int = 20
    default_ding_tail_text: str = None
    scheduler_kwargs: dict = {}
    global start_time
    start_time = 0
    global end_time
    end_time = 0
    url= ''

    ws = None
    current_time = time.time()

    def __init__(self, config):
        self.config = config

    def ding(self, content, title=None, custom_content=None):
        config = self.config['ding']
        timestamp = str(round(time.time() * 1000))
        secret = config['secret']
        secret_enc = secret.encode('utf-8')
        sign = urllib.parse.quote_plus(base64.b64encode(
            hmac.new(secret_enc, '{}\n{}'.format(timestamp, secret).encode('utf-8'),
                     digestmod=hashlib.sha256).digest()))
        url = 'https://oapi.dingtalk.com/robot/send?' \
              f'access_token={config["access_token"]}&' \
              f'timestamp={timestamp}&' \
              f'sign={sign}'
        headers = {'Content-Type': 'application/json'}
        data = {
            'at': {
                'atMobiles': [],
                'atUserIds': [],
                'isAtAll': False
            },
            'markdown': {
                'title': title or self.default_ding_title,
                'text': content
            },
            'msgtype': 'markdown'
        }
        custom_content and data.update(custom_content)
        try:
            response = requests.post(url, data=json.dumps(data), headers=headers)
            logging.info(f'钉钉通知：{response.text}')
        except Exception as e:
            logging.error(f'钉钉通知异常：{e}')

    @staticmethod
    def default_api_monitor_assert(response: 'Response', timeout=10, assert_data_code=True):
        assert response.status_code == 200, f'接口状态码异常，期望：200，实际：{response.status_code}'
        assert response.elapsed.total_seconds() <= timeout, f'接口耗时异常，期望：<= {timeout}s，实际：{response.elapsed.total_seconds()}s'
        if assert_data_code:
            assert response.json().get('code') == 0, f'接口返回code异常，期望：0，实际：{response.json().get("code")}'

    def api_monitor(self, method, url, data=None, name=None, headers=None, assert_func=None, use_default_assert=True,
                    request_stop_after_attempt=1, request_retry_wait=1, **kwargs):

        url = url if self.base_url is None else build_url(self.base_url, url)
        base_headers = {
            'Content-Type': 'application/json'
        }
        if isinstance(headers, dict):
            base_headers.update(headers)

        if isinstance(data, dict) and base_headers.get('Content-Type') == 'application/json':
            data = json.dumps(data)

        if not 'timeout' in kwargs:
            kwargs['timeout'] = self.default_api_timeout

        response = None

        @retry(stop=stop_after_attempt(request_stop_after_attempt), reraise=True, wait=wait_fixed(request_retry_wait))
        def request():
            return requests.request(method, url, data=data, headers=base_headers, **kwargs)

        try:
            response = request()
            logging.debug(
                f'【{self.title}】：name={name}, url={url}，status_code={response.status_code}，response={response.text}')
            if use_default_assert:
                self.default_api_monitor_assert(response)
            assert_func and assert_func(response)
            logging.info(f'【{self.title}】：接口请求结果断言成功。name={name}, url={url}')
            logging.debug(
                f'【{self.title}】：name={name}, url={url}，status_code={response.status_code}，response={response.text}')
            return response
        except Exception as e:
            logging.error(
                f'【{self.title}】：接口请求结果断言失败：{e}。name={name}，url={url}，'
                f'status_code={response.status_code if response else ""}，'
                f'response={response.text if response else ""}')
            ding_text = f'**【警告】 - {self.title}**\n' \
                        f'#### 接口：{name}\n' \
                        f'#### {e}\n' \
                        f'###### [{url}]({url})'
            if self.default_ding_tail_text:
                ding_text += f'\n{self.default_ding_tail_text}'
        self.ding(ding_text)

    @staticmethod
    def default_ws_monitor_assert(response: 'Response', timeout=10):
        response.settimeout(10)
        response_time = end_time-start_time
        res_time = round(response_time,2)  # 取小数点后两位
        with open('answer_content.txt') as r:
            res = r.read()

        assert response.getstatus() == 101, f'接口状态码异常，期望：101，实际：{response.getstatus()}'
        assert response.gettimeout() <= timeout, f'接口耗时异常，期望：<= {timeout}s，实际：{response.gettimeout()}s'
        assert res is not None,f'返回结果异常，实际为：{res}'
        assert response_time <= 20, f'websocket接口回答耗时异常，期望：20s，实际：{res_time}s'

    def ws_monitor(self,  url, data=None, name=None, assert_func=None, use_default_assert=True,
                   request_stop_after_attempt=1, request_retry_wait=1, **kwargs):

        url = url if self.base_url is None else build_url(self.base_url, url)

        if not 'timeout' in kwargs:
            kwargs['timeout'] = self.default_api_timeout

        response = None

        @retry(stop=stop_after_attempt(request_stop_after_attempt), reraise=True, wait=wait_fixed(request_retry_wait))
        def ws_request():
            return create_connection(url)

        try:
            response = ws_request()
            c = 0
            global start_time
            global end_time
            start_time = time.time()
            response.send(json.dumps(data))
            # time.sleep(21)
            while c < 2:
                # 4、获取返回结果
                result = response.recv()
                if result == '':
                    c=1
                else:
                    with open('answer_content.txt', 'w') as f:
                        f.write(result)
                    # print("接收结果：", result)
                    c += 1
            end_time = time.time()
            time.sleep(1)
            response.close()

            logging.debug(
                f'【{self.title}】：name={name}, url={url}，status_code={response.getstatus()}，response={response}')
            if use_default_assert:
                self.default_ws_monitor_assert(response)
            assert_func and assert_func(response)
            logging.info(f'【{self.title}】：接口请求结果断言成功。name={name}, url={url}')
            logging.debug(
                f'【{self.title}】：name={name}, url={url}，status_code={response.getstatus()}，response={response.getstatus()}')
            return response

        except Exception as e:
            logging.error(
                f'【{self.title}】：接口请求结果断言失败：{e}。name={name}，url={url}，'
                f'status_code={response.getstatus() if response else ""}，'
                f'response={response if response else ""}')
            ding_text = f'**【警告】 - {self.title}**\n' \
                        f'#### 接口：{name}\n' \
                        f'#### {e}\n' \
                        f'###### [{url}]({url})'
            if self.default_ding_tail_text:
                ding_text += f'\n{self.default_ding_tail_text}'
        self.ding(ding_text)

    def exec(self):
        [getattr(self, i)() for i in dir(self) if i.startswith('monitor_') and callable(getattr(self, i))]








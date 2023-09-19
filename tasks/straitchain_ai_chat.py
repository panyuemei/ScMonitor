from common.monitor import BaseMonitor

class Monitor(BaseMonitor):
    title = '海峡链AI-问答'
    default_ding_title = '海峡链AI-问答'
    base_url = 'wss://glm.straitchain.com/chatglm/'
    default_ding_tail_text = '[海峡链AI-问答](https://glm.straitchain.com/chat)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_chat_socket_custom(self):
        self.ws_monitor('/chat_socket/test', name='用户端问答模拟',
                        data={"question": "1+1=", "address": "test"},
                        use_default_assert=False,
                        assert_func=lambda x: self.default_ws_monitor_assert(x, 30),
                        timeout=20,
                        request_stop_after_attempt=2)
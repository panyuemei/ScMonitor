from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '玩链科技AI-问答'
    default_ding_title = '玩链科技AI-问答告警'
    base_url = "wss://playchain.straitchain.com/glm-prod-all/"
    default_ding_tail_text = '[玩链科技AI-问答](https://playchain.straitchain.com/?id=sdgv)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_chat_socket_custom(self):
        self.ws_monitor('chat_socket/straits-02/test', name='用户端问答模拟',
                        data={"question": "1+1=", "address": "test"},
                        use_default_assert=False,
                        assert_func=lambda x: self.default_ws_monitor_assert(x, 30),
                        timeout=20,
                        request_stop_after_attempt=2)


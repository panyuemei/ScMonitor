from common.monitor import BaseMonitor

class Monitor(BaseMonitor):
    title = '云知识库02-底层问答'
    default_ding_title = '云知识库02-底层告警'
    base_url = 'wss://u168495-b6f8-da5ae064.westb.seetacloud.com:8443/local_doc_qa/'
    default_ding_tail_text = '[云知识库02-底层问答](http://webdev.straitchain.com:8080/chatglm-custom-11dom/)'

    scheduler_kwargs = {
        'seconds': 20
    }

    def monitor_chat_socket_custom(self):
        self.ws_monitor('stream-chat/straits-02', name='问答模拟',
                        data={"question": "1+1=",
                              "answertype": "亲密和撒娇","history": [], "knowledge_base_id": "straits-02"},
                        use_default_assert=False,
                        assert_func=lambda x: self.default_ws_monitor_assert(x, 30),
                        timeout=20,
                        request_stop_after_attempt=2)

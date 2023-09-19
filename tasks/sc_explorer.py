from datetime import datetime
from functools import reduce
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from requests import Response
from common.monitor import BaseMonitor


class Monitor(BaseMonitor):
    title = '海峡链区块链浏览器'
    default_ding_title = '海峡链区块链浏览器告警'
    base_url = 'https://explorer.straitchain.com/strait'
    default_ding_tail_text = '[海峡链浏览器](https://explorer.straitchain.com/)'

    def monitor_total_info(self):
        self.api_monitor('post', '/home/totalInfo', name='汇总统计')

    @staticmethod
    def _assert_data_list(response: 'Response', min_len=10, key='data'):
        data = reduce(lambda x, y: x.get(y), key.split('.'), response.json())
        assert data is not None and isinstance(data, list) and len(data) >= min_len, f'接口数据[data]异常'
        return data

    def _assert_statistics(self, response: 'Response'):
        data = self._assert_data_list(response)
        assert all([datetime.strptime(data[i]['groupDate'], '%Y.%m.%d') < datetime.strptime(
            data[i + 1]['groupDate'], '%Y.%m.%d') for i in range(len(data) - 1)]), '接口折线图横坐标日期异常'
        return data

    def monitor_statistics(self):
        def assert_func(response: 'Response'):
            data = self._assert_statistics(response)
            key_map = {
                'accountNum': '账户地址数统计',
                'ipfsSliceNum': 'IPFS分片数统计',
                'nftNum': '藏品数统计',
                'transNum': '交易统计'
            }
            for key, name in key_map.items():
                assert all([float(data[i][key]) <= float(data[i + 1][key]) for i in
                            range(len(data) - 1)]), f'接口内【{name}】数据异常'

        self.api_monitor('post', '/home/dailyStatistics',
                         data={
                             'beginDate': '',
                             'currentDate': '',
                             'endDate': ''
                         }, name='统计折线图', assert_func=assert_func)

    def monitor_evidence_statistics(self):
        def assert_func(response: 'Response'):
            data = self._assert_statistics(response)
            assert all([float(data[i]['czNum']) <= float(data[i + 1]['czNum']) for i in
                        range(len(data) - 1)]), f'存证总数折线图数据异常'

        self.api_monitor('post', '/home/dailyCzStatistics',
                         data={
                             'beginDate': '',
                             'currentDate': '',
                             'endDate': ''
                         }, name='存证总数统计折线图', assert_func=assert_func)

    def monitor_consensus_block_last(self):
        self.api_monitor('post', '/home/blockFront10', data={'chainId': ''}, name='开放共识链最近区块',
                         assert_func=self._assert_data_list)

    def monitor_consensus_trans_last(self):
        self.api_monitor('post', '/home/transFront10', data={'chainId': ''}, name='开放共识链最近交易',
                         assert_func=self._assert_data_list)

    def monitor_permissioned_block_last(self):
        self.api_monitor('post', 'https://api.league.search.straitchain.com:9009/subChain/bs/block/list',
                         data={'curPage': 1, 'limit': 10}, name='开放许可链最近区块',
                         assert_func=lambda x: self._assert_data_list(x, key='data.list'))

    def monitor_permissioned_trans_last(self):
        self.api_monitor('post', 'https://api.league.search.straitchain.com:9009/subChain/bs/trans/list',
                         data={'curPage': 1, 'limit': 10}, name='开放许可链最近交易',
                         assert_func=lambda x: self._assert_data_list(x, key='data.list'))

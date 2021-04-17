import logging
import time
import sys
from JoycontrolPlugin import JoycontrolPlugin, JoycontrolPluginError
from pathlib import Path

sys.path.append(str(Path().cwd().parent / 'common'))
from CustomCommon import CustomCommon

logger = logging.getLogger(__name__)
# 回収周期 デフォルトは5
CHECK_CYCLE = 5

class RajangMarathon(CustomCommon):
    def __init__(self, controller_state, options):
        super().__init__(controller_state, options)
        if options is None or len(options) < 2:
            raise JoycontrolPluginError('2つのオプションを指定してください ex "-p 試行回数 回収対象"')
        self.limit_count = int(options[0])
        if self.limit_count > 1000:
            raise JoycontrolPluginError('試行回数は 1000 までの範囲で指定してください。')
        self.get_type = options[1]
        if self.get_type not in ['all', 'nest', 'home', 'no']:
            raise JoycontrolPluginError('回収対象は all nest home no のいずれかを指定してください。all=フクズクの巣と自宅(オトモ隠密隊と交易船), nest=フクズクの巣, home=自宅(オトモ隠密隊と交易船) no=回収しない')

    async def vs_rajang(self):
        # ウツシに向かってダッシュ
        await self.button_press('r')
        await self.left_stick(angle=122)
        await self.wait(2.7)
        await self.left_stick('center')
        # 闘技大会05を受注
        await self.button_ctl('a', w_sec=1.5)
        await self.button_release('r')
        await self.button_ctl('a', w_sec=1.5)
        await self.button_ctl('up', w_sec=0.5)
        await self.button_ctl('a', w_sec=0.5)
        await self.button_ctl('a', w_sec=2.5)
        await self.button_ctl('zr', w_sec=0.5)
        await self.button_ctl('a', w_sec=1.5)
        await self.button_ctl('left', w_sec=0.5)
        await self.button_ctl('up', w_sec=0.5)
        await self.button_ctl('a', w_sec=0.5)
        await self.button_ctl('a')
        await self.wait(12.5)
        # クエスト開始
        await self.button_press('r')
        await self.left_stick(angle=70)
        await self.wait(0.7)
        await self.left_stick(angle=90)
        await self.wait(0.4)
        await self.button_press('zl')
        await self.wait(0.2)
        await self.button_ctl('x', w_sec=1.0)
        await self.button_ctl('b', p_sec=1.0)
        await self.button_ctl('a', p_sec=0.8)
        await self.left_stick('center')
        await self.button_release('zl')
        await self.button_release('r')
        # ZR連打
        for _ in range(90):
            await self.button_ctl('zr')
        # まだクエスト失敗してなければクエスト中止
        await self.button_ctl('plus')
        await self.button_ctl('right')
        await self.button_ctl('up')
        await self.button_ctl('a')
        await self.button_ctl('left')
        await self.button_ctl('a')
        # A連打
        for _ in range(60):
            await self.button_ctl('a')
        await self.wait(12.0)

    async def check_nest(self):
        # 巣のある木に向かって移動
        await self.button_press('r')
        await self.left_stick(angle=110)
        await self.wait(0.4)
        await self.button_press('zl')
        await self.wait(0.2)
        await self.button_ctl('x', w_sec=1.0)
        await self.button_ctl('b', p_sec=0.6)
        await self.button_ctl('x', w_sec=1.0)
        await self.wait(2.0)
        # 木登りからの巣チェック
        await self.left_stick(angle=330)
        await self.button_release('zl')
        await self.wait(4.6)
        await self.left_stick(angle=260)
        for _ in range(20):
            await self.button_ctl('a')
        await self.button_release('r')
        await self.left_stick('center')

    async def finish_party(self):
        # オトモ探索隊を帰還させる
        await self.button_ctl('a', w_sec=2.0)
        await self.button_ctl('down')
        await self.button_ctl('a', w_sec=2.0)
        await self.button_ctl('a', w_sec=2.0)
        await self.button_ctl('up')
        await self.button_ctl('a')
        # これ入れておかないと探索未完了時のサルベージができない
        for i in range(12):
            await self.wait(1.0)
        await self.button_ctl('up')
        await self.button_ctl('a')
        for _ in range(10):
            await self.button_ctl('b')

    async def start_party(self):
        # オトモ探索隊を出発させる
        await self.button_ctl('a', w_sec=2.0)
        await self.button_ctl('down')
        await self.button_ctl('a')
        await self.button_ctl('a')
        await self.button_ctl('a')
        await self.button_ctl('up')
        await self.button_ctl('a')
        await self.button_ctl('up')
        await self.button_ctl('a')
        for _ in range(6):
            await self.button_ctl('a')
        await self.button_ctl('x')
        await self.button_ctl('a', w_sec=0.2)
        await self.button_ctl('a')
        for _ in range(10):
            await self.button_ctl('b')

    async def trade_order(self):
        # 交易船の依頼アイテムを回収する
        await self.button_ctl('a', w_sec=2.0)
        await self.button_ctl('down')
        await self.button_ctl('down')
        await self.button_ctl('a')
        await self.button_ctl('a')
        await self.button_ctl('up')
        await self.button_ctl('a')
        await self.button_ctl('up')
        await self.button_ctl('a')
        for _ in range(10):
            await self.button_ctl('b')

    async def run(self):
        logger.info('プラグイン実行開始')
        try_count = 0
        for _ in range(self.limit_count):
            try_count += 1
            await self.vs_rajang() # クエスト実施
            logger.info('{}/{} クエスト消化'.format(try_count, self.limit_count))
            if self.get_type == 'no':
                continue
            if try_count % CHECK_CYCLE == 0:
                # 里内移動画面表示
                await self.button_ctl('left')
                await self.button_ctl('down')
                if self.get_type != 'home': # 自宅のみでなければ先ずフクズクの巣を確認
                    await self.button_ctl('down')
                    await self.button_ctl('a', w_sec=2.0)
                    await self.check_nest()
                    await self.button_ctl('down')
                if self.get_type != 'nest': # フクズクの巣のみでなければ自宅でオトモ隠密隊と交易船回収
                    await self.button_ctl('down')
                    await self.button_ctl('down')
                    await self.button_ctl('down')
                    await self.button_ctl('a', w_sec=2.0)
                    await self.left_stick(angle=15)
                    await self.wait(1.0)
                    await self.left_stick('center')
                    await self.finish_party()
                    await self.start_party()
                    await self.trade_order()
                    await self.button_ctl('down')
                await self.button_ctl('up')
                await self.button_ctl('a', w_sec=2.0)
        finish_msg = 'プラグイン実行終了'
        # await self.send_slack_message(finish_msg)
        logger.info(finish_msg)

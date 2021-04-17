# RajangMarathon

## 前提条件

- 携帯モードになっていること(hdmi出力しているか別のBluetooth接続があるとボタン操作がズレてしまう可能性高いので)
- オートセーブはオンにしておくこと
- アクションスライダー左1回で「里内移動」であること
- オトモ広場と自宅のオトモ隠密隊と交易船が公開されていること
- 交易船の依頼設定をしていること
- オトモ隠密隊の選択が1画面内で完結できること
- スタート位置が集会所移動直後の状態であること

## セッティング

CHECK_CYCLE = 5

これがデフォルト。5回毎にオトモ広場や自宅の回収をする。

## 実行方法とオプション

実行方法は以下

```sh
$ cd ~/switch-auto-mhr/std/
$ sudo joycontrol-pluginloader -r <Mac address> RajangMarathon.py -p 試行回数 回収対象
```

2つのオプションは必須です。

- 第1引数 試行回数
    - 試行回数を数値で指定 1000以下
- 第2引数 回収対象 all, nest, home, no から1つ指定
    - all = フクズクの巣と自宅(オトモ隠密隊と交易船)
    - nest = フクズクの巣
    - home = 自宅(オトモ隠密隊と交易船)
    - no = 回収しない

サンプルで、クエスト10回でオトモ広場も自宅も寄る場合、以下のように指定します。

```sh
$ sudo joycontrol-pluginloader -r <Mac address> RajangMarathon.py -p 10 all
```

## ディレクトリ説明用ドキュメント

### `/analysis`
実験的に数値計算を行ってみたプログラム

### `/assignmentProblem`
自転車とユーザーの割り当てをシミュレートし，結果として自転車の散らばり具合を出力するためのプロトタイププログラム

### `/bikeSharePerMinute`
タクシーデータをシミュレーションデータとして最初の1分間のみのデータを元にシミュレーションを実行するプログラム

### `/environmentCheck`
数値計算を実行しているマシンのスペックを確認するためのプログラム

### `/formatLookUpCSV`
ロケーションIDから実際の座標をマッピングするためのCSVを生成するプログラム

### `/optimizationBasedDispatchModel`
目的関数と制約条件を一通り実装したモデル．`bikeSharePerMinute.ipynb`をモジュール化したプログラム

### `/randomBasedDispatchModel`
各々のリクエストに対してランダムに自転車を割り当てるプログラム．最適化ベースの割り当てと比較するためのベースラインとして構築．

### `/routingProblem`
最適化問題のサンプルプログラム

### `/withoutStackOptBasedDispatchModel`
リクエストをスタックすることなく、各々のリクエストに対して`optimizationBasedDispatchModel`を適用したプログラム

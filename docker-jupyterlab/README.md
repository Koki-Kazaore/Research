# Dockerを用いたPython実行環境構築
{{TODO}}<br>
- 前提条件
    - 想定する実行マシンのOSはWindowsもしくはUnix/Linuxとする．それ以外のOS上で動作させる場合は適宜変更が必要な可能性がある．
    - Dockerコマンドが利用できる．
    - Docker Desktopがインストールされている．

## Dockerとは
{{TODO}}

## Dockerによる環境構築のメリット
{{TODO}}

## 環境構築手順
1. `Research\docker-jupyterlab`をカレントディレクトリとする．

2. Dockerコンテナをビルドして起動する．
```bash
docker compose up -d --build
```

3. コンテナの正常起動を確認する．`jupyterlab-test`というNameのコンテナが表示されない場合は上手くDockerコンテナが起動していないため，ここまでにエラーがやタイポが無いかを確認する．
```bash
docker container ls
```

4. Python環境へ接続する．
```bash
docker compose exec -it jupyterlab bash
```

5. Python用のライブラリをインストールする．
```bash
python -m pip install numpy
```

6. サンプルプログラムを実行する．出力が確認できたらbash接続を退避する．
```bash
python sample.py
# Hello World

exit
```

7. jupyterlabのトークンを確認してクリップボードにコピーする．トークンは以下のコマンド実行後に表示されるdockerのログ内の`token=`に続く長い文字列を指す．
```bash
# Windowsの場合
docker logs jupyterlab-test | Select-Object -Last 10

# Unix/Linuxの場合
docker logs jupyterlab-test | tail
```

8. `.env.example`を`.env`としてコピーし，step7にてクリップボードにコピーしたトークンを環境変数`JUPYTERLAB_TOKEN`として設定する．

9. Dockerコンテナを再ビルドする．
```bash
docker compose up -d --build
```

## JupyterLabへのアクセス
以下のURLへアクセスするとJupyterlabが表示される．<br>
http://localhost:8888

# UmaCapSt
このアプリはSteam版ウマ娘のスクリーンショットを撮影するアプリです。
This app saves screenshots of Uma Musume (Steam version).
![アプリ画面サンプル](https://github.com/user-attachments/assets/d85e821f-73fc-4973-a275-f3ebf731f594)

## 前提条件
* Pythonが使える環境が必要です

## 使い方
1. build.batをダブルクリックする
2. フォルダ「dist」にUmaCapSt.exeが出力されるので任意の場所に置く（そのままでも良い）
3. Steam版ウマ娘を起動した状態でUmaCapSt.exeをダブルクリックする
4. 撮影用のアイコン（全体、左側、右側）のいずれかをクリックする
5. 保存用フォルダに画像が保存されます。

**機能**
- Set Folder：保存先フォルダを指定できます
- Open Folder：保存先フォルダをエクスプローラで開きます
- TOP ON：このアプリを最前面に表示し続ける機能が有効な状態です。
- TOP OFF：最前面機能がオフです。

## カスタムの仕方
1. config.jsonを弄る
2. build.batをダブルクリックする
3. フォルダ「dist」にUmaCapSt.exeが出力されるのでコピーして今のexeに上書きする

**設定値の説明**
* save_dir: 保存先のフォルダパス
* game_title: 探しに行くゲームの名称
* app_width: アプリの幅
* app_height: アプリの高さ
* app_shift_x": アプリの初期位置のうち、ゲーム画面の左端から何px右にズレるか
* app_shift_y": アプリの初期位置のうち、ゲーム画面の上端から何px下にズレるか
* left_crop_ratio": ゲーム画面の左側半分を切り取った際に、左端を何%削るか
* right_crop_ratio": ゲーム画面の右側半分を切り取った際に、右端を何%削るか
* capture_delay": ゲーム画面のキャプチャボタンを押して何秒後にキャプチャするか

## 開発環境
- OS：Windows11 Pro 24H2
- Pythonバージョン：3.10.6
- Gitバージョン：2.43.0
- GPU：Geforce RTX4080
- エディタ：VisualStudioCode

## ライセンス
AGPL-2.0

## 開発者
[aburahamu](https://twitter.com/aburahamu_aa)

# Pop'nTube 譜面バックアップスクリプト

## 概要

Pop'nTube の譜面をバックアップする python スクリプトです。  
`getStageData`では、フォルダ下に`stage/(製作者の名前)/(譜面ID).js`というファイルが生成されます。  
`makeSaveData`では、フォルダ下に`save/(譜面ID).json`というファイルが生成されます。  
このjsonファイルは、Dancing☆Onigiri HTML5エディター( https://github.com/superkuppabros/danoni-editor )で使用可能です。  

## 使い方

リポジトリを適宜ダウンロードし、`getStageData.exe`, `makeSaveData.exe`を実行すると動きます。  
製作者や譜面IDの入力が求められるので、正確に入力してください。

コマンドラインから直接使用する方法(例)  
Windows

```
$ git clone https://github.com/superkuppabros/scrp_pt.git
$ getStageData.exe
```

Mac

```
$ git clone https://github.com/superkuppabros/scrp_pt.git
$ python getStageData.py
```

## 注意

- サーバの負荷を軽減するため、実行は最小限に留めるようお願いします。
- 取得したデータを再配布する等の行為はお控えください。

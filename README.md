# 環境構築

リポジトリをクローン  
`git clone https://github.com/Tanakaryuki/ChallengeCaravan2023_backend.git`

ビルドする  
`docker-compose build`

# 開発の開始

起動  
`docker-compose up`

API のテスト(バックエンド向け)  
[http://localhost:8000/docs](http://localhost:8000/docs)から行う

API ドキュメントの確認(フロントエンド向け)  
[http://localhost:8000/redoc](http://localhost:8000/redoc)から行う

パッケージインストール  
(docker が立ち上がった状態で)  
`docker-compose exec api poetry add {package_name}`

DB のマイグレーション  
`docker-compose exec api poetry run python -m api.migrate_db`

# 開発の終了

停止
`Ctrl + c`

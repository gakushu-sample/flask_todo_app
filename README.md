# flask_todo_app

Flask で ToDo アプリを作成する。  
Linux 環境では、すべて root ユーザで作業をしている前提でコマンドを記載しています。

## VM の準備

プロジェクトフォルダ直下に Vagrantfile を準備しているので、それを用いて起動します。  
ファイルは移動せず、カレントディレクトリをプロジェクトフォルダに移動してコマンドを実行してください。

```bash
vagrant up
```

SELinux を無効化するため、再起動してください。

```bash
vagrant reload
```

## venv の準備(Windows)

リポジトリには venv を入れていないので、自分でやってください。

```bash
py -3.12 -m venv .venv
.venv\Scripts\Activate
# venv 環境に入ったら以下を実行
pip install -r requirements.txt
```

## VM にも Python ライブラリをインストール(Linux)

VM では venv を使う必要はないので、そのままインストールします。

```bash
pip3.12 install -r /vagrant/requirements.txt
```

## MariaDB の設定(Linux)

Vagrantfile 内で色々先にやってしまっているのですが、少しは手を動かしましょう。  
`vi` コマンドが分からないなら、調べてください。

```bash
vi /etc/my.cnf.d/server.cnf
```

`[mysqld]` というセクションがあるので、以下のように書きます。

```ini
[mysqld]
character-set-server=utf8mb4
collation-server=utf8mb4_bin
```

保存したら再起動。

```bash
systemctl restart mysql
```

## DB とテーブルの作成(Linux)

普通に作ります。

```bash
mysql -e "create database todo_app"
mysql todo_app -e "create table todos (\
    id int not null auto_increment,\
    task varchar(100) not null,\
    completion_flg tinyint unsigned not null default 0,\
    primary key (id)\
)"
```

あとはテスト用の DB も作ります。

```bash
mysql -e "create database todo_app_test"
mysql todo_app_test -e "create table todos (\
    id int not null auto_increment,\
    task varchar(100) not null,\
    completion_flg tinyint unsigned not null default 0,\
    primary key (id)\
)"
```

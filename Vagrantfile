# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "flask-todo-app" do |todo_app|
    todo_app.vm.box = "bento/rockylinux-8"
    todo_app.vm.box_version = "202508.03.0"
    todo_app.vm.hostname = "flask-todo-app.local"
    todo_app.vm.network "private_network", ip: "192.168.33.11"
    todo_app.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
      vb.cpus = 1
    end
    todo_app.vm.provision "shell", inline: <<-SHELL
      # SELinux を無効化（再起動が必要）
      sudo sed -i 's/^SELINUX=enforcing/SELINUX=disabled/' /etc/selinux/config

      # firewalld を停止・無効化
      sudo systemctl stop firewalld
      sudo systemctl disable firewalld

      # パッケージのインストール
      sudo dnf install -y python3.12 python3.12-pip

      # pycファイルの生成を無効にする環境変数を設定
      echo 'export PYTHONDONTWRITEBYTECODE=1' >> /etc/environment
      echo 'export PYTHONDONTWRITEBYTECODE=1' >> ~/.bashrc

      # MariaDB 10.11 のインストール
      # MariaDB公式リポジトリを追加
      sudo curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | sudo bash -s -- --mariadb-server-version="10.11"

      # MariaDB 10.11をインストール
      sudo dnf install -y MariaDB-server MariaDB-client
      sudo systemctl start mariadb
      sudo systemctl enable mariadb
      # 起動に時間がかかるかもなので、少し待機する
      sleep 10

      # MariaDB の初期設定
      sudo mysql -e "DELETE FROM mysql.user WHERE User='';"
      sudo mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
      sudo mysql -e "DROP DATABASE IF EXISTS test;"
      sudo mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
      sudo mysql -e "FLUSH PRIVILEGES;"

      # appユーザーの作成と権限設定
      sudo mysql -e "CREATE USER 'app'@'localhost' IDENTIFIED BY 'app_password';"
      sudo mysql -e "CREATE USER 'app'@'%' IDENTIFIED BY 'app_password';"
      sudo mysql -e "GRANT ALL PRIVILEGES ON todo_app.* TO 'app'@'localhost';"
      sudo mysql -e "GRANT ALL PRIVILEGES ON todo_app.* TO 'app'@'%';"
      sudo mysql -e "FLUSH PRIVILEGES;"

      # テストコード実行用のユーザーを追加
      sudo mysql -e "GRANT ALL PRIVILEGES ON todo_app_test.* TO 'Test'@'localhost' IDENTIFIED BY 'Test';"
      sudo mysql -e "FLUSH PRIVILEGES;"

    SHELL
  end
end

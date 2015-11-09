# update packages
sudo apt-get -y update

# mysql
sudo apt-get install -y mysql-client
echo mysql-server mysql-server/root_password password strangehat | sudo debconf-set-selections
echo mysql-server mysql-server/root_password_again password strangehat | sudo debconf-set-selections
sudo apt-get install -y -q mysql-server

# setup mysql
sudo sed -i 's/bind-address\t\t= 127.0.0.1/bind-address\t\t= 0.0.0.0/g' /etc/mysql/my.cnf
sudo sed -i 's/\[mysqld\]/\[mysqld\]\ncharacter-set-server=utf8\ncollation-server=utf8_general_ci\n/g' /etc/mysql/my.cnf
sudo /etc/init.d/mysql restart
sudo mysql --user root --password=strangehat --execute='CREATE DATABASE hivelocity_shared;'
sudo mysql --user root --password=strangehat --execute='CREATE USER "hivelocity"@"%";'
sudo mysql --user root --password=strangehat --execute='GRANT ALL ON *.* TO "hivelocity"@"%";'

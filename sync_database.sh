ssh-keygen -R 10.42.45.100
ssh hvdb1-private mysqldump -u hivelocity -p --single-transaction --routines --triggers myvelocity > /tmp/temp.sql
scp -o stricthostkeychecking=no /tmp/temp.sql ubuntu@10.42.45.100:/tmp/temp.sql
ssh ubuntu@10.42.45.100 mysql -u hivelocity myvelocity < /tmp/temp.sql
rm /tmp/temp.sql
ssh ubuntu@10.42.45.100 rm /tmp/temp.sql

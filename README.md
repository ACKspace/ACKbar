# ACKbar
Buying drinks and snacks in your hacker-/maker-/foospace is easy with ACKbar.

Don't burden your participants with calculating change; math is for nerds.
Instead, create an account and enjoy the benefits of having an account balance.

Accounts don't have passwords because it didn't make sense for our usecase.

## Run
Run with 'python app.py'

## Requirements
* python 3.6+
    * sqlalchemy
    * pymysql
* figlet
* lolcat

## config
Set database type and credentials in `connection.txt` file (in the parent folder outside this project):
* For sqlite, do: `echo 'sqlite:///ackbar.db' > ../connection.txt`
* For mariadb, do: `echo 'mysql+mysqldb://username:password@host:port/databasename' > ../connection.txt`

Also, fill your database with the desired figlet fonts (list them by running `figlist`)
## external tools
If you want to audit your database, you might want to use a GUI tool:
* for both database types, check out: [Beekeeper](https://www.beekeeperstudio.io/get) (your mileage might vary)
* for sqlite, check out [sqlitestudio](https://github.com/pawelsalawa/sqlitestudio/releases)
* for mariadb, check out [mysql workbench](https://www.mysql.com/products/workbench/)

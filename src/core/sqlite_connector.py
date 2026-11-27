import sqlite3

path = "C:\GitRepos\Email_Generator_LGraph\src\DB\database.sqlite"

conn = sqlite3.connect(path, check_same_thread=False)

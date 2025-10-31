import pyodbc

# --- Параметри підключення ---
server = 'ACEREXTENSA'
database = 'CopyTravelAgencyDB'
driver = '{ODBC Driver 17 for SQL Server}'

# --- Підключення ---
conn = pyodbc.connect(
    f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes'
)

cursor = conn.cursor()

# --- Перевірка ---
cursor.execute("SELECT GETDATE()")
row = cursor.fetchone()
print("Підключено! Сервер час:", row[0])

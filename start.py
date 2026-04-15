import subprocess
import sys
import os

def install_requirements():
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'])

def init_database():
    import importlib.util
    spec = importlib.util.spec_from_file_location("database", "database.py")
    db_mod = importlib.util.load_from_spec(spec)
    spec.loader.exec_module(db_mod)

    conn = db_mod.get_connection()
    cursor = conn.cursor()

    with open('sql/schema.sql', 'r') as f:
        schema = f.read()

    for stmt in schema.split(';'):
        stmt = stmt.strip()
        if stmt:
            try:
                cursor.execute(stmt)
            except Exception as e:
                print(f"Schema warning: {e}")

    conn.commit()

    cursor.execute("SELECT COUNT(*) AS total FROM CHAUFFEUR")
    count = cursor.fetchone()
    if count and count.get('total', 0) == 0:
        print("Inserting test data...")
        with open('sql/data.sql', 'r') as f:
            data_sql = f.read()
        for stmt in data_sql.split(';'):
            stmt = stmt.strip()
            if stmt and not stmt.upper().startswith('USE'):
                try:
                    cursor.execute(stmt)
                except Exception as e:
                    print(f"Data warning: {e}")
        conn.commit()
        print("Test data inserted.")
    else:
        print("Data already present, skipping.")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    print("Installing dependencies...")
    install_requirements()
    print("Initializing database...")
    init_database()
    print("Starting server...")
    port = int(os.environ.get('PORT', 8080))
    subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--host', '127.0.0.1', '--port', str(port)])

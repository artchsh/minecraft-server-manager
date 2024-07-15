import sqlite3

DB = 'msm.db'

def create_tables():
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS servers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            core TEXT,
            version TEXT,
            eula TEXT,
            local_ip TEXT,
        )
    ''')
    connection.commit()
    connection.close()

def create_new_server_record(server_name: str, core: str, version: str):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    create_tables()
    cursor.execute('''
        INSERT INTO servers (name, core, version, eula, local_ip) VALUES (?, ?, ?, ?, ?)
    ''', (server_name, core, version, 'false', ''))
    connection.commit()
    connection.close()
    
def get_server_by_name(server_name: str):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM servers WHERE name = ?
    ''', (server_name,))
    data = cursor.fetchone()
    connection.close()
    return data

def get_all_servers():
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute('''
        SELECT * FROM servers
    ''')
    data = cursor.fetchall()
    connection.close()
    return data

def update_server_eula(server_name: str, eula: str):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE servers SET eula = ? WHERE name = ?
    ''', (eula, server_name))
    connection.commit()
    connection.close()
    
def update_server_local_ip(server_name: str, local_ip: str):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute('''
        UPDATE servers SET local_ip = ? WHERE name = ?
    ''', (local_ip, server_name))
    connection.commit()
    connection.close()
    
def delete_server(server_name: str):
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute('''
        DELETE FROM servers WHERE name = ?
    ''', (server_name,))
    connection.commit()
    connection.close()
    
def delete_all_servers():
    connection = sqlite3.connect(DB)
    cursor = connection.cursor()
    cursor.execute('''
        DELETE FROM servers
    ''')
    connection.commit()
    connection.close()


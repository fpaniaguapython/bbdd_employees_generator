import csv
import sqlite3

DATABASE_NAME = 'database.db'

def get_provincias():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        SELECT *
        FROM provincias
    ''')

    provincias = cursor.fetchall()
    conn.close()
    return provincias

def generate_comunidades_autonomas(comunidades_autonomas: list):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comunidades_autonomas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')

    for comunidad in comunidades_autonomas:
        cursor.execute('INSERT INTO comunidades_autonomas (nombre) VALUES (?)', (comunidad,))

    conn.commit()
    conn.close()

def generate_provincias(provincias: list):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS provincias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            comunidad_autonoma_id INTEGER,
            FOREIGN KEY (comunidad_autonoma_id) REFERENCES comunidades_autonomas (id)
        )
    ''')

    comunidades = dict(cursor.execute(
        'SELECT nombre, id FROM comunidades_autonomas'
    ).fetchall())

    try:
        for nombre, comunidad in provincias:
            cursor.execute(
                'INSERT INTO provincias (nombre, comunidad_autonoma_id) VALUES (?, ?)',
                (nombre, comunidades.get(comunidad))
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def generate_employees(employees: list):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname1 TEXT NOT NULL,
            surname2 TEXT NOT NULL,
            job_category TEXT NOT NULL,
            salary REAL NOT NULL,
            province_id INTEGER,
            FOREIGN KEY (province_id) REFERENCES provincias (id)
        )
    ''')

    try:
        for employee in employees:
            cursor.execute(
                '''INSERT INTO employees (
                    name, surname1, surname2, job_category, salary, province_id
                ) VALUES (?, ?, ?, ?, ?, ?)''',
                (
                    employee.name,
                    employee.surname1,
                    employee.surname2,
                    employee.job_category,
                    employee.salary,
                    employee.province
                )
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
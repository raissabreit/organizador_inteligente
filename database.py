import sqlite3
import pandas as pd

def criar_banco():
    conn = sqlite3.connect('organizador.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_arquivo TEXT,
            tipo TEXT,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def registrar_movimentacao(nome_arquivo, tipo):
    conn = sqlite3.connect('organizador.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO movimentacoes (nome_arquivo, tipo) VALUES (?, ?)', (nome_arquivo, tipo))
    conn.commit()
    conn.close()

def obter_historico():
    conn = sqlite3.connect('organizador.db')
    df = pd.read_sql_query("SELECT * FROM movimentacoes ORDER BY data_hora DESC", conn)
    conn.close()
    return df

from flask import Flask, render_template, request, abort
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Lista de pizzas disponíveis
PIZZAS = [
    {'id': '3-queijos', 'nome': '3 Queijos', 'imagem': '3queijos.jpeg'},
    {'id': 'marguerita', 'nome': 'Marguerita', 'imagem': 'marguerita.jpeg'},
    {'id': 'mussarela', 'nome': 'Mussarela', 'imagem': 'mussarela.jpeg'},
    {'id': 'calabresa', 'nome': 'Calabresa', 'imagem': 'calabresa.jpeg'},
    {'id': 'portuguesa', 'nome': 'Portuguesa', 'imagem': 'portuguesa.jpeg'},
    {'id': 'vegetariana', 'nome': 'Vegetariana', 'imagem': 'vegetariana.jpeg'},
    {'id': 'lombo-requeijao', 'nome': 'Lombo com Requeijão', 'imagem': 'lombo-requeijao.jpeg'},
    {'id': 'frango-requeijao', 'nome': 'Frango com Requeijão', 'imagem': 'frango-requeijao.jpeg'},
    {'id': 'milho-requeijao', 'nome': 'Milho com Requeijão', 'imagem': 'milho-requeijao.jpeg'}
]

# Função para calcular o preço total baseado na regra do projeto
def calcular_preco_total(total_pizzas):
    if total_pizzas == 0:
        return 0
    num_pares = total_pizzas // 2
    restante_impar = total_pizzas % 2
    return (num_pares * 90) + (restante_impar * 50)

# Conexão com o banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('pedidos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Rota principal (formulário)
@app.route('/')
def index():
    return render_template('index.html', pizzas=PIZZAS)

# Rota para processar o pedido
@app.route('/enviar-pedido', methods=['POST'])
def enviar_pedido():
    nome = request.form.get('name')
    whatsapp = request.form.get('whatsapp')
    retirada = request.form.get('retirada')
    dia_retirada = request.form.get('dia_retirada') if retirada == 'arena' else None
    nome_voluntario = request.form.get('nome_voluntario') if retirada == 'voluntario' else None

    # Pizzas selecionadas com quantidade > 0
    pizzas_selecionadas = []
    for pizza in PIZZAS:
        quantidade = int(request.form.get(f'pizza-{pizza["id"]}', 0))
        if quantidade > 0:
            pizzas_selecionadas.append({
                'sabor': pizza['nome'],
                'quantidade': quantidade
            })

    total_pizzas = sum(p['quantidade'] for p in pizzas_selecionadas)
    total_preco = calcular_preco_total(total_pizzas)

    # Salvar no banco de dados
    salvar_no_banco(nome, whatsapp, pizzas_selecionadas, retirada, dia_retirada, nome_voluntario, total_preco)

    return render_template('confirmacao.html', nome=nome, total=total_preco, pizzas=pizzas_selecionadas)

# Função para salvar os dados no banco
def salvar_no_banco(nome, whatsapp, pizzas, retirada, dia_retirada, nome_voluntario, total_preco):
    conn = get_db_connection()
    cursor = conn.cursor()

    total_pizzas = sum(p['quantidade'] for p in pizzas)

    cursor.execute('''
        INSERT INTO pedidos (nome, whatsapp, retirada, dia_retirada, nome_voluntario, total_pizzas, total_preco)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, whatsapp, retirada, dia_retirada, nome_voluntario, total_pizzas, total_preco))

    pedido_id = cursor.lastrowid

    for pizza in pizzas:
        cursor.execute('''
            INSERT INTO pizzas_pedido (pedido_id, sabor, quantidade)
            VALUES (?, ?, ?)
        ''', (pedido_id, pizza['sabor'], pizza['quantidade']))

    conn.commit()
    conn.close()

CODIGO_SECRETO = os.getenv("CODIGO_SECRETO")


@app.route('/visualizar-pedidos')
def visualizar_pedidos():
    codigo = request.args.get("codigo")

    if codigo != CODIGO_SECRETO:
        abort(403)  # código HTTP para "proibido"

    conn = sqlite3.connect("pedidos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pedidos ORDER BY data_pedido DESC")
    pedidos = cursor.fetchall()

    cursor.execute("SELECT * FROM pizzas_pedido")
    pizzas = cursor.fetchall()

    conn.close()

    return render_template("visualizar_pedidos.html", pedidos=pedidos, pizzas=pizzas)
# Iniciar o servidor
if __name__ == "__main__":
    app.run(debug=True)

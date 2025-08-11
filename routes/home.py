from flask import Blueprint, render_template, request, send_file
from database.models.pizzas import Pedidos
import pandas as pd
import io
from database.database import db

home_route = Blueprint('home', __name__)

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

def calcular_preco_total(total_pizzas):
    if total_pizzas == 0:
        return 0
    num_pares = total_pizzas // 2
    restante_impar = total_pizzas % 2
    return (num_pares * 80) + (restante_impar * 45)

@home_route.route('/')
def pedidos():
    """ Renderizar Formulario das Pizzas"""
    return render_template('form.html', pizzas=PIZZAS)

@home_route.route('/', methods=['POST'])
def submit():
    """ Enviar os Pedidos para o Banco de Dados + redirecionar para Página do Comprovante """

    nome = request.form.get('nome')
    whatsapp = request.form.get('whatsapp')
    retirada = request.form.get('retirada')

    if retirada == 'arena':
        detalhe = request.form.get('dia_retirada')
    elif retirada == 'voluntario':
        detalhe = request.form.get('nome_voluntario')
    else:
        detalhe = 'Doação para famílias carentes'

    pizzas_selecionadas = []
    total_pizzas = 0

    for pizza in PIZZAS:
        key = f"pizza-{pizza['id']}"
        quantidade = int(request.form.get(key, 0))
        if quantidade > 0:
            pizzas_selecionadas.append({
                "sabor": pizza['nome'],
                "quantidade": quantidade
            })
            total_pizzas += quantidade

    pizzas_str = ", ".join([f"{p['sabor']} x{p['quantidade']}" for p in pizzas_selecionadas])
    total = calcular_preco_total(total_pizzas)

    # SALVAR NO BANCO COM PEEWEE
    Pedidos.create(
        nome=nome,
        whatsapp=whatsapp,
        retirada=retirada,
        detalhe_retirada=detalhe,
        pizzas=pizzas_str,
        total=total
    )
    return render_template('comprovante.html', nome=nome, total=total)

@home_route.route('/view')
def view():
    pedidos = Pedidos.select().order_by(Pedidos.id.asc())
    return render_template('lista_pedidos.html', pedidos=pedidos)

@home_route.route('/reset', methods=['GET'])
def reset_pedidos():
    Pedidos.delete().execute()
    db.execute_sql("ALTER SEQUENCE pedidos_id_seq RESTART WITH 1;")
    return "Todos os pedidos foram apagados."

@home_route.route('/exportar_excel')
def exportar_excel():
    pedidos = Pedidos.select().dicts()  # Retorna lista de dicionários

    if not pedidos:
        return "Nenhum pedido para exportar."

    df = pd.DataFrame(pedidos)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Pedidos')

    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="pedidos.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
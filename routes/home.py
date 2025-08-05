from flask import Blueprint, render_template, request
from database.models.pizzas import Pedidos

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
    return (num_pares * 90) + (restante_impar * 50)

@home_route.route('/pizzas')
def pedidos():
    """ Renderizar Formulario das Pizzas"""
    return render_template('form.html', pizzas=PIZZAS)

@home_route.route('/pizzas', methods=['POST'])
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
    pedidos = Pedidos.select().order_by(Pedidos.data.desc())
    return render_template('lista_pedidos.html', pedidos=pedidos)
from flask import Flask, render_template, request

app = Flask(__name__)

sabores = {
    "3 Queijos": "3queijos.jpeg",
    "Marguerita": "marguerita.jpeg",
    "Mussarela": "mussarela.jpeg",
    "Vegetariana": "vegetariana.jpeg",
    "Portuguesa": "portuguesa.jpeg",
    "Calabresa": "calabresa.jpeg",
    "Lombo com Requeijão": "lombo-requeijao.jpeg",
    "Frango com Requeijão": "frango-requeijao.jpeg",
    "Milho com Requeijão": "milho-requeijao.jpeg"
}

@app.route('/')
def index():
    return render_template('index.html', sabores=sabores)

@app.route('/enviar-pedido', methods=["POST"])
def submit():
    return render_template('confirm.html')
app.run(debug=True)
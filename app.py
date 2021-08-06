from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os, time

app = Flask(__name__)

app.secret_key = "jisung"

diretorio = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(diretorio,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Carro (db.Model):
    __tablename__ = 'carros'
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(150))
    modelo = db.Column(db.String(150))
    cor = db.Column(db.String(100))
    combustivel = db.Column(db.String(100))
    ano = db.Column(db.Integer)

    def __init__(self, marca, modelo, cor, combustivel, ano):
        self.marca=marca
        self.modelo=modelo
        self.cor=cor
        self.combustivel=combustivel
        self.ano=ano


class Usuario (db.Model):
    __tablename__ = 'usuarios'
    nome = db.Column(db.String(100))
    email = db.Column(db.String(100), primary_key=True)
    senha = db.Column(db.String(100))

    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha


@app.route('/home')
def index():
    s = session.get("logado")
    if session.get("logado") != None:
        datas = Carro.query.all()
        return render_template("index.html", carros=datas)
    else:
        return redirect(url_for('login_inicio'))

@app.route('/inserir', methods=['POST'])
def inserir():
    if request.method == 'POST':
        marca=request.form['marca']
        modelo = request.form['modelo']
        cor = request.form['cor']
        combustivel = request.form['combustivel']
        ano = request.form['ano']

        carro=Carro(marca, modelo, cor, combustivel, ano)
        db.session.add(carro)
        db.session.commit()
        db.session.close()

        flash("Carro cadastrado com sucesso.")

        return redirect(url_for('index'))

@app.route('/edit', methods = ['GET', 'POST'])
def atualiza():
    if request.method == 'POST':
        carro = Carro.query.get(request.form.get('id'))

        carro.marca = request.form['marca']
        carro.modelo = request.form['modelo']
        carro.cor = request.form['cor']
        carro.combustivel = request.form['combustivel']
        carro.ano = request.form['ano']

        db.session.commit()

        flash("O cadastro foi editado.")

        return redirect(url_for('index'))

@app.route('/deletar/<id>/', methods = ['GET', 'POST'])
def deletar(id):
    carro = Carro.query.get(id)
    db.session.delete(carro)
    db.session.commit()

    flash("Cadastro de carro foi deletado.")

    time.sleep(2)

    return redirect(url_for('index'))

@app.route('/')
def login_inicio():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods = ['POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        users = Usuario(nome, email, senha)

        try:
            db.session.add(users)
            db.session.commit()
            db.session.close()

        except:
            flash(email + " já está cadastrado!")

        return redirect(url_for('login_inicio'))

@app.route('/logar', methods = ['POST'])
def logar ():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        pesquisa = Usuario.query.filter_by(email=email).first()
        if pesquisa != None:
            if pesquisa.email == email and pesquisa.senha == senha:
                session.setdefault("logado", True)
                return redirect(url_for('index'))
        flash("Por favor, cadastre-se primeiro.")
        return redirect(url_for('login_inicio'))

@app.route ('/logout')
def logout():
    session.clear()
    flash('Sessão encerrada.')
    return redirect(url_for('login_inicio'))

app.run(debug=True)
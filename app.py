from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

# Criando objeto da classe Flask
app = Flask(__name__)
CORS(app)

# App mobile realiza para obter lista de vegetais cadastrados
@app.route('/vegetal', methods=['GET'])
def obtem_vegetal():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Lista de vegetais
    lista_vegetais = []

    # Selecionando os dados do banco
    query_str = 'SELECT * FROM Vegetal'
    info = cursor.execute(query_str).fetchall()

    try:
        for item in info:
            lista_vegetais.append({"nome": item[0], "tempIdeal": item
            [1], "umidadeIdeal": item[2]})

        return jsonify({'lista_vegetais': lista_vegetais})
    except:
        return make_response(jsonify('Erro ao retornar lista de vegetal!'), 406)


# App mobile realiza para cadastrar novo vegetal
@app.route('/vegetal', methods=['POST'])
def cadastra_vegetal():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Leitura dos parâmetros recebidos
    nome = request.json.get('nome')
    tempIdeal = request.json.get('tempIdeal')
    umidadeIdeal = request.json.get('umidadeIdeal')

    try:
        query_str = 'INSERT INTO Vegetal (nome,tempIdeal,umidadeIdeal) VALUES (\'' \
                    + nome + '\',\'' + tempIdeal + '\',\'' + umidadeIdeal + '\')'
        cursor.execute(query_str)
        banco.commit()
        return make_response(jsonify('Vegetal cadastrado!'), 201)
    except Exception as e:
        return make_response(jsonify('Vegetal não cadastrado!'), 406)


# App mobile realiza para alterar vegetal cadastrado
@app.route('/vegetal', methods=['PUT'])
def altera_vegetal():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Leitura dos parâmetros recebidos
    nome = request.json.get('nome')
    tempIdeal = request.json.get('tempIdeal')
    umidadeIdeal = request.json.get('umidadeIdeal')

    try:
        query_str = 'UPDATE Vegetal SET tempIdeal = ' + tempIdeal + ', umidadeIdeal = ' + umidadeIdeal + \
                    ' WHERE nome = \'' + nome + '\''
        cursor.execute(query_str)
        banco.commit()
        return make_response(jsonify('Vegetal atualizado!'), 201)
    except Exception as e:
        return make_response(jsonify('Vegetal não atualizado!'), 406)


# App mobile realiza para obter o estado dos vasos
@app.route('/vaso', methods=['GET'])
def obtem_vaso():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Lista de vegetais
    lista_vasos = []

    # Selecionando os dados do banco
    query_str = 'SELECT * FROM Vaso'
    info = cursor.execute(query_str).fetchall()

    try:
        for item in info:
            lista_vasos.append({"id": item[0], "status": item[1], "bomba": item[2],
                                "tempo": item[3], "vegetal": item[4]})

        return jsonify({'lista_vasos': lista_vasos})
    except:
        return make_response(jsonify('Erro ao retornar lista de vasos!'), 406)


# App mobile realiza para alterar o estado dos vasos (Informa o vegetal)
@app.route('/vaso', methods=['PUT'])
def altera_vaso():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    idVaso = request.json.get('idVaso')
    nomeVegetal = request.json.get('nomeVegetal')

    try:
        query_str = 'UPDATE Vaso SET nomeVegetal = \'' + nomeVegetal + '\', status = 1' + \
                    ' WHERE id = ' + idVaso
        cursor.execute(query_str)
        banco.commit()
        return make_response(jsonify('Vaso atualizado!'), 201)
    except Exception as e:
        return make_response(jsonify('Vaso não atualizado!'), 406)


# App mobile realiza para desligar os vasos
@app.route('/vaso', methods=['DELETE'])
def desliga_vaso():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    idVaso = request.json.get('idVaso')

    try:
        query_str = 'UPDATE Vaso SET nomeVegetal = null, status = 0 WHERE id = ' + idVaso
        cursor.execute(query_str)
        banco.commit()
        return make_response(jsonify('Vaso desligado!'), 201)
    except Exception as e:
        return make_response(jsonify('Não foi possível desligar o vaso!'), 406)


# App mobile realiza para ligar a bomba dos vasos
@app.route('/bomba', methods=['PUT'])
def ativa_bomba():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    idVaso = request.json.get('idVaso')
    tempo = request.json.get('tempo')

    try:
        query_str = 'UPDATE Vaso SET tempo = \'' + tempo + '\', bomba = 1' + \
                    ' WHERE id = ' + idVaso
        cursor.execute(query_str)
        banco.commit()
        return make_response(jsonify('A bomba será ativada!'), 201)
    except Exception as e:
        return make_response(jsonify('Erro ao ativar bomba!'), 406)


# App mobile realiza para obter dados do banco
@app.route('/informacao', methods=['GET'])
def obtem_info():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Lista de informação
    lista_info = []

    # Selecionando os dados do banco
    query_str = 'SELECT informacao.idVaso, vaso.nomeVegetal, informacao.temperatura, informacao.umidade, informacao.data ' \
                'FROM Informacao JOIN Vaso ON informacao.idVaso = Vaso.id ORDER BY informacao.data desc'

    info = cursor.execute(query_str).fetchall()
    for item in info:
        lista_info.append({"idVaso": item[0], "nomeVegetal": item[1], "temperatura": item
        [2], "umidade": item[3], "data": item[4]})

    return jsonify({'lista_info': lista_info})


# Nodemcu realiza para verificar se deve ligar a bomba
@app.route('/bomba', methods=['GET'])
def liga_bomba():
    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Lista de vasos que devem ligar a bomba
    lista_vasos_bomba = []

    # Selecionando os dados do banco
    query_str = 'SELECT tempo FROM Vaso'
    info = cursor.execute(query_str).fetchall() # list [(0,),(0,)]
    tempo1 = info[0]
    tempo2 = info[1]

    try:
        lista_vasos_bomba.append({"tempo1": tempo1[0], "tempo2": tempo2[0]})
        query_str = 'UPDATE Vaso SET tempo = 0, bomba = 0' # Zera novamente a bomba do vaso
        cursor.execute(query_str)
        banco.commit()
        return jsonify({'lista_vasos_bomba': lista_vasos_bomba})

    except:
        return make_response(jsonify('Erro!'), 404)

# Nodemcu realiza para verificar qual vaso está ativo
@app.route('/ativo', methods=['GET'])
def vaso_ativo():

    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Lista de vasos que devem ligar a bomba
    lista_vasos_ativos = []

    # Selecionando os dados do banco
    query_str = 'SELECT status FROM Vaso'
    info = cursor.execute(query_str).fetchall() # list[(1,),(1,)]
    status_vaso1 = info[0]
    status_vaso2 = info[1]

    lista_vasos_ativos.append({"idVaso1": status_vaso1[0], "idVaso2": status_vaso2[0]})

    return jsonify({'lista_vasos_bomba': lista_vasos_ativos})


# Nodemcu realiza para inserir informação no banco
@app.route('/informacao', methods=['POST'])
def add_info():

    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    # Leitura dos parâmetros recebidos
    idVaso = request.json.get('idVaso')
    temperatura = request.json.get('t')
    umidade = request.json.get('u')
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Verifica se o VASO está ativo
    query_str = 'SELECT status FROM Vaso WHERE id = ' + idVaso
    aux = cursor.execute(query_str).fetchall() # list[(1,0)]
    status = aux[0]

    if status[0] == 1:
        # Inserção no banco
        query_str = 'INSERT INTO Informacao (temperatura,umidade,data,idvaso) VALUES (\'' \
                    + temperatura + '\',\'' + umidade + '\',\'' + data + '\',\'' + idVaso + '\')'
        cursor.execute(query_str)

        try:
            banco.commit()
            verifica_medidas(idVaso, temperatura, umidade) # Analisando situação do vegetal
            return make_response(jsonify('Objeto cadastrado!'), 200)

        except Exception as e:
            return make_response(jsonify('Objeto não cadastrado!'), 406)
    else:
        return make_response(jsonify('O Vaso não está ativo!'), 406)


# Verifica se precisa acionar a bomba e adiciona na lista de bomba
def verifica_medidas(idVaso, temperatura, umidade):

    # Conexão com o banco
    banco = sqlite3.connect('banco.db')
    cursor = banco.cursor()

    query_str = 'SELECT Vegetal.tempIdeal, Vegetal.umidadeIdeal FROM Vaso INNER JOIN Vegetal ON Vaso.nomeVegetal = Vegetal.nome' \
                ' WHERE Vaso.id = ' + idVaso

    aux = cursor.execute(query_str).fetchall()[0]
    tempIdeal = aux[0]
    umidadeIdeal = aux[1]

    if float(temperatura) > 0.3 * float(tempIdeal) and float(umidade) < 0.8 * float(umidadeIdeal):
        query_str = 'UPDATE Vaso SET tempo = \'' + str(5) + '\', bomba = 1' + \
                    ' WHERE id = ' + idVaso
        cursor.execute(query_str)
        banco.commit()


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()

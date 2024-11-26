from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

placar = {'jogador': 0, 'ia': 0, 'empates': 0}


def verificar_vitoria(tabuleiro, jogador):
    vitorias = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], 
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]             
    ]
    for linha in vitorias:
        if tabuleiro[linha[0]] == tabuleiro[linha[1]] == tabuleiro[linha[2]] == jogador:
            return True
    return False


def verificar_empate(tabuleiro):
    return '' not in tabuleiro


def minimax(tabuleiro, profundidade, maximizando):
    if verificar_vitoria(tabuleiro, 'O'): 
        return 10 - profundidade
    if verificar_vitoria(tabuleiro, 'X'):  
        return profundidade - 10
    if verificar_empate(tabuleiro): 
        return 0
    
    if maximizando:
        melhor = -float('inf')
        for i in range(9):
            if tabuleiro[i] == '':
                tabuleiro[i] = 'O'
                melhor = max(melhor, minimax(tabuleiro, profundidade + 1, False))
                tabuleiro[i] = ''
        return melhor
    else:
        melhor = float('inf')
        for i in range(9):
            if tabuleiro[i] == '':
                tabuleiro[i] = 'X'
                melhor = min(melhor, minimax(tabuleiro, profundidade + 1, True))
                tabuleiro[i] = ''
        return melhor


def jogar_ia(tabuleiro):
    melhor_jogada = -1
    melhor_valor = -float('inf')
    for i in range(9):
        if tabuleiro[i] == '':
            tabuleiro[i] = 'O'
            valor = minimax(tabuleiro, 0, False)
            tabuleiro[i] = ''
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = i
    return melhor_jogada

@app.route('/')
def index():
    return render_template('index.html', placar=placar)

@app.route('/jogar', methods=['POST'])
def jogar():
    data = request.get_json()
    tabuleiro = data['tabuleiro']
    posicao = data['posicao']
    jogador = data['jogador']

    tabuleiro[posicao] = jogador

    if verificar_vitoria(tabuleiro, 'X'):
        placar['jogador'] += 1
        return jsonify({'tabuleiro': tabuleiro, 'vencedor': 'Jogador'})

    if verificar_empate(tabuleiro):
        placar['empates'] += 1
        return jsonify({'tabuleiro': tabuleiro, 'vencedor': 'empate'})

   
    posicao_ia = jogar_ia(tabuleiro)
    tabuleiro[posicao_ia] = 'O'

    if verificar_vitoria(tabuleiro, 'O'):
        placar['ia'] += 1
        return jsonify({'tabuleiro': tabuleiro, 'vencedor': 'IA'})

    if verificar_empate(tabuleiro):
        placar['empates'] += 1
        return jsonify({'tabuleiro': tabuleiro, 'vencedor': 'empate'})

    return jsonify({'tabuleiro': tabuleiro, 'vencedor': None})

@app.route('/reset', methods=['POST'])
def reset():
    global placar
    placar = {'jogador': 0, 'ia': 0, 'empates': 0}
    return jsonify({'placar': placar})

if __name__ == "__main__":
    app.run(debug=True)

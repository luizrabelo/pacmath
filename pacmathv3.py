# PacMath - Edição Pacman com Tabuada de Pitágoras
# Autor: Luiz - Jogo educativo de multiplicação com visual do Pacman
"""
Jogo educativo onde os jogadores precisam acertar 4 multiplicações consecutivas
para vencer, com visual inspirado no Pacman.
Inclui uma tabuada de Pitágoras como dica expansível.

Execução:
    python pacmath_v3.py
"""

import random
import pygame
import time

# ======= Parâmetros do jogo =======
LARGURA_TABULEIRO = 61           # largura do tabuleiro em células
CENTRO = LARGURA_TABULEIRO // 2  # posição central do tabuleiro
JOGADORES = ["Larissa", "Leticia"]

# Níveis de dificuldade com diferentes fatores para multiplicação
NIVEIS_DIFICULDADE = {
    "1": [1, 2, 3],                    # Fácil - números pequenos
    "2": [1, 2, 3, 4, 5, 6],          # Médio - números médios
    "3": [1, 2, 3, 4, 5, 6, 7, 8, 9], # Difícil - todos os números
    "4": [7, 8, 9]                     # Especial - apenas números altos
}

# ======= Interface gráfica Pygame =======
def executar_jogo_pacmath():
    """Função principal que executa o jogo PacMath"""
    pygame.init()
    
    # Configurações da tela
    LARGURA_JOGO = 1400        # largura da área do jogo
    LARGURA_TABUADA = 400      # largura da tabuada quando expandida
    ALTURA_PIXELS = 500        # altura da tela
    LARGURA_CELULA = LARGURA_JOGO // LARGURA_TABULEIRO  # largura de cada célula
    
    # Variável para controlar se a tabuada está expandida
    tabuada_expandida = False
    
    # Função para obter largura atual da tela
    def obter_largura_tela():
        return LARGURA_JOGO + (LARGURA_TABUADA if tabuada_expandida else 0)
    
    tela = pygame.display.set_mode((obter_largura_tela(), ALTURA_PIXELS))
    pygame.display.set_caption("PacMath - Edição Pacman")
    
    # Configuração de fontes para diferentes tamanhos de texto
    fonte_normal = pygame.font.SysFont("Arial", 28)
    fonte_pequena = pygame.font.SysFont("Arial", 20)
    fonte_grande = pygame.font.SysFont("Arial", 36, bold=True)
    fonte_mini = pygame.font.SysFont("Arial", 14)
    fonte_tabuada = pygame.font.SysFont("Arial", 16, bold=True)
    relogio = pygame.time.Clock()

    # Definição de cores usando RGB
    COR_FUNDO = (30, 30, 40)          # azul escuro
    COR_COMIDA = (255, 200, 0)        # amarelo dourado
    COR_PACMAN = (255, 255, 0)        # amarelo
    COR_PAREDE = (0, 0, 255)          # azul
    COR_TEXTO = (255, 255, 255)       # branco
    COR_BOTAO = (200, 200, 200)       # cinza claro
    COR_BOTAO_SELECIONADO = (100, 200, 100)  # verde
    COR_BORDA_BOTAO = (0, 0, 0)       # preto
    COR_MENSAGEM = (255, 255, 0)      # amarelo
    COR_SEGUNDA_CHANCE = (255, 165, 0)  # laranja para segunda chance
    COR_TABUADA_FUNDO = (50, 50, 60)  # cinza azulado para fundo da tabuada
    COR_TABUADA_HEADER = (100, 100, 120)  # cor dos cabeçalhos
    COR_TABUADA_DESTAQUE = (255, 255, 100)  # amarelo para destacar

    # Configurações visuais do Pacman e comida
    RAIO_COMIDA = 6         # raio dos pontinhos de comida
    RAIO_PACMAN = 18        # raio do Pacman
    POSICAO_Y_COMIDA = ALTURA_PIXELS // 2  # posição vertical da comida
    POSICOES_COMIDA = [i for i in range(1, LARGURA_TABULEIRO-1)]  # posições horizontais da comida
    comida_consumida = set()  # conjunto de posições onde a comida foi consumida

    # Variáveis de estado do jogo
    posicao_bola = CENTRO          # posição atual do Pacman
    executando = True              # controla se o jogo está rodando
    estado_jogo = "dificuldade"    # estados: dificuldade, jogando, fim_jogo
    jogador_atual = 0              # índice do jogador atual (0 ou 1)
    acertos_consecutivos = [0, 0]  # contador de acertos consecutivos para cada jogador
    fatores = []                   # lista de números para multiplicação
    
    # Variáveis da pergunta atual
    pergunta = ""           # texto da pergunta
    resposta_correta = 0    # resposta correta da multiplicação
    numero_a, numero_b = 0, 0  # números da multiplicação
    alternativas = []       # lista de alternativas de resposta
    alternativa_selecionada = None  # índice da alternativa selecionada
    texto_usuario = ""      # texto digitado pelo usuário
    mensagem = ""           # mensagem exibida na tela
    vencedor = None         # nome do vencedor
    
    # NOVA VARIÁVEL: Controla se o jogador está na segunda chance
    segunda_chance = False

    def obter_botao_tabuada():
        """Retorna o retângulo do botão de tabuada"""
        return pygame.Rect(LARGURA_JOGO - 80, 20, 60, 30)

    def desenhar_botao_tabuada():
        """Desenha o botão para expandir/recolher a tabuada"""
        botao = obter_botao_tabuada()
        cor_botao = COR_BOTAO_SELECIONADO if tabuada_expandida else COR_BOTAO
        pygame.draw.rect(tela, cor_botao, botao)
        pygame.draw.rect(tela, COR_BORDA_BOTAO, botao, 2)
        
        texto = "<<" if tabuada_expandida else "?"
        superficie_texto = fonte_normal.render(texto, True, COR_BORDA_BOTAO)
        tela.blit(superficie_texto, (botao.x + botao.width//2 - superficie_texto.get_width()//2, 
                                   botao.y + botao.height//2 - superficie_texto.get_height()//2))

    def desenhar_tabuada():
        """Desenha a tabuada de Pitágoras na área expandida"""
        if not tabuada_expandida:
            return
        
        # Área da tabuada
        x_inicio = LARGURA_JOGO
        largura_tabuada = LARGURA_TABUADA
        
        # Fundo da tabuada
        pygame.draw.rect(tela, COR_TABUADA_FUNDO, (x_inicio, 0, largura_tabuada, ALTURA_PIXELS))
        
        # Título
        titulo = fonte_normal.render("Tabuada de Pitágoras", True, COR_TEXTO)
        tela.blit(titulo, (x_inicio + 10, 10))
        
        # Configurações da tabela
        margem_x = x_inicio + 20
        margem_y = 50
        tamanho_celula = 35
        
        # Desenha a tabela 10x10 (0-9)
        for i in range(10):
            for j in range(10):
                x = margem_x + j * tamanho_celula
                y = margem_y + i * tamanho_celula
                
                # Retângulo da célula
                retangulo = pygame.Rect(x, y, tamanho_celula, tamanho_celula)
                
                # Cor da célula
                if i == 0 or j == 0:
                    # Cabeçalho
                    cor_celula = COR_TABUADA_HEADER
                    cor_texto = COR_TEXTO
                    if i == 0 and j == 0:
                        texto = "×"
                    elif i == 0:
                        texto = str(j)
                    else:
                        texto = str(i)
                else:
                    # Célula de resultado
                    resultado = i * j
                    cor_celula = COR_TABUADA_FUNDO
                    cor_texto = COR_TEXTO
                    
                    # Destaca se for a multiplicação atual
                    if estado_jogo == "jogando" and ((i == numero_a and j == numero_b) or (i == numero_b and j == numero_a)):
                        cor_celula = COR_TABUADA_DESTAQUE
                        cor_texto = COR_BORDA_BOTAO
                    
                    texto = str(resultado)
                
                # Desenha a célula
                pygame.draw.rect(tela, cor_celula, retangulo)
                pygame.draw.rect(tela, COR_BORDA_BOTAO, retangulo, 1)
                
                # Desenha o texto
                superficie_texto = fonte_tabuada.render(texto, True, cor_texto)
                texto_x = x + tamanho_celula//2 - superficie_texto.get_width()//2
                texto_y = y + tamanho_celula//2 - superficie_texto.get_height()//2
                tela.blit(superficie_texto, (texto_x, texto_y))

    def tela_escolher_dificuldade():
        """Desenha a tela de seleção de dificuldade e retorna os botões"""
        tela.fill(COR_FUNDO)
        
        # Desenha o título
        titulo = fonte_grande.render("PacMath - Escolha a Dificuldade", True, COR_TEXTO)
        tela.blit(titulo, (LARGURA_JOGO//2 - titulo.get_width()//2, 50))
        
        # Lista de opções de dificuldade
        opcoes = [
            "1 - Fácil (1, 2, 3)",
            "2 - Médio (1 a 6)", 
            "3 - Difícil (1 a 9)",
            "4 - Especial (7, 8, 9)"
        ]
        
        # Cria os botões para cada opção
        botoes = []
        for i, opcao in enumerate(opcoes):
            y = 150 + i * 60  # posição vertical de cada botão
            retangulo = pygame.Rect(LARGURA_JOGO//2 - 200, y, 400, 50)
            botoes.append((retangulo, str(i+1)))
            
            # Desenha o botão
            pygame.draw.rect(tela, COR_BOTAO, retangulo)
            pygame.draw.rect(tela, COR_BORDA_BOTAO, retangulo, 2)
            
            # Desenha o texto do botão
            texto = fonte_normal.render(opcao, True, COR_BORDA_BOTAO)
            tela.blit(texto, (retangulo.x + 10, retangulo.y + 15))
        
        # Desenha o botão da tabuada mesmo na tela de dificuldade
        desenhar_botao_tabuada()
        desenhar_tabuada()
        
        return botoes

    def desenhar_pacman(superficie, x, y, raio, virado_esquerda):
        """Desenha o Pacman na posição especificada"""
        # Desenha o corpo circular do Pacman
        pygame.draw.circle(superficie, COR_PACMAN, (x, y), raio)
        
        # Desenha a boca do Pacman (triângulo)
        pontos_boca = [
            (x, y),  # centro
            (x + (raio if not virado_esquerda else -raio), y - int(raio * 0.5)),  # ponto superior
            (x + (raio if not virado_esquerda else -raio), y + int(raio * 0.5))   # ponto inferior
        ]
        pygame.draw.polygon(superficie, COR_FUNDO, pontos_boca)

    def desenhar_tela_jogo(mostrar_equacao=True, destacar_errado=False, valor_correto=None):
        """Desenha a tela principal do jogo"""
        tela.fill(COR_FUNDO)
        
        # Desenha os pontinhos de comida
        for i in POSICOES_COMIDA:
            if i not in comida_consumida and i != posicao_bola:
                x = i * LARGURA_CELULA + LARGURA_CELULA // 2
                pygame.draw.circle(tela, COR_COMIDA, (x, POSICAO_Y_COMIDA), RAIO_COMIDA)
        
        # Desenha as paredes laterais
        pygame.draw.rect(tela, COR_PAREDE, (0, POSICAO_Y_COMIDA - 40, 10, 80))
        pygame.draw.rect(tela, COR_PAREDE, (LARGURA_JOGO - 10, POSICAO_Y_COMIDA - 40, 10, 80))
        
        # Desenha o Pacman na posição atual
        pacman_x = posicao_bola * LARGURA_CELULA + LARGURA_CELULA // 2
        virado_esquerda = jogador_atual == 1  # Leticia vira para esquerda
        desenhar_pacman(tela, pacman_x, POSICAO_Y_COMIDA, RAIO_PACMAN, virado_esquerda)
        
        # Desenha os nomes dos jogadores
        nome1 = fonte_normal.render("Larissa", True, COR_TEXTO)
        nome2 = fonte_normal.render("Leticia", True, COR_TEXTO)
        tela.blit(nome1, (20, 20))
        tela.blit(nome2, (LARGURA_JOGO-220, 20))
        
        # Desenha os contadores de acertos
        acertos1 = fonte_pequena.render(f"Acertos seguidos: {acertos_consecutivos[0]}", True, COR_TEXTO)
        acertos2 = fonte_pequena.render(f"Acertos seguidos: {acertos_consecutivos[1]}", True, COR_TEXTO)
        tela.blit(acertos1, (20, 50))
        tela.blit(acertos2, (LARGURA_JOGO-320, 50))
        
        # Desenha o botão da tabuada
        desenhar_botao_tabuada()
        
        # NOVA FUNCIONALIDADE: Indica se está na segunda chance
        if segunda_chance:
            indica_segunda_chance = fonte_pequena.render("SEGUNDA CHANCE", True, COR_SEGUNDA_CHANCE)
            tela.blit(indica_segunda_chance, (LARGURA_JOGO//2 - indica_segunda_chance.get_width()//2, 80))
        
        # Desenha a mensagem atual
        if mensagem:
            cor_msg = COR_SEGUNDA_CHANCE if segunda_chance else COR_MENSAGEM
            msg = fonte_pequena.render(mensagem, True, cor_msg)
            tela.blit(msg, (LARGURA_JOGO//2 - msg.get_width()//2, ALTURA_PIXELS-40))

        # Desenha a equação matemática
        if mostrar_equacao:
            cor_equacao = (255, 80, 80) if destacar_errado else (255, 255, 0)
            if segunda_chance and not destacar_errado:
                cor_equacao = COR_SEGUNDA_CHANCE  # Cor diferente para segunda chance
            texto_equacao = f"{numero_a} × {numero_b} = ?" if not destacar_errado else f"{numero_a} × {numero_b} = {valor_correto}"
            superficie_equacao = fonte_grande.render(texto_equacao, True, cor_equacao)
            tela.blit(superficie_equacao, (LARGURA_JOGO//2 - superficie_equacao.get_width()//2, ALTURA_PIXELS-150))

        # Desenha os botões de alternativas
        y_botao = ALTURA_PIXELS - 200
        largura_botao = 120
        altura_botao = 40
        espaco_botao = 20
        botoes = []
        
        for idx, alternativa in enumerate(alternativas):
            x_botao = LARGURA_JOGO//2 - (len(alternativas) * largura_botao + (len(alternativas)-1) * espaco_botao) // 2 + idx * (largura_botao + espaco_botao)
            retangulo = pygame.Rect(x_botao, y_botao, largura_botao, altura_botao)
            botoes.append(retangulo)
            
            # Escolhe a cor do botão (verde se selecionado, laranja se segunda chance)
            if alternativa_selecionada == idx:
                cor = COR_BOTAO_SELECIONADO
            elif segunda_chance:
                cor = (255, 200, 100)  # laranja claro para segunda chance
            else:
                cor = COR_BOTAO
            pygame.draw.rect(tela, cor, retangulo)
            pygame.draw.rect(tela, COR_BORDA_BOTAO, retangulo, 2)
            
            # Desenha o texto do botão
            texto = fonte_normal.render(str(alternativa), True, COR_BORDA_BOTAO)
            tela.blit(texto, (x_botao + largura_botao//2 - texto.get_width()//2, y_botao + altura_botao//2 - texto.get_height()//2))
        
        # Desenha a tabuada se expandida
        desenhar_tabuada()
        
        return botoes

    def desenhar_tela_fim_jogo():
        """Desenha a tela de fim de jogo"""
        tela.fill(COR_FUNDO)
        
        # Desenha o título de vitória
        titulo = fonte_grande.render(f"{vencedor} Venceu!", True, COR_TEXTO)
        tela.blit(titulo, (LARGURA_JOGO//2 - titulo.get_width()//2, ALTURA_PIXELS//2 - 100))
        
        # Desenha a mensagem para reiniciar
        msg_reiniciar = fonte_normal.render("Pressione ESPAÇO para jogar novamente ou ESC para sair", True, COR_TEXTO)
        tela.blit(msg_reiniciar, (LARGURA_JOGO//2 - msg_reiniciar.get_width()//2, ALTURA_PIXELS//2 - 50))
        
        # Desenha o botão da tabuada
        desenhar_botao_tabuada()
        desenhar_tabuada()

    def nova_pergunta():
        """Gera uma nova pergunta de multiplicação"""
        nonlocal numero_a, numero_b, pergunta, resposta_correta, alternativas, alternativa_selecionada, segunda_chance
        
        # Escolhe dois números aleatórios dos fatores disponíveis
        numero_a = random.choice(fatores)
        numero_b = random.choice(fatores)
        resposta_correta = numero_a * numero_b
        pergunta = f"{JOGADORES[jogador_atual]}, quanto é {numero_a} × {numero_b}?"
        
        # Gera alternativas incorretas
        resposta_errada1 = resposta_correta + random.choice([i for i in range(-10, 11) if i != 0 and resposta_correta + i > 0])
        resposta_errada2 = resposta_correta + random.choice([i for i in range(-20, 21) if i != 0 and resposta_correta + i > 0 and resposta_correta + i != resposta_errada1])
        
        # Mistura as alternativas
        alternativas = [resposta_correta, resposta_errada1, resposta_errada2]
        random.shuffle(alternativas)
        alternativa_selecionada = None
        segunda_chance = False  # Reset da segunda chance para nova pergunta

    def animar_movimento_pacman(posicao_inicial, posicao_final, virado_esquerda):
        """Anima o movimento do Pacman da posição inicial para a final"""
        passos = abs(posicao_final - posicao_inicial)
        if passos == 0:
            return
            
        direcao = 1 if posicao_final > posicao_inicial else -1
        
        # Anima passo a passo
        for passo in range(1, passos + 1):
            posicao_intermediaria = posicao_inicial + direcao * passo
            tela.fill(COR_FUNDO)
            
            # Redesenha a comida
            for i in POSICOES_COMIDA:
                if i not in comida_consumida and i != posicao_intermediaria:
                    x = i * LARGURA_CELULA + LARGURA_CELULA // 2
                    pygame.draw.circle(tela, COR_COMIDA, (x, POSICAO_Y_COMIDA), RAIO_COMIDA)
            
            # Redesenha as paredes
            pygame.draw.rect(tela, COR_PAREDE, (0, POSICAO_Y_COMIDA - 40, 10, 80))
            pygame.draw.rect(tela, COR_PAREDE, (LARGURA_JOGO - 10, POSICAO_Y_COMIDA - 40, 10, 80))
            
            # Redesenha o Pacman na nova posição
            pacman_x = posicao_intermediaria * LARGURA_CELULA + LARGURA_CELULA // 2
            desenhar_pacman(tela, pacman_x, POSICAO_Y_COMIDA, RAIO_PACMAN, virado_esquerda)
            
            # Redesenha os nomes dos jogadores
            nome1 = fonte_normal.render("Larissa", True, COR_TEXTO)
            nome2 = fonte_normal.render("Leticia", True, COR_TEXTO)
            tela.blit(nome1, (20, 20))
            tela.blit(nome2, (LARGURA_JOGO-220, 20))
            
            # Redesenha os contadores
            acertos1 = fonte_pequena.render(f"Acertos seguidos: {acertos_consecutivos[0]}", True, COR_TEXTO)
            acertos2 = fonte_pequena.render(f"Acertos seguidos: {acertos_consecutivos[1]}", True, COR_TEXTO)
            tela.blit(acertos1, (20, 50))
            tela.blit(acertos2, (LARGURA_JOGO-320, 50))
            
            # Redesenha o botão da tabuada
            desenhar_botao_tabuada()
            
            # Redesenha a mensagem
            if mensagem:
                msg = fonte_pequena.render(mensagem, True, COR_MENSAGEM)
                tela.blit(msg, (LARGURA_JOGO//2 - msg.get_width()//2, ALTURA_PIXELS-40))
            
            # Redesenha a tabuada se expandida
            desenhar_tabuada()
            
            pygame.display.flip()
            pygame.time.delay(40)  # pausa entre frames para suavizar a animação

    def animar_transicao_equacao():
        """Anima a transição mostrando números aleatórios antes da equação real"""
        for _ in range(12):
            numero_aleatorio_a = random.randint(1, 9)
            numero_aleatorio_b = random.randint(1, 9)
            superficie_equacao = fonte_grande.render(f"{numero_aleatorio_a} × {numero_aleatorio_b} = ?", True, (180, 180, 180))
            
            # Limpa apenas a área da equação
            tela.fill(COR_FUNDO, (0, ALTURA_PIXELS-90, LARGURA_JOGO, 90))
            tela.blit(superficie_equacao, (LARGURA_JOGO//2 - superficie_equacao.get_width()//2, ALTURA_PIXELS-80))
            
            # Redesenha a tabuada se expandida
            desenhar_tabuada()
            
            pygame.display.flip()
            pygame.time.delay(40)

    def processar_resposta(resposta):
        """Processa a resposta do jogador e atualiza o estado do jogo"""
        nonlocal jogador_atual, vencedor, estado_jogo, mensagem, posicao_bola, alternativa_selecionada, segunda_chance
        
        if resposta == resposta_correta:
            # ===== RESPOSTA CORRETA =====
            if not segunda_chance:
                # PRIMEIRA TENTATIVA CORRETA - Pacman se move
                acertos_consecutivos[jogador_atual] += 1
                mensagem = f"Correto! ({acertos_consecutivos[jogador_atual]}/4)"
                
                # Calcula quantos passos o Pacman deve se mover
                passos = (LARGURA_TABULEIRO // 2) // 4
                
                if jogador_atual == 0:  # Larissa se move para direita
                    nova_posicao = min(LARGURA_TABULEIRO - 1, posicao_bola + passos)
                    animar_movimento_pacman(posicao_bola, nova_posicao, virado_esquerda=False)
                    posicao_bola = nova_posicao
                else:  # Leticia se move para esquerda
                    nova_posicao = max(0, posicao_bola - passos)
                    animar_movimento_pacman(posicao_bola, nova_posicao, virado_esquerda=True)
                    posicao_bola = nova_posicao
                
                # Verifica condição de vitória
                if acertos_consecutivos[jogador_atual] >= 4 or posicao_bola <= 0 or posicao_bola >= LARGURA_TABULEIRO - 1:
                    vencedor = JOGADORES[jogador_atual]
                    estado_jogo = "fim_jogo"
                    posicao_bola = 0 if jogador_atual == 1 else LARGURA_TABULEIRO - 1
                else:
                    # Muda para o próximo jogador
                    jogador_atual = 1 - jogador_atual
                    animar_transicao_equacao()
                    nova_pergunta()
                    mensagem = pergunta
            else:
                # SEGUNDA CHANCE CORRETA - Pacman NÃO se move
                mensagem = f"Correto na segunda chance! Pacman não se move. ({acertos_consecutivos[jogador_atual]}/4)"
                # Muda para o próximo jogador
                jogador_atual = 1 - jogador_atual
                animar_transicao_equacao()
                nova_pergunta()
                mensagem = pergunta
        else:
            # ===== RESPOSTA INCORRETA =====
            if not segunda_chance:
                # PRIMEIRA TENTATIVA INCORRETA - Dá segunda chance
                # Mostra a resposta correta destacada em vermelho
                for _ in range(15):
                    desenhar_tela_jogo(mostrar_equacao=True, destacar_errado=True, valor_correto=resposta_correta)
                    pygame.display.flip()
                    pygame.time.delay(30)
                
                segunda_chance = True
                mensagem = f"Errado! A resposta era {resposta_correta}. Segunda chance!"
                # Não zera acertos consecutivos ainda, não muda jogador
            else:
                # SEGUNDA TENTATIVA INCORRETA - Perde a vez
                # Mostra a resposta correta destacada em vermelho
                for _ in range(15):
                    desenhar_tela_jogo(mostrar_equacao=True, destacar_errado=True, valor_correto=resposta_correta)
                    pygame.display.flip()
                    pygame.time.delay(30)
                
                mensagem = f"Errado novamente! A resposta era {resposta_correta}. Perdeu a vez!"
                acertos_consecutivos[jogador_atual] = 0  # Zera os acertos consecutivos
                segunda_chance = False
                # Muda para o próximo jogador
                jogador_atual = 1 - jogador_atual
                animar_transicao_equacao()
                nova_pergunta()
                mensagem = pergunta

    def reiniciar_jogo():
        """Reinicia o jogo para o estado inicial"""
        nonlocal posicao_bola, jogador_atual, acertos_consecutivos, estado_jogo, vencedor, texto_usuario, alternativa_selecionada, segunda_chance
        posicao_bola = CENTRO
        jogador_atual = 0
        acertos_consecutivos = [0, 0]
        estado_jogo = "dificuldade"
        vencedor = None
        texto_usuario = ""
        alternativa_selecionada = None
        segunda_chance = False
        comida_consumida.clear()

    def alternar_tabuada():
        """Alterna entre expandir e recolher a tabuada"""
        nonlocal tabuada_expandida
        tabuada_expandida = not tabuada_expandida
        # Redimensiona a tela
        pygame.display.set_mode((obter_largura_tela(), ALTURA_PIXELS))

    # Inicialização do jogo
    fatores = [1, 2, 3, 4, 5, 6]  # Médio por padrão
    nova_pergunta()
    mensagem = pergunta

    # Loop principal do jogo
    while executando:
        # Processa eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False
                
                elif estado_jogo == "fim_jogo":
                    if evento.key == pygame.K_SPACE:
                        reiniciar_jogo()
                
                elif estado_jogo == "jogando":
                    if evento.key == pygame.K_RETURN and texto_usuario:
                        try:
                            resposta = int(texto_usuario)
                            processar_resposta(resposta)
                            texto_usuario = ""
                        except ValueError:
                            mensagem = "Digite um número válido."
                    elif evento.key == pygame.K_BACKSPACE:
                        texto_usuario = texto_usuario[:-1]
                    elif evento.unicode.isdigit() and len(texto_usuario) < 8:
                        texto_usuario += evento.unicode
            
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Verifica clique no botão da tabuada
                if obter_botao_tabuada().collidepoint(mouse_x, mouse_y):
                    alternar_tabuada()
                
                elif estado_jogo == "dificuldade":
                    # Processa clique nos botões de dificuldade
                    botoes = tela_escolher_dificuldade()
                    for retangulo, nivel in botoes:
                        if retangulo.collidepoint(mouse_x, mouse_y):
                            fatores = NIVEIS_DIFICULDADE[nivel]
                            estado_jogo = "jogando"
                            nova_pergunta()
                            mensagem = pergunta
                            break
                
                elif estado_jogo == "jogando":
                    # Processa clique nos botões de alternativas
                    botoes = desenhar_tela_jogo()
                    for idx, retangulo in enumerate(botoes):
                        if retangulo.collidepoint(mouse_x, mouse_y):
                            alternativa_selecionada = idx
                            processar_resposta(alternativas[idx])
                            break

        # Desenha a tela apropriada baseada no estado do jogo
        if estado_jogo == "dificuldade":
            tela_escolher_dificuldade()
        elif estado_jogo == "jogando":
            desenhar_tela_jogo()
        elif estado_jogo == "fim_jogo":
            desenhar_tela_fim_jogo()
        
        # Atualiza a tela
        pygame.display.flip()
        relogio.tick(60)  # limita a 60 FPS

    pygame.quit()

if __name__ == "__main__":
    print("PacMath - Edição Pacman")
    print("Certifique-se de ter o pygame instalado: pip install pygame")
    print("Iniciando jogo...")
    executar_jogo_pacmath()

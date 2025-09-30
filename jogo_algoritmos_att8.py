import pyxel
import random

class Personagem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.larg = 16
        self.alt = 14
        pyxel.images[1].load(0, 0, "nave_16x16.png")
    def move(self, dx, dy):
        velocidade = 3
        self.x = self.x + dx * velocidade
        self.y = self.y + dy * velocidade
        if self.x > 256 - 16:
            self.x = 256 - 16
        if self.x < 0:
            self.x = 0
        if self.y > 256 - 16: 
            self.y = 256 -16
        if self.y < 0:
            self.y = 0
    def desenha(self):
        pyxel.blt(self.x, self.y, 1 , 0, 0, self.larg,self.alt)


class Inimigo:
    def __init__(self):
        self.x = random.randint(0, 240)
        pyxel.images[2].load(0, 0, "ufo_enemy_16x16.png")
        self.y = -16
        self.larg = 14
        self.alt = 14
    def move(self):
        velocidade = 2
        self.y = self.y + 1 * velocidade
    def desenha(self):
        pyxel.blt(self.x, self.y, 2 , 0, 0, self.larg,self.alt)
    def verificar_colisao(self, tiro):
        return (self.x < tiro.x + tiro.larg and
                self.x + self.larg > tiro.x and
                self.y < tiro.y + tiro.alt and
                self.y + self.alt > tiro.y)
    def colidiu_com_personagem(self, p):
       return (self.x < p.x + p.larg and
               self.x + self.larg > p.x and
               self.y < p.y + p.alt and
               self.y + self.alt > p.y)


class InimigoDiagonal(Inimigo):
    def __init__(self):
        super().__init__()
        self.direcao_x = random.choice([-1, 1])
        self.velocidade_x = 2
        self.velocidade_y = 1.5

    def move(self):
        self.y += self.velocidade_y
        self.x += self.direcao_x * self.velocidade_x

        if self.x <= 0 or self.x >= 256 - self.larg:
            self.direcao_x *= -1


class Tiro:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.larg = 5
        self.alt = 5
        self.cor = 7
        
    def move(self):
        velocidade = 5
        self.y = self.y - velocidade
    def desenha(self):
        pyxel.blt(self.x, self.y, 1, 0, 16, 5, 5)


class Cenario:
    def __init__(self):
        self.p = Personagem(10, 200)
        self.tiros = []
        self.inimigos = []
        self.tempo_recarga = 0


class Jogo:
    def __init__(self):
        pyxel.init(256, 256, title="Jogo")
        pyxel.images[0].load(0, 0, "espaço.jpg")
        pyxel.images[1].load(0,16,"fireball_5x5_final.png")
        self.cenario = Cenario()
        self.colidiu = False
        self.pontuacao = 0
        self.bg_y = 0
        self.speed_y = 0.8
        pyxel.run(self.update, self.draw)


    def update(self):
        if self.colidiu:
            if pyxel.btnp(pyxel.KEY_R):
                self.cenario = Cenario()
                self.pontuacao = 0
                self.colidiu = False
                self.bg_y = 0
            return
        self.bg_y += self.speed_y
        
        if self.bg_y >= 256:
            self.bg_y -= 256
        dx = pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_A)
        dy = pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_W)
        
        if self.cenario.tempo_recarga > 0:
            self.cenario.tempo_recarga = self.cenario.tempo_recarga - 1
        
        if pyxel.btnp(pyxel.KEY_SPACE) and self.cenario.tempo_recarga == 0:
            novo_tiro = Tiro(self.cenario.p.x + self.cenario.p.larg // 2 - 2,
                                  self.cenario.p.y)
            self.cenario.tiros.append(novo_tiro)
            self.cenario.tempo_recarga = 8

        for tiro in self.cenario.tiros:
            tiro.move()
        
        for tiro in self.cenario.tiros[:]:
            for inimigo in self.cenario.inimigos[:]:
                if inimigo.verificar_colisao(tiro):
                    self.pontuacao = self.pontuacao + 10
                    self.cenario.tiros.remove(tiro)
                    self.cenario.inimigos.remove(inimigo)
                    break
        
        limite_spawn = max(10, 60 - (pyxel.frame_count // 120))
        if random.randint(1, int(limite_spawn)) == 1:
            # --- ALTERAÇÃO PARA ESCOLHER QUAL INIMIGO CRIAR ---
            if random.random() < 0.3: # 30% de chance de ser diagonal
                novo_inimigo = InimigoDiagonal()
            else: # 70% de chance de ser o normal
                novo_inimigo = Inimigo()
            self.cenario.inimigos.append(novo_inimigo)
        
        self.cenario.p.move(dx, dy)
        
        for inimigo in self.cenario.inimigos:
            inimigo.move()
        for inimigo in self.cenario.inimigos:
            if inimigo.colidiu_com_personagem(self.cenario.p):
                self.colidiu = True
                break
        self.cenario.inimigos = [inimigo for inimigo in self.cenario.inimigos if inimigo.y < pyxel.height]
        self.cenario.tiros = [tiro for tiro in self.cenario.tiros if tiro.y > -tiro.alt]

    def draw(self):
        pyxel.cls(0)
        y = int(self.bg_y)
        pyxel.blt(0, y - 256, 0, 0, 0, 256, 256)
        pyxel.blt(0, y, 0, 0, 0, 256, 256)
        pyxel.text(5, 5, f"PONTOS: {self.pontuacao}", 7)
        self.cenario.p.desenha()
        
        for inimigo in self.cenario.inimigos:
            inimigo.desenha()

        for tiro in self.cenario.tiros:
            tiro.desenha()
        
        if self.colidiu: 
            pyxel.rect(20, 100, 216, 56, 0)      
            pyxel.rectb(20, 100, 216, 56, 8)      
            pyxel.text(40, 112, "GAME OVER", 8)
            pyxel.text(40, 124, f"PONTOS: {self.pontuacao}", 7)
            pyxel.text(40, 136, "Pressione R para reiniciar", 7)

Jogo()
import pyxel
import random

class Personagem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.larg = 16
        self.alt = 16
        self.cor = 4
        pyxel.images[1].load(0, 0, "nave_16x16.png")
    def move(self, dx, dy):
        velocidade = 3
        self.x = self.x + dx * velocidade
        self.y = self.y + dy * velocidade
    def desenha(self):
        pyxel.blt(self.x, self.y, 1 , 0, 0, self.larg,self.alt)


class Inimigo:
    def __init__(self):
        self.x = random.randint(0, 256)
        self.y = 0
        self.larg = 10
        self.alt = 10
        self.cor = 6
    def move(self):
        velocidade = 2
        self.y = self.y + 1 * velocidade
    def desenha(self):
        pyxel.rect(self.x, self.y, self.larg, self.alt, self.cor)


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
        pyxel.rect(self.x, self.y, self.larg, self.alt, self.cor)


class Cenario:
    def __init__(self):
        self.p = Personagem(10, 200)
        self.i = Inimigo()
        self.tiros = []
        self.tempo_recarga = 0


class Jogo:
    def __init__(self):
        pyxel.init(256, 256, title="Jogo")
        pyxel.images[0].load(0, 0, "espaço.jpg")
        self.cenario = Cenario()
        pyxel.run(self.update, self.draw)

    def update(self):
        dx = 0
        dy = 0
        if pyxel.btn(pyxel.KEY_D):
            dx = 1
        if pyxel.btn(pyxel.KEY_A):
            dx = -1
        if pyxel.btn(pyxel.KEY_W):
            dy = -1
        if pyxel.btn(pyxel.KEY_S):
            dy = 1
        
        if self.cenario.tempo_recarga > 0:
            self.cenario.tempo_recarga = self.cenario.tempo_recarga - 1
        
        if pyxel.btnp(pyxel.KEY_SPACE) and self.cenario.tempo_recarga == 0:
            novo_tiro = Tiro(self.cenario.p.x + self.cenario.p.larg // 2 - 2,
                             self.cenario.p.y)
            self.cenario.tiros.append(novo_tiro)
            self.cenario.tempo_recarga = 8

        for tiro in self.cenario.tiros:
            tiro.move()
        
        self.cenario.p.move(dx, dy)
        self.cenario.i.move()

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0,0,0,0,0,256,256)
        self.cenario.p.desenha()
        self.cenario.i.desenha()
        for tiro in self.cenario.tiros:
            tiro.desenha()


Jogo()
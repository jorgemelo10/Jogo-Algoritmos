import pyxel
import random

class Personagem:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.larg = 16
        self.alt = 16
        pyxel.images[1].load(0, 0, "nave_16x16.png")
    def move(self, dx, dy):
        velocidade = 4
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
        self.larg = 16
        self.alt = 16
        self.pode_atirar = random.random() < 0.4
        if self.pode_atirar:
            self.intervalo_tiro = random.randint(50, 90)
            self.timer_tiro = self.intervalo_tiro

    def move(self, lista_tiros_inimigos):
        velocidade = 2
        self.y = self.y + 1 * velocidade

        if self.pode_atirar:
            self.timer_tiro -= 1
            if self.timer_tiro <= 0:
                novo_tiro = TiroInimigo(self.x + self.larg // 2 - 1, self.y + self.alt)
                lista_tiros_inimigos.append(novo_tiro)
                self.timer_tiro = self.intervalo_tiro

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
                self.y + p.alt > p.y)


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


class TiroInimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.larg = 3
        self.alt = 7
        self.cor = 8

    def move(self):
        velocidade = 3
        self.y = self.y + velocidade

    def desenha(self):
        pyxel.rect(self.x, self.y, self.larg, self.alt, self.cor)


class Cenario:
    def __init__(self):
        self.p = Personagem(10, 200)
        self.tiros = []
        self.inimigos = []
        self.tiros_inimigos = []
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
        self.frame_inicio_jogo = pyxel.frame_count
        pyxel.run(self.update, self.draw)

    def update(self):
        if self.colidiu:
            if pyxel.btnp(pyxel.KEY_R):
                self.cenario = Cenario()
                self.pontuacao = 0
                self.colidiu = False
                self.bg_y = 0
                self.frame_inicio_jogo = pyxel.frame_count
            return
        
        self.bg_y = (self.bg_y + self.speed_y) % 256
        
        dx = pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_A)
        dy = pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_W)
        
        if self.cenario.tempo_recarga > 0:
            self.cenario.tempo_recarga -= 1
        
        if pyxel.btnp(pyxel.KEY_SPACE) and self.cenario.tempo_recarga == 0:
            novo_tiro = Tiro(self.cenario.p.x + self.cenario.p.larg // 2 - 2, self.cenario.p.y)
            self.cenario.tiros.append(novo_tiro)
            self.cenario.tempo_recarga = 8

        for tiro in self.cenario.tiros:
            tiro.move()
        
        for tiro in self.cenario.tiros[:]:
            for inimigo in self.cenario.inimigos[:]:
                if inimigo.verificar_colisao(tiro):
                    self.pontuacao += 10
                    self.cenario.tiros.remove(tiro)
                    self.cenario.inimigos.remove(inimigo)
                    break
        
        frames_corridos = pyxel.frame_count - self.frame_inicio_jogo
        limite_spawn = max(10, 30 - (frames_corridos // 120))
        
        if random.randint(1, int(limite_spawn)) == 1:
            novo_inimigo = Inimigo()

            pode_spawnar = True
            for i_existente in self.cenario.inimigos:
                if i_existente.y < novo_inimigo.alt:
                    distancia_x = abs(novo_inimigo.x - i_existente.x)
                    if distancia_x < novo_inimigo.larg:
                        pode_spawnar = False
                        break
            
            if pode_spawnar:
                self.cenario.inimigos.append(novo_inimigo)
        
        self.cenario.p.move(dx, dy)
        
        for inimigo in self.cenario.inimigos:
            inimigo.move(self.cenario.tiros_inimigos)
            
        for inimigo in self.cenario.inimigos:
            if inimigo.colidiu_com_personagem(self.cenario.p):
                self.colidiu = True
                break

        for tiro_inimigo in self.cenario.tiros_inimigos:
            tiro_inimigo.move()

        for tiro_inimigo in self.cenario.tiros_inimigos[:]:
            p = self.cenario.p
            if (p.x < tiro_inimigo.x + tiro_inimigo.larg and
                p.x + p.larg > tiro_inimigo.x and
                p.y < tiro_inimigo.y + tiro_inimigo.alt and
                p.y + p.alt > tiro_inimigo.y):
                self.colidiu = True
                self.cenario.tiros_inimigos.remove(tiro_inimigo)
                break
        
        self.cenario.inimigos = [inimigo for inimigo in self.cenario.inimigos if inimigo.y < pyxel.height]
        self.cenario.tiros = [tiro for tiro in self.cenario.tiros if tiro.y > -tiro.alt]
        self.cenario.tiros_inimigos = [ti for ti in self.cenario.tiros_inimigos if ti.y < pyxel.height]

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
        
        for tiro_inimigo in self.cenario.tiros_inimigos:
            tiro_inimigo.desenha()

        if self.colidiu: 
            pyxel.rect(20, 100, 216, 56, 0)
            pyxel.rectb(20, 100, 216, 56, 8)
            pyxel.text(40, 112, "GAME OVER", 8)
            pyxel.text(40, 124, f"PONTOS: {self.pontuacao}", 7)
            pyxel.text(40, 136, "Pressione R para reiniciar", 7)

Jogo()
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
        pyxel.blt(self.x, self.y, 1 , 0, 0, self.larg,self.alt,0)


class Inimigo:
    def __init__(self):
        self.x = random.randint(0, 240)
        self.y = -16
        self.larg = 14
        self.alt = 14
        self.pontos = 2
    def move(self, lista_tiros_inimigos):
        velocidade = 2
        self.y = self.y + 1 * velocidade
    def desenha(self):
        pyxel.blt(self.x, self.y, 2, 0, 0, self.larg, self.alt,0)
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
        self.pontos = 4
    def move(self, lista_tiros_inimigos):
        self.y += self.velocidade_y
        self.x += self.direcao_x * self.velocidade_x

        if self.x <= 0 or self.x >= 256 - self.larg:
            self.direcao_x *= -1
    def desenha(self):
        pyxel.blt(self.x, self.y, 2, 16, 0, self.larg, self.alt,0)


class InimigoAtirador(Inimigo):
    def __init__(self):
        super().__init__()
        self.pontos = 6
        self.intervalo_tiro = random.randint(30, 60) # A cada 2-4 segundos (a 30fps)
        self.timer_tiro = self.intervalo_tiro
    def move(self, lista_tiros_inimigos):
        super().move(lista_tiros_inimigos)
        self.timer_tiro -= 1
        if self.timer_tiro <= 0:
            novo_tiro = TiroInimigo(self.x + self.larg // 2 - 1, self.y + self.alt)
            lista_tiros_inimigos.append(novo_tiro)
            self.timer_tiro = self.intervalo_tiro
    def desenha(self):
        pyxel.blt(self.x, self.y, 2, 32, 0, self.larg, self.alt, 0)

class power_up:
    def __init__(self):
        self.x = random.randint(0, 240)
        self.y = 0
        self.larg = 16
        self.alt = 16
        self.tipo = "triple_shot" 
    
    def move(self):
        self.y += 2
    
    def desenha(self):   
        pyxel.blt(self.x, self.y, 1, 0, 32, self.larg, self.alt)
    
    def colidiu_com_personagem(self, p):
        return(
            self.x < p.x + p.larg and
            self.x + self.larg > p.x and
            self.y < p.y + p.alt and
            self.y + self.alt > p.y
        )

class Tiro:
    def __init__(self, x, y, vx=0, vy=-5):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.larg = 5
        self.alt = 5
        self.cor = 7
       
    def move(self):
        self.x += self.vx
        self.y += self.vy

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
        self.powerups = []
        self.trishot_timer = 0



class Jogo:
    def __init__(self):
        pyxel.init(256, 256, title="Jogo")
        pyxel.images[0].load(0, 0, "espaço.jpg")
        pyxel.images[1].load(0,16,"fireball_5x5_final.png")
        pyxel.images[2].load(0, 0, "ufo_enemy_16x16.png")      
        pyxel.images[2].load(16, 0, "alienigena_verde_laranja_16x16.png")
        pyxel.images[2].load(32, 0, "inimigo_atirador_16x16.png")
        pyxel.images[1].load(0, 32, "powerup_trishot_16x16.png")
        pyxel.sound(0).set("c3", "p", "7", "n", 10)
        pyxel.sound(1).set("e3c2", "p", "7", "n", 15)
        self.cenario = Cenario()
        self.colidiu = False
        self.pontuacao = 0
        self.bg_y = 0
        self.speed_y = 0.8
        self.recorde = 0
        self.frames_partida = 0
        
        pyxel.run(self.update, self.draw)


    def update(self):
        if self.colidiu:
            if self.pontuacao > self.recorde:
                self.recorde = self.pontuacao
                
            if pyxel.btnp(pyxel.KEY_R):
                self.cenario = Cenario()
                self.pontuacao = 0
                self.colidiu = False
                self.bg_y = 0
                self.frames_partida = 0
            return
            
        self.frames_partida += 1
        self.bg_y += self.speed_y
        
        if self.bg_y >= 256:
            self.bg_y -= 256
        dx = pyxel.btn(pyxel.KEY_D) - pyxel.btn(pyxel.KEY_A)
        dy = pyxel.btn(pyxel.KEY_S) - pyxel.btn(pyxel.KEY_W)
        
        if self.cenario.tempo_recarga > 0:
            self.cenario.tempo_recarga = self.cenario.tempo_recarga - 1
        
        if pyxel.btnp(pyxel.KEY_SPACE) and self.cenario.tempo_recarga == 0:
  
            cx = self.cenario.p.x + self.cenario.p.larg // 2 - 2
            cy = self.cenario.p.y

            if self.cenario.trishot_timer > 0:
                self.cenario.tiros.append(Tiro(cx, cy, vx=0, vy=-5))
                self.cenario.tiros.append(Tiro(cx, cy, vx=-2, vy=-5))
                self.cenario.tiros.append(Tiro(cx, cy, vx=+2, vy=-5))
                self.cenario.tempo_recarga = 10
            else:       
                self.cenario.tiros.append(Tiro(cx, cy, vx=0, vy=-5))
                self.cenario.tempo_recarga = 8
            pyxel.play(0, 0) 

        for tiro in self.cenario.tiros:
            tiro.move()
        
        for tiro in self.cenario.tiros[:]:
            for inimigo in self.cenario.inimigos[:]:
                if inimigo.verificar_colisao(tiro):
                    self.pontuacao += inimigo.pontos
                    self.cenario.tiros.remove(tiro)
                    self.cenario.inimigos.remove(inimigo)
                    pyxel.play(1, 1)
                    break
        
        limite_spawn = max(10, 60 - (self.frames_partida // 120))
        if random.randint(1, int(limite_spawn)) == 1:
            chance = random.random()
            if chance < 0.2: # 20% de chance para o InimigoAtirador
                novo_inimigo = InimigoAtirador()
            elif chance < 0.5: # 30% de chance para o InimigoDiagonal
                novo_inimigo = InimigoDiagonal()
            else: # 50% de chance para o Inimigo normal
                novo_inimigo = Inimigo()
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
        
        if random.randint(1, 1500) == 1:
            self.cenario.powerups.append(power_up())
        
        for power in self.cenario.powerups:
            power.move()


        for power in self.cenario.powerups[:]:
            if power.colidiu_com_personagem(self.cenario.p):
                if power.tipo == "triple_shot":
                    self.cenario.trishot_timer = 480
                self.cenario.powerups.remove(power)
        
        if self.cenario.trishot_timer > 0:
            self.cenario.trishot_timer -= 1
                
        self.cenario.inimigos = [inimigo for inimigo in self.cenario.inimigos if inimigo.y < pyxel.height]
        self.cenario.tiros = [
            tiro for tiro in self.cenario.tiros
            if (-tiro.alt <= tiro.y <= pyxel.height and -tiro.larg <= tiro.x <= pyxel.width)]
        self.cenario.tiros_inimigos = [ti for ti in self.cenario.tiros_inimigos if ti.y < pyxel.height]


    def draw(self):
        pyxel.cls(0)
        y = int(self.bg_y)
        pyxel.blt(0, y - 256, 0, 0, 0, 256, 256)
        pyxel.blt(0, y, 0, 0, 0, 256, 256)
        pyxel.text(5, 5, f"PONTOS: {self.pontuacao}", 7)
        pyxel.text(60, 5, f"RECORDE: {self.recorde}", 8)

        self.cenario.p.desenha()
        
        for inimigo in self.cenario.inimigos:
            inimigo.desenha()

        for tiro in self.cenario.tiros:
            tiro.desenha()
            
        for tiro_inimigo in self.cenario.tiros_inimigos:
            tiro_inimigo.desenha()
        
        for power in self.cenario.powerups:
            power.desenha()

        if self.cenario.trishot_timer > 0:
            restante = self.cenario.trishot_timer // 60  
            pyxel.text(160, 5, f"TRI-SHOT: {restante}s", 10)
        
        if self.colidiu: 
            pyxel.rect(20, 100, 216, 56, 0)      
            pyxel.rectb(20, 100, 216, 56, 8)      
            pyxel.text(40, 112, "GAME OVER", 8)
            pyxel.text(40, 124, f"PONTUACAO FINAL: {self.pontuacao}", 7)
            pyxel.text(40, 136, "Pressione R para reiniciar", 7)

Jogo()
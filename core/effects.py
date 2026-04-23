import pymunk
import pygame
import math
import random

class Particle:
    def __init__(self, x, y, vx, vy, color, size, life, gravity=0, friction=0.99):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.gravity = gravity
        self.friction = friction
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= self.friction
        self.vy *= self.friction
        self.life -= 1
        self.size = max(1, self.size * 0.98)
        
    def render(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            color = (*self.color, alpha) if len(self.color) == 3 else self.color
            pos = (int(self.x), int(self.y))
            
            surf = pygame.Surface((int(self.size) * 2, int(self.size) * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (int(self.size), int(self.size)), int(self.size))
            screen.blit(surf, (pos[0] - int(self.size), pos[1] - int(self.size)))


class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def add_particle(self, x, y, vx, vy, color, size, life, gravity=0, friction=0.99):
        particle = Particle(x, y, vx, vy, color, size, life, gravity, friction)
        self.particles.append(particle)
        return particle
        
    def emit_blood(self, x, y, count=10):
        for _ in range(count):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-5, -1)
            self.add_particle(x, y, vx, vy, (180, 20, 20), random.uniform(2, 5), random.uniform(30, 60), 0.3, 0.98)
            
    def emit_fire(self, x, y, count=5):
        for _ in range(count):
            vx = random.uniform(-1, 1)
            vy = random.uniform(-2, -0.5)
            color = random.choice([(255, 100, 0), (255, 150, 0), (255, 200, 0), (255, 50, 0)])
            self.add_particle(x, y, vx, vy, color, random.uniform(3, 8), random.uniform(20, 40), 0.1, 0.95)
            
    def emit_smoke(self, x, y, count=3):
        for _ in range(count):
            vx = random.uniform(-0.5, 0.5)
            vy = random.uniform(-1.5, -0.5)
            color = (100, 100, 100)
            self.add_particle(x, y, vx, vy, color, random.uniform(5, 12), random.uniform(40, 80), -0.05, 0.99)
            
    def emit_sparks(self, x, y, count=8):
        for _ in range(count):
            vx = random.uniform(-4, 4)
            vy = random.uniform(-4, 4)
            self.add_particle(x, y, vx, vy, (255, 255, 100), random.uniform(1, 3), random.uniform(15, 30), 0.2, 0.92)
            
    def emit_debris(self, x, y, count=6):
        for _ in range(count):
            vx = random.uniform(-3, 3)
            vy = random.uniform(-4, 2)
            color = random.choice([(120, 100, 80), (80, 80, 80), (60, 50, 40)])
            self.add_particle(x, y, vx, vy, color, random.uniform(2, 6), random.uniform(40, 80), 0.4, 0.95)
            
    def emit_electricity(self, x1, y1, x2, y2):
        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        steps = max(int(dist / 10), 2)
        
        for i in range(steps):
            t = i / steps
            x = x1 + (x2 - x1) * t + random.uniform(-3, 3)
            y = y1 + (y2 - y1) * t + random.uniform(-3, 3)
            self.add_particle(x, y, 0, 0, (100, 150, 255), random.uniform(2, 4), random.uniform(5, 15), 0, 0.9)
            
    def emit_water(self, x, y, count=15):
        for _ in range(count):
            vx = random.uniform(-2, 2)
            vy = random.uniform(-1, 3)
            self.add_particle(x, y, vx, vy, (50, 100, 200), random.uniform(2, 5), random.uniform(30, 60), 0.3, 0.97)

    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
                
    def render(self, screen, camera_offset=(0, 0)):
        for particle in self.particles:
            screen_x = particle.x - camera_offset[0]
            screen_y = particle.y - camera_offset[1]
            
            if 0 <= screen_x <= 1280 and 0 <= screen_y <= 720:
                pos = (int(screen_x), int(screen_y))
                size = max(1, int(particle.size))
                
                if len(particle.color) == 3:
                    pygame.draw.circle(screen, particle.color, pos, size)
                else:
                    surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(surf, particle.color, (size, size), size)
                    screen.blit(surf, (pos[0] - size, pos[1] - size))
                    
    def clear(self):
        self.particles.clear()
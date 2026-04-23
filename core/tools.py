import pymunk
import pygame
import math
import random
from core import effects

class Tool:
    def __init__(self, name, category, damage=0, speed=1, range_val=0, is_projectile=False, is_explosive=False):
        self.name = name
        self.category = category
        self.damage = damage
        self.speed = speed
        self.range_val = range_val
        self.is_projectile = is_projectile
        self.is_explosive = is_explosive
        self.color = (150, 150, 150)
        self.size = 10
        
    def use(self, x, y, angle, game):
        pass
        
    def render(self, screen, x, y, angle=0):
        pass


class MeleeWeapon(Tool):
    def __init__(self, name, damage, speed, range_val, size, color):
        super().__init__(name, "melee", damage, speed, range_val, is_projectile=False)
        self.color = color
        self.size = size
        
    def use(self, x, y, angle, game, particles):
        hit_objects = self.get_hit_objects(x, y, angle, game)
        
        for obj in hit_objects:
            if hasattr(obj, 'apply_damage'):
                obj.apply_damage(self.damage)
                if particles:
                    particles.emit_blood(obj.x, obj.y)
                    
        if particles and hit_objects:
            particles.emit_sparks(x + math.cos(angle) * self.range_val, y + math.sin(angle) * self.range_val)
            
    def get_hit_objects(self, x, y, angle, game):
        hit_radius = self.range_val
        hit_objects = []
        
        for ragdoll in game.ragdolls:
            for body in ragdoll.bodies:
                dist = math.sqrt((body.position.x - x)**2 + (body.position.y - y)**2)
                if dist < hit_radius:
                    hit_objects.append(body)
                    
        return hit_objects
    
    def render(self, screen, x, y, angle=0):
        end_x = x + math.cos(angle) * self.range_val
        end_y = y + math.sin(angle) * self.range_val
        
        pygame.draw.line(screen, self.color, (int(x), int(y)), (int(end_x), int(end_y)), int(self.size // 2))
        pygame.draw.circle(screen, self.color, (int(end_x), int(end_y)), int(self.size // 2))


class Firearm(Tool):
    def __init__(self, name, damage, speed, range_val, projectile_speed, ammo, color):
        super().__init__(name, "firearm", damage, speed, range_val, is_projectile=True)
        self.projectile_speed = projectile_speed
        self.ammo = ammo
        self.max_ammo = ammo
        self.color = color
        self.projectiles = []
        
    def use(self, x, y, angle, game, particles):
        if self.ammo > 0:
            self.ammo -= 1
            
            bullet_vx = math.cos(angle) * self.projectile_speed
            bullet_vy = math.sin(angle) * self.projectile_speed
            
            projectile = Projectile(x, y, bullet_vx, bullet_vy, self.damage, self.range_val)
            self.projectiles.append(projectile)
            
            if particles:
                particles.emit_sparks(x, y, 3)
                
    def update(self, game, particles):
        for projectile in self.projectiles[:]:
            projectile.update()
            
            if projectile.life <= 0:
                self.projectiles.remove(projectile)
                continue
                
            for ragdoll in game.ragdolls:
                for body in ragdoll.bodies:
                    dist = math.sqrt((body.position.x - projectile.x)**2 + (body.position.y - projectile.y)**2)
                    if dist < body.position.length * 0.1 + 15:
                        if hasattr(body, 'apply_damage'):
                            pass
                        if particles:
                            particles.emit_blood(projectile.x, projectile.y)
                        self.projectiles.remove(projectile)
                        break
                        
    def render(self, screen, camera_offset):
        for projectile in self.projectiles:
            pos = (int(projectile.x - camera_offset[0]), int(projectile.y - camera_offset[1]))
            pygame.draw.circle(screen, self.color, pos, 3)
            
    def reload(self):
        self.ammo = self.max_ammo


class Projectile:
    def __init__(self, x, y, vx, vy, damage, life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.damage = damage
        self.life = life
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1


class Explosive(Tool):
    def __init__(self, name, damage, radius, delay=0):
        super().__init__(name, "explosive", damage, 1, radius, is_explosive=True)
        self.delay = delay
        self.timer = delay
        self.exploded = False
        self.color = (80, 80, 80)
        self.x = 0
        self.y = 0
        
    def use(self, x, y, angle, game, particles):
        self.x = x
        self.y = y
        self.timer = self.delay
        self.exploded = False
        
    def update(self, game, particles):
        if self.timer > 0:
            self.timer -= 1
        elif not self.exploded:
            self.explode(game, particles)
            
    def explode(self, game, particles):
        self.exploded = True
        
        for ragdoll in game.ragdolls:
            for body in ragdoll.bodies:
                dist = math.sqrt((body.position.x - self.x)**2 + (body.position.y - self.y)**2)
                if dist < self.range_val:
                    force_mag = self.damage * (1 - dist / self.range_val)
                    angle = math.atan2(body.position.y - self.y, body.position.x - self.x)
                    body.apply_impulse_at_world_point((
                        math.cos(angle) * force_mag,
                        math.sin(angle) * force_mag
                    ), body.position)
                    
        if particles:
            particles.emit_fire(self.x, self.y, 20)
            particles.emit_smoke(self.x, self.y, 10)
            particles.emit_debris(self.x, self.y, 15)
            
    def render(self, screen, camera_offset):
        pos = (int(self.x - camera_offset[0]), int(self.y - camera_offset[1]))
        color = (255, 50, 50) if self.timer > 0 and self.timer < 30 else self.color
        pygame.draw.circle(screen, color, pos, 8)
        pygame.draw.circle(screen, (0, 0, 0), pos, 8, 1)


def create_default_weapons():
    weapons = {}
    
    weapons['knife'] = MeleeWeapon('Cuchillo', 15, 2, 40, 4, (180, 180, 180))
    weapons['sword'] = MeleeWeapon('Espada', 25, 1.5, 60, 6, (160, 160, 165))
    weapons['axe'] = MeleeWeapon('Hacha', 35, 2, 50, 8, (140, 100, 60))
    weapons['machete'] = MeleeWeapon('Machete', 20, 1.8, 55, 5, (120, 120, 120))
    weapons['bat'] = MeleeWeapon('Bate', 15, 2.5, 45, 5, (139, 90, 43))
    weapons['chain'] = MeleeWeapon('Cadena', 10, 3, 60, 3, (100, 100, 100))
    weapons['hammer'] = MeleeWeapon('Martillo', 40, 3, 35, 10, (80, 80, 90))
    weapons['wrench'] = MeleeWeapon('Llave Inglesa', 15, 2, 35, 4, (150, 150, 160))
    weapons['saw'] = MeleeWeapon('Sierra', 30, 1, 30, 6, (200, 150, 50))
    weapons['spear'] = MeleeWeapon('Lanza', 20, 1.5, 70, 3, (139, 119, 94))
    
    weapons['pistol'] = Firearm('Pistola', 20, 0.5, 500, 15, 12, (80, 80, 85))
    weapons['rifle'] = Firearm('Rifle', 25, 0.3, 800, 20, 30, (70, 70, 75))
    weapons['shotgun'] = Firearm('Escopeta', 15, 1, 200, 12, 8, (60, 60, 65))
    weapons['smg'] = Firearm('Subfusil', 10, 0.1, 400, 18, 50, (75, 75, 80))
    weapons['sniper'] = Firearm('Fusil de francotirador', 60, 2, 1500, 30, 5, (50, 50, 55))
    weapons['minigun'] = Firearm('Minigun', 8, 0.05, 600, 22, 200, (90, 90, 95))
    weapons['rocket_launcher'] = Firearm('Lanzacohetes', 100, 3, 1000, 10, 5, (100, 80, 50))
    
    weapons['grenade'] = Explosive('Granada', 50, 100, 90)
    weapons['c4'] = Explosive('C4', 80, 150, 0)
    weapons['dynamite'] = Explosive('Dinamita', 60, 120, 180)
    weapons['mine'] = Explosive('Mina', 40, 80, 0)
    weapons['nuke'] = Explosive('Mini Nucleo', 200, 300, 300)
    
    return weapons
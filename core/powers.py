import pymunk
import pygame
import math
import random

class Power:
    def __init__(self, name, description, cooldown, duration):
        self.name = name
        self.description = description
        self.cooldown = cooldown
        self.duration = duration
        self.timer = 0
        self.active = False
        
    def activate(self, x, y, game):
        self.timer = self.duration
        self.active = True
        
    def update(self, game, particles):
        if self.timer > 0:
            self.timer -= 1
        if self.timer <= 0:
            self.active = False
            
    def render(self, screen, camera_offset):
        pass


class FirePower(Power):
    def __init__(self):
        super().__init__("Fire", "Burn objects and ragdolls", 0, 1)
        self.color = (255, 100, 0)
        
    def activate(self, x, y, game):
        super().activate(x, y, game)
        
    def update(self, game, particles):
        if self.active:
            for ragdoll in game.ragdolls:
                for body in ragdoll.bodies:
                    if random.random() < 0.1:
                        particles.emit_fire(body.position.x, body.position.y, 2)
                        
    def render(self, screen, camera_offset):
        if self.active:
            pygame.draw.circle(screen, self.color, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 100)


class IcePower(Power):
    def __init__(self):
        super().__init__("Ice", "Freeze objects and create ice walls", 0, 0)
        self.color = (150, 200, 255)
        self.frozen_bodies = []
        
    def activate(self, x, y, game):
        self.frozen_bodies.clear()
        
    def update(self, game, particles):
        for ragdoll in game.ragdolls:
            for body in ragdoll.bodies:
                if body not in self.frozen_bodies:
                    self.frozen_bodies.append(body)
                    
    def render(self, screen, camera_offset):
        pass


class ElectricityPower(Power):
    def __init__(self):
        super().__init__("Electricity", "Electrocute objects and activate motors", 0, 1)
        self.color = (100, 150, 255)
        self.arc_positions = []
        
    def activate(self, x, y, game):
        self.arc_positions = [(x, y)]
        
    def update(self, game, particles):
        if self.active:
            for ragdoll in game.ragdolls:
                for body in ragdoll.bodies:
                    if random.random() < 0.15:
                        if particles:
                            self.arc_positions.append((body.position.x, body.position.y))
                            if len(self.arc_positions) > 1:
                                prev = self.arc_positions[-2]
                                curr = self.arc_positions[-1]
                                particles.emit_electricity(prev[0], prev[1], curr[0], curr[1])
                                
                                if len(self.arc_positions) > 5:
                                    self.arc_positions.clear()
                                    
    def render(self, screen, camera_offset):
        pass


class GravityPower(Power):
    def __init__(self):
        super().__init__("Gravity", "Manipulate world gravity", 0, 0)
        self.original_gravity = (0, 900)
        self.modified = False
        
    def activate(self, x, y, game):
        self.modified = not self.modified
        if self.modified:
            game.space.gravity = (0, -900)
        else:
            game.space.gravity = (0, 900)
            
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


class WindPower(Power):
    def __init__(self):
        super().__init__("Wind", "Create wind currents", 0, 1)
        self.color = (200, 200, 200)
        self.wind_force = 5
        
    def activate(self, x, y, game):
        self.active = True
        
    def update(self, game, particles):
        if self.active:
            for ragdoll in game.ragdolls:
                for body in ragdoll.bodies:
                    force = (self.wind_force * random.uniform(-1, 1), -self.wind_force)
                    body.apply_force_at_center(force)
                    
            if random.random() < 0.2:
                particles.add_particle(
                    random.randint(0, SCREEN_WIDTH),
                    SCREEN_HEIGHT,
                    random.uniform(-2, 2),
                    random.uniform(-5, -2),
                    self.color,
                    random.uniform(3, 8),
                    random.uniform(20, 40),
                    -0.1,
                    0.99
                )
                
    def render(self, screen, camera_offset):
        pass


class TransmutePower(Power):
    def __init__(self):
        super().__init__("Transmute", "Convert objects into other materials", 0, 0)
        self.transmutation_targets = [
            ("Gold", (255, 215, 0)),
            ("Silver", (192, 192, 192)),
            ("Pizza", (255, 200, 100)),
            ("Cookies", (210, 180, 140)),
            ("Cookies!", (139, 69, 19)),
            ("Money", (50, 200, 50)),
        ]
        self.current_index = 0
        
    def activate(self, x, y, game):
        target_name, target_color = self.transmutation_targets[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.transmutation_targets)
        
        for ragdoll in game.ragdolls:
            for shape in ragdoll.shapes:
                if hasattr(shape, 'color'):
                    shape.color = target_color
                    
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


class ExplosionPower(Power):
    def __init__(self):
        super().__init__("Shockwave", "Create explosive shockwaves", 0, 0)
        
    def activate(self, x, y, game):
        for ragdoll in game.ragdolls:
            for body in ragdoll.bodies:
                dist = math.sqrt((body.position.x - x)**2 + (body.position.y - y)**2)
                if dist > 0:
                    force_mag = 1000 / dist
                    angle = math.atan2(body.position.y - y, body.position.x - x)
                    body.apply_impulse_at_center((
                        math.cos(angle) * force_mag,
                        math.sin(angle) * force_mag
                    ))
                    
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


class XRayPower(Power):
    def __init__(self):
        super().__init__("X-Ray", "See internal structures", 0, 0)
        
    def activate(self, x, y, game):
        pass
        
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


class RegeneratePower(Power):
    def __init__(self):
        super().__init__("Regenerate", "Restore damaged ragdolls", 0, 0)
        
    def activate(self, x, y, game):
        for ragdoll in game.ragdolls[:]:
            ragdoll.destroy()
        game.ragdolls.clear()
        
        from core.ragdoll import Ragdoll
        for _ in range(3):
            x = random.randint(200, SCREEN_WIDTH - 200)
            y = random.randint(200, SCREEN_HEIGHT - 200)
            game.ragdolls.append(Ragdoll(game.space, x, y))
            
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


class MutatePower(Power):
    def __init__(self):
        super().__init__("Mutate", "Transform ragdolls into monsters", 0, 0)
        
    def activate(self, x, y, game):
        for ragdoll in game.ragdolls:
            for shape in ragdoll.shapes:
                shape.color = (100, 200, 100)
                
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


class SpawnPower(Power):
    def __init__(self):
        super().__init__("Spawn", "Spawn new ragdolls", 0, 0)
        
    def activate(self, x, y, game):
        from core.ragdoll import Ragdoll
        game.ragdolls.append(Ragdoll(game.space, x, y))
        
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


class GodPower(Power):
    def __init__(self):
        super().__init__("God Mode", "Make ragdolls invincible", 0, 0)
        
    def activate(self, x, y, game):
        pass
        
    def update(self, game, particles):
        pass
        
    def render(self, screen, camera_offset):
        pass


def create_default_powers():
    powers = {}
    
    powers['fire'] = FirePower()
    powers['ice'] = IcePower()
    powers['electricity'] = ElectricityPower()
    powers['gravity'] = GravityPower()
    powers['wind'] = WindPower()
    powers['transmute'] = TransmutePower()
    powers['shockwave'] = ExplosionPower()
    powers['xray'] = XRayPower()
    powers['regenerate'] = RegeneratePower()
    powers['mutate'] = MutatePower()
    powers['spawn'] = SpawnPower()
    powers['god'] = GodPower()
    
    return powers


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
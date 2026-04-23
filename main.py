import pygame
import sys
import json
import os
import pymunk
import math

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

COLORS = {
    'background': (40, 44, 52),
    'ui_background': (60, 66, 78),
    'ui_selected': (100, 150, 200),
    'ui_text': (220, 220, 220),
    'blood': (180, 20, 20),
    'fire': (255, 100, 0),
    'water': (50, 100, 200),
}

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Mutillateadoll2")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = 'menu'
        
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        
        self.create_boundaries()
        
        self.ragdolls = []
        self.particles = []
        self.selected_tool = None
        self.selected_power = None
        
        self.camera_offset = [0, 0]
        self.zoom = 1.0
        self.dragging = False
        self.dragged_object = None
        self.dragged_ragdoll = None
        self.mouse_angle = 0
        
        self.current_tool_category = 0
        self.current_tool_name = 'knife'
        self.current_tool_index = 0
        self.tool_category_weapons = {
            'Cuerpo a Cuerpo': ['knife', 'sword', 'axe', 'machete', 'bat', 'chain', 'hammer'],
            'Armas de Fuego': ['pistol', 'rifle', 'shotgun', 'smg', 'sniper', 'rocket_launcher'],
            'Explosivos': ['grenade', 'c4', 'dynamite', 'mine', 'nuke'],
        }
        self.tool_category_powers = ['fire', 'ice', 'electricity', 'gravity', 'wind', 'transmute', 'shockwave', 'regenerate', 'spawn']
        
        self.current_power_active = False
        self.mouse_pressed = False
        
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        
        self.options = {
            'blood': True,
            'fullscreen': False,
            'sound': True,
        }
        
        from core.ragdoll import Ragdoll
        from core.effects import ParticleSystem
        from core.tools import create_default_weapons
        from core.powers import create_default_powers
        
        self._ragdoll_class = Ragdoll
        self.particles = ParticleSystem()
        self.weapons = create_default_weapons()
        self.powers = create_default_powers()
        
        self.current_tool_name = 'knife'
        self.current_tool_index = 0
        self.tool_category_weapons = {
            'Melee': ['knife', 'sword', 'axe', 'machete', 'bat', 'chain', 'hammer'],
            'Firearm': ['pistol', 'rifle', 'shotgun', 'smg', 'sniper', 'rocket_launcher'],
            'Explosive': ['grenade', 'c4', 'dynamite', 'mine', 'nuke'],
        }
        self.tool_category_powers = ['fire', 'ice', 'electricity', 'gravity', 'wind', 'transmute', 'shockwave', 'regenerate', 'spawn']
        
        self.mouse_pressed = False
        
    def create_boundaries(self):
        ground = pymunk.Segment(self.space.static_body, (50, SCREEN_HEIGHT - 50), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), 5)
        ground.friction = 1.0
        self.space.add(ground)
        
        left_wall = pymunk.Segment(self.space.static_body, (50, 50), (50, SCREEN_HEIGHT - 50), 5)
        left_wall.friction = 1.0
        self.space.add(left_wall)
        
        right_wall = pymunk.Segment(self.space.static_body, (SCREEN_WIDTH - 50, 50), (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50), 5)
        right_wall.friction = 1.0
        self.space.add(right_wall)
        
        ceiling = pymunk.Segment(self.space.static_body, (50, 50), (SCREEN_WIDTH - 50, 50), 5)
        ceiling.friction = 1.0
        self.space.add(ceiling)
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] - self.camera_offset[0]
        mouse_y = mouse_pos[1] - self.camera_offset[1]
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == 'game':
                        self.state = 'menu'
                    else:
                        self.running = False
                elif event.key == pygame.K_F5:
                    if self.state == 'game':
                        self.reset()
                elif event.key == pygame.K_n and self.state == 'game':
                    self.spawn_ragdoll(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                elif event.key == pygame.K_1:
                    self.current_tool_category = 0
                    self.update_tool()
                elif event.key == pygame.K_2:
                    self.current_tool_category = 1
                    self.update_tool()
                elif event.key == pygame.K_3:
                    self.current_tool_category = 2
                    self.update_tool()
                elif event.key == pygame.K_4:
                    self.current_power_active = True
                elif event.key == pygame.K_5:
                    self.use_current_power()
                elif event.key == pygame.K_LEFT:
                    self.current_tool_index = max(0, self.current_tool_index - 1)
                    self.update_tool()
                elif event.key == pygame.K_RIGHT:
                    self.current_tool_index += 1
                    self.update_tool()
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.state == 'menu':
                        self.check_menu_click(mouse_pos)
                    elif self.state == 'game':
                        self.check_game_click(mouse_pos)
                        self.mouse_pressed = True
                elif event.button == 4:
                    self.zoom_in()
                elif event.button == 5:
                    self.zoom_out()
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    self.dragged_object = None
                    self.dragged_ragdoll = None
                    self.mouse_pressed = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.dragged_ragdoll:
                    pos = pygame.mouse.get_pos()
                    mouse_x = pos[0] - self.camera_offset[0]
                    mouse_y = pos[1] - self.camera_offset[1]
                    
                    min_x = 50
                    max_x = SCREEN_WIDTH - 50
                    min_y = 50
                    max_y = SCREEN_HEIGHT - 50
                    
                    mouse_x = max(min_x, min(max_x, mouse_x))
                    mouse_y = max(min_y, min(max_y, mouse_y))
                    
                    center = self.dragged_ragdoll.get_position()
                    dx = mouse_x - center.x
                    dy = mouse_y - center.y
                    
                    for body in self.dragged_ragdoll.bodies:
                        body.position = (body.position.x + dx, body.position.y + dy)
        
        # No camera movement - keep ragdoll always visible
            
    def check_menu_click(self, pos):
        button_width = 200
        button_height = 50
        start_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        new_button = pygame.Rect(start_x, start_y, button_width, button_height)
        if new_button.collidepoint(pos):
            self.state = 'game'
            self.reset()
            
        quit_button = pygame.Rect(start_x, start_y + 70, button_width, button_height)
        if quit_button.collidepoint(pos):
            self.running = False
            
    def check_game_click(self, pos):
        mouse_x = pos[0] - self.camera_offset[0]
        mouse_y = pos[1] - self.camera_offset[1]
        
        for ragdoll in self.ragdolls:
            for body in ragdoll.bodies:
                if body.position.get_distance((mouse_x, mouse_y)) < 40:
                    self.dragging = True
                    self.dragged_ragdoll = ragdoll
                    return
                    
    def spawn_ragdoll(self, x=None, y=None):
        if x is None:
            x = SCREEN_WIDTH // 2
        if y is None:
            y = SCREEN_HEIGHT // 2
            
        ragdoll = self._ragdoll_class(self.space, x, y)
        self.ragdolls.append(ragdoll)
        
    def reset(self):
        for ragdoll in self.ragdolls:
            ragdoll.destroy()
        self.ragdolls.clear()
        self.particles.clear()
        self.camera_offset = [0, 0]
        self.zoom = 1.0
        self.spawn_ragdoll(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
    def zoom_in(self):
        self.zoom = min(2.0, self.zoom * 1.1)
        
    def zoom_out(self):
        self.zoom = max(0.5, self.zoom * 0.9)
        
    def update_tool(self):
        categories = list(self.tool_category_weapons.keys())
        if self.current_tool_category < len(categories):
            category = categories[self.current_tool_category]
            tools = self.tool_category_weapons[category]
            if self.current_tool_index < len(tools):
                self.current_tool_name = tools[self.current_tool_index]
                
    def use_current_power(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_x = mouse_pos[0] - self.camera_offset[0]
        mouse_y = mouse_pos[1] - self.camera_offset[1]
        
        if self.tool_category_powers:
            power_name = self.tool_category_powers[self.current_tool_index % len(self.tool_category_powers)]
            power = self.powers.get(power_name)
            if power:
                power.activate(mouse_x, mouse_y, self)
        
    def update(self):
        if self.state == 'game':
            dt = 1.0 / FPS
            self.space.step(dt)
            
            for ragdoll in self.ragdolls:
                ragdoll.update()
                
            for name, power in self.powers.items():
                power.update(self, self.particles)
                
            self.particles.update()
            
            if self.mouse_pressed and self.current_tool_name:
                mouse_pos = pygame.mouse.get_pos()
                tool = self.weapons.get(self.current_tool_name)
                if tool:
                    if hasattr(tool, 'is_projectile') and tool.is_projectile:
                        pass
                    elif hasattr(tool, 'is_explosive') and tool.is_explosive:
                        tool.update(self, self.particles)
                    else:
                        mouse_x = mouse_pos[0] - self.camera_offset[0]
                        mouse_y = mouse_pos[1] - self.camera_offset[1]
                        for ragdoll in self.ragdolls:
                            for body in ragdoll.bodies:
                                dist = body.position.get_distance((mouse_x, mouse_y))
                                if dist < 50:
                                    force = 20
                                    angle = math.atan2(body.position.y - mouse_y, body.position.x - mouse_x)
                                    body.apply_impulse_at_world_point((
                                        math.cos(angle) * force,
                                        math.sin(angle) * force
                                    ), body.position)
                                    if self.options.get('blood', True):
                                        self.particles.emit_blood(body.position.x, body.position.y, 5)
            
    def render(self):
        self.screen.fill(COLORS['background'])
        
        if self.state == 'menu':
            self.render_menu()
        elif self.state == 'game':
            self.render_game()
            
        pygame.display.flip()
        
    def render_menu(self):
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("Mutillateadoll2", True, COLORS['ui_text'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        button_width = 200
        button_height = 50
        start_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        new_button = pygame.Rect(start_x, start_y, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['ui_selected'], new_button)
        new_text = self.font.render("NUEVO JUEGO", True, COLORS['ui_text'])
        new_text_rect = new_text.get_rect(center=new_button.center)
        self.screen.blit(new_text, new_text_rect)
        
        quit_button = pygame.Rect(start_x, start_y + 70, button_width, button_height)
        pygame.draw.rect(self.screen, COLORS['ui_background'], quit_button)
        quit_text = self.font.render("SALIR", True, COLORS['ui_text'])
        quit_text_rect = quit_text.get_rect(center=quit_button.center)
        self.screen.blit(quit_text, quit_text_rect)
        
    def render_game(self):
        for ragdoll in self.ragdolls:
            ragdoll.render(self.screen, self.camera_offset)
            
        self.particles.render(self.screen, self.camera_offset)
        
        self.render_hud()
        
    def render_hud(self):
        hud_rect = pygame.Rect(10, 10, 250, SCREEN_HEIGHT - 20)
        pygame.draw.rect(self.screen, COLORS['ui_background'], hud_rect)
        
        title = self.font.render("Mutillateadoll2", True, COLORS['ui_text'])
        self.screen.blit(title, (20, 20))
        
        instructions = [
            "Controles:",
            "N - Nuevo Ragdoll",
            "F5 - Reiniciar",
            "1 - Armas Cuerpo a Cuerpo",
            "2 - Armas de Fuego",
            "3 - Explosivos",
            "4 - Activar Poder",
            "5 - Usar Poder",
            "Click - Atacar",
            "Izquierda/Derecha - Cambiar",
            "Flechas/WASD - Mover",
            "Rueda Raton - Zoom",
            "ESC - Menu",
        ]
        
        for i, text in enumerate(instructions):
            text_surf = self.small_font.render(text, True, COLORS['ui_text'])
            self.screen.blit(text_surf, (20, 80 + i * 22))
            
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
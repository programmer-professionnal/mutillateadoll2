import pygame

class Toolbox:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 20)
        
        self.categories = {
            'Melee': [],
            'Firearm': [],
            'Explosive': [],
            'Powers': [],
            'Build': [],
        }
        
        self.current_category = 'Melee'
        self.selected_tool = None
        self.selected_index = 0
        
        self.expanded = False
        self.expanded_rect = pygame.Rect(10, 80, 220, 400)
        
    def add_tool(self, tool, category):
        if category in self.categories:
            self.categories[category].append(tool)
            
    def select_next(self):
        tools = self.categories[self.current_category]
        self.selected_index = (self.selected_index + 1) % len(tools)
        self.selected_tool = tools[self.selected_index] if tools else None
        
    def select_previous(self):
        tools = self.categories[self.current_category]
        self.selected_index = (self.selected_index - 1) % len(tools)
        self.selected_tool = tools[self.selected_index] if tools else None
        
    def set_category(self, category):
        if category in self.categories:
            self.current_category = category
            self.selected_index = 0
            tools = self.categories[category]
            self.selected_tool = tools[0] if tools else None
            
    def render(self, colors):
        bg_rect = pygame.Rect(10, 10, 200, 60)
        pygame.draw.rect(self.screen, colors['ui_background'], bg_rect)
        pygame.draw.rect(self.screen, colors['ui_text'], bg_rect, 2)
        
        title = self.font.render(f"Category: {self.current_category}", True, colors['ui_text'])
        self.screen.blit(title, (20, 15))
        
        if self.expanded:
            pygame.draw.rect(self.screen, colors['ui_background'], self.expanded_rect)
            pygame.draw.rect(self.screen, colors['ui_text'], self.expanded_rect, 2)
            
            start_y = self.expanded_rect.y + 10
            
            for i, category in enumerate(self.categories.keys()):
                rect = pygame.Rect(self.expanded_rect.x + 10, start_y + i * 30, 180, 25)
                color = colors['ui_selected'] if category == self.current_category else colors['ui_background']
                pygame.draw.rect(self.screen, color, rect)
                
                text = self.font.render(category, True, colors['ui_text'])
                self.screen.blit(text, (rect.x + 10, rect.y + 3))


class HUD:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        self.left_panel_rect = pygame.Rect(10, 10, 250, 500)
        self.right_panel_rect = pygame.Rect(SCREEN_WIDTH - 160, 10, 150, 400)
        
    def render(self, colors, game_state):
        pygame.draw.rect(self.screen, colors['ui_background'], self.left_panel_rect)
        
        title = self.font.render("Mutillateadoll2", True, colors['ui_text'])
        self.screen.blit(title, (20, 15))
        
        instructions = [
            "Controls:",
            "N - New Ragdoll",
            "F5 - Reset",
            "1-5 - Select Category",
            "Arrow Keys/WASD - Move",
            "Mouse Wheel - Zoom",
            "Click + Drag - Move",
            "R - Rotate Tool",
            "ESC - Menu",
        ]
        
        for i, text in enumerate(instructions):
            text_surf = self.small_font.render(text, True, colors['ui_text'])
            self.screen.blit(text_surf, (20, 45 + i * 22))
            
        pygame.draw.rect(self.screen, colors['ui_background'], self.right_panel_rect)
        
        stats_title = self.font.render("Stats", True, colors['ui_text'])
        self.screen.blit(stats_title, (SCREEN_WIDTH - 150, 15))
        
        stats = [
            f"Ragdolls: {game_state.get('ragdoll_count', 0)}",
            f"FPS: {game_state.get('fps', 0)}",
        ]
        
        for i, text in enumerate(stats):
            text_surf = self.small_font.render(text, True, colors['ui_text'])
            self.screen.blit(text_surf, (SCREEN_WIDTH - 150, 45 + i * 22))


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
import pygame
import json

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 28)
        self.title_font = pygame.font.Font(None, 72)
        
        self.buttons = []
        self.selected = 0
        
    def add_button(self, text, action):
        self.buttons.append({'text': text, 'action': action})
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.buttons[self.selected]['action']
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.buttons):
                if button['rect'].collidepoint(pos):
                    return button['action']
        return None
        
    def render(self, colors):
        pass


class MainMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            {'text': 'New Game', 'action': 'new'},
            {'text': 'Load', 'action': 'load'},
            {'text': 'Options', 'action': 'options'},
            {'text': 'Quit', 'action': 'quit'},
        ]
        
    def render(self, colors):
        self.screen.fill(colors['background'])
        
        title = self.title_font.render("Mutillateadoll2", True, colors['ui_text'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        button_width = 200
        button_height = 50
        start_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        for i, button in enumerate(self.buttons):
            rect = pygame.Rect(start_x, start_y + i * 70, button_width, button_height)
            button['rect'] = rect
            
            color = colors['ui_selected'] if i == self.selected else colors['ui_background']
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, colors['ui_text'], rect, 2)
            
            text = self.font.render(button['text'], True, colors['ui_text'])
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)


class PauseMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            {'text': 'Resume', 'action': 'resume'},
            {'text': 'Restart', 'action': 'restart'},
            {'text': 'Save', 'action': 'save'},
            {'text': 'Load', 'action': 'load'},
            {'text': 'Options', 'action': 'options'},
            {'text': 'Main Menu', 'action': 'menu'},
        ]
        
    def render(self, colors, paused=False):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        title = self.title_font.render("PAUSED" if paused else "MENU", True, colors['ui_text'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        button_width = 200
        button_height = 50
        start_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        for i, button in enumerate(self.buttons):
            rect = pygame.Rect(start_x, start_y + i * 70, button_width, button_height)
            button['rect'] = rect
            
            color = colors['ui_selected'] if i == self.selected else colors['ui_background']
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, colors['ui_text'], rect, 2)
            
            text = self.font.render(button['text'], True, colors['ui_text'])
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)


class OptionsMenu(Menu):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            {'text': 'Blood: ON', 'action': 'toggle_blood'},
            {'text': 'Fullscreen: NO', 'action': 'toggle_fullscreen'},
            {'text': 'Back', 'action': 'back'},
        ]
        
    def render(self, colors, options):
        self.screen.fill(colors['background'])
        
        title = self.title_font.render("OPTIONS", True, colors['ui_text'])
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title, title_rect)
        
        button_width = 250
        button_height = 50
        start_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - 50
        
        self.buttons[0]['text'] = f"Blood: {'ON' if options.get('blood', True) else 'OFF'}"
        self.buttons[1]['text'] = f"Fullscreen: {'YES' if options.get('fullscreen', False) else 'NO'}"
        
        for i, button in enumerate(self.buttons):
            rect = pygame.Rect(start_x, start_y + i * 70, button_width, button_height)
            button['rect'] = rect
            
            color = colors['ui_selected'] if i == self.selected else colors['ui_background']
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, colors['ui_text'], rect, 2)
            
            text = self.font.render(button['text'], True, colors['ui_text'])
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
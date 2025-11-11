import pygame
import random
import sys

# OPEN SOURCE DO WHATEVER U WANT TO DO HERE

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
DARK_RED = (139, 0, 0)

# Background color palettes for day/night cycle
DAY_SKY = (135, 206, 235)      # Bright blue
SUNSET_SKY = (255, 140, 100)   # Orange-pink
NIGHT_SKY = (25, 25, 60)       # Dark blue
DAWN_SKY = (255, 180, 150)     # Light orange-pink

# Game variables
GRAVITY = 0.5
FLAP_STRENGTH = -7  # Reduced from -10 for better control
INITIAL_PIPE_GAP = 320  # Starting gap size - Very easy at start
MIN_PIPE_GAP = 200  # Minimum gap at high scores - Still playable
PIPE_WIDTH = 70
INITIAL_PIPE_VELOCITY = 2  # Slower initial speed
MAX_PIPE_VELOCITY = 8  # Maximum speed at high scores
INITIAL_SPAWN_TIME = 1800  # Starting spawn time
MIN_SPAWN_TIME = 1000  # Minimum spawn time at high scores

# Game States
HOME = 0
PLAYING = 1
SETTINGS = 2
MODDING = 3
GAME_OVER = 4


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-8, -2)
        self.life = 60  # frames
        self.size = random.randint(3, 8)
        self.color = random.choice([RED, ORANGE, YELLOW, DARK_RED])
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3  # gravity
        self.life -= 1
        self.size = max(1, self.size - 0.1)
        
    def draw(self, screen):
        if self.life > 0:
            alpha = int(255 * (self.life / 60))
            color = tuple(min(255, c + (255 - c) * (1 - self.life / 60)) for c in self.color[:3])
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))
            
    def is_alive(self):
        return self.life > 0


class Airplane:
    def __init__(self, image=None):
        self.x = 100
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = 40  # Reduced for better collision
        self.height = 24  # Reduced for better collision
        self.angle = 0
        self.image = image
        self.use_image = image is not None
        
    def flap(self):
        self.velocity = FLAP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
        # Update angle based on velocity
        if self.velocity < 0:
            self.angle = min(25, -self.velocity * 3)
        else:
            self.angle = max(-90, -self.velocity * 2)
            
    def draw(self, screen):
        if self.use_image:
            # Draw image centered at airplane position
            img_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(self.image, img_rect)
        else:
            # Draw airplane body (fallback)
            points = [
                (self.x - 20, self.y),
                (self.x + 20, self.y - 5),
                (self.x + 25, self.y),
                (self.x + 20, self.y + 5)
            ]
            pygame.draw.polygon(screen, GRAY, points)
            
            # Draw wings
            pygame.draw.polygon(screen, RED, [
                (self.x - 10, self.y - 2),
                (self.x - 10, self.y - 15),
                (self.x + 5, self.y - 2)
            ])
            pygame.draw.polygon(screen, RED, [
                (self.x - 10, self.y + 2),
                (self.x - 10, self.y + 15),
                (self.x + 5, self.y + 2)
            ])
            
            # Draw tail
            pygame.draw.polygon(screen, YELLOW, [
                (self.x - 20, self.y - 8),
                (self.x - 25, self.y),
                (self.x - 20, self.y + 8)
            ])
            
            # Draw cockpit window
            pygame.draw.circle(screen, BLACK, (self.x + 15, self.y), 4)
        
    def get_rect(self):
        # More accurate collision box - centered on airplane
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        
    def is_off_screen(self):
        return self.y < 0 or self.y > SCREEN_HEIGHT


class Pipe:
    def __init__(self, x, velocity=INITIAL_PIPE_VELOCITY, gap_size=INITIAL_PIPE_GAP, pipe_image=None):
        self.x = x
        self.velocity = velocity
        self.gap_size = gap_size
        # Ensure pipe gap is always in a playable position
        # Minimum 100px from top, maximum leaves 100px at bottom
        min_height = 100
        max_height = SCREEN_HEIGHT - gap_size - 100
        # Ensure max_height is always greater than min_height
        if max_height <= min_height:
            max_height = min_height + 50
        self.height = random.randint(min_height, max_height)
        self.passed = False
        self.pipe_image = pipe_image
        self.use_image = pipe_image is not None
        
        # Falling animation properties
        self.falling = False
        self.fall_rotation = 0
        self.fall_direction = random.choice([-1, 1])  # -1 for left, 1 for right
        self.fall_speed = 0
        self.fall_y_offset = 0
        
    def update(self):
        if not self.falling:
            self.x -= self.velocity
        else:
            # Falling animation
            self.fall_rotation += 3 * self.fall_direction  # Rotate
            self.fall_speed += 0.5  # Gravity
            self.fall_y_offset += self.fall_speed  # Fall down
            self.x += self.fall_direction * 2  # Move sideways
        
    def draw(self, screen):
        if self.falling:
            # Draw falling pipes with rotation
            if self.use_image:
                # Top pipe falling
                top_pipe_img = pygame.transform.flip(self.pipe_image, False, True)
                top_pipe_scaled = pygame.transform.scale(top_pipe_img, (PIPE_WIDTH, self.height))
                rotated_top = pygame.transform.rotate(top_pipe_scaled, self.fall_rotation)
                top_rect = rotated_top.get_rect(center=(self.x + PIPE_WIDTH // 2, self.height // 2 + self.fall_y_offset))
                screen.blit(rotated_top, top_rect)
                
                # Bottom pipe falling
                bottom_y = self.height + self.gap_size
                bottom_height = SCREEN_HEIGHT - bottom_y
                bottom_pipe_scaled = pygame.transform.scale(self.pipe_image, (PIPE_WIDTH, bottom_height))
                rotated_bottom = pygame.transform.rotate(bottom_pipe_scaled, self.fall_rotation)
                bottom_rect = rotated_bottom.get_rect(center=(self.x + PIPE_WIDTH // 2, bottom_y + bottom_height // 2 + self.fall_y_offset))
                screen.blit(rotated_bottom, bottom_rect)
            else:
                # Fallback: draw rotated rectangles
                # Create surfaces for pipes
                top_surface = pygame.Surface((PIPE_WIDTH, self.height), pygame.SRCALPHA)
                pygame.draw.rect(top_surface, GREEN, (0, 0, PIPE_WIDTH, self.height))
                pygame.draw.rect(top_surface, DARK_GREEN, (0, 0, PIPE_WIDTH, self.height), 3)
                rotated_top = pygame.transform.rotate(top_surface, self.fall_rotation)
                top_rect = rotated_top.get_rect(center=(self.x + PIPE_WIDTH // 2, self.height // 2 + self.fall_y_offset))
                screen.blit(rotated_top, top_rect)
                
                bottom_y = self.height + self.gap_size
                bottom_height = SCREEN_HEIGHT - bottom_y
                bottom_surface = pygame.Surface((PIPE_WIDTH, bottom_height), pygame.SRCALPHA)
                pygame.draw.rect(bottom_surface, GREEN, (0, 0, PIPE_WIDTH, bottom_height))
                pygame.draw.rect(bottom_surface, DARK_GREEN, (0, 0, PIPE_WIDTH, bottom_height), 3)
                rotated_bottom = pygame.transform.rotate(bottom_surface, self.fall_rotation)
                bottom_rect = rotated_bottom.get_rect(center=(self.x + PIPE_WIDTH // 2, bottom_y + bottom_height // 2 + self.fall_y_offset))
                screen.blit(rotated_bottom, bottom_rect)
        else:
            # Normal drawing
            if self.use_image:
                # Draw top pipe (flipped and stretched to fill height)
                top_pipe_img = pygame.transform.flip(self.pipe_image, False, True)
                top_pipe_scaled = pygame.transform.scale(top_pipe_img, (PIPE_WIDTH, self.height))
                screen.blit(top_pipe_scaled, (self.x, 0))
                
                # Draw bottom pipe (stretched to fill height)
                bottom_y = self.height + self.gap_size
                bottom_height = SCREEN_HEIGHT - bottom_y
                bottom_pipe_scaled = pygame.transform.scale(self.pipe_image, (PIPE_WIDTH, bottom_height))
                screen.blit(bottom_pipe_scaled, (self.x, bottom_y))
            else:
                # Draw top pipe (fallback)
                pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
                pygame.draw.rect(screen, DARK_GREEN, (self.x, 0, PIPE_WIDTH, self.height), 3)
                pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, self.height - 20, PIPE_WIDTH + 10, 20))
                
                # Draw bottom pipe (fallback)
                bottom_y = self.height + self.gap_size
                bottom_height = SCREEN_HEIGHT - bottom_y
                pygame.draw.rect(screen, GREEN, (self.x, bottom_y, PIPE_WIDTH, bottom_height))
                pygame.draw.rect(screen, DARK_GREEN, (self.x, bottom_y, PIPE_WIDTH, bottom_height), 3)
                pygame.draw.rect(screen, DARK_GREEN, (self.x - 5, bottom_y, PIPE_WIDTH + 10, 20))
        
    def is_off_screen(self):
        return self.x < -PIPE_WIDTH
        
    def start_falling(self):
        """Start the falling animation"""
        self.falling = True
    
    def collides_with(self, airplane):
        if self.falling:  # Don't check collision if already falling
            return False
        airplane_rect = airplane.get_rect()
        top_pipe = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        bottom_pipe = pygame.Rect(self.x, self.height + self.gap_size, PIPE_WIDTH, 
                                  SCREEN_HEIGHT - self.height - self.gap_size)
        return airplane_rect.colliderect(top_pipe) or airplane_rect.colliderect(bottom_pipe)


class Button:
    """Simple button class for UI"""
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, screen, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=10)
        
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
        
    def update_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)


class Slider:
    """Volume slider class"""
    def __init__(self, x, y, width, height, min_val=0, max_val=100, initial_val=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.dragging = False
        
        # Slider components
        self.track_rect = pygame.Rect(x, y + height // 2 - 2, width, 4)
        self.handle_radius = 10
        self.update_handle_pos()
        
    def update_handle_pos(self):
        """Update handle position based on value"""
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.x + int(ratio * self.width)
        self.handle_y = self.y + self.height // 2
        
    def draw(self, screen, font):
        # Draw track
        pygame.draw.rect(screen, GRAY, self.track_rect, border_radius=2)
        # Draw filled portion
        filled_width = int((self.value - self.min_val) / (self.max_val - self.min_val) * self.width)
        filled_rect = pygame.Rect(self.x, self.y + self.height // 2 - 2, filled_width, 4)
        pygame.draw.rect(screen, (46, 204, 113), filled_rect, border_radius=2)
        
        # Draw handle
        pygame.draw.circle(screen, WHITE, (self.handle_x, self.handle_y), self.handle_radius)
        pygame.draw.circle(screen, (46, 204, 113), (self.handle_x, self.handle_y), self.handle_radius - 2)
        
        # Draw value text
        value_text = font.render(f"{int(self.value)}%", True, WHITE)
        screen.blit(value_text, (self.x + self.width + 15, self.y))
        
    def handle_event(self, event, mouse_pos):
        """Handle mouse events for slider"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if clicked on handle
            dist = ((mouse_pos[0] - self.handle_x) ** 2 + (mouse_pos[1] - self.handle_y) ** 2) ** 0.5
            if dist <= self.handle_radius:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update value based on mouse position
            new_x = max(self.x, min(mouse_pos[0], self.x + self.width))
            ratio = (new_x - self.x) / self.width
            self.value = self.min_val + ratio * (self.max_val - self.min_val)
            self.update_handle_pos()
            return True
        return False


class Dropdown:
    """Dropdown menu for music selection"""
    def __init__(self, x, y, width, height, options, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.options = options
        self.selected_index = 0
        self.is_open = False
        self.font = font
        
        self.main_rect = pygame.Rect(x, y, width, height)
        self.arrow_size = 8
        
    def draw(self, screen):
        # Draw main box
        color = (52, 152, 219) if not self.is_open else (41, 128, 185)
        pygame.draw.rect(screen, color, self.main_rect, border_radius=5)
        pygame.draw.rect(screen, WHITE, self.main_rect, 2, border_radius=5)
        
        # Draw selected option
        if self.options:
            text = self.options[self.selected_index]
            # Truncate if too long
            if len(text) > 20:
                text = text[:17] + "..."
            text_surface = self.font.render(text, True, WHITE)
            screen.blit(text_surface, (self.x + 10, self.y + 10))
        
        # Draw arrow
        arrow_x = self.x + self.width - 20
        arrow_y = self.y + self.height // 2
        if self.is_open:
            # Up arrow
            points = [(arrow_x, arrow_y + 3), (arrow_x - self.arrow_size, arrow_y - 3), 
                     (arrow_x + self.arrow_size, arrow_y - 3)]
        else:
            # Down arrow
            points = [(arrow_x, arrow_y + 3), (arrow_x - self.arrow_size, arrow_y - 3), 
                     (arrow_x + self.arrow_size, arrow_y - 3)]
        pygame.draw.polygon(screen, WHITE, points)
        
        # Draw dropdown options if open
        if self.is_open and self.options:
            for i, option in enumerate(self.options):
                option_y = self.y + self.height + i * self.height
                option_rect = pygame.Rect(self.x, option_y, self.width, self.height)
                
                # Highlight selected
                if i == self.selected_index:
                    pygame.draw.rect(screen, (41, 128, 185), option_rect)
                else:
                    pygame.draw.rect(screen, (52, 152, 219), option_rect)
                pygame.draw.rect(screen, WHITE, option_rect, 2)
                
                # Draw option text
                text = option
                if len(text) > 20:
                    text = text[:17] + "..."
                text_surface = self.font.render(text, True, WHITE)
                screen.blit(text_surface, (self.x + 10, option_y + 10))
    
    def handle_click(self, pos):
        """Handle click events"""
        if self.main_rect.collidepoint(pos):
            self.is_open = not self.is_open
            return True
        
        if self.is_open and self.options:
            for i in range(len(self.options)):
                option_y = self.y + self.height + i * self.height
                option_rect = pygame.Rect(self.x, option_y, self.width, self.height)
                if option_rect.collidepoint(pos):
                    self.selected_index = i
                    self.is_open = False
                    return True
        return False
    
    def get_selected(self):
        """Get currently selected option"""
        if self.options and 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index]
        return None


class DummySound:
    """Dummy sound class for when numpy is not available"""
    def play(self):
        pass


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Osama")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 72)
        
        # Game state
        self.state = HOME
        self.music_enabled = True
        self.music_loaded = False
        self.music_volume = 30  # 0-100 (30% volume)
        self.available_music = []  # List of available music files
        self.current_music_index = 0
        
        # High score
        self.high_score = self.load_high_score()
        
        # Background transition
        self.game_time = 0  # Track time for day/night cycle
        self.cycle_duration = 60000  # Full day/night cycle in milliseconds (60 seconds)
        
        # Modding parameters (editable)
        self.mod_gravity = GRAVITY
        self.mod_flap_strength = abs(FLAP_STRENGTH)
        self.mod_initial_gap = INITIAL_PIPE_GAP
        self.mod_min_gap = MIN_PIPE_GAP
        self.mod_pipe_width = PIPE_WIDTH
        self.mod_initial_velocity = INITIAL_PIPE_VELOCITY
        self.mod_max_velocity = MAX_PIPE_VELOCITY
        self.mod_initial_spawn = INITIAL_SPAWN_TIME
        self.mod_min_spawn = MIN_SPAWN_TIME
        
        # Tooltip  
        self.tooltip_text = ""
        self.tooltip_visible = False
        
        # Initialize sound mixer
        pygame.mixer.init()
        self.load_sounds()
        self.load_music()
        
        # Load images
        self.load_images()
        
        # Create buttons
        self.create_buttons()
        
        self.reset()
        
    def create_buttons(self):
        """Create UI buttons"""
        button_width = 240
        button_height = 60
        center_x = SCREEN_WIDTH // 2 - button_width // 2
        
        # Home screen buttons
        self.start_button = Button(
            center_x, 420, button_width, button_height,
            "START", (46, 204, 113), (39, 174, 96)
        )
        self.settings_button = Button(
            center_x, 510, button_width, button_height,
            "SETTINGS", (52, 152, 219), (41, 128, 185)
        )
        
        # Settings screen buttons
        self.music_button = Button(
            center_x, 260, button_width, button_height,
            "Music: ON", (241, 196, 15), (243, 156, 18)
        )
        
        # Volume slider
        self.volume_slider = Slider(
            100, 420, 400, 40, 0, 100, self.music_volume
        )
        
        # Modding button
        self.modding_button = Button(
            center_x, 560, button_width, button_height,
            "MODDING", (155, 89, 182), (142, 68, 173)
        )
        
        self.back_button = Button(
            center_x, 650, button_width, button_height,
            "BACK", (231, 76, 60), (192, 57, 43)
        )
        
        # Modding screen sliders
        slider_x = 100
        slider_width = 400
        self.gravity_slider = Slider(slider_x, 240, slider_width, 35, 0.1, 2.0, self.mod_gravity)
        self.flap_slider = Slider(slider_x, 310, slider_width, 35, 5, 15, self.mod_flap_strength)
        self.initial_gap_slider = Slider(slider_x, 380, slider_width, 35, 200, 350, self.mod_initial_gap)
        self.min_gap_slider = Slider(slider_x, 450, slider_width, 35, 180, 280, self.mod_min_gap)
        self.pipe_width_slider = Slider(slider_x, 520, slider_width, 35, 30, 100, self.mod_pipe_width)
        self.initial_vel_slider = Slider(slider_x, 590, slider_width, 35, 1, 5, self.mod_initial_velocity)
        self.max_vel_slider = Slider(slider_x, 660, slider_width, 35, 5, 12, self.mod_max_velocity)
        
        # Back button for modding
        self.modding_back_button = Button(
            center_x, 720, button_width, button_height,
            "BACK", (231, 76, 60), (192, 57, 43)
        )
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open('highscore.txt', 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open('highscore.txt', 'w') as f:
                f.write(str(self.high_score))
        except Exception as e:
            print(f"[ERROR] Could not save high score: {e}")
            
    def load_music(self):
        """Load all available background music files"""
        import os
        try:
            # Scan directory for music files
            music_extensions = ['.mp3', '.ogg', '.wav']
            for file in os.listdir('.'):
                if any(file.lower().endswith(ext) for ext in music_extensions):
                    self.available_music.append(file)
            
            if self.available_music:
                # Sort alphabetically
                self.available_music.sort()
                # Load first music file
                self.load_music_track(0)
                print(f"[OK] Found {len(self.available_music)} music file(s)")
                for music in self.available_music:
                    print(f"  - {music}")
            else:
                print("[WARNING] No background music file found.")
                print("  Supported formats: .mp3, .ogg, .wav")
                print("  Place music files in the game directory to enable background music.")
        except Exception as e:
            print(f"[ERROR] Could not load background music: {e}")
            self.music_loaded = False
            
    def load_music_track(self, index):
        """Load a specific music track by index"""
        if 0 <= index < len(self.available_music):
            try:
                pygame.mixer.music.load(self.available_music[index])
                self.current_music_index = index
                self.music_loaded = True
                # Set volume
                pygame.mixer.music.set_volume(self.music_volume / 100)
                # Play if enabled
                if self.music_enabled:
                    pygame.mixer.music.play(-1)  # -1 means loop forever
                return True
            except Exception as e:
                print(f"[ERROR] Could not load {self.available_music[index]}: {e}")
                return False
        return False
            
    def load_images(self):
        """Load airplane and pipe images"""
        self.airplane_image = None
        self.pipe_image = None
        
        try:
            # Try to load airplane image (try both airplane.png and plane.png)
            try:
                img = pygame.image.load('airplane.png').convert_alpha()
            except (pygame.error, FileNotFoundError):
                img = pygame.image.load('plane.png').convert_alpha()
            # Scale to appropriate size (50x30)
            self.airplane_image = pygame.transform.scale(img, (50, 30))
            print("[OK] Airplane image loaded successfully")
        except (pygame.error, FileNotFoundError):
            print("[WARNING] airplane.png or plane.png not found. Using drawn graphics.")
            print("  Place 'airplane.png' or 'plane.png' in the game directory to use custom image.")
        
        try:
            # Try to load pipe image
            img = pygame.image.load('pipe.png').convert_alpha()
            # Scale width to PIPE_WIDTH, keep aspect ratio for height
            aspect_ratio = img.get_height() / img.get_width()
            pipe_height = int(PIPE_WIDTH * aspect_ratio)
            self.pipe_image = pygame.transform.scale(img, (PIPE_WIDTH, pipe_height))
            print("[OK] Pipe image loaded successfully")
        except (pygame.error, FileNotFoundError):
            print("[WARNING] pipe.png not found. Using drawn graphics.")
            print("  Place 'pipe.png' in the game directory to use custom image.")
        
    def load_sounds(self):
        """Create simple sound effects using pygame.mixer"""
        # Try to load custom crash sound first (check both with and without space)
        crash_sound_loaded = False
        for name in ['crash sound', 'crash']:
            for ext in ['.mp3', '.wav', '.ogg']:
                try:
                    self.crash_sound = pygame.mixer.Sound(f'{name}{ext}')
                    self.crash_sound.set_volume(0.3)  # Set low volume (30%)
                    print(f"[OK] Custom crash sound loaded: {name}{ext}")
                    crash_sound_loaded = True
                    break
                except (pygame.error, FileNotFoundError):
                    continue
            if crash_sound_loaded:
                break
        
        try:
            # Try to create sounds with numpy
            import numpy as np
            self.flap_sound = self.create_beep_numpy(frequency=440, duration=100)
            self.score_sound = self.create_beep_numpy(frequency=660, duration=150)
            
            # Use dummy sound if custom crash sound wasn't loaded (no beep fallback)
            if not crash_sound_loaded:
                self.crash_sound = DummySound()
                print("[WARNING] Crash sound not found. Add 'crash sound.mp3' or 'crash.mp3' for crash sound.")
            
            self.sounds_enabled = True
        except (ImportError, AttributeError):
            # Fallback: create dummy sound objects
            print("[INFO] NumPy not available. Running without sound effects.")
            print("[INFO] To enable sounds, install numpy: pip install numpy")
            self.sounds_enabled = False
            self.flap_sound = DummySound()
            self.score_sound = DummySound()
            if not crash_sound_loaded:
                self.crash_sound = DummySound()
        
    def create_beep_numpy(self, frequency=440, duration=100):
        """Generate a simple beep sound using numpy"""
        import numpy as np
        sample_rate = 22050
        n_samples = int(round(duration * sample_rate / 1000))
        
        # Generate sine wave
        buf = np.sin(2 * np.pi * frequency * np.linspace(0, duration / 1000, n_samples))
        # Apply envelope to avoid clicks
        envelope = np.linspace(1, 0, n_samples)
        buf = buf * envelope
        # Scale to 16-bit range
        buf = (buf * 32767).astype(np.int16)
        
        # Convert to stereo
        stereo = np.column_stack((buf, buf))
        sound = pygame.sndarray.make_sound(stereo)
        sound.set_volume(0.3)
        return sound
        
    def reset(self):
        self.airplane = Airplane(self.airplane_image)
        self.pipes = []
        self.particles = []
        self.score = 0
        self.game_over = False
        self.game_started = False
        self.last_pipe_time = 0
        self.current_velocity = INITIAL_PIPE_VELOCITY
        self.current_gap = INITIAL_PIPE_GAP
        self.game_over_time = 0  # Track when game ended
        self.restart_cooldown = 3000  # 3 seconds cooldown in milliseconds
        
        # Update high score if needed
        if hasattr(self, 'high_score') and self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        self.current_spawn_time = INITIAL_SPAWN_TIME
        
        # Reset game time for background transition
        self.game_time = 0
        
    def get_pipe_velocity(self):
        """Calculate pipe velocity based on score for progressive difficulty"""
        # Progressive speed levels
        # Level 1-2 (0-5): Slow - 2.0 speed
        # Level 3 (6-9): Medium - 3.5 speed
        # Level 4 (10-14): Fast - 4.5 speed
        # Level 5 (15-19): Very Fast - 5.5 speed
        # Level 6-7 (20-29): Super Fast - 6.5 speed
        # Level 8+ (30+): Maximum - 7.0-8.0 speed
        
        if self.score < 6:
            return 2.0  # Level 1-2
        elif self.score < 10:
            return 3.5  # Level 3
        elif self.score < 15:
            return 4.5  # Level 4
        elif self.score < 20:
            return 5.5  # Level 5
        elif self.score < 30:
            return 6.5  # Level 6-7
        else:
            return min(7.0 + (self.score - 30) * 0.05, MAX_PIPE_VELOCITY)  # Level 8+ (gradually increases)
        
    def get_pipe_gap(self):
        """Calculate pipe gap based on score - gets smaller as score increases"""
        # Progressive difficulty levels based on score
        # Level 1-2 (0-5): Very Easy - 320px gap
        # Level 3 (6-9): Easy - 300px gap
        # Level 4 (10-14): Medium - 280px gap
        # Level 5 (15-19): Hard - 260px gap
        # Level 6-7 (20-29): Very Hard - 240px gap
        # Level 8+ (30+): Expert - 220-200px gap
        
        if self.score < 6:
            return 320  # Level 1-2: Very Easy
        elif self.score < 10:
            return 300  # Level 3: Easy
        elif self.score < 15:
            return 280  # Level 4: Medium
        elif self.score < 20:
            return 260  # Level 5: Hard
        elif self.score < 30:
            return 240  # Level 6-7: Very Hard
        else:
            return max(230 - (self.score - 30) // 5 * 5, MIN_PIPE_GAP)  # Level 8+: Expert (gradually harder)
        
    def get_spawn_time(self):
        """Calculate spawn time based on score - pipes spawn faster at higher scores"""
        # Progressive spawn rate levels
        # Level 1-2 (0-5): Slow - 1800ms
        # Level 3 (6-9): Medium - 1650ms
        # Level 4 (10-14): Fast - 1500ms
        # Level 5 (15-19): Very Fast - 1350ms
        # Level 6-7 (20-29): Super Fast - 1200ms
        # Level 8+ (30+): Maximum - 1100-1000ms
        
        if self.score < 6:
            return 1800  # Level 1-2
        elif self.score < 10:
            return 1650  # Level 3
        elif self.score < 15:
            return 1500  # Level 4
        elif self.score < 20:
            return 1350  # Level 5
        elif self.score < 30:
            return 1200  # Level 6-7
        else:
            return max(1150 - (self.score - 30) // 5 * 20, MIN_SPAWN_TIME)  # Level 8+ (gradually faster)
        
    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        if self.state == HOME:
            self.start_button.update_hover(mouse_pos)
            self.settings_button.update_hover(mouse_pos)
        elif self.state == SETTINGS:
            self.music_button.update_hover(mouse_pos)
            self.modding_button.update_hover(mouse_pos)
            self.back_button.update_hover(mouse_pos)
        elif self.state == MODDING:
            self.modding_back_button.update_hover(mouse_pos)
            # Check hover for tooltips
            self.update_tooltips(mouse_pos)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.MOUSEMOTION:
                # Handle slider dragging
                if self.state == SETTINGS:
                    if self.volume_slider.handle_event(event, mouse_pos):
                        # Update volume
                        self.music_volume = self.volume_slider.value
                        if self.music_loaded:
                            pygame.mixer.music.set_volume(self.music_volume / 100)
                elif self.state == MODDING:
                    # Handle modding sliders
                    if self.gravity_slider.handle_event(event, mouse_pos):
                        self.mod_gravity = round(self.gravity_slider.value, 2)
                    elif self.flap_slider.handle_event(event, mouse_pos):
                        self.mod_flap_strength = round(self.flap_slider.value, 1)
                    elif self.initial_gap_slider.handle_event(event, mouse_pos):
                        self.mod_initial_gap = int(self.initial_gap_slider.value)
                    elif self.min_gap_slider.handle_event(event, mouse_pos):
                        self.mod_min_gap = int(self.min_gap_slider.value)
                    elif self.pipe_width_slider.handle_event(event, mouse_pos):
                        self.mod_pipe_width = int(self.pipe_width_slider.value)
                    elif self.initial_vel_slider.handle_event(event, mouse_pos):
                        self.mod_initial_velocity = round(self.initial_vel_slider.value, 1)
                    elif self.max_vel_slider.handle_event(event, mouse_pos):
                        self.mod_max_velocity = round(self.max_vel_slider.value, 1)
                            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle slider click
                if self.state == SETTINGS:
                    self.volume_slider.handle_event(event, mouse_pos)
                elif self.state == MODDING:
                    self.gravity_slider.handle_event(event, mouse_pos)
                    self.flap_slider.handle_event(event, mouse_pos)
                    self.initial_gap_slider.handle_event(event, mouse_pos)
                    self.min_gap_slider.handle_event(event, mouse_pos)
                    self.pipe_width_slider.handle_event(event, mouse_pos)
                    self.initial_vel_slider.handle_event(event, mouse_pos)
                    self.max_vel_slider.handle_event(event, mouse_pos)
                if self.state == HOME:
                    if self.start_button.is_clicked(mouse_pos):
                        self.state = PLAYING
                        self.reset()
                    elif self.settings_button.is_clicked(mouse_pos):
                        self.state = SETTINGS
                        
                elif self.state == SETTINGS:
                    if self.music_button.is_clicked(mouse_pos):
                        self.music_enabled = not self.music_enabled
                        self.music_button.text = f"Music: {'ON' if self.music_enabled else 'OFF'}"
                        # Control music playback
                        if self.music_loaded:
                            if self.music_enabled:
                                pygame.mixer.music.unpause()
                                if not pygame.mixer.music.get_busy():
                                    pygame.mixer.music.play(-1)
                            else:
                                pygame.mixer.music.pause()
                    elif self.modding_button.is_clicked(mouse_pos):
                        self.state = MODDING
                    elif self.back_button.is_clicked(mouse_pos):
                        self.state = HOME
                    elif self.music_dropdown.handle_click(mouse_pos):
                        # Music track changed
                        new_index = self.music_dropdown.selected_index
                        if new_index != self.current_music_index:
                            self.load_music_track(new_index)
                            
                elif self.state == MODDING:
                    if self.modding_back_button.is_clicked(mouse_pos):
                        self.state = SETTINGS
                        self.apply_mods()
                        
                elif self.state == PLAYING:
                    if not self.game_over:
                        self.airplane.flap()
                        self.game_started = True
                        self.flap_sound.play()
                    else:
                        # Check if cooldown has passed
                        if pygame.time.get_ticks() - self.game_over_time >= self.restart_cooldown:
                            self.state = HOME
                        
            if event.type == pygame.MOUSEBUTTONUP:
                # Handle slider release
                if self.state == SETTINGS:
                    self.volume_slider.handle_event(event, mouse_pos)
                elif self.state == MODDING:
                    self.gravity_slider.handle_event(event, mouse_pos)
                    self.flap_slider.handle_event(event, mouse_pos)
                    self.initial_gap_slider.handle_event(event, mouse_pos)
                    self.min_gap_slider.handle_event(event, mouse_pos)
                    self.pipe_width_slider.handle_event(event, mouse_pos)
                    self.initial_vel_slider.handle_event(event, mouse_pos)
                    self.max_vel_slider.handle_event(event, mouse_pos)
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.state == PLAYING:
                        if not self.game_over:
                            self.airplane.flap()
                            self.game_started = True
                            self.flap_sound.play()
                        else:
                            # Check if cooldown has passed
                            if pygame.time.get_ticks() - self.game_over_time >= self.restart_cooldown:
                                self.state = HOME
                elif event.key == pygame.K_ESCAPE:
                    if self.state == SETTINGS:
                        self.state = HOME
                    elif self.state == MODDING:
                        self.state = SETTINGS
                        self.apply_mods()
                    elif self.state == PLAYING and self.game_over:
                        self.state = HOME
                    else:
                        return False
        return True
        
    def get_background_color(self):
        """Calculate current background color based on game time (day/night cycle)"""
        # Calculate position in cycle (0.0 to 1.0)
        cycle_pos = (self.game_time % self.cycle_duration) / self.cycle_duration
        
        # Define 4 phases: Day -> Sunset -> Night -> Dawn -> Day
        # Each phase is 25% of the cycle
        if cycle_pos < 0.25:  # Day (0% - 25%)
            # Transition from day to sunset
            t = cycle_pos / 0.25
            return self.lerp_color(DAY_SKY, SUNSET_SKY, t)
        elif cycle_pos < 0.5:  # Sunset to Night (25% - 50%)
            # Transition from sunset to night
            t = (cycle_pos - 0.25) / 0.25
            return self.lerp_color(SUNSET_SKY, NIGHT_SKY, t)
        elif cycle_pos < 0.75:  # Night (50% - 75%)
            # Transition from night to dawn
            t = (cycle_pos - 0.5) / 0.25
            return self.lerp_color(NIGHT_SKY, DAWN_SKY, t)
        else:  # Dawn to Day (75% - 100%)
            # Transition from dawn to day
            t = (cycle_pos - 0.75) / 0.25
            return self.lerp_color(DAWN_SKY, DAY_SKY, t)
    
    def lerp_color(self, color1, color2, t):
        """Linear interpolation between two colors"""
        r = int(color1[0] + (color2[0] - color1[0]) * t)
        g = int(color1[1] + (color2[1] - color1[1]) * t)
        b = int(color1[2] + (color2[2] - color1[2]) * t)
        return (r, g, b)
    
    def update(self):
        # Only update game if in PLAYING state
        if self.state != PLAYING:
            return
            
        # Update particles even when game is over
        for particle in self.particles:
            particle.update()
        self.particles = [p for p in self.particles if p.is_alive()]
        
        # Update pipes even when game is over (for falling animation)
        for pipe in self.pipes:
            pipe.update()
        
        if not self.game_started or self.game_over:
            return
        
        # Update game time for background transition
        self.game_time += self.clock.get_time()
            
        self.airplane.update()
        
        # Check if airplane hits ground or ceiling
        if self.airplane.is_off_screen():
            if not self.game_over:  # Only trigger once
                self.game_over = True
                self.game_over_time = pygame.time.get_ticks()
                self.crash_sound.play()
                self.create_explosion(self.airplane.x, self.airplane.y)
                # Update high score
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
        
        # Check collisions and scoring for each pipe
        for pipe in self.pipes:
            # Check collision
            if pipe.collides_with(self.airplane):
                if not self.game_over:  # Only trigger once
                    self.game_over = True
                    self.game_over_time = pygame.time.get_ticks()
                    self.crash_sound.play()
                    # Start pipe falling animation
                    pipe.start_falling()
                    # Create explosion at collision point
                    self.create_explosion(self.airplane.x, self.airplane.y)
                    # Update high score
                    if self.score > self.high_score:
                        self.high_score = self.score
                        self.save_high_score()
                
            # Check if passed pipe
            if not pipe.passed and pipe.x + PIPE_WIDTH < self.airplane.x:
                pipe.passed = True
                self.score += 1
                self.score_sound.play()
                
        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
        
        # Spawn new pipes with current difficulty
        current_time = pygame.time.get_ticks()
        self.current_spawn_time = self.get_spawn_time()
        if current_time - self.last_pipe_time > self.current_spawn_time:
            self.current_velocity = self.get_pipe_velocity()
            self.current_gap = self.get_pipe_gap()
            self.pipes.append(Pipe(SCREEN_WIDTH, self.current_velocity, self.current_gap, self.pipe_image))
            self.last_pipe_time = current_time
            
    def create_explosion(self, x, y):
        """Create explosion particles at the given position"""
        for _ in range(30):  # Create 30 particles
            self.particles.append(Particle(x, y))
            
    def apply_mods(self):
        """Apply modding parameters to game constants"""
        global GRAVITY, FLAP_STRENGTH, INITIAL_PIPE_GAP, MIN_PIPE_GAP, PIPE_WIDTH
        global INITIAL_PIPE_VELOCITY, MAX_PIPE_VELOCITY, INITIAL_SPAWN_TIME, MIN_SPAWN_TIME
        
        GRAVITY = self.mod_gravity
        FLAP_STRENGTH = -self.mod_flap_strength
        INITIAL_PIPE_GAP = self.mod_initial_gap
        MIN_PIPE_GAP = self.mod_min_gap
        PIPE_WIDTH = self.mod_pipe_width
        INITIAL_PIPE_VELOCITY = self.mod_initial_velocity
        MAX_PIPE_VELOCITY = self.mod_max_velocity
        INITIAL_SPAWN_TIME = self.mod_initial_spawn
        MIN_SPAWN_TIME = self.mod_min_spawn
        
    def update_tooltips(self, mouse_pos):
        """Update tooltip text based on mouse position"""
        self.tooltip_visible = False
        
        # Check each slider area
        if 100 <= mouse_pos[0] <= 500:
            if 230 <= mouse_pos[1] <= 265:
                self.tooltip_text = "Gravity: How fast the plane falls"
                self.tooltip_visible = True
            elif 300 <= mouse_pos[1] <= 335:
                self.tooltip_text = "Flap Strength: How high the plane jumps"
                self.tooltip_visible = True
            elif 370 <= mouse_pos[1] <= 405:
                self.tooltip_text = "Initial Gap: Starting gap size between pipes"
                self.tooltip_visible = True
            elif 440 <= mouse_pos[1] <= 475:
                self.tooltip_text = "Min Gap: Smallest gap at high scores"
                self.tooltip_visible = True
            elif 510 <= mouse_pos[1] <= 545:
                self.tooltip_text = "Pipe Width: Width of obstacles"
                self.tooltip_visible = True
            elif 580 <= mouse_pos[1] <= 615:
                self.tooltip_text = "Initial Speed: Starting pipe speed"
                self.tooltip_visible = True
            elif 650 <= mouse_pos[1] <= 685:
                self.tooltip_text = "Max Speed: Maximum pipe speed"
                self.tooltip_visible = True
            
    def draw(self):
        # Draw sky with dynamic color based on game state
        if self.state == PLAYING:
            # Use dynamic day/night cycle during gameplay
            bg_color = self.get_background_color()
            self.screen.fill(bg_color)
        else:
            # Use default sky blue for menus
            self.screen.fill(SKY_BLUE)
        
        if self.state == HOME:
            self.draw_home_screen()
        elif self.state == SETTINGS:
            self.draw_settings_screen()
        elif self.state == MODDING:
            self.draw_modding_screen()
        elif self.state == PLAYING:
            self.draw_game_screen()
            
        pygame.display.flip()
        
    def draw_home_screen(self):
        """Draw the home screen with title and buttons"""
        # Draw title
        title_text = self.title_font.render("FLAPPY", True, WHITE)
        title_text2 = self.title_font.render("OSAMA", True, YELLOW)
        title_outline = self.title_font.render("FLAPPY", True, BLACK)
        title_outline2 = self.title_font.render("OSAMA", True, BLACK)
        
        self.screen.blit(title_outline, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 3, 153))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))
        self.screen.blit(title_outline2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2 + 3, 233))
        self.screen.blit(title_text2, (SCREEN_WIDTH // 2 - title_text2.get_width() // 2, 230))
        
        # Draw airplane preview
        if self.airplane_image:
            preview_img = pygame.transform.scale(self.airplane_image, (140, 84))
            self.screen.blit(preview_img, (SCREEN_WIDTH // 2 - 70, 320))
        
        # Draw high score
        highscore_label = self.small_font.render("HIGH SCORE", True, YELLOW)
        highscore_value = self.font.render(str(self.high_score), True, WHITE)
        highscore_outline = self.font.render(str(self.high_score), True, BLACK)
        
        self.screen.blit(highscore_label, (SCREEN_WIDTH // 2 - highscore_label.get_width() // 2, 600))
        self.screen.blit(highscore_outline, (SCREEN_WIDTH // 2 - highscore_value.get_width() // 2 + 2, 642))
        self.screen.blit(highscore_value, (SCREEN_WIDTH // 2 - highscore_value.get_width() // 2, 640))
        
        # Draw buttons
        self.start_button.draw(self.screen, self.small_font)
        self.settings_button.draw(self.screen, self.small_font)
        
        # Draw footer
        footer_text = self.small_font.render("Press ESC to quit", True, WHITE)
        self.screen.blit(footer_text, (SCREEN_WIDTH // 2 - footer_text.get_width() // 2, 720))
        
    def draw_settings_screen(self):
        """Draw the settings screen"""
        # Draw decorative background panels
        panel_color = (44, 62, 80)
        pygame.draw.rect(self.screen, panel_color, (40, 230, 520, 110), border_radius=15)
        pygame.draw.rect(self.screen, panel_color, (40, 360, 520, 130), border_radius=15)
        pygame.draw.rect(self.screen, panel_color, (40, 510, 520, 130), border_radius=15)
        
        # Draw title with icon
        title_text = self.font.render("SETTINGS", True, WHITE)
        title_outline = self.font.render("SETTINGS", True, BLACK)
        self.screen.blit(title_outline, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 2, 72))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 70))
        
        # Draw gear icon (simple)
        gear_center = (SCREEN_WIDTH // 2, 160)
        pygame.draw.circle(self.screen, (189, 195, 199), gear_center, 30, 4)
        pygame.draw.circle(self.screen, (189, 195, 199), gear_center, 15)
        
        # Section 1: Music Toggle
        section1_label = self.small_font.render("Music Control", True, (189, 195, 199))
        self.screen.blit(section1_label, (60, 240))
        
        self.music_button.draw(self.screen, self.small_font)
        
        # Section 2: Volume Control
        section2_label = self.small_font.render("Volume Control", True, (189, 195, 199))
        self.screen.blit(section2_label, (60, 370))
        
        volume_label = self.small_font.render("Volume:", True, WHITE)
        self.screen.blit(volume_label, (100, 425))
        
        self.volume_slider.draw(self.screen, self.small_font)
        
        # Draw modding button
        self.modding_button.draw(self.screen, self.small_font)
        
        # Draw back button
        self.back_button.draw(self.screen, self.small_font)
        
        # Draw music status at bottom
        if self.music_loaded:
            status_text = self.small_font.render(f"{len(self.available_music)} track(s) available", True, (46, 204, 113))
        else:
            status_text = self.small_font.render("No music files found", True, GRAY)
        self.screen.blit(status_text, (SCREEN_WIDTH // 2 - status_text.get_width() // 2, 720))
        
    def draw_modding_screen(self):
        """Draw the modding/customization screen"""
        # Draw title
        title_text = self.font.render("MODDING", True, (155, 89, 182))
        title_outline = self.font.render("MODDING", True, BLACK)
        self.screen.blit(title_outline, (SCREEN_WIDTH // 2 - title_text.get_width() // 2 + 2, 52))
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        
        subtitle = self.small_font.render("Customize Game Parameters", True, WHITE)
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 100))
        
        # Draw parameter labels and sliders
        param_font = pygame.font.Font(None, 28)
        
        params = [
            ("Gravity:", self.gravity_slider, f"{self.mod_gravity:.2f}", 240),
            ("Flap Power:", self.flap_slider, f"{self.mod_flap_strength:.1f}", 310),
            ("Initial Gap:", self.initial_gap_slider, f"{self.mod_initial_gap}", 380),
            ("Min Gap:", self.min_gap_slider, f"{self.mod_min_gap}", 450),
            ("Pipe Width:", self.pipe_width_slider, f"{self.mod_pipe_width}", 520),
            ("Init Speed:", self.initial_vel_slider, f"{self.mod_initial_velocity:.1f}", 590),
            ("Max Speed:", self.max_vel_slider, f"{self.mod_max_velocity:.1f}", 660),
        ]
        
        for label, slider, value, y_pos in params:
            # Draw label
            label_text = param_font.render(label, True, WHITE)
            self.screen.blit(label_text, (100, y_pos - 25))
            
            # Draw slider
            slider.draw(self.screen, param_font)
            
            # Draw value
            value_text = param_font.render(value, True, (46, 204, 113))
            self.screen.blit(value_text, (520, y_pos - 25))
        
        # Draw tooltip if visible
        if self.tooltip_visible:
            tooltip_bg = pygame.Rect(50, 140, 500, 70)
            pygame.draw.rect(self.screen, (44, 62, 80), tooltip_bg, border_radius=10)
            pygame.draw.rect(self.screen, (155, 89, 182), tooltip_bg, 3, border_radius=10)
            
            tooltip_surface = self.small_font.render(self.tooltip_text, True, WHITE)
            self.screen.blit(tooltip_surface, (70, 165))
        
        # Draw back button
        self.modding_back_button.draw(self.screen, self.small_font)
        
    def draw_game_screen(self):
        
        # Calculate cycle position for celestial objects
        cycle_pos = (self.game_time % self.cycle_duration) / self.cycle_duration
        
        # Draw moon and stars during night (fade in during sunset, fade out during dawn)
        if 0.25 <= cycle_pos <= 0.75:  # Sunset to Dawn
            # Calculate opacity (0-255)
            if cycle_pos < 0.375:  # Fading in during sunset
                alpha = int(((cycle_pos - 0.25) / 0.125) * 255)
            elif cycle_pos > 0.625:  # Fading out during dawn
                alpha = int(((0.75 - cycle_pos) / 0.125) * 255)
            else:  # Full night
                alpha = 255
            
            # Draw stars
            star_positions = [
                (100, 80), (180, 120), (280, 90), (380, 110), (480, 70),
                (150, 180), (320, 160), (450, 200), (220, 240), (520, 150),
                (80, 300), (200, 350), (350, 320), (500, 380), (140, 420),
                (420, 280), (560, 240), (90, 500), (300, 480), (470, 520)
            ]
            
            for star_x, star_y in star_positions:
                # Twinkling effect
                twinkle = abs((self.game_time // 300 + star_x) % 100 - 50) / 50
                star_alpha = int(alpha * (0.5 + 0.5 * twinkle))
                
                # Create star surface with alpha
                star_surface = pygame.Surface((6, 6), pygame.SRCALPHA)
                star_color = (255, 255, 255, star_alpha)
                
                # Draw star shape (cross pattern)
                pygame.draw.circle(star_surface, star_color, (3, 3), 2)
                pygame.draw.line(star_surface, star_color, (3, 0), (3, 6), 1)
                pygame.draw.line(star_surface, star_color, (0, 3), (6, 3), 1)
                
                self.screen.blit(star_surface, (star_x, star_y))
            
            # Draw moon
            moon_x = 480
            moon_y = 120
            moon_radius = 35
            
            # Create moon surface with alpha
            moon_surface = pygame.Surface((moon_radius * 2 + 10, moon_radius * 2 + 10), pygame.SRCALPHA)
            moon_color = (240, 240, 200, alpha)  # Pale yellow
            
            # Draw moon circle
            pygame.draw.circle(moon_surface, moon_color, (moon_radius + 5, moon_radius + 5), moon_radius)
            
            # Draw craters for detail
            crater_color = (200, 200, 180, alpha // 2)
            pygame.draw.circle(moon_surface, crater_color, (moon_radius - 5, moon_radius), 6)
            pygame.draw.circle(moon_surface, crater_color, (moon_radius + 10, moon_radius + 8), 4)
            pygame.draw.circle(moon_surface, crater_color, (moon_radius + 5, moon_radius - 8), 5)
            
            self.screen.blit(moon_surface, (moon_x - moon_radius - 5, moon_y - moon_radius - 5))
        
        # Draw clouds (visible during day, less visible at night)
        cloud_alpha = 255
        if 0.25 <= cycle_pos <= 0.75:  # Night time - make clouds darker/less visible
            cloud_alpha = 100
        
        for i in range(3):
            x = (i * 200 + pygame.time.get_ticks() // 50) % (SCREEN_WIDTH + 100)
            if cloud_alpha < 255:
                # Draw darker clouds at night
                cloud_surface = pygame.Surface((150, 50), pygame.SRCALPHA)
                cloud_color = (200, 200, 200, cloud_alpha)
                pygame.draw.ellipse(cloud_surface, cloud_color, (0, 10, 80, 40))
                pygame.draw.ellipse(cloud_surface, cloud_color, (20, 0, 60, 40))
                pygame.draw.ellipse(cloud_surface, cloud_color, (40, 10, 70, 35))
                self.screen.blit(cloud_surface, (x, 50 + i * 80))
            else:
                # Draw normal white clouds during day
                pygame.draw.ellipse(self.screen, WHITE, (x, 50 + i * 80, 80, 40))
                pygame.draw.ellipse(self.screen, WHITE, (x + 20, 40 + i * 80, 60, 40))
                pygame.draw.ellipse(self.screen, WHITE, (x + 40, 50 + i * 80, 70, 35))
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
            
        # Draw airplane (only if not exploded or still showing particles)
        if not self.game_over or len(self.particles) == 0:
            self.airplane.draw(self.screen)
        
        # Draw explosion particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(str(self.score), True, WHITE)
        score_outline = self.font.render(str(self.score), True, BLACK)
        self.screen.blit(score_outline, (SCREEN_WIDTH // 2 - score_text.get_width() // 2 + 2, 52))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 50))
        
        # Draw difficulty indicator with level
        if self.game_started and self.score >= 0:
            # Determine current level with more detailed progression
            if self.score < 3:
                level = 1
                level_name = "Beginner"
            elif self.score < 6:
                level = 2
                level_name = "Novice"
            elif self.score < 10:
                level = 3
                level_name = "Apprentice"
            elif self.score < 15:
                level = 4
                level_name = "Skilled"
            elif self.score < 20:
                level = 5
                level_name = "Advanced"
            elif self.score < 25:
                level = 6
                level_name = "Expert"
            elif self.score < 30:
                level = 7
                level_name = "Master"
            elif self.score < 35:
                level = 8
                level_name = "Elite"
            elif self.score < 40:
                level = 9
                level_name = "Champion"
            elif self.score < 50:
                level = 10
                level_name = "Legend"
            elif self.score < 60:
                level = 11
                level_name = "Mythic"
            elif self.score < 75:
                level = 12
                level_name = "Godlike"
            elif self.score < 100:
                level = 13
                level_name = "Immortal"
            else:
                level = 14 + (self.score - 100) // 20
                level_name = "Transcendent"
            
            difficulty_text = self.small_font.render(f"Lv.{level}: {level_name}", True, WHITE)
            difficulty_outline = self.small_font.render(f"Lv.{level}: {level_name}", True, BLACK)
            self.screen.blit(difficulty_outline, (12, 12))
            self.screen.blit(difficulty_text, (10, 10))
        
        # Draw instructions or game over
        if not self.game_started:
            instruction_text = self.small_font.render("Press SPACE or Click to Fly", True, WHITE)
            instruction_outline = self.small_font.render("Press SPACE or Click to Fly", True, BLACK)
            self.screen.blit(instruction_outline, 
                           (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2 + 2, 
                            SCREEN_HEIGHT // 2 + 52))
            self.screen.blit(instruction_text, 
                           (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 50))
        elif self.game_over:
            game_over_text = self.font.render("GAME OVER", True, RED)
            game_over_outline = self.font.render("GAME OVER", True, BLACK)
            self.screen.blit(game_over_outline, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2 + 2, 
                            SCREEN_HEIGHT // 2 + 2))
            self.screen.blit(game_over_text, 
                           (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2))
            
            # Calculate remaining cooldown time
            time_elapsed = pygame.time.get_ticks() - self.game_over_time
            time_remaining = max(0, self.restart_cooldown - time_elapsed)
            
            if time_remaining > 0:
                # Show countdown timer
                seconds_left = int(time_remaining / 1000) + 1
                countdown_text = self.small_font.render(f"Restarting in {seconds_left}...", True, YELLOW)
                countdown_outline = self.small_font.render(f"Restarting in {seconds_left}...", True, BLACK)
                self.screen.blit(countdown_outline, 
                               (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2 + 2, 
                                SCREEN_HEIGHT // 2 + 62))
                self.screen.blit(countdown_text, 
                               (SCREEN_WIDTH // 2 - countdown_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2 + 60))
            else:
                # Show restart instruction
                restart_text = self.small_font.render("Press SPACE or Click to Restart", True, WHITE)
                restart_outline = self.small_font.render("Press SPACE or Click to Restart", True, BLACK)
                self.screen.blit(restart_outline, 
                               (SCREEN_WIDTH // 2 - restart_text.get_width() // 2 + 2, 
                                SCREEN_HEIGHT // 2 + 62))
                self.screen.blit(restart_text, 
                               (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2 + 60))
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()

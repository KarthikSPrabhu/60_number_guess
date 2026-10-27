import random
import pygame
from game.text_box import TextBox

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.max_attempts = 10
        self.min_val = 1
        self.max_val = 100
        self.guess_history = []
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False

        self.input_box = TextBox(width // 2 - 110, 130, 120, 46)
        self.submit_btn = pygame.Rect(width // 2 + 25, 130, 100, 46)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)

    def submit_guess(self):
        if self.game_won or self.game_over:
            return

        if not self.input_box.text.strip():
            self.feedback_msg = "Please enter a number first!"
            self.feedback_color = (240, 180, 60)
            return

        guess = int(self.input_box.text)

        self.attempts += 1
        self.input_box.clear()

        if guess == self.secret_number:
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.game_won = True
            self.guess_history.append((guess, "CORRECT"))
        elif guess < self.secret_number:
            self.min_val = max(self.min_val, guess + 1)
            self.guess_history.append((guess, "LOW"))
            if self.attempts >= self.max_attempts:
                self.game_over = True
                self.feedback_msg = f"GAME OVER! The number was {self.secret_number}."
                self.feedback_color = (240, 70, 70)
            else:
                self.feedback_msg = f"TOO LOW! (Guess was {guess})"
                self.feedback_color = (80, 160, 240)
        else:
            self.max_val = min(self.max_val, guess - 1)
            self.guess_history.append((guess, "HIGH"))
            if self.attempts >= self.max_attempts:
                self.game_over = True
                self.feedback_msg = f"GAME OVER! The number was {self.secret_number}."
                self.feedback_color = (240, 70, 70)
            else:
                self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
                self.feedback_color = (240, 100, 80)

    def reset(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.min_val = 1
        self.max_val = 100
        self.guess_history = []
        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.game_over = False
        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()
            elif event.key == pygame.K_r and (self.game_won or self.game_over):
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

    def update(self):
        pass

    def render(self, screen):
        screen.fill((30, 34, 42))

        title_surf = self.font_title.render("Number Guessing Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 22))

        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts} / {self.max_attempts}", True, (180, 185, 195)
        )
        screen.blit(attempts_surf, (self.width // 2 - attempts_surf.get_width() // 2, 65))

        range_surf = self.font_medium.render(f"Current Range: {self.min_val} - {self.max_val}", True, (180, 185, 195))
        screen.blit(range_surf, (self.width // 2 - range_surf.get_width() // 2, 93))

        self.input_box.render(screen)

        pygame.draw.rect(screen, (50, 150, 80), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(
            btn_text,
            (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2),
        )

        feedback_surf = self.font_medium.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 192))

        if self.guess_history:
            history_title = self.font_small.render("Recent Guesses:", True, (180, 185, 195))
            screen.blit(history_title, (self.width // 2 - history_title.get_width() // 2, 234))

            recent = self.guess_history[-5:]
            chips = []
            for guess_val, result in recent:
                if result == "LOW":
                    color = (80, 160, 240)
                elif result == "HIGH":
                    color = (240, 100, 80)
                else:
                    color = (80, 220, 90)
                text_surf = self.font_small.render(f"{guess_val} ({result})", True, color)
                chips.append((text_surf, color))

            chip_spacing = 10
            chip_pad_x = 8
            chip_pad_y = 4
            total_w = sum(t.get_width() + chip_pad_x * 2 for t, _ in chips) + chip_spacing * (len(chips) - 1)
            cur_x = self.width // 2 - total_w // 2
            chip_y = 260

            for text_surf, color in chips:
                w = text_surf.get_width() + chip_pad_x * 2
                h = text_surf.get_height() + chip_pad_y * 2
                chip_rect = pygame.Rect(cur_x, chip_y, w, h)
                pygame.draw.rect(screen, (40, 45, 58), chip_rect, border_radius=5)
                pygame.draw.rect(screen, color, chip_rect, width=1, border_radius=5)
                screen.blit(text_surf, (cur_x + chip_pad_x, chip_y + chip_pad_y))
                cur_x += w + chip_spacing
        else:
            history_title = self.font_small.render("Recent Guesses: None", True, (140, 145, 155))
            screen.blit(history_title, (self.width // 2 - history_title.get_width() // 2, 242))

        if self.game_won or self.game_over:
            restart_surf = self.font_medium.render("Press [R] to Start a New Game", True, (255, 220, 80))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, 318))

    @property
    def min_range(self):
        return self.min_val

    @min_range.setter
    def min_range(self, val):
        self.min_val = val

    @property
    def max_range(self):
        return self.max_val

    @max_range.setter
    def max_range(self, val):
        self.max_val = val

    @property
    def is_game_over(self):
        return self.game_over

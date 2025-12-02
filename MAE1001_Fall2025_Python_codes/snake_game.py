#!/usr/bin/env python3
"""
Raspberry Pi Sense HAT Snake Game
Code Written for MAE1001
"""
from sense_hat import SenseHat
from time import sleep
import random
import csv
import os

class SnakeGame:
    def __init__(self):
        self.sense = SenseHat()
        
        # Try to enable low light mode (may not work on all setups)
        try:
            self.sense.low_light = True
        except (OSError, AttributeError):
            pass  # Low light mode not supported, continue anyway
        
        # Colors (R, G, B)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BRIGHT_GREEN = (100, 255, 100)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.WHITE = (255, 255, 255)
        
        # Game state
        self.reset_game()
        
        # Player name
        self.player_name = ""
        
        # Score file
        self.score_file = 'snake_scores.csv'
        self.init_score_file()
    
    def init_score_file(self):
        """Initialize CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.score_file):
            with open(self.score_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Score', 'Length'])
    
    def reset_game(self):
        """Reset game to initial state"""
        self.snake = [(4, 4)]  # Start in center
        self.direction = (0, -1)  # Start moving up
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.speed = 0.4  # Initial game speed
    
    def spawn_food(self):
        """Spawn food at random empty position"""
        while True:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            if (x, y) not in self.snake:
                return (x, y)
    
    def draw_game(self):
        """Render the game on the Sense HAT display"""
        # Clear display
        self.sense.clear()
        
        # Draw snake body
        for i, segment in enumerate(self.snake):
            if i == 0:
                # Snake head - brighter green
                self.sense.set_pixel(segment[0], segment[1], self.BRIGHT_GREEN)
            else:
                # Snake body - regular green
                self.sense.set_pixel(segment[0], segment[1], self.GREEN)
        
        # Draw food with animation effect
        self.sense.set_pixel(self.food[0], self.food[1], self.RED)
    
    def move_snake(self):
        """Move snake in current direction"""
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check wall collision
        if not (0 <= new_head[0] <= 7 and 0 <= new_head[1] <= 7):
            self.game_over = True
            return
        
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            # Increase speed slightly as snake grows
            self.speed = max(0.1, self.speed - 0.02)
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def handle_input(self):
        """Handle joystick input for direction changes"""
        for event in self.sense.stick.get_events():
            if event.action == "pressed":
                if event.direction == "up" and self.direction != (0, 1):
                    self.direction = (0, -1)
                elif event.direction == "down" and self.direction != (0, -1):
                    self.direction = (0, 1)
                elif event.direction == "left" and self.direction != (1, 0):
                    self.direction = (-1, 0)
                elif event.direction == "right" and self.direction != (-1, 0):
                    self.direction = (1, 0)
                elif event.direction == "middle":
                    # Middle button exits game
                    return False
        return True
    
    def show_score(self):
        """Display final score on Sense HAT"""
        self.sense.clear()
        message = f"Score: {self.score}"
        self.sense.show_message(message, scroll_speed=0.05, text_colour=self.YELLOW)
    
    def save_score(self):
        """Save score to CSV file"""
        with open(self.score_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.player_name, self.score, len(self.snake)])
        
        print(f"Score saved for {self.player_name}: {self.score} points, Snake length: {len(self.snake)}")
    
    def get_player_name(self):
        """Prompt for player name"""
        self.sense.show_message("Enter name on computer", scroll_speed=0.05, text_colour=self.BLUE)
        
        # Get name from terminal input
        print("\n" + "="*40)
        print("SNAKE GAME - PLAYER REGISTRATION")
        print("="*40)
        name = input("Enter your name: ").strip()
        
        while not name:
            print("Name cannot be empty!")
            name = input("Enter your name: ").strip()
        
        self.player_name = name
        self.sense.show_message(f"Hi {name}!", scroll_speed=0.05, text_colour=self.GREEN)
        return name
    
    def show_leaderboard(self):
        """Display top 5 scores from leaderboard"""
        try:
            # Read all scores
            scores = []
            with open(self.score_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    scores.append({
                        'name': row['Name'],
                        'score': int(row['Score']),
                        'length': int(row['Length'])
                    })
            
            # Sort by score (descending)
            scores.sort(key=lambda x: x['score'], reverse=True)
            
            # Display top 5
            print("\n" + "="*40)
            print("LEADERBOARD - TOP 5 SCORES")
            print("="*40)
            
            for i, entry in enumerate(scores[:5], 1):
                print(f"{i}. {entry['name']}: {entry['score']} pts (Length: {entry['length']})")
            
            print("="*40 + "\n")
            
            # Show on Sense HAT
            if scores:
                self.sense.show_message("Top Score:", scroll_speed=0.05, text_colour=self.YELLOW)
                top = scores[0]
                self.sense.show_message(f"{top['name']} {top['score']}", scroll_speed=0.05, text_colour=self.YELLOW)
        
        except FileNotFoundError:
            print("No scores yet!")
        except Exception as e:
            print(f"Error reading leaderboard: {e}")
    
    def game_over_animation(self):
        """Show game over animation"""
        # Flash screen red
        for _ in range(3):
            self.sense.clear(self.RED)
            sleep(0.2)
            self.sense.clear()
            sleep(0.2)
    
    def show_start_screen(self):
        """Display start screen"""
        self.sense.show_message("Snake Game!", scroll_speed=0.05, text_colour=self.GREEN)
        self.sense.show_message("Use Joystick to move", scroll_speed=0.05, text_colour=self.BLUE)
        self.sense.show_message("Press Middle to quit", scroll_speed=0.05, text_colour=self.WHITE)
        sleep(0.5)
    
    def run(self):
        """Main game loop"""
        # Get player name first
        self.get_player_name()
        
        self.show_start_screen()
        
        while True:
            # Game loop
            while not self.game_over:
                self.draw_game()
                
                if not self.handle_input():
                    # Middle button pressed - quit game
                    self.sense.show_message("Bye!", scroll_speed=0.05, text_colour=self.WHITE)
                    self.sense.clear()
                    self.show_leaderboard()
                    return
                
                self.move_snake()
                sleep(self.speed)
            
            # Game over sequence
            self.game_over_animation()
            self.show_score()
            self.save_score()
            self.show_leaderboard()
            
            # Ask to play again
            self.sense.show_message("Again? Up=Yes Down=No", scroll_speed=0.05, text_colour=self.BLUE)
            
            # Wait for input
            waiting = True
            while waiting:
                for event in self.sense.stick.get_events():
                    if event.action == "pressed":
                        if event.direction == "up":
                            self.reset_game()
                            waiting = False
                        elif event.direction == "down" or event.direction == "middle":
                            self.sense.show_message("Bye!", scroll_speed=0.05, text_colour=self.WHITE)
                            self.sense.clear()
                            self.show_leaderboard()
                            return
                sleep(0.1)


def main():
    """Entry point for the game"""
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    finally:
        # Clean up
        sense = SenseHat()
        sense.clear()
        print("Game ended. Check snake_scores.csv for saved scores!")


if __name__ == "__main__":
    main()
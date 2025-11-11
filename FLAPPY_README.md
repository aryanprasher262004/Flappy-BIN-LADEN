# Flappy Airplane Game

A fun Flappy Bird-style game featuring an airplane instead of a bird! Navigate through pipes and see how high you can score.

## Features

- **Airplane Graphics**: Custom-drawn airplane with wings, tail, and cockpit
- **Explosion Effects**: Spectacular particle explosion when the plane crashes! 💥
- **Sound Effects**: Flap, score, and crash sounds (requires NumPy)
- **Smooth Physics**: Realistic gravity and flight mechanics
- **Animated Clouds**: Moving clouds in the background for atmosphere
- **Score Tracking**: Keep track of your high score
- **Simple Controls**: One-button gameplay (Space or Mouse Click)
- **Instant Restart**: Quick restart after game over

## Requirements

- Python 3.x
- Pygame 2.5.2
- NumPy (optional, for sound effects)

## Installation

1. Install the required dependency:

```bash
pip install -r requirements.txt
```

Or install packages directly:

```bash
pip install pygame
pip install numpy  # Optional: for sound effects
```

**Note**: The game will run without NumPy, but sound effects will be disabled.

## How to Run

Run the game with:

```bash
python flappy_airplane.py
```

## How to Play

### Controls
- **SPACE** or **Mouse Click**: Make the airplane fly upward
- **ESC**: Quit the game

### Gameplay
1. Press SPACE or click to start the game
2. The airplane will fall due to gravity
3. Press SPACE or click to make it fly upward
4. Navigate through the gaps between pipes
5. Each pipe you pass increases your score by 1
6. Avoid hitting pipes or flying off-screen
7. When you crash, press SPACE to restart

### Tips
- Tap gently for better control
- Time your taps to navigate smoothly through pipes
- Don't fly too high or too low
- Practice makes perfect!

## Game Elements

- **Airplane**: Gray body with red wings and yellow tail
- **Pipes**: Green obstacles with gaps to fly through
- **Explosion**: Colorful particle effects when crashing (red, orange, yellow flames)
- **Sky**: Beautiful blue background with animated clouds
- **Score**: Displayed at the top center of the screen
- **Sounds**: Wing flap, scoring beep, and crash sound effects

## Scoring

- +1 point for each pipe successfully passed
- Try to beat your high score!

Enjoy flying! ✈️

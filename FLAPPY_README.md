# 🛩️ Flappy Osama

A Flappy Bird-style arcade game featuring an airplane navigating through obstacles. This open-source game includes advanced features like custom graphics, background music, particle effects, and extensive modding capabilities.

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/pygame-2.5.2-green.svg)
![License](https://img.shields.io/badge/license-Open%20Source-orange.svg)

## 🎮 Features

### Core Gameplay
- **Classic Flappy Bird Mechanics**: One-button control with gravity-based physics
- **Progressive Difficulty**: Game gets harder as your score increases
  - Pipes move faster
  - Gap between pipes shrinks
  - Spawn rate increases
- **High Score Tracking**: Persistent high score saved to file

### Visual Effects
- **Custom Graphics Support**: Load your own airplane and pipe images
- **Particle Explosion System**: Spectacular crash effects with colorful particles
- **Day/Night Cycle**: Dynamic background color transitions
- **Falling Pipe Animation**: Pipes rotate and fall when hit
- **Smooth Animations**: 60 FPS gameplay with fluid motion

### Audio
- **Background Music System**: 
  - Supports MP3, OGG, and WAV formats
  - Multiple track support with playlist
  - Volume control slider
  - Toggle music on/off
- **Sound Effects**:
  - Crash sound (customizable)
  - Score sound
  - Flap sound

### Customization
- **Modding Menu**: Adjust game parameters in real-time
  - Gravity strength
  - Flap power
  - Pipe gap sizes
  - Pipe velocity
  - Spawn timing
  - Pipe width
- **Custom Assets**: Replace default graphics with your own images

## 📋 Requirements

- **Python 3.x**
- **Pygame 2.5.2**
- **NumPy** (optional, for enhanced sound effects)

## 🚀 Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pygame==2.5.2
   pip install numpy  # Optional
   ```

3. **Run the game:**
   ```bash
   python flappy_airplane.py
   ```

## 🎯 How to Play

### Controls
- **SPACE** or **Left Mouse Click**: Make the airplane fly upward
- **ESC**: Quit the game

### Gameplay
1. Click **START** from the home screen
2. Press **SPACE** or click to make the airplane fly
3. Navigate through gaps between pipes
4. Each pipe passed = +1 point
5. Avoid hitting pipes or flying off-screen
6. Try to beat your high score!

### Tips
- Tap gently for better control
- Time your flaps carefully
- The game gets progressively harder
- Practice makes perfect!

## 🎨 Customization

### Adding Custom Graphics

Place these files in the game directory:

#### **airplane.png** (or **plane.png**)
- Recommended size: 50x30 pixels
- Format: PNG with transparent background
- Orientation: Airplane facing right →

#### **pipe.png**
- Recommended width: 70 pixels
- Format: PNG
- Will be tiled vertically to create pipes

See [IMAGE_GUIDE.md](IMAGE_GUIDE.md) for detailed instructions.

### Adding Background Music

Place music files in the game directory with these formats:
- `.mp3` (recommended)
- `.ogg`
- `.wav`

The game will automatically detect and load all music files. You can:
- Toggle music on/off in settings
- Adjust volume with the slider
- Switch between tracks (if multiple files present)

See [MUSIC_GUIDE.md](MUSIC_GUIDE.md) for detailed instructions.

### Adding Custom Sounds

Place these files in the game directory:
- **crash sound.mp3** (or crash.mp3/crash.wav/crash.ogg)
- Volume is automatically set to 30%

## ⚙️ Settings Menu

Access the settings menu from the home screen:

- **Music Toggle**: Turn background music on/off
- **Volume Slider**: Adjust music volume (0-100%)
- **Modding**: Access game parameter customization
- **Back**: Return to home screen

## 🔧 Modding Menu

Customize game difficulty and behavior:

| Parameter | Range | Description |
|-----------|-------|-------------|
| Gravity | 0.1 - 2.0 | How fast the airplane falls |
| Flap Strength | 5 - 15 | How much the airplane rises per flap |
| Initial Gap | 200 - 350 | Starting gap size between pipes |
| Min Gap | 180 - 280 | Minimum gap at high scores |
| Pipe Width | 30 - 100 | Width of pipe obstacles |
| Initial Velocity | 1 - 5 | Starting pipe speed |
| Max Velocity | 5 - 12 | Maximum pipe speed at high scores |

Changes apply immediately when you start a new game!

## 📁 Project Structure

```
FLAPPY BIN LADEN/
├── flappy_airplane.py      # Main game file
├── requirements.txt        # Python dependencies
├── highscore.txt          # Saved high score
├── README.md              # This file
├── FLAPPY_README.md       # Original readme
├── IMAGE_GUIDE.md         # Custom graphics guide
├── MUSIC_GUIDE.md         # Background music guide
├── airplane.png           # Airplane sprite (optional)
├── pipe.png              # Pipe texture (optional)
├── bg sound.mp3          # Background music (optional)
└── crash sound.mp3       # Crash sound effect (optional)
```

## 🎮 Game States

- **HOME**: Main menu with START and SETTINGS buttons
- **PLAYING**: Active gameplay
- **SETTINGS**: Audio and customization options
- **MODDING**: Game parameter adjustment
- **GAME_OVER**: Score display and restart option

## 🎨 Visual Elements

### Colors
- Sky Blue background with day/night transitions
- Green pipes with dark green borders
- Gray airplane body (default)
- Red wings and yellow tail (default)
- Colorful explosion particles (red, orange, yellow)

### Animations
- Airplane rotation based on velocity
- Particle explosion on crash
- Falling pipes with rotation
- Smooth background color transitions

## 🐛 Troubleshooting

### Music Not Playing?
1. Check file format (MP3, OGG, or WAV)
2. Ensure files are in the game directory
3. Check music toggle is ON in settings
4. Verify volume slider is not at 0%

### Images Not Loading?
1. Check file names: `airplane.png` or `plane.png`, `pipe.png`
2. Ensure files are in the game directory
3. Verify PNG format
4. Check console for error messages

### Game Running Slow?
1. Close other applications
2. Reduce screen resolution (edit SCREEN_WIDTH/SCREEN_HEIGHT in code)
3. Disable particle effects (edit code)

### Sound Effects Not Working?
1. Install NumPy: `pip install numpy`
2. Check audio files are in correct format
3. Verify pygame.mixer is initialized

## 🔊 Audio Files Included

- **bg sound.mp3**: Background music track
- **crash sound.mp3**: Crash sound effect

## 📝 License

**OPEN SOURCE - DO WHATEVER YOU WANT**

This game is completely open source. Feel free to:
- Modify the code
- Add new features
- Create your own versions
- Share with others
- Use for learning
- Commercial use

No attribution required, but appreciated!

## 🤝 Contributing

This is an open-source project. Contributions are welcome!

Ideas for improvements:
- More sound effects
- Additional game modes
- Power-ups
- Multiplayer support
- Leaderboard system
- More visual effects
- Mobile version

## 🎓 Learning Resources

This game demonstrates:
- Pygame basics (sprites, collision detection, rendering)
- Game state management
- UI elements (buttons, sliders, dropdowns)
- Particle systems
- Sound and music integration
- File I/O for high scores
- Image loading and transformation
- Event handling

Perfect for learning game development with Python!

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the guide files (IMAGE_GUIDE.md, MUSIC_GUIDE.md)
3. Check console output for error messages
4. Verify all dependencies are installed

## 🎉 Credits

- Game concept inspired by Flappy Bird
- Built with Pygame
- Particle system and animations custom-built
- Open source and free to use

---

**Enjoy flying! ✈️**

Made with ❤️ using Python and Pygame

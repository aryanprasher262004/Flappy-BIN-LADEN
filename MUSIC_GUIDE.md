# Background Music Guide

Your Flappy Airplane game now supports background music!

## How to Add Music

### Step 1: Get a Music File

You need a music file in one of these formats:
- **MP3** (recommended) - `.mp3`
- **OGG** - `.ogg`
- **WAV** - `.wav`

### Step 2: Name Your File

Rename your music file to one of these names:
- `background_music.mp3` (recommended)
- `background_music.ogg`
- `background_music.wav`
- `music.mp3`
- `music.ogg`
- `music.wav`

### Step 3: Place in Game Directory

Put the music file in the same folder as the game:

```
d:/tic tac toe/
├── flappy_airplane.py
├── plane.png
├── pipe.png
└── background_music.mp3    ← Your music file here
```

### Step 4: Run the Game

When you start the game, you'll see:
```
✓ Background music loaded: background_music.mp3
```

The music will automatically start playing and loop continuously!

## Music Controls

### In-Game Settings
1. Click **SETTINGS** button from home screen
2. Click **Music: ON/OFF** button to toggle music
3. Music state is shown in the settings screen:
   - ✓ "♪ Music file loaded" (green) - Music file found
   - "No music file found" (gray) - No music file

### Features
- **Auto-loop**: Music plays continuously in a loop
- **Volume**: Set to 50% by default (can be adjusted in code)
- **Pause/Resume**: Toggle ON/OFF in settings
- **Persistent**: Music continues across game sessions

## Where to Find Music

### Free Music Resources
1. **Incompetech** - https://incompetech.com/music/royalty-free/
2. **FreePD** - https://freepd.com/
3. **OpenGameArt** - https://opengameart.org/
4. **Bensound** - https://www.bensound.com/
5. **Purple Planet** - https://www.purple-planet.com/

### Tips for Choosing Music
- **Upbeat tempo**: Matches the fast-paced gameplay
- **Loopable**: Choose tracks that loop seamlessly
- **Short duration**: 30-60 seconds works well for loops
- **Instrumental**: Avoids distracting vocals
- **Retro/Chiptune**: Fits the arcade game style

## Adjusting Volume

To change the music volume, edit this line in `flappy_airplane.py`:

```python
pygame.mixer.music.set_volume(0.5)  # 0.0 to 1.0 (50% volume)
```

Change `0.5` to:
- `0.3` for quieter music
- `0.7` for louder music
- `1.0` for maximum volume

## Troubleshooting

### Music Not Playing?

1. **Check file name**: Must be exactly `background_music.mp3` (or other supported names)
2. **Check file location**: Must be in `d:/tic tac toe/` folder
3. **Check file format**: MP3, OGG, or WAV only
4. **Check settings**: Music toggle should be ON
5. **Check console**: Look for error messages when starting game

### Music Cuts Out?

- Make sure the file isn't corrupted
- Try converting to a different format (MP3 recommended)
- Check that the file plays in other media players

### Want Different Music for Menu vs Game?

You can modify the code to play different tracks for different game states. This requires editing the `handle_events` function to change music when switching between HOME and PLAYING states.

## Example Music Files

Good starter music (search for these on free music sites):
- "Pixel Peeker Polka" by Kevin MacLeod
- "8-bit Adventure" 
- "Retro Platforming"
- "Arcade Funk"
- "Chiptune Does"

Enjoy your game with music! 🎵✈️

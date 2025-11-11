# Image Guide for Flappy Airplane

The game now supports custom images for the airplane and pipes!

## Required Images

Place these image files in the same directory as `flappy_airplane.py`:

### 1. **airplane.png**
- **Recommended size**: 50x30 pixels (or any size with similar aspect ratio)
- **Format**: PNG with transparent background
- **Orientation**: Airplane should face **right** →
- **Tips**: 
  - Use a side view of an airplane
  - Transparent background works best
  - The image will be automatically scaled to 50x30 pixels

### 2. **pipe.png**
- **Recommended width**: 70 pixels
- **Height**: Any height (will be tiled vertically)
- **Format**: PNG with or without transparency
- **Tips**:
  - This image will be repeated/tiled to create tall pipes
  - The image will be flipped upside-down for top pipes
  - Width will be scaled to 70 pixels, height keeps aspect ratio

## How It Works

1. **Place your images** in the game directory:
   ```
   d:/tic tac toe/
   ├── flappy_airplane.py
   ├── airplane.png    ← Your airplane image
   └── pipe.png        ← Your pipe image
   ```

2. **Run the game**: The game will automatically detect and load your images

3. **Fallback**: If images are not found, the game will use the original drawn graphics

## Image Status Messages

When you run the game, you'll see:
- ✓ **Airplane image loaded successfully** - Your airplane.png was found and loaded
- ✓ **Pipe image loaded successfully** - Your pipe.png was found and loaded
- ⚠ **airplane.png not found** - Using drawn graphics for airplane
- ⚠ **pipe.png not found** - Using drawn graphics for pipes

## Example Image Specifications

### Good Airplane Image
```
Size: 50x30 pixels (or 100x60, 150x90, etc.)
Format: PNG
Background: Transparent
Content: Side view of airplane facing right
```

### Good Pipe Image
```
Size: 70x100 pixels (or 70x any height)
Format: PNG
Background: Any (can be solid color or transparent)
Content: Vertical pipe/column texture
```

## Tips for Best Results

1. **Airplane**: 
   - Keep it simple and recognizable
   - Ensure it's clearly visible against the blue sky
   - Transparent background prevents white boxes

2. **Pipes**:
   - Create a seamless texture that tiles well
   - Test with different heights to ensure it looks good when repeated
   - Consider adding some detail but not too busy

## Where to Find Images

- **Create your own** using image editing software (GIMP, Photoshop, Paint.NET)
- **Free sprite resources**: OpenGameArt.org, itch.io, Kenney.nl
- **AI generators**: Use AI tools to generate custom sprites
- **Pixel art tools**: Piskel, Aseprite for creating retro-style sprites

Enjoy customizing your game! ✈️

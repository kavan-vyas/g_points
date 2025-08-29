# Gravity Points

A pygame thing that simulates particles being attracted to gravity points.
***Looking for collaborators to improve game physics**

## What it does

There are two versions:
- `gpoints.py` - basic version with some hardcoded patterns, then I thought, I should add slider etc to make it better... and then the next file was born:
- `egpoints.py` - fancier version with UI controls and better graphics

Particles move around and get pulled toward gravity points. You can click to add more gravity points.


## How to run

Install everything in requirements.py first:
```zsh
pip3 install -r requirements.txt
```

Then run either:
```zsh
python3 gravity_points.py
```

or

```zsh
python3 enhanced_gravity_points.py
```


## Controls

- Click anywhere to add gravity points
- In the enhanced version there are sliders and buttons for controlling stuff

The enhanced version has more particles, trails, colors, and UI controls. The basic version just has green particles and some preset patterns.

## Notes

The physics aren't super realistic but it looks cool. 
Particles wrap around screen edges. The enhanced version runs at higher resolution (2560x1080) while basic is 1920x1080.

That's about it.

Also thanks to the maintainers of this fantastic library pygame and props to them, may pygame live forever!


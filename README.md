# 🐍 Snake Game (Python + Tkinter)

A classic Snake Game built entirely with Python and Tkinter, featuring grid rendering, movement logic, growing snake behavior, and apple spawning.
This lightweight project requires no external game engines and demonstrates canvas manipulation and event-driven input handling.

## 🎮 Features

  - 🟩 Fully drawn 20×20 grid
  
  - 🐍 Snake movement with WASD or Arrow Keys
  
  - 🍎 Random apple spawning with collision avoidance
  
  - ➕ Snake grows each time it eats an apple
  
  - 💥 Self-collision and wall-collision detection
  
  - ⚡ Adjustable speed
  
  - 🎨 Clean canvas rendering

## 🖥️ Controls

  - Move Up	↑ or W
  - Move Down	↓ or S
  - Move Left	← or A
  - Move Right	→ or D

## 📦 Requirements

This game uses only standard Python modules except for tkinter, which is included by default.

No extra installation required on Windows or macOS.

If you're on Linux and Tkinter is missing:

sudo apt-get install python3-tk

## 🚀 How to Run

git clone https://github.com/xHady/Snake-Game.git

cd Snake-Game

python main.py


## 🧠 How It Works

### Grid

 A 20×20 grid is drawn on a Tkinter canvas.

Border tiles are colored differently to indicate walls.

### Snake

The snake is represented as a list of rectangle IDs (SnakePosition).

Each game loop moves the head and shifts the rest of the body behind it.

### Apple

The apple appears at a random location that is not occupied by the snake

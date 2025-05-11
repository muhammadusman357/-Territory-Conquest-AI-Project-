# Territory Vonquest - Human vs AI and AI vs AI Game

### Submitted By: 
Muhammad Usman
Muhammad waqi
Muhammad Shahaf

### Course: AI
### Instructor: Abdullah Yaqoob

________________________________________
# Demo Video:
Link: https://drive.google.com/file/d/1Q7MCag4bpM6n2SGpY5Y19VoDv_Vlu_5Z/view?usp=sharing
________________________________________
## 1. Executive Summary
### Project Overview:
This project intends to transform a basic 2D grid-based game into a more interactive and strategic version. The basic game has two players who play to capture tiles on a grid, but with the addition of two modes: **Human vs AI** and **AI vs AI**. The AI employs a **Minimax algorithm with Alpha-Beta Pruning** to determine the best possible move in both modes. Power-ups such as Freeze and Bonus are introduced to enhance the richness of the game and provide special powers to players.
________________________________________
## 2. Introduction
### Background:
**Territory Vonquest** is a variation based on old grid-style competitive games. The intention of the project is to incorporate Artificial Intelligence (AI) in the game such that an AI plays against a human or another AI. The game begins with a blank grid, and the players keep alternating in claiming tiles by shifting their pieces. This implementation of the game brings in strategic depth with the addition of **power-ups** like `Freeze` and `Bonus`, which add one level of strategy and uncertainty to the game.
The project was chosen because it entails applying AI through the Minimax algorithm and applying this method within an actual competitive environment. Game mechanics were tailored to accommodate two distinct modes: Human vs AI and AI vs AI, with each having its own challenge.

### Objectives:
- Develop a grid-based competitive game.
- Integrate Human vs AI and AI vs AI modes.
- Implement the **Minimax algorithm** with **Alpha-Beta Pruning**.
- Add power-ups (`Freeze`, `Bonus`) for strategic gameplay.
- Analyze AI performance in both game modes.

________________________________________
## 3. Game Description

### Original Game Rules:
The original game is a simple grid-based board where players alternate turns to capture tiles. The first player to capture all the tiles wins the game. Players move in four directions (up, down, left, right) to capture tiles.

### Innovations and Modifications:
- **AI Integration**: Implemented the Minimax algorithm for AI decision-making, with Alpha-Beta Pruning for faster evaluation.  
- **Game Modes**:  
  - Human vs AI Mode: A human player controls one piece while the AI controls the opponent's piece. The AI competes with the human player.  
  - AI vs AI Mode: Two AI players compete against each other, both using Minimax to make decisions.  
- **Power-Ups**: Added two power-ups:  
  - `Freeze`: Temporarily disables the opponent's movement.  
  - `Bonus`: Increases the score of the player capturing the tile with this power-up.  
- **Timer**: A countdown timer of 30 seconds for each game, adding urgency to the game.

________________________________________
## 4. AI Approach and Methodology
## AI Techniques Used:
The AI uses the Minimax algorithm with Alpha-Beta Pruning to evaluate the best possible moves. The algorithm evaluates all possible moves, simulates their outcomes, and selects the most strategic move based on a predefined evaluation function. The Alpha-Beta Pruning optimizes this process by eliminating branches of the game tree that do not need to be explored, improving performance.
Algorithm and Heuristic Design:
### Techniques Used:
-**Minimax Algorithm** evaluates possible game states by simulating moves.
### Heuristic Design:
  -The evaluation function considers the current state of the board and assigns a score based on the number of tiles captured by the player or AI, the presence of power-ups, and the strategic positioning of the pieces.
- **Alpha-Beta Pruning** speeds up the search by pruning unnecessary branches in the Minimax tree.
### AI Performance Evaluation:
 -The AI’s performance was evaluated in terms of decision-making time and win rate against human players and the second AI player.
 -The AI showed a 40% win rate in Human vs AI mode and could make decisions within an average of 1-2 seconds per move.
________________________________________
## 5. Game Mechanics and Rules
### Modified Game Rules:
•	The game is played on a grid, where players capture tiles.
•	Human vs AI Mode: The human player controls the BLACK piece, and the AI controls the PURPLE piece.
•	AI vs AI Mode: Two AIs, one controlled by Minimax (PURPLE) and the other (GREEN), compete against each other.
•	Power-ups: Players can capture power-ups that give temporary advantages. The Freeze power-up disables the opponent temporarily, while the Bonus power-up adds points to the player's score.
•	Players can only move one tile at a time, and they cannot move onto the opponent's occupied tiles unless capturing them.
### Turn-based Mechanics:
•	Players take turns moving their pieces.
•	Each player moves once per turn. In AI vs AI, both AI players take turns making decisions.
### Winning Conditions:
The game ends when:
•	A player captures all tiles on the grid.
•	Time runs out (game duration of 30 seconds).
________________________________________
## 6. Implementation and Development
### Development Process:
• The game was developed using Python and Pygame for rendering and gameplay.
• Minimax Algorithm was implemented in Python to analyze the possible moves of the AI and decide.
•Power-ups were introduced as unique tiles on the grid that can be seized for temporary benefits.
### Programming Languages and Tools:
•	Programming Language: Python 3
•	Libraries: Pygame (for game development and rendering)
•	Tools: GitHub for version control
### Challenges Encountered:
• The greatest challenge was to make sure that the AI made sound decisions without being too slow or inefficient.
• Integrating the Alpha-Beta Pruning into the Minimax algorithm was challenging because it needed to optimize the pruning and evaluation functions to balance between performance and accuracy.________________________________________
## 7. Team Contributions
•	Muhammad Usman: Responsible for the AI algorithm development (Minimax with Alpha-Beta Pruning), implementing decision-making strategies, and evaluating AI performance.
•	Muhammad: Handled game rule modifications, including the integration of power-ups and the development of AI vs AI mode.
•	Muhammad Shahaf: Focused on user interface development, integrating AI with gameplay, and handling graphical rendering.
________________________________________
## 8. Results and Discussion
AI Performance:
•	The AI achieved a 40% win rate in Human vs AI mode, showing that the Minimax algorithm was effective at decision-making.
•	The AI vs AI mode was successful, with the two AIs competing in an engaging manner. The AI decision-making time averaged around 1-2 seconds per move.
________________________________________
## 9. References
1.	Pygame Documentation – Official Pygame documentation for handling graphics, user input, and game development. 
2.	Minimax Algorithm and Alpha-Beta Pruning – Various resources on the Minimax algorithm and optimizations like Alpha-Beta Pruning. 
3.	Artificial Intelligence: A Modern Approach – A book by Stuart Ru


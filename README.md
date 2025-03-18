# Cells Expansion Game with Python
## Project Description

"War of Expansion" is a turn-based strategy game where players control units on a grid-based board, planning moves and attacks to defeat opponents. The project utilizes the Qt framework, including QGraphicsScene and QGraphicsItem, to implement dynamic and interactive gameplay.

## Features

* QGraphicsScene – implementation of the game scene.

* Units as objects – inheritance from QGraphicsItem, each unit is a separate object.

* Interactive units – clickable, draggable, and context menu functionality.

* Unit control – selection from a menu and movement on the board grid.

* Unit graphics – loading unit graphics from a .rc file.

* Highlighting possible moves and attacks – based on unit multipliers.

* Combat system – including levels, unit multiplication, and special battle effects.

* Turn-based mechanism and timer – round timer limiting the time for each move.

* Strategic hints system – AI-based suggestions for the best move in a turn.

* Gesture-based control – units can be controlled with hand gestures detected by a camera.

* Logger – displays messages in the console and a QTextEdit interface with rotating logs.

* View switching between 2D and 3D – rendering units in 3D.


## Technologies

* Programming Language: Python 

* Libraries:  PySide6, Qt6 

* File Formats: .rc (for resources), JSON (for game saves and settings)

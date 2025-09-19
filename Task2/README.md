# ENCS3320 – Project Task 2
## TCP/UDP Hybrid Quiz Game

---
### 1. Overview
This project implements a multiplayer quiz game using both **TCP** and **UDP** socket programming.

- **TCP** is used for:
  - Player registration
  - Reliable delivery of quiz questions
  - Final results announcement

- **UDP** is used for:
  - Fast-paced submission of player answers
  - Immediate feedback ("Correct"/"Wrong")

The system supports **2–4 players** connected simultaneously.

---
### 2. Requirements
- Python 
- Standard libraries only:
  - `socket`
  - `threading`
  - `random`
  - `time`

---
### 3. Port Numbers
Port numbers are derived from the student ID used by the team.

Example (Student ID = 1230892):
- **TCP Port** = last 3 digits + 3000 = `256 + 3000 = 3256`
- **UDP Port** = first 3 digits + 6000 = `123 + 6000 = 6123`


---
### 4. Files in this Folder

---
### 5. How to Run

#### Step 1 – Start the Server
python3 server.py
```
The server will:
- Listen on TCP_PORT for incoming connections
- Wait until at least 2 players register

#### Step 2 – Start the Clients
Open a new terminal window for each client and run:
python3 client.py
Each client must register with a unique username:
```
JOIN <username>
```
Example:
```
JOIN Player1
```

#### Step 3 – Start the Game
Once enough players join, the server announces **"Game Start"**.
- Questions are sent via **TCP**  
- Players submit answers via **UDP**  
- Server responds quickly with **"Correct"** or **"Wrong"**  

#### Step 4 – Results
After 5 questions (default), the server calculates final scores.  
Final results and the winner are sent to all players via TCP.

---
### 6. Game Rules
- Min players = 2  
- Max players = 4  
- Number of questions = 5  
- Scoring:  
  - Correct answer = +1 point  
  - Wrong or no answer = 0 points  

---
### 7. Example Run

**Server Terminal:**
```
[SERVER] Listening on TCP port 3310 and UDP port 6124...
[SERVER] Player1 joined
[SERVER] Player2 joined
[SERVER] Game Start!
[SERVER] Q1 sent
[SERVER] Player1 -> Correct
[SERVER] Player2 -> Wrong
...
[SERVER] Final Results:
Player1: 3 points
Player2: 2 points
Winner: Player1
```

**Client Terminal (Player1):**
```
JOIN Player1
[SERVER] Welcome, Player1!
Q1: What does HTTP stand for?
Enter answer: b
Feedback: Correct
...
Final Results:
You scored 3 points
Winner: Player1
```

---
### 8. Notes
- Unique usernames must be used by each client.  
- If fewer than 2 players connect, the game will not start.  

---
### 9. Authors
- **Team Number:** T006  
- **Student IDs:** 1230892, 1230800, 1230256  

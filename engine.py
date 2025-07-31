from random import *
import cv2
import mediapipe as mp
import time
from tic import tictaktoe
import PIL


class GameEngine:
    def __init__(self,player = randint(0,1),difficulty=2) -> None:
        self.next_move_time_gap = 2
        self.next_move_time = time.time() + 4

        self.mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

        self.cap = self.select_camera()

    def send_value(self):

        while True:
            ret,frame = self.cap.read()
            if not ret: break
            row,col = self.finger_count(frame)
            # cv2.imwrite(filename="image.jpg",img=frame)
            # return [row,col],cv2.imread('image.jpg')
            return [row,col]

    def select_camera(self):
        for i in range(3,-1,-1):
            cap = cv2.VideoCapture(i,cv2.CAP_MSMF)
            if cap.read()[0]:
                break
        return cap

    def finger_count(self,frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.mp_hands.process(frame_rgb)
        row = -1
        col = -1

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [(lm.x, lm.y) for lm in hand_landmarks.landmark]

                thumb_up = landmarks[4][1] < landmarks[3][1]
                finger_count = sum([landmarks[i][1] < landmarks[i - 2][1] for i in range(6, 20, 4)]) + thumb_up
                if finger_count == 4:
                    finger_count = 1
                elif finger_count == 3:
                    finger_count = 2
                elif finger_count == 5:
                    finger_count = 0

                # Determine left or right hand based on landmark position
                if landmarks[0][0] < landmarks[17][0]:
                    row = finger_count
                else:
                    col = finger_count
        return [row,col]

    def current_state(self,frame,fingers,result):
        # Draw the game board on the webcam image
        for i in range(1, 3):
            cv2.line(frame, (220 * i, 0), (220 * i, 480), (255, 0, 0), 2)
            cv2.line(frame, (0, 160 * i), (640, 160 * i), (255, 0, 0), 2)

        # Display row and column count
        if result == "" or result == "Position already occupied.":
            cv2.putText(frame, f"Row Count: {fingers[0]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv2.putText(frame, f"Column Count: {fingers[1]}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            cv2.putText(frame, result, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Display the current state of the game board
        for i in range(len(self.start.game)):
            for cell in range(len(self.start.game[i])):
                row = i
                col = cell
                x = 40 + col * 220
                y = 80 + row * 160
                if self.game[row][cell] != 0:
                    text = "X" if self.game[row][cell] == 1 else "O"
                    cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, f"{row},{col}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    def engine_start(self):
        loop = True
        string = ""
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            row,column = self.finger_count(frame)

            self.current_state(frame,[row,column],string)

            # ------- AI vs Player mode -------
            if loop and time.time() >= self.next_move_time:
                if self.player:
                    if [row,column] in self.moves:
                        self.moves.remove([row,column])
                        string,loop,self.player = self.start.pvp(self.player,row,column)
                        self.next_move_time = time.time() + self.next_move_time_gap
                else:
                    row,column = self.start.AI() if self.difficulty_moves() else self.random_move()
                    self.moves.remove([row,column])
                    string,loop,self.player=self.start.pvp(self.player,row,column)
                    self.next_move_time = time.time() + self.next_move_time_gap


            cv2.imshow('Tic Tac Toe', frame)


            # Exit the loop by pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

class AI_move(tictaktoe):
    def __init__(self,difficulty : int = 2) -> None:

        # self.start = tictaktoe([[0,0,0],[0,0,0],[0,0,0]])
        self.player = 0
        self.moves = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
        super().__init__([[0,0,0],[0,0,0],[0,0,0]])

        self.difficulty = difficulty

    def start_new(self):
        self.player = randint(0,1)
        if self.player:
            a = True # Human Player's Move

        else:
            a = False # AI's Move
        return a


    def process_AI(self):
        row,column = super().AI() if self.difficulty_moves() else self.random_move()
        self.moves.remove([row,column])
        string,loop,self.player = super().pvp(self.player,row,column)
        return [string,loop,self.player,[row,column]]

    def process_player(self,move):
        row,column = move
        if [row,column] in self.moves:
            self.moves.remove([row,column])
        string,loop,self.player = super().pvp(self.player,row,column)
        return [string,loop,self.player,[row,column]]

    def difficulty_moves(self):
        if self.difficulty == 2:
            return True
        elif self.difficulty == 1:
            return True if randint(0,9) < 7 else False
        elif self.difficulty == 0:
            return True if randint(0,9) < 4 else False


    def random_move(self):
        while True:
            ai_move = super().AI()
            random_move = choice(self.moves) # function in ramdom module
            if ai_move != random_move and len(self.moves)>1:return random_move
            else:return ai_move

    def reset(self):
        return self.game

if __name__ == "__main__":
    eng = GameEngine()
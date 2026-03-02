# import cv2
# import numpy as np
# from sklearn.neighbors import KNeighborsClassifier
# import random
# import time

# # Initialize classifier
# knn = KNeighborsClassifier(n_neighbors=3)

# # Data storage
# data = []
# labels = []

# # Classes
# classes = {0: 'Rock', 1: 'Paper', 2: 'Scissors'}

# # Capture training data
# def collect_data(label, name):
#     print(f"Show {name} for 5 seconds...")
#     start = time.time()
#     while time.time() - start < 5:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         roi = frame[100:300, 100:300]
#         gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#         gray = cv2.resize(gray, (50, 50)).flatten()
#         data.append(gray)
#         labels.append(label)
#         cv2.rectangle(frame, (100,100), (300,300), (0,255,0), 2)
#         cv2.imshow("Collecting Data", frame)
#         if cv2.waitKey(1) & 0xFF == 27:
#             break

# # Start video capture
# cap = cv2.VideoCapture(0)

# # Collect training samples
# for label, name in classes.items():
#     collect_data(label, name)

# # Train model
# data = np.array(data)
# labels = np.array(labels)
# knn.fit(data, labels)
# print("Training completed!")

# # Play game
# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break

#     roi = frame[100:300, 100:300]
#     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#     gray = cv2.resize(gray, (50, 50)).flatten().reshape(1, -1)
    
#     pred = knn.predict(gray)[0]
#     user_move = classes[pred]
#     computer_move = random.choice(list(classes.values()))

#     # Winner logic
#     if user_move == computer_move:
#         result = "Draw"
#     elif (user_move == "Rock" and computer_move == "Scissors") or \
#          (user_move == "Paper" and computer_move == "Rock") or \
#          (user_move == "Scissors" and computer_move == "Paper"):
#         result = "You Win!"
#     else:
#         result = "Computer Wins!"

#     cv2.putText(frame, f"Your Move: {user_move}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
#     cv2.putText(frame, f"Computer: {computer_move}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
#     cv2.putText(frame, f"Result: {result}", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

#     cv2.rectangle(frame, (100,100), (300,300), (0,255,0), 2)
#     cv2.imshow("Rock Paper Scissors", frame)

#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cap.release()
# cv2.destroyAllWindows()

import cv2
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import random
import time

# =============================
# 1. SETUP
# =============================

classes = {0: 'Rock', 1: 'Paper', 2: 'Scissors'}
data = []
labels = []
knn = KNeighborsClassifier(n_neighbors=3)

cap = cv2.VideoCapture(0)

# =============================
# 2. COLLECT TRAINING DATA
# =============================
def collect_data(label, name):
    print(f"Show {name} for 5 seconds...")
    start_time = time.time()
    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if not ret:
            break
        roi = frame[100:300, 100:300]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (50, 50)).flatten()
        data.append(gray)
        labels.append(label)
        cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)
        cv2.putText(frame, f"Show {name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Collecting Data", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

for label, name in classes.items():
    collect_data(label, name)

data = np.array(data)
labels = np.array(labels)
knn.fit(data, labels)
print("✅ Training completed!")

# =============================
# 3. PLAY GAME
# =============================
user_move = None
computer_move = None
result = None
waiting_for_move = True
show_result_until = None

print("Press SPACE to lock your move. Press ESC to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[100:300, 100:300]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (50, 50)).flatten().reshape(1, -1)
    pred = knn.predict(gray)[0]
    predicted_move = classes[pred]

    # Game state handling
    if waiting_for_move:
        cv2.putText(frame, f"Your Move: {predicted_move} (Press SPACE)", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(frame, f"Your Move: {user_move}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Computer: {computer_move}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        cv2.putText(frame, f"Result: {result}", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        if time.time() > show_result_until:
            waiting_for_move = True  # Go back to detecting mode

    # Draw ROI
    cv2.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 2)
    cv2.imshow("Rock Paper Scissors", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == 32 and waiting_for_move:  # SPACE to lock in move
        user_move = predicted_move
        computer_move = random.choice(list(classes.values()))

        if user_move == computer_move:
            result = "Draw"
        elif (user_move == "Rock" and computer_move == "Scissors") or \
             (user_move == "Paper" and computer_move == "Rock") or \
             (user_move == "Scissors" and computer_move == "Paper"):
            result = "You Win!"
        else:
            result = "Computer Wins!"

        waiting_for_move = False
        show_result_until = time.time() + 2  # Show result for 2 seconds

cap.release()
cv2.destroyAllWindows()

# Mindplay Family 🧠✨

A beautiful, interactive Flutter quiz application designed to engage both kids and parents in collaborative, adaptive brain training. Spark curiosity, challenge cognitive skills, and track progress together as a family!

---

## 🌟 Project Overview

**Mindplay Family** is an educational and entertainment platform built with Flutter. It adapts to the player's age and level, providing tailored question sets across various subjects. 

The application implements a custom offline database layer using JSON-serialized `SharedPreferences` to manage user profiles, sessions, quiz history, and progressive level-unlock systems locally and securely.

---

## 🚀 Key Features

*   **🔒 Offline Authentication & User Profiles**
    *   Register, sign in, and persist user profiles locally.
    *   Saves names, emails, phone numbers, and child age groups.
*   **🎭 Dual Mode Dashboard (Kids vs. Parents)**
    *   **Kids Quest Mode:** Vibrant, gamified, child-safe interface featuring age-appropriate questions (ages 4-15).
    *   **Parents Discovery Mode:** Sleek, mature theme hosting advanced cognitive tasks, logic puzzles, and trivia.
*   **🎯 Adaptive Question Filtering**
    *   Dynamic level-unlocking system up to Level 25 per category.
    *   Age-gate fallbacks that filter questions based on the child's age range (`minAge` and `maxAge`).
*   **🧮 Dynamic Math Question Generator**
    *   Auto-generates arithmetic questions dynamically matching the selected level:
        *   *Levels 1-10:* Addition challenges.
        *   *Levels 11-20:* Subtraction challenges.
        *   *Levels 21-50:* Multiplication challenges.
*   **📚 Rich Topic Categories**
    *   Math, Science, History, Geography, Arts, Technology, Mixed Mode, and **Daily Challenges**.
*   **📊 Score Card & Progress Tracker**
    *   Historical tracking of quiz attempts.
    *   Shows a visual breakdown of completed quizzes, scores, and next level unlocks.
*   **🌐 Online Quiz Flow**
    *   Interactive skeleton flow for multiplayer / online match-making quizzes.

---

## 🛠️ Tech Stack

*   **Framework:** [Flutter](https://flutter.dev/) (SDK version `^3.10.7` using Material 3 design)
*   **Language:** [Dart](https://dart.dev/)
*   **Local Storage & Session Persistence:** `shared_preferences` (configured as a serialized database)
*   **Typography:** Google Fonts (Roboto)

---

## 📁 Project Directory Structure

```text
lib/
├── main.dart                      # App entry point & theme initialization
├── core/
│   ├── data/
│   │   ├── question_generator.dart # Dynamic math generator & option shuffler
│   │   └── quiz_data.dart          # Static quiz datasets and filter logic
│   ├── models/
│   │   ├── question_model.dart     # Question & option structures
│   │   └── user_model.dart         # User profile & QuizAttempt schemas
│   ├── services/
│   │   └── auth_service.dart       # Local registration, login & level unlock logic
│   └── theme/
│       └── category_theme.dart     # Visual category-specific styles
└── features/
    ├── auth/
    │   └── login_screen.dart       # Authentication UI
    ├── home/
    │   └── home_screen.dart        # Mode switching, daily challenges, and category navigation
    └── quiz/
        ├── kids_quiz_screen.dart   # Interactive quiz engine for kids
        ├── parents_quiz_screen.dart # Advanced quiz engine for parents
        ├── level_selection_screen.dart # Progress mapping screen (Levels 1-25)
        ├── online_quiz_flow.dart   # Stub UI for online matchmaking
        ├── result_screen.dart      # Score breakdowns and animation triggers
        └── score_card.dart         # Historical score tracking dashboard
```

---

## ⚙️ Installation & Setup Steps

### Prerequisites

Make sure you have Flutter installed on your system. Verify your setup with:
```bash
flutter doctor
```

### Run Locally

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Sp1606/mindplay-family-app.git
   cd mindplay-family-app
   ```

2. **Fetch Dependencies:**
   ```bash
   flutter pub get
   ```

3. **Launch the Application:**
   Ensure an emulator or physical device is connected, then run:
   ```bash
   flutter run
   ```

### Build Releases

*   **Android Release APK:**
    ```bash
    flutter build apk
    ```
*   **iOS Release Build:**
    ```bash
    flutter build ios
    ```

---

## 📸 Screenshots Section

*Add your app screenshots here once running on a simulated or physical device:*

| 👦 Kids Quiz Screen | 👩 Parents Quiz Screen | 📊 Score Card Dashboard |
|:---:|:---:|:---:|
| *[Screenshot Placeholder]* | *[Screenshot Placeholder]* | *[Screenshot Placeholder]* |

---

Developed with ❤️ for family learning.

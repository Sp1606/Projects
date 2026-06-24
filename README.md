# Shanmukha's Project Hub 🚀

Welcome to my personal project workspace! This repository contains a curated collection of Python projects spanning **Artificial Intelligence & Machine Learning**, **Interactive GUI Applications**, and **Arcade Games**.

---

## 📁 Repository Directory Structure

```text
Projects/
├── README.md               # Repository overview (this file)
├── .gitignore              # Ignored local files (.DS_Store, etc.)
├── project_venv/           # Python virtual environment containing packages
└── python_projects/
    └── Python/             # Folder containing all Python scripts and datasets
```

---

## 🤖 1. AI & Machine Learning Projects

These applications demonstrate data analysis, predictive modeling, computer vision, and NLP (Natural Language Processing).

*   **📊 AI-Driven Customer Segmentation** (`AI-DRIVEN CUSTOMER SEGMENTATION .py` & `End To End AI Powered Segmentation.py`)
    *   *Description:* Analyzes the `Mall_Customers.csv` dataset. Uses **K-Means Clustering**, **StandardScaler** scaling, and **PCA (Principal Component Analysis)** dimensionality reduction to group customers by spending behavior, visualized using Matplotlib and Seaborn.
*   **🎥 YouTube Video Summarizer** (`yt_video_summarizer.py`)
    *   *Description:* An automated script that downloads YouTube video audio using `yt_dlp`, transcribes the speech to text using `pydub` and the Python `SpeechRecognition` library, and then generates structured summaries using Hugging Face's `transformers` pipelines.
*   **✌️ ML Hand Gesture Recognition** (`ML Gesture.py`)
    *   *Description:* A computer vision script that uses OpenCV to capture real-time webcam feeds and training data, converting hand gestures to classify Rock, Paper, Scissors using a **K-Nearest Neighbors (KNN)** classifier.
*   **🌸 Iris Flower Classifier** (`Iris flower classifier.py`)
    *   *Description:* Implements a classic classification algorithm to categorize Iris species based on sepal and petal measurements.
*   **🎬 Movie Recommendation System** (`Movie recomendation system.py`)
    *   *Description:* Analyzes movie features and preferences to generate tailored recommendations.

---

## 🖥️ 2. Desktop & GUI Applications (Tkinter & Kivy)

Interactive tools designed with clean desktop user interfaces.

*   **💳 SQLite Expense Tracker** (`Expense Tracker App.py`)
    *   *Description:* A feature-rich desktop dashboard built with **Tkinter** and **SQLite**. Allows users to add income/expense transactions, specify categories, track monthly savings, and view graphical reports.
*   **🌦️ Weather Reporter App** (`Wheather APP.py`)
    *   *Description:* Interacts with weather APIs to display current temperatures, forecasts, and humidity details in a visual interface.
*   **🧩 CAPTCHA Generator** (`CAPTCHA Generator.py` & `captcha.png`)
    *   *Description:* Dynamically generates random alphanumeric text and distorts it into image formats to simulate security verification flows.
*   **🧮 Calculator & Currency Converter** (`Calculator App.py` & `currency calculatar.py`)
    *   *Description:* Desktop tools for performing everyday calculations and live currency exchanges.
*   **⏳ Waste Time Converter** (`waste time converter.py`)
    *   *Description:* A tracker designed to analyze, convert, and visualize time spent on unproductive tasks.

---

## 🎮 3. Interactive Games

Fun, interactive terminal and graphical games.

*   **🧩 Sudoku Solver & Game** (`sudoku_game.py` & `sudoku_logic.py`)
    *   *Description:* A fully playable Sudoku game built using Python, complete with backtracking board solving logic to help players check their moves or solve boards automatically.
*   **🪓 Hangman Game** (`Hangman.py`)
    *   *Description:* A terminal-based word-guessing game featuring classic hangman visuals.
*   **🎯 Classic Games Hub** (`games.py`)
    *   *Description:* A package of assorted classic minigames.

---

## 🛠️ Getting Started

To run these applications, ensure you have the virtual environment activated or install the required packages.

### Setting Up a Virtual Environment

1. **Activate the existing virtual environment:**
   * **macOS/Linux:**
     ```bash
     source project_venv/bin/activate
     ```
   * **Windows:**
     ```bash
     project_venv\Scripts\activate
     ```

2. **Install required packages (as needed per script):**
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn opencv-python speechrecognition pydub transformers yt-dlp Kivy
   ```

---

Developed with 💻 and 🐍.

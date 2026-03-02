import 'package:flutter/material.dart';
import 'kids_quiz_screen.dart';
import 'parents_quiz_screen.dart';

class ResultScreen extends StatelessWidget {
  final int score;
  final int total;
  final bool isLevelComplete;
  final String category;
  final int currentLevel;
  final bool isKids;

  const ResultScreen({
    super.key, 
    required this.score, 
    required this.total,
    this.isLevelComplete = false,
    this.category = 'Mixed',
    this.currentLevel = 1,
    this.isKids = true,
  });

  @override
  Widget build(BuildContext context) {
    final percentage = (score / total * 100).toInt();
    
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF6A11CB), Color(0xFF2575FC)],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(30.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  isLevelComplete ? 'Level Complete! 🏆' : 'Quiz Result',
                  style: const TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
                ),
                const SizedBox(height: 10),
                if (isLevelComplete)
                  const Text(
                    'Next level has been unlocked!',
                    style: TextStyle(color: Colors.amberAccent, fontWeight: FontWeight.bold),
                  ),
                const SizedBox(height: 40),
                Container(
                  padding: const EdgeInsets.all(40),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(color: Colors.black.withOpacity(0.2), blurRadius: 20, spreadRadius: 5),
                    ],
                  ),
                  child: Column(
                    children: [
                      Text(
                        '$percentage%',
                        style: const TextStyle(fontSize: 48, fontWeight: FontWeight.bold, color: Color(0xFF6A11CB)),
                      ),
                      Text(
                        '$score / $total',
                        style: const TextStyle(fontSize: 20, color: Colors.grey),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 40),
                _buildFeedbackText(percentage),
                const SizedBox(height: 60),
                if (isLevelComplete && currentLevel < 25 && category != 'Daily Challenge')
                  Padding(
                    padding: const EdgeInsets.only(bottom: 16.0),
                    child: SizedBox(
                      width: 250,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 20),
                          backgroundColor: Colors.green, // Correct = Green
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                          elevation: 5,
                        ),
                        onPressed: () {
                          Navigator.pushReplacement(
                            context,
                            MaterialPageRoute(
                              builder: (context) => isKids
                                ? KidsQuizScreen(category: category, level: currentLevel + 1)
                                : ParentsQuizScreen(category: category, level: currentLevel + 1),
                            ),
                          );
                        },
                        child: const Text('Next Level', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      ),
                    ),
                  )
                else if (!isLevelComplete && category != 'Daily Challenge')
                  Padding(
                    padding: const EdgeInsets.only(bottom: 16.0),
                    child: SizedBox(
                      width: 250,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 20),
                          backgroundColor: Colors.orange, // Wrong = Orange/Red
                          foregroundColor: Colors.white,
                          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                          elevation: 5,
                        ),
                        onPressed: () {
                          Navigator.pushReplacement(
                            context,
                            MaterialPageRoute(
                              builder: (context) => isKids
                                ? KidsQuizScreen(category: category, level: currentLevel)
                                : ParentsQuizScreen(category: category, level: currentLevel),
                            ),
                          );
                        },
                        child: const Text('Retry', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                      ),
                    ),
                  ),
                SizedBox(
                  width: 250,
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 20),
                      backgroundColor: Colors.white.withOpacity(0.2),
                      foregroundColor: Colors.white,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                      side: const BorderSide(color: Colors.white, width: 1),
                    ),
                    onPressed: () => Navigator.of(context).popUntil((route) => route.isFirst),
                    child: const Text('Back to Home', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildFeedbackText(int percentage) {
    String text;
    IconData icon;
    if (percentage >= 100) {
      text = 'Perfect Score! Next Level Awaits!';
      icon = Icons.star;
    } else if (percentage >= 80) {
      text = 'Excellent! You are a genius!';
      icon = Icons.emoji_events;
    } else if (percentage >= 50) {
      text = 'Good job! Keep it up!';
      icon = Icons.thumb_up;
    } else {
      text = 'Keep practicing, you can do it!';
      icon = Icons.psychology;
    }

    return Column(
      children: [
        Icon(icon, size: 60, color: Colors.white),
        const SizedBox(height: 10),
        Text(
          text,
          style: const TextStyle(fontSize: 22, color: Colors.white70),
          textAlign: TextAlign.center,
        ),
      ],
    );
  }
}

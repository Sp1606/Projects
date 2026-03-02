import '../models/question_model.dart';

class QuestionGenerator {
  static List<Question> generateMathQuestions() {
    List<Question> questions = [];
    
    for (int level = 1; level <= 50; level++) {
      if (level <= 10) {
        for (int i = 0; i < 5; i++) {
          int a = level + 4 + i;
          int b = level + 2 + (i % 2);
          int ans = a + b;
          questions.add(Question(
            questionText: 'Level $level: What is $a + $b?',
            options: [ans.toString(), (ans - 2).toString(), (ans + 5).toString(), (ans + 1).toString()],
            correctAnswerIndex: 0, // Initial index, will be shuffled
            category: 'Math',
            level: level,
            minAge: 4,
            maxAge: 8,
            explanation: '$a plus $b is $ans!',
          ));
        }
      } else if (level <= 20) {
        int a = level * 2;
        int b = level;
        int ans = a - b;
        questions.add(Question(
          questionText: 'Level $level: What is $a - $b?',
          options: [(ans + 1).toString(), (ans - 1).toString(), ans.toString(), (ans + 10).toString()],
          correctAnswerIndex: 2,
          category: 'Math',
          level: level,
          minAge: 7,
          maxAge: 12,
        ));
      } else {
        int a = level;
        int b = 5;
        int ans = a * b;
        questions.add(Question(
          questionText: 'Level $level: What is $a times $b?',
          options: [ans.toString(), (ans - 5).toString(), (ans + 10).toString(), (ans + 5).toString()],
          correctAnswerIndex: 0,
          category: 'Math',
          level: level,
          minAge: 9,
          maxAge: 15,
        ));
      }
    }
    return questions;
  }

  /// Shuffles options and returns a new Question object with the updated index
  static Question shuffleOptions(Question q) {
    String correctOption = q.options[q.correctAnswerIndex];
    List<String> shuffledOptions = List<String>.from(q.options)..shuffle();
    int newIndex = shuffledOptions.indexOf(correctOption);
    
    return Question(
      questionText: q.questionText,
      options: shuffledOptions,
      correctAnswerIndex: newIndex,
      category: q.category,
      explanation: q.explanation,
      difficulty: q.difficulty,
      level: q.level,
      minAge: q.minAge,
      maxAge: q.maxAge,
    );
  }
}

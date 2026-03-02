class Question {
  final String questionText;
  final List<String> options;
  final int correctAnswerIndex;
  final String category;
  final String explanation;
  final int difficulty; // 1: Easy, 2: Medium, 3: Hard
  final int level; // 1-50
  final int minAge;
  final int maxAge;

  Question({
    required this.questionText,
    required this.options,
    required this.correctAnswerIndex,
    required this.category,
    this.explanation = '',
    this.difficulty = 1,
    this.level = 1,
    this.minAge = 0,
    this.maxAge = 100,
  });
}
import 'dart:convert';

class QuizAttempt {
  final String category;
  final int score;
  final int total;
  final DateTime date;

  QuizAttempt({
    required this.category,
    required this.score,
    required this.total,
    required this.date,
  });

  Map<String, dynamic> toMap() {
    return {
      'category': category,
      'score': score,
      'total': total,
      'date': date.toIso8601String(),
    };
  }

  factory QuizAttempt.fromMap(Map<String, dynamic> map) {
    return QuizAttempt(
      category: map['category'],
      score: map['score'],
      total: map['total'],
      date: DateTime.parse(map['date']),
    );
  }
}

class UserProfile {
  final String name;
  final String email;
  final String password;
  final String phone;
  final int age;
  final Map<String, int> unlockedLevels; // Category -> Max Unlocked Level
  final List<QuizAttempt> quizHistory;

  UserProfile({
    required this.name,
    required this.email,
    required this.password,
    required this.phone,
    this.age = 0,
    this.unlockedLevels = const {},
    this.quizHistory = const [],
  });

  Map<String, dynamic> toMap() {
    return {
      'name': name,
      'email': email,
      'password': password,
      'phone': phone,
      'age': age,
      'unlockedLevels': unlockedLevels,
      'quizHistory': quizHistory.map((x) => x.toMap()).toList(),
    };
  }

  factory UserProfile.fromMap(Map<String, dynamic> map) {
    var historyList = map['quizHistory'] as List<dynamic>?;
    var rawUnlocked = map['unlockedLevels'] as Map<dynamic, dynamic>? ?? {};
    
    return UserProfile(
      name: map['name'] ?? '',
      email: map['email'] ?? '',
      password: map['password'] ?? '',
      phone: map['phone'] ?? '',
      age: map['age'] ?? 0,
      unlockedLevels: rawUnlocked.map((k, v) => MapEntry(k.toString(), v as int)),
      quizHistory: historyList?.map((x) => QuizAttempt.fromMap(x as Map<String, dynamic>)).toList() ?? [],
    );
  }
}

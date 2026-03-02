import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';

class AuthService {
  static const String _activeUserKey = 'active_user_email';
  static const String _usersDbKey = 'users_database';

  // Save/Update user in the main database
  Future<void> saveUserToDb(UserProfile user) async {
    final prefs = await SharedPreferences.getInstance();
    final dbJson = prefs.getString(_usersDbKey) ?? '{}';
    final Map<String, dynamic> db = jsonDecode(dbJson);
    
    db[user.email] = user.toMap();
    await prefs.setString(_usersDbKey, jsonEncode(db));
  }

  // Set the active session
  Future<void> setActiveUser(String email) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_activeUserKey, email);
  }

  // Get active user profile
  Future<UserProfile?> getUser() async {
    final prefs = await SharedPreferences.getInstance();
    final email = prefs.getString(_activeUserKey);
    if (email == null) return null;

    final dbJson = prefs.getString(_usersDbKey) ?? '{}';
    final Map<String, dynamic> db = jsonDecode(dbJson);
    
    if (db.containsKey(email)) {
      return UserProfile.fromMap(db[email]);
    }
    return null;
  }

  // Verify credentials and login
  Future<UserProfile?> login(String email, String password) async {
    final prefs = await SharedPreferences.getInstance();
    final dbJson = prefs.getString(_usersDbKey) ?? '{}';
    final Map<String, dynamic> db = jsonDecode(dbJson);

    if (db.containsKey(email)) {
      final user = UserProfile.fromMap(db[email]);
      if (user.password == password) {
        await setActiveUser(email);
        return user;
      }
    }
    return null;
  }

  Future<void> addQuizAttempt(QuizAttempt attempt) async {
    final user = await getUser();
    if (user != null) {
      final updatedHistory = List<QuizAttempt>.from(user.quizHistory)..add(attempt);
      final updatedUser = UserProfile(
        name: user.name,
        email: user.email,
        password: user.password,
        phone: user.phone,
        age: user.age,
        unlockedLevels: user.unlockedLevels,
        quizHistory: updatedHistory,
      );
      await saveUserToDb(updatedUser);
    }
  }

  Future<void> unlockNextLevel(String category, int completedLevel) async {
    final user = await getUser();
    if (user != null) {
      final currentMax = user.unlockedLevels[category] ?? 1;
      if (completedLevel >= currentMax && completedLevel < 25) {
        final updatedLevels = Map<String, int>.from(user.unlockedLevels);
        updatedLevels[category] = completedLevel + 1;
        print('UNLOCKED: $category Level ${completedLevel + 1}');
        
        final updatedUser = UserProfile(
          name: user.name,
          email: user.email,
          password: user.password,
          phone: user.phone,
          age: user.age,
          unlockedLevels: updatedLevels,
          quizHistory: user.quizHistory,
        );
        await saveUserToDb(updatedUser);
      }
    }
  }

  Future<bool> isLoggedIn() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey(_activeUserKey);
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_activeUserKey);
  }
}

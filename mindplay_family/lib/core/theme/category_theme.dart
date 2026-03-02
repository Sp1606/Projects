import 'package:flutter/material.dart';

class CategoryTheme {
  final Color primaryColor;
  final Color secondaryColor;
  final Color accentColor;
  final String? imagePath;

  CategoryTheme({
    required this.primaryColor,
    required this.secondaryColor,
    required this.accentColor,
    this.imagePath,
  });

  static Map<String, CategoryTheme> kidsThemes = {
    'Math': CategoryTheme(
      primaryColor: const Color(0xFFE3F2FD),
      secondaryColor: const Color(0xFFF3E5F5),
      accentColor: Colors.blueAccent,
      imagePath: 'assets/images/math_kids.png',
    ),
    'Science': CategoryTheme(
      primaryColor: const Color(0xFFE0F2F1),
      secondaryColor: const Color(0xFFFFF9C4),
      accentColor: Colors.teal,
      imagePath: 'assets/images/science_kids.png',
    ),
    'Geography': CategoryTheme(
      primaryColor: const Color(0xFFE8F5E9),
      secondaryColor: const Color(0xFFC8E6C9),
      accentColor: Colors.green,
    ),
    'Arts': CategoryTheme(
      primaryColor: const Color(0xFFFFF3E0),
      secondaryColor: const Color(0xFFFFE0B2),
      accentColor: Colors.orangeAccent,
    ),
    'History': CategoryTheme(
      primaryColor: const Color(0xFFFBE9E7),
      secondaryColor: const Color(0xFFEFEBE9),
      accentColor: Colors.deepOrangeAccent,
    ),
    'Mixed': CategoryTheme(
      primaryColor: const Color(0xFFF3E5F5),
      secondaryColor: const Color(0xFFE1F5FE),
      accentColor: Colors.purpleAccent,
    ),
  };

  static Map<String, CategoryTheme> parentsThemes = {
    'Science': CategoryTheme(
      primaryColor: const Color(0xFF1A237E),
      secondaryColor: const Color(0xFF0D47A1),
      accentColor: Colors.cyanAccent,
    ),
    'Technology': CategoryTheme(
      primaryColor: const Color(0xFF212121),
      secondaryColor: const Color(0xFF424242),
      accentColor: Colors.blueGrey,
    ),
    'History': CategoryTheme(
      primaryColor: const Color(0xFF263238),
      secondaryColor: const Color(0xFF37474F),
      accentColor: Colors.amberAccent,
    ),
    'Geography': CategoryTheme(
      primaryColor: const Color(0xFF004D40),
      secondaryColor: const Color(0xFF00695C),
      accentColor: Colors.tealAccent,
    ),
    'Mixed': CategoryTheme(
      primaryColor: const Color(0xFF1B5E20),
      secondaryColor: const Color(0xFF2E7D32),
      accentColor: Colors.lightGreenAccent,
    ),
    'Daily Challenge': CategoryTheme(
      primaryColor: const Color(0xFF311B92),
      secondaryColor: const Color(0xFF4527A0),
      accentColor: Colors.pinkAccent,
    ),
  };

  static CategoryTheme getTheme(String category, bool forKids) {
    if (forKids) {
      return kidsThemes[category] ?? kidsThemes['Mixed']!;
    } else {
      return parentsThemes[category] ?? parentsThemes['Mixed']!;
    }
  }
}

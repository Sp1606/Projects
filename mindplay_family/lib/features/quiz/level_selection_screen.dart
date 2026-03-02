import 'package:flutter/material.dart';
import '../../core/models/user_model.dart';
import '../../core/services/auth_service.dart';
import '../../core/theme/category_theme.dart';
import 'kids_quiz_screen.dart';
import 'parents_quiz_screen.dart';

class LevelSelectionScreen extends StatefulWidget {
  final String category;
  final bool isKids;

  const LevelSelectionScreen({
    super.key,
    required this.category,
    required this.isKids,
  });

  @override
  State<LevelSelectionScreen> createState() => _LevelSelectionScreenState();
}

class _LevelSelectionScreenState extends State<LevelSelectionScreen> {
  final _authService = AuthService();
  UserProfile? _user;
  late CategoryTheme _theme;

  @override
  void initState() {
    super.initState();
    _theme = CategoryTheme.getTheme(widget.category, widget.isKids);
    _loadUser();
  }

  Future<void> _loadUser() async {
    final user = await _authService.getUser();
    setState(() {
      _user = user;
    });
  }

  @override
  Widget build(BuildContext context) {
    final unlockedLevel = _user?.unlockedLevels[widget.category] ?? 1;

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [_theme.primaryColor, _theme.secondaryColor],
          ),
        ),
        child: SafeArea(
          child: Column(
            children: [
              _buildHeader(),
              Expanded(
                child: Container(
                  margin: const EdgeInsets.only(top: 20),
                  padding: const EdgeInsets.all(20),
                  decoration: const BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.only(
                      topLeft: Radius.circular(30),
                      topRight: Radius.circular(30),
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 10),
                        child: Text(
                          'Select Level',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                            color: _theme.primaryColor,
                          ),
                        ),
                      ),
                      Expanded(
                        child: GridView.builder(
                          padding: const EdgeInsets.all(10),
                          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                            crossAxisCount: 5,
                            mainAxisSpacing: 15,
                            crossAxisSpacing: 15,
                          ),
                          itemCount: 25,
                          itemBuilder: (context, index) {
                            final level = index + 1;
                            final isUnlocked = level <= unlockedLevel;
                            return _buildLevelButton(level, isUnlocked);
                          },
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back_ios, color: Colors.white),
            onPressed: () => Navigator.pop(context),
          ),
          const SizedBox(width: 10),
          Text(
            widget.category,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLevelButton(int level, bool isUnlocked) {
    return GestureDetector(
      onTap: isUnlocked ? () => _startQuiz(level) : null,
      child: Container(
        decoration: BoxDecoration(
          color: isUnlocked ? _theme.accentColor : Colors.grey[200],
          borderRadius: BorderRadius.circular(15),
          boxShadow: isUnlocked ? [
            BoxShadow(
              color: _theme.accentColor.withOpacity(0.3),
              blurRadius: 8,
              offset: const Offset(0, 4),
            )
          ] : [],
        ),
        child: Center(
          child: isUnlocked 
            ? Text(
                '$level',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              )
            : Icon(Icons.lock_outline, color: Colors.grey[400], size: 20),
        ),
      ),
    );
  }

  void _startQuiz(int level) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => widget.isKids
          ? KidsQuizScreen(category: widget.category, level: level)
          : ParentsQuizScreen(category: widget.category, level: level),
      ),
    ).then((_) => _loadUser());
  }
}

import 'package:flutter/material.dart';
import '../../core/data/quiz_data.dart';
import '../../core/data/question_generator.dart';
import '../../core/models/question_model.dart';
import '../../core/models/user_model.dart';
import '../../core/services/auth_service.dart';
import '../../core/theme/category_theme.dart';
import 'result_screen.dart';

class ParentsQuizScreen extends StatefulWidget {
  final String category;
  final int level;

  const ParentsQuizScreen({
    super.key, 
    this.category = 'Mixed',
    this.level = 1,
  });

  @override
  State<ParentsQuizScreen> createState() => _ParentsQuizScreenState();
}

class _ParentsQuizScreenState extends State<ParentsQuizScreen> {
  late int _currentLevel;
  int _questionIndexInLevel = 0;
  int _totalScore = 0;
  bool _isSubmitted = false;
  int? _selectedIndex;
  List<Question>? _currentLevelQuestions;
  late CategoryTheme _theme;
  final _authService = AuthService();
  UserProfile? _user;

  @override
  void initState() {
    super.initState();
    _currentLevel = widget.level;
    _theme = CategoryTheme.getTheme(widget.category, false);
    _initializeQuiz();
  }

  Future<void> _initializeQuiz() async {
    _user = await _authService.getUser();
    final filtered = QuizData.getFilteredQuestions(
      category: widget.category,
      forKids: false,
      level: _currentLevel,
      age: _user?.age ?? 30,
      isDaily: widget.category == 'Daily Challenge',
    );

    setState(() {
      _currentLevelQuestions = filtered.map((q) => QuestionGenerator.shuffleOptions(q)).toList();
    });
  }

  void _finishQuiz() async {
    final questions = _currentLevelQuestions;
    if (questions == null) return;

    final attempt = QuizAttempt(
      category: widget.category,
      score: _totalScore,
      total: questions.length,
      date: DateTime.now(),
    );
    await _authService.addQuizAttempt(attempt);

    bool unlocked = false;
    final isPass = _totalScore / questions.length >= 0.7;
    if (isPass && widget.category != 'Daily Challenge') {
      await _authService.unlockNextLevel(widget.category, _currentLevel);
      unlocked = true;
    }
    
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            score: _totalScore, 
            total: questions.length,
            isLevelComplete: unlocked,
            category: widget.category,
            currentLevel: _currentLevel,
            isKids: false,
          ),
        ),
      );
    }
  }

  void _submitAnswer() {
    final questions = _currentLevelQuestions;
    if (_selectedIndex == null || _isSubmitted || questions == null) return;

    setState(() {
      _isSubmitted = true;
      if (_selectedIndex == questions[_questionIndexInLevel].correctAnswerIndex) {
        _totalScore++;
      }
    });

    Future.delayed(const Duration(seconds: 1), () {
      if (mounted) _finishQuiz();
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_user == null || _currentLevelQuestions == null) {
      return const Scaffold(backgroundColor: Color(0xFF0F1113), body: Center(child: CircularProgressIndicator()));
    }

    final questions = _currentLevelQuestions!;
    if (questions.isEmpty) {
      return Scaffold(
        backgroundColor: const Color(0xFF0F1113),
        appBar: AppBar(title: Text(widget.category), backgroundColor: Colors.transparent),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('Level updates coming soon!', style: TextStyle(color: Colors.white70)),
              const SizedBox(height: 20),
              ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text('Return')),
            ],
          ),
        ),
      );
    }

    final question = questions[_questionIndexInLevel];

    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topRight,
            end: Alignment.bottomLeft,
            colors: [_theme.primaryColor, _theme.secondaryColor],
          ),
        ),
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(24.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                _buildHeader(),
                const SizedBox(height: 20),
                _buildProgressIndicator(),
                const SizedBox(height: 30),
                _buildQuestionCard(question),
                const SizedBox(height: 40),
                Expanded(
                  child: ListView.builder(
                    itemCount: question.options.length,
                    itemBuilder: (context, index) => _buildOptionButton(index, question.options[index], question.correctAnswerIndex),
                  ),
                ),
                const SizedBox(height: 20),
                _buildSubmitButton(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  // Helper removed

  Widget _buildProgressIndicator() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        Text(
          widget.category == 'Daily Challenge' ? 'ONE SHOT MIXER' : 'LEVEL $_currentLevel: QUESTION ${_questionIndexInLevel + 1}/${_currentLevelQuestions?.length ?? 0}',
          style: const TextStyle(color: Colors.white, fontSize: 11, letterSpacing: 1.5, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 10),
        ClipRRect(
          borderRadius: BorderRadius.circular(4),
          child: LinearProgressIndicator(
            value: (_questionIndexInLevel + 1) / (_currentLevelQuestions?.length ?? 1),
            backgroundColor: Colors.white.withOpacity(0.15),
            valueColor: AlwaysStoppedAnimation<Color>(_theme.accentColor),
            minHeight: 6,
          ),
        ),
      ],
    );
  }

  Widget _buildHeader() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.white70),
          onPressed: () => Navigator.pop(context),
        ),
        Text(
          'SCORE: $_totalScore',
          style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, letterSpacing: 1.2),
        ),
        IconButton(
          icon: const Icon(Icons.info_outline, color: Colors.white60),
          onPressed: () {},
        ),
      ],
    );
  }

  Widget _buildQuestionCard(Question question) {
    return Container(
      padding: const EdgeInsets.all(32),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.white.withOpacity(0.1)),
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.stars, size: 14, color: _theme.accentColor),
              const SizedBox(width: 8),
              Text(
                '${question.category.toUpperCase()} • ${widget.category == "Daily Challenge" ? "DAILY" : "LEVEL $_currentLevel"}',
                style: TextStyle(color: _theme.accentColor, letterSpacing: 2, fontSize: 10, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          const SizedBox(height: 24),
          Text(
            question.questionText,
            style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Colors.white, height: 1.4),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildOptionButton(int index, String text, int correctIndex) {
    Color borderColor = Colors.white.withOpacity(0.4);
    Color? fillColor;
    IconData? feedbackIcon;

    if (_isSubmitted) {
      if (index == correctIndex) {
        borderColor = Colors.greenAccent;
        fillColor = Colors.greenAccent.withOpacity(0.1);
        feedbackIcon = Icons.check_circle_outline;
      } else if (index == _selectedIndex) {
        borderColor = Colors.redAccent;
        fillColor = Colors.redAccent.withOpacity(0.1);
        feedbackIcon = Icons.highlight_off;
      }
    } else if (_selectedIndex == index) {
      borderColor = _theme.accentColor;
      fillColor = _theme.accentColor.withOpacity(0.15);
    }

    return Padding(
      padding: const EdgeInsets.only(bottom: 16.0),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        child: OutlinedButton(
          style: OutlinedButton.styleFrom(
            padding: const EdgeInsets.all(22),
            side: BorderSide(color: borderColor, width: 1.5),
            backgroundColor: fillColor,
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          ),
          onPressed: _isSubmitted ? null : () => setState(() => _selectedIndex = index),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(child: Text(text, style: const TextStyle(fontSize: 17, color: Colors.white, fontWeight: FontWeight.w500))),
              if (feedbackIcon != null) Icon(feedbackIcon, color: borderColor, size: 20),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSubmitButton() {
    return SizedBox(
      width: double.infinity,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: _theme.accentColor,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(vertical: 20),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)), // More premium rounded for parents
          elevation: 5,
        ),
        onPressed: (_selectedIndex == null || _isSubmitted) ? null : _submitAnswer,
        child: const Text('SUBMIT ANSWER', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, letterSpacing: 2)),
      ),
    );
  }
}

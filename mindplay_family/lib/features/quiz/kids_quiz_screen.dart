import 'package:flutter/material.dart';
import '../../core/data/quiz_data.dart';
import '../../core/data/question_generator.dart';
import '../../core/models/question_model.dart';
import '../../core/models/user_model.dart';
import '../../core/services/auth_service.dart';
import '../../core/theme/category_theme.dart';
import 'result_screen.dart';

class KidsQuizScreen extends StatefulWidget {
  final String category;
  final int level;

  const KidsQuizScreen({
    super.key, 
    this.category = 'Mixed',
    this.level = 1,
  });

  @override
  State<KidsQuizScreen> createState() => _KidsQuizScreenState();
}

class _KidsQuizScreenState extends State<KidsQuizScreen> {
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
    _theme = CategoryTheme.getTheme(widget.category, true);
    _initializeQuiz();
  }

  Future<void> _initializeQuiz() async {
    _user = await _authService.getUser();
    final age = _user?.age ?? 10;
    
    final filtered = QuizData.getFilteredQuestions(
      category: widget.category,
      forKids: true,
      level: _currentLevel,
      age: age,
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

    final isPass = _totalScore / questions.length >= 0.7;
    if (isPass && widget.category != 'Daily Challenge') {
      await _authService.unlockNextLevel(widget.category, _currentLevel);
    }
    
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => ResultScreen(
            score: _totalScore, 
            total: questions.length,
            isLevelComplete: isPass,
            category: widget.category,
            currentLevel: _currentLevel,
            isKids: true,
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
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }
    
    final questions = _currentLevelQuestions!;
    if (questions.isEmpty) {
      return Scaffold(
        appBar: AppBar(title: Text(widget.category)),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text('No more questions for this level yet!'),
              const SizedBox(height: 20),
              ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text('Go Back')),
            ],
          ),
        ),
      );
    }

    final question = questions[_questionIndexInLevel];

    return Scaffold(
      backgroundColor: _theme.primaryColor,
      body: Container(
        width: double.infinity,
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
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
                const SizedBox(height: 10),
                _buildProgressBar(),
                const SizedBox(height: 20),
                if (_theme.imagePath != null)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 20.0),
                    child: Image.asset(_theme.imagePath!, height: 160, fit: BoxFit.contain),
                  ),
                _buildQuestionCard(question),
                const SizedBox(height: 30),
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

  Widget _buildProgressBar() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(widget.category == 'Daily Challenge' ? 'One Shot Challenge' : 'Level $_currentLevel Progress', 
          style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold)),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(10),
          child: LinearProgressIndicator(
            value: (_questionIndexInLevel + 1) / (_currentLevelQuestions?.length ?? 1),
            backgroundColor: Colors.black.withOpacity(0.15),
            valueColor: AlwaysStoppedAnimation<Color>(_theme.accentColor),
            minHeight: 10,
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
          icon: const Icon(Icons.close, color: Colors.white),
          onPressed: () => Navigator.pop(context),
        ),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.3),
            borderRadius: BorderRadius.circular(20),
          ),
          child: Text(
            widget.category == 'Daily Challenge' ? 'Daily' : 'Level $_currentLevel',
            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
          ),
        ),
        Text(
          'Age: ${_user?.age ?? "?"}',
          style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  Widget _buildQuestionCard(Question question) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(25),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 15, offset: const Offset(0, 5)),
        ],
      ),
      child: Column(
        children: [
          Text(
            'QUESTION ${_questionIndexInLevel + 1}',
            style: TextStyle(color: _theme.accentColor.withOpacity(0.5), fontWeight: FontWeight.bold, letterSpacing: 1.2),
          ),
          const SizedBox(height: 12),
          Text(
            question.questionText,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: Color(0xFF2D3142)),
            textAlign: TextAlign.center,
          ),
          if (_isSubmitted && question.explanation.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 16.0),
              child: Text(
                question.explanation,
                style: TextStyle(color: Colors.blueGrey.shade600, fontSize: 14, fontStyle: FontStyle.italic),
                textAlign: TextAlign.center,
              ),
            ),
        ],
      ),
    );
  }

  Widget _buildOptionButton(int index, String text, int correctIndex) {
    Color buttonColor = Colors.white;
    Color textColor = const Color(0xFF4F5D75);
    IconData? feedbackIcon;

    if (_isSubmitted) {
      if (index == correctIndex) {
        buttonColor = const Color(0xFFE8F5E9);
        textColor = const Color(0xFF2E7D32);
        feedbackIcon = Icons.check_circle_rounded;
      } else if (index == _selectedIndex) {
        buttonColor = const Color(0xFFFFEBEE);
        textColor = const Color(0xFFC62828);
        feedbackIcon = Icons.cancel_rounded;
      }
    } else if (_selectedIndex == index) {
      buttonColor = _theme.accentColor.withOpacity(0.1);
      textColor = _theme.accentColor;
    }

    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 20),
          backgroundColor: buttonColor,
          foregroundColor: textColor,
          elevation: _isSubmitted ? 0 : 2,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
          side: _selectedIndex == index && !_isSubmitted
              ? BorderSide(color: _theme.accentColor, width: 2)
              : BorderSide.none,
        ),
        onPressed: _isSubmitted ? null : () => setState(() => _selectedIndex = index),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Expanded(child: Text(text, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w600))),
            if (feedbackIcon != null) Icon(feedbackIcon, color: textColor),
          ],
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
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
          elevation: 5,
        ),
        onPressed: (_selectedIndex == null || _isSubmitted) ? null : _submitAnswer,
        child: const Text('SUBMIT', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, letterSpacing: 2)),
      ),
    );
  }
}

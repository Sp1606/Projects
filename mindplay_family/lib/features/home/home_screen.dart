import 'package:flutter/material.dart';
import '../quiz/kids_quiz_screen.dart';
import '../quiz/parents_quiz_screen.dart';
import '../quiz/level_selection_screen.dart';
import '../auth/login_screen.dart';
import '../quiz/score_card.dart';
import '../quiz/online_quiz_flow.dart';
import '../../core/data/quiz_data.dart';
import '../../core/services/auth_service.dart';
import '../../core/models/user_model.dart';
import '../../core/theme/category_theme.dart';

class HomeScreen extends StatefulWidget {
  final String userName;

  const HomeScreen({super.key, this.userName = 'Explorer'});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  UserProfile? _user;
  bool _isKidsMode = true;
  DateTime _selectedDate = DateTime.now();
  final _authService = AuthService();

  @override
  void initState() {
    super.initState();
    _loadUser();
  }

  Future<void> _loadUser() async {
    final user = await _authService.getUser();
    if (mounted) {
      setState(() {
        _user = user;
      });
    }
  }

  void _logout(BuildContext context) async {
    await _authService.logout();
    if (context.mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(builder: (context) => const LoginScreen()),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8F9FE),
      drawer: _buildDrawer(context),
      body: CustomScrollView(
        slivers: [
          _buildSliverAppBar(context),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildModeToggle(),
                  const SizedBox(height: 24),
                  _buildDailyChallengeCard(context),
                  const SizedBox(height: 32),
                  Text(
                    _isKidsMode ? 'Kids Learning Quest' : 'Parents Discovery Journey',
                    style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold, color: Color(0xFF1A1C1E)),
                  ),
                  const SizedBox(height: 16),
                  _buildCategoryList(context, _isKidsMode),
                  const SizedBox(height: 32),
                  _buildOnlinePlayCard(context),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDrawer(BuildContext context) {
    return Drawer(
      child: Column(
        children: [
          UserAccountsDrawerHeader(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                colors: [Color(0xFF6A11CB), Color(0xFF2575FC)],
              ),
            ),
            currentAccountPicture: CircleAvatar(
              backgroundColor: Colors.white,
              child: Text(
                widget.userName.isNotEmpty ? widget.userName[0].toUpperCase() : 'U',
                style: const TextStyle(fontSize: 40.0, color: Color(0xFF6A11CB)),
              ),
            ),
            accountName: Text(widget.userName),
            accountEmail: Text(_user?.email ?? 'Loading...'),
            otherAccountsPictures: [
              if (_user?.phone != null)
                const Icon(Icons.phone, color: Colors.white, size: 20),
            ],
          ),
          ListTile(
            leading: const Icon(Icons.person),
            title: const Text('My Profile'),
            subtitle: Text(_user?.phone ?? ''),
            onTap: () {},
          ),
          ListTile(
            leading: const Icon(Icons.history),
            title: const Text('Quiz History'),
            subtitle: Text('${_user?.quizHistory.length ?? 0} quizzes completed'),
            onTap: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => const ScoreCardScreen()));
            },
          ),
          ListTile(
            leading: const Icon(Icons.settings),
            title: const Text('Settings'),
            onTap: () {},
          ),
          const Divider(),
          ListTile(
            leading: const Icon(Icons.logout, color: Colors.red),
            title: const Text('Logout', style: TextStyle(color: Colors.red)),
            onTap: () => _logout(context),
          ),
        ],
      ),
    );
  }

  Widget _buildSliverAppBar(BuildContext context) {
    return SliverAppBar(
      expandedHeight: 180,
      floating: false,
      pinned: true,
      backgroundColor: const Color(0xFF6A11CB),
      iconTheme: const IconThemeData(color: Colors.white),
      actions: [
        Padding(
          padding: const EdgeInsets.only(right: 16.0),
          child: CircleAvatar(
            radius: 18,
            backgroundColor: Colors.white.withOpacity(0.2),
            child: Text(
              widget.userName.isNotEmpty ? widget.userName[0].toUpperCase() : 'U',
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            ),
          ),
        ),
      ],
      flexibleSpace: FlexibleSpaceBar(
        background: Container(
          decoration: const BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment.topLeft,
              end: Alignment.bottomRight,
              colors: [Color(0xFF6A11CB), Color(0xFF2575FC)],
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.fromLTRB(24, 60, 24, 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                Text(
                  'Hello, ${widget.userName}!',
                  style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 4),
                const Text(
                  'What are we learning today?',
                  style: TextStyle(color: Colors.white70, fontSize: 16),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildModeToggle() {
    return Container(
      padding: const EdgeInsets.all(4),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.05), blurRadius: 10)],
      ),
      child: Row(
        children: [
          _modeButton('Kids', _isKidsMode, Icons.child_care),
          _modeButton('Parents', !_isKidsMode, Icons.person),
        ],
      ),
    );
  }

  Widget _modeButton(String label, bool active, IconData icon) {
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => _isKidsMode = label == 'Kids'),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: active ? (label == 'Kids' ? const Color(0xFFFF9966) : const Color(0xFF6A11CB)) : Colors.transparent,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, color: active ? Colors.white : Colors.grey, size: 20),
              const SizedBox(width: 8),
              Text(
                label,
                style: TextStyle(
                  color: active ? Colors.white : Colors.grey,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _getFormattedDate(DateTime date) {
    final months = [
      'Jan', 'Feb', 'March', 'April', 'May', 'June',
      'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec'
    ];
    return '${months[date.month - 1]} ${date.day}';
  }

  void _selectDate(BuildContext context) async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _selectedDate,
      firstDate: DateTime(2024),
      lastDate: DateTime.now(),
    );
    if (picked != null && picked != _selectedDate) {
      setState(() {
        _selectedDate = picked;
      });
    }
  }

  Widget _buildDailyChallengeCard(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: _isKidsMode 
            ? [const Color(0xFFFF9966), const Color(0xFFFF5E62)]
            : [const Color(0xFF6A11CB), const Color(0xFF2575FC)],
        ),
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(color: Colors.black.withOpacity(0.1), blurRadius: 20, offset: const Offset(0, 10)),
        ],
      ),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('DAILY CHALLENGE', style: TextStyle(color: Colors.white70, fontWeight: FontWeight.bold, fontSize: 12, letterSpacing: 1.2)),
              IconButton(
                onPressed: () => _selectDate(context),
                icon: const Icon(Icons.calendar_month, color: Colors.white70),
                tooltip: 'History',
              ),
            ],
          ),
          const SizedBox(height: 8),
          Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${_getFormattedDate(_selectedDate)} Mixer',
                      style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 22),
                    ),
                    const SizedBox(height: 16),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white, 
                        foregroundColor: _isKidsMode ? const Color(0xFFFF5E62) : const Color(0xFF6A11CB)
                      ),
                      onPressed: () => Navigator.push(
                        context, 
                        MaterialPageRoute(
                          builder: (_) => _isKidsMode 
                            ? const KidsQuizScreen(category: 'Daily Challenge')
                            : const ParentsQuizScreen(category: 'Daily Challenge')
                        )
                      ),
                      child: const Text('Start Now'),
                    ),
                  ],
                ),
              ),
              const Icon(Icons.bolt, size: 80, color: Colors.white24),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildOnlinePlayCard(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: const Color(0xFFE0E0E0)),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 10)],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: const Color(0xFFE3F2FD),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.public, color: Color(0xFF1976D2)),
          ),
          const SizedBox(width: 16),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Online Multiplayer', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                Text('Challenge players worldwide!', style: TextStyle(color: Colors.grey, fontSize: 13)),
              ],
            ),
          ),
          TextButton(
            onPressed: () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => const OnlineQuizFlow()));
            },
            child: const Text('JOIN'),
          ),
        ],
      ),
    );
  }

  Widget _buildCategoryList(BuildContext context, bool forKids) {
    final categories = forKids 
      ? QuizData.categories.where((c) => c != 'Daily Challenge').toList()
      : QuizData.categories.where((c) => c != 'Math').toList();

    return SizedBox(
      height: 160,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: categories.length,
        itemBuilder: (context, index) {
          final category = categories[index];
          final theme = CategoryTheme.getTheme(category, forKids);
          final currentLevel = (_user?.unlockedLevels[category]) ?? 1;
          
          return GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => LevelSelectionScreen(
                    category: category,
                    isKids: forKids,
                  ),
                ),
              ).then((_) => _loadUser());
            },
            child: Container(
              width: 130,
              margin: const EdgeInsets.only(right: 16),
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [theme.primaryColor, theme.secondaryColor],
                ),
                borderRadius: BorderRadius.circular(20),
                boxShadow: [
                  BoxShadow(color: theme.accentColor.withOpacity(0.1), blurRadius: 10, offset: const Offset(0, 4)),
                ],
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.5),
                      shape: BoxShape.circle,
                    ),
                    child: Icon(_getCategoryIcon(category), color: theme.accentColor, size: 28),
                  ),
                  const SizedBox(height: 12),
                  Text(
                    category,
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: theme.accentColor.withOpacity(0.8),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: theme.accentColor.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      'Level $currentLevel',
                      style: TextStyle(
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                        color: theme.accentColor,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  IconData _getCategoryIcon(String category) {
    switch (category) {
      case 'Math': return Icons.calculate;
      case 'Science': return Icons.science;
      case 'History': return Icons.history_edu;
      case 'Geography': return Icons.public;
      case 'Arts': return Icons.palette;
      case 'Technology': return Icons.terminal;
      case 'Mixed': return Icons.auto_awesome;
      default: return Icons.category;
    }
  }
}
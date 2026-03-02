import 'package:flutter/material.dart';
import '../../core/models/user_model.dart';
import '../../core/services/auth_service.dart';

class ScoreCardScreen extends StatelessWidget {
  const ScoreCardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Score Card & History'),
        backgroundColor: const Color(0xFF6A11CB),
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<UserProfile?>(
        future: AuthService().getUser(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          
          final user = snapshot.data;
          if (user == null || user.quizHistory.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.quiz_outlined, size: 80, color: Colors.grey),
                  SizedBox(height: 16),
                  Text('No quiz history yet. Start playing!', style: TextStyle(color: Colors.grey)),
                ],
              ),
            );
          }

          final history = user.quizHistory.reversed.toList();

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: history.length,
            itemBuilder: (context, index) {
              final attempt = history[index];
              final percentage = (attempt.score / attempt.total * 100).toInt();
              
              return Card(
                margin: const EdgeInsets.only(bottom: 16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
                child: ListTile(
                  contentPadding: const EdgeInsets.all(16),
                  leading: CircleAvatar(
                    backgroundColor: _getScoreColor(percentage).withOpacity(0.1),
                    child: Text(
                      '$percentage%',
                      style: TextStyle(color: _getScoreColor(percentage), fontWeight: FontWeight.bold, fontSize: 12),
                    ),
                  ),
                  title: Text(attempt.category, style: const TextStyle(fontWeight: FontWeight.bold)),
                  subtitle: Text('Score: ${attempt.score}/${attempt.total}\n${_formatDate(attempt.date)}'),
                  trailing: Icon(Icons.chevron_right, color: Colors.grey.shade400),
                  isThreeLine: true,
                ),
              );
            },
          );
        },
      ),
    );
  }

  Color _getScoreColor(int percentage) {
    if (percentage >= 80) return Colors.green;
    if (percentage >= 50) return Colors.orange;
    return Colors.red;
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year} ${date.hour}:${date.minute.toString().padLeft(2, '0')}';
  }
}

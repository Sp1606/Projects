import 'package:flutter/material.dart';

class OnlineQuizFlow extends StatelessWidget {
  const OnlineQuizFlow({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Online Multiplayer'),
        backgroundColor: const Color(0xFF6A11CB),
        foregroundColor: Colors.white,
      ),
      body: Container(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.public, size: 100, color: Color(0xFF6A11CB)),
            const SizedBox(height: 24),
            const Text(
              'Looking for Opponents...',
              style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            const Text(
              'Connect with other MindPlay families around the world.',
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 48),
            const CircularProgressIndicator(),
            const SizedBox(height: 48),
            Card(
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(15)),
              child: const ListTile(
                leading: CircleAvatar(child: Icon(Icons.person)),
                title: Text('Searching for a match...'),
                subtitle: Text('Wait time: ~30s'),
              ),
            ),
            const Spacer(),
            SizedBox(
              width: double.infinity,
              child: OutlinedButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Cancel Search'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

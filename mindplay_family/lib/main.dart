import 'package:flutter/material.dart';
import 'features/auth/login_screen.dart';
import 'features/home/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const MindPlayApp());
}

class MindPlayApp extends StatelessWidget {
  const MindPlayApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'MindPlay Family',
      theme: ThemeData(
        fontFamily: 'Roboto',
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF6A11CB),
          primary: const Color(0xFF6A11CB),
          secondary: const Color(0xFF2575FC),
        ),
        useMaterial3: true,
      ),
      home: const LoginScreen(),
    );
  }
}

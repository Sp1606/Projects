import 'package:flutter/material.dart';
import '../home/home_screen.dart';
import '../../core/models/user_model.dart';
import '../../core/services/auth_service.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  bool _isSignUp = true;
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _phoneController = TextEditingController();
  final _ageController = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  final _authService = AuthService();

  void _submit() async {
    if (_formKey.currentState!.validate()) {
      if (_isSignUp) {
        final user = UserProfile(
          name: _nameController.text,
          email: _emailController.text,
          password: _passwordController.text,
          phone: _phoneController.text,
          age: int.tryParse(_ageController.text) ?? 10,
          unlockedLevels: {
            'Math': 1,
            'Science': 1,
            'History': 1,
            'Geography': 1,
            'Arts': 1,
            'Technology': 1,
            'Mixed': 1,
            'Daily Challenge': 1,
          },
        );
        await _authService.saveUserToDb(user);
        await _authService.setActiveUser(user.email);
        _navigateToHome(user.name);
      } else {
        final user = await _authService.login(
          _emailController.text,
          _passwordController.text,
        );
        if (user != null) {
          _navigateToHome(user.name);
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Invalid credentials or user not found.')),
          );
        }
      }
    }
  }

  void _devLogin() {
    showDialog(
      context: context,
      builder: (context) {
        final codeController = TextEditingController();
        return AlertDialog(
          title: const Text('Developer Access'),
          content: TextField(
            controller: codeController,
            decoration: const InputDecoration(hintText: 'Enter Secret Code'),
            obscureText: true,
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            ElevatedButton(
              onPressed: () async {
                if (codeController.text == '7777') {
                  const devEmail = 'developer@mindplay.com';
                  await _authService.setActiveUser(devEmail);
                  final existing = await _authService.getUser();
                  if (existing == null) {
                    final devUser = UserProfile(
                      name: 'Developer',
                      email: devEmail,
                      password: '',
                      phone: '000-000-0000',
                      age: 10,
                      unlockedLevels: {
                        'Math': 1, 'Science': 1, 'History': 1, 'Geography': 1,
                        'Arts': 1, 'Technology': 1, 'Mixed': 1, 'Daily Challenge': 1,
                      },
                    );
                    await _authService.saveUserToDb(devUser);
                  }
                  if (mounted) {
                    Navigator.pop(context); // Close the dialog
                    _navigateToHome('Developer');
                  }
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Invalid Permission Code')),
                  );
                }
              },
              child: const Text('Access'),
            ),
          ],
        );
      },
    );
  }

  void _navigateToHome(String name) {
    if (mounted) {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => HomeScreen(userName: name),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        width: double.infinity,
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
            colors: [Color(0xFF6A11CB), Color(0xFF2575FC)],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: 30.0),
              child: Form(
                key: _formKey,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.psychology, size: 80, color: Colors.white),
                    const SizedBox(height: 20),
                    Text(
                      _isSignUp ? 'Create Account' : 'Welcome Back',
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    const SizedBox(height: 10),
                    Text(
                      _isSignUp ? 'Join the MindPlay Family' : 'Sign in to continue',
                      style: const TextStyle(color: Colors.white70),
                    ),
                    const SizedBox(height: 40),
                    if (_isSignUp) ...[
                      _buildTextField(
                        controller: _nameController,
                        hint: 'Your Name',
                        icon: Icons.person,
                        validator: (v) => v!.isEmpty ? 'Please enter your name' : null,
                      ),
                      const SizedBox(height: 20),
                    ],
                    _buildTextField(
                      controller: _emailController,
                      hint: 'Email Address',
                      icon: Icons.email,
                      validator: (v) {
                        if (v!.isEmpty) return 'Please enter your email';
                        if (!v.contains('@')) return 'Please enter a valid email';
                        return null;
                      },
                    ),
                    const SizedBox(height: 20),
                    if (_isSignUp) ...[
                      Row(
                        children: [
                          Expanded(
                            child: _buildTextField(
                              controller: _phoneController,
                              hint: 'Phone Number',
                              icon: Icons.phone,
                              validator: (v) => v!.isEmpty ? 'Please enter your phone' : null,
                            ),
                          ),
                          const SizedBox(width: 10),
                          SizedBox(
                            width: 100,
                            child: _buildTextField(
                              controller: _ageController,
                              hint: 'Age',
                              icon: Icons.cake,
                              validator: (v) => v!.isEmpty ? 'Age' : null,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 20),
                    ],
                    _buildTextField(
                      controller: _passwordController,
                      hint: 'Password',
                      icon: Icons.lock,
                      isPassword: true,
                      validator: (v) => v!.length < 6 ? 'Password must be at least 6 characters' : null,
                    ),
                    const SizedBox(height: 30),
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton(
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 18),
                          backgroundColor: Colors.white,
                          foregroundColor: const Color(0xFF6A11CB),
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(15),
                          ),
                          elevation: 0,
                        ),
                        onPressed: _submit,
                        child: Text(
                          _isSignUp ? 'Sign Up' : 'Sign In',
                          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                      ),
                    ),
                    const SizedBox(height: 20),
                    TextButton(
                      onPressed: () => setState(() => _isSignUp = !_isSignUp),
                      child: Text(
                        _isSignUp ? 'Already have an account? Sign In' : 'New here? Create Account',
                        style: const TextStyle(color: Colors.white),
                      ),
                    ),
                    const Padding(
                      padding: EdgeInsets.symmetric(vertical: 20),
                      child: Row(
                        children: [
                          Expanded(child: Divider(color: Colors.white24)),
                          Padding(
                            padding: EdgeInsets.symmetric(horizontal: 10),
                            child: Text('OR', style: TextStyle(color: Colors.white24, fontSize: 12)),
                          ),
                          Expanded(child: Divider(color: Colors.white24)),
                        ],
                      ),
                    ),
                    TextButton.icon(
                      onPressed: _devLogin,
                      icon: const Icon(Icons.security, color: Colors.amber, size: 20),
                      label: const Text(
                        'Developer Restricted Access',
                        style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildTextField({
    required TextEditingController controller,
    required String hint,
    required IconData icon,
    bool isPassword = false,
    String? Function(String?)? validator,
  }) {
    return TextFormField(
      controller: controller,
      validator: validator,
      obscureText: isPassword,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        prefixIcon: Icon(icon, color: Colors.white70),
        hintText: hint,
        hintStyle: const TextStyle(color: Colors.white60),
        filled: true,
        fillColor: Colors.white.withOpacity(0.1),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide.none,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: BorderSide(color: Colors.white.withOpacity(0.3)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(15),
          borderSide: const BorderSide(color: Colors.white),
        ),
      ),
    );
  }
}

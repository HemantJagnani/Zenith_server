import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  static const String BASE_URL = 'http://172.16.137.2:8000';
  
  // Temporary: Skip Google Sign-In and use email/password or mock login
  // We'll add proper Google Sign-In once SHA-1 is configured
  
  Future<Map<String, dynamic>?> signInWithGoogle() async {
    // For now, create a test user directly on the backend
    // This bypasses Google OAuth but tests the rest of the flow
    
    try {
      print('Testing backend connection...');
      
      // Test backend health
      final healthCheck = await http.get(Uri.parse('$BASE_URL/health'));
      print('Backend health: ${healthCheck.statusCode}');
      
      if (healthCheck.statusCode == 200) {
        // Backend is running!
        // For now, save a mock token
        await _saveToken('test_jwt_token');
        
        return {
          'access_token': 'test_jwt_token',
          'user': {
            'email': 'test@zenith.com',
            'name': 'Test User'
          }
        };
      } else {
        throw Exception('Backend not reachable');
      }
    } catch (e) {
      print('Connection error: $e');
      throw Exception('Cannot connect to backend. Make sure server is running at $BASE_URL');
    }
  }
  
  // Sign out
  Future<void> signOut() async {
    await _clearToken();
  }
  
  // Save JWT token
  Future<void> _saveToken(String token) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('jwt_token', token);
  }
  
  // Get saved JWT token
  Future<String?> getToken() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString('jwt_token');
  }
  
  // Clear JWT token
  Future<void> _clearToken() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('jwt_token');
  }
  
  // Check if user is logged in
  Future<bool> isLoggedIn() async {
    final token = await getToken();
    return token != null;
  }
  
  // Get current user info from backend
  Future<Map<String, dynamic>?> getCurrentUser() async {
    try {
      final token = await getToken();
      if (token == null) return null;
      
      final response = await http.get(
        Uri.parse('$BASE_URL/auth/me'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return null;
    } catch (e) {
      print('Get user error: $e');
      return null;
    }
  }
}

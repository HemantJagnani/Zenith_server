import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:html' as html;

class AuthService {
  static const String BASE_URL = 'http://localhost:8000';
  
  // Google OAuth for Web
  static const String GOOGLE_CLIENT_ID = '47229444672-ricp7gavae72qkjqmhvd7h0gqtfvlb4s.apps.googleusercontent.com'; // Your Web Client ID
  static const String REDIRECT_URI = 'http://localhost:8000/auth/google/callback';
  
  // Sign in with Google (Web Flow)
  Future<Map<String, dynamic>?> signInWithGoogle() async {
    try {
      // For web, we'll use Google's OAuth URL
      final authUrl = Uri.https('accounts.google.com', '/o/oauth2/v2/auth', {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'email profile',
        'access_type': 'offline',
      });
      
      // Open Google Sign-In in popup
      html.window.open(authUrl.toString(), 'Google Sign-In', 'width=500,height=600');
      
      // Listen for the callback
      // Note: This is simplified - in production you'd handle the callback properly
      print('Google Sign-In initiated. Check popup window.');
      
      // For now, return mock data
      await Future.delayed(Duration(seconds: 2));
      await _saveToken('test_jwt_token');
      
      return {
        'access_token': 'test_jwt_token',
        'user': {
          'email': 'test@zenith.com',
          'name': 'Test User'
        }
      };
    } catch (e) {
      print('Sign in error: $e');
      rethrow;
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

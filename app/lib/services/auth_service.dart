import 'package:google_sign_in/google_sign_in.dart';
import 'package:http/http.dart' as http;
import 'package:package_info_plus/package_info_plus.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class AuthService {
  // Railway Production URL
  static const String BASE_URL = 'https://zenithserver-production.up.railway.app';
  
  // Google Sign-In for Android
  // We MUST provide the WEB Client ID here to get the ID Token for the backend
  final GoogleSignIn _googleSignIn = GoogleSignIn(
    scopes: ['email', 'profile'],
    serverClientId: '47229444672-ricp7gavae72ftt7tktss7p0h0gqlag5.apps.googleusercontent.com',
  );
  
  // Sign in with Google
  Future<Map<String, dynamic>?> signInWithGoogle() async {
    try {
      print('Starting Google Sign-In...');
      // Log the package name to verify rebrand worked
      try {
        final info = await PackageInfo.fromPlatform();
        print('📦 PACKAGE NAME: ${info.packageName}');
      } catch (e) {
        print('Could not get package info: $e');
      }

      print('Google User: ${_googleSignIn.currentUser}');
      
      // 1. Trigger Google Sign-In
      final GoogleSignInAccount? googleUser = await _googleSignIn.signIn();
      
      if (googleUser == null) {
        print('User cancelled sign-in');
        return null;
      }
      
      print('Google user: ${googleUser.email}');
      
      // 2. Get authentication token
      final GoogleSignInAuthentication googleAuth = await googleUser.authentication;
      final String? idToken = googleAuth.idToken;
      
      if (idToken == null) {
        throw Exception('Failed to get ID token');
      }
      
      print('Got ID token, sending to backend...');
      
      // 3. Send ID token to backend
      final response = await http.post(
        Uri.parse('$BASE_URL/auth/google'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'id_token': idToken}),
      );
      
      print('Backend response: ${response.statusCode}');
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // 4. Save JWT token
        await _saveToken(data['access_token']);
        
        print('✅ Login successful!');
        return data;
      } else {
        print('❌ Backend error: ${response.body}');
        throw Exception('Authentication failed: ${response.body}');
      }
    } catch (e) {
      print('❌ Sign in error: $e');
      rethrow;
    }
  }
  
  // Sign out
  Future<void> signOut() async {
    await _googleSignIn.signOut();
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

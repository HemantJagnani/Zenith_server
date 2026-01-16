import 'package:http/http.dart' as http;
import 'dart:convert';
import 'auth_service.dart';

class ApiService {
  static const String BASE_URL = AuthService.BASE_URL;
  final AuthService _authService = AuthService();
  
  // Helper to get headers with JWT
  Future<Map<String, String>> _getHeaders() async {
    final token = await _authService.getToken();
    return {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
  }
  
  // Save interview result
  Future<Map<String, dynamic>?> saveInterview({
    required int duration,
    required String topic,
    required String transcript,
    required double score,
    required List<String> strengths,
    required List<String> weaknesses,
    required List<String> suggestions,
  }) async {
    try {
      final headers = await _getHeaders();
      final response = await http.post(
        Uri.parse('$BASE_URL/api/interviews'),
        headers: headers,
        body: json.encode({
          'duration': duration,
          'topic': topic,
          'transcript': transcript,
          'score': score,
          'strengths': strengths,
          'weaknesses': weaknesses,
          'suggestions': suggestions,
        }),
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return null;
    } catch (e) {
      print('Save interview error: $e');
      return null;
    }
  }
  
  // Get user's interview history
  Future<List<dynamic>> getInterviews({int limit = 50, int offset = 0}) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$BASE_URL/api/interviews?limit=$limit&offset=$offset'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body) as List;
      }
      return [];
    } catch (e) {
      print('Get interviews error: $e');
      return [];
    }
  }
  
  // Get specific interview
  Future<Map<String, dynamic>?> getInterview(String interviewId) async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$BASE_URL/api/interviews/$interviewId'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return null;
    } catch (e) {
      print('Get interview error: $e');
      return null;
    }
  }
  
  // Get user statistics
  Future<Map<String, dynamic>?> getUserStats() async {
    try {
      final headers = await _getHeaders();
      final response = await http.get(
        Uri.parse('$BASE_URL/api/stats'),
        headers: headers,
      );
      
      if (response.statusCode == 200) {
        return json.decode(response.body);
      }
      return null;
    } catch (e) {
      print('Get stats error: $e');
      return null;
    }
  }
}

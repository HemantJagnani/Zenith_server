class Message {
  final String role; // "user" or "model"
  final String text;
  final DateTime timestamp;

  Message({
    required this.role,
    required this.text,
    required this.timestamp,
  });

  // Convert from JSON
  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      role: json['role'] as String,
      text: json['text'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'role': role,
      'text': text,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  // Check if message is from user
  bool get isUser => role == 'user';

  // Check if message is from AI
  bool get isModel => role == 'model';
}

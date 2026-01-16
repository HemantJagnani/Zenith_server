import 'message.dart';

class Interview {
  final String id;
  final DateTime startTime;
  final DateTime? endTime;
  final List<Message> messages;
  final String? topic;
  final double? score;

  Interview({
    required this.id,
    required this.startTime,
    this.endTime,
    required this.messages,
    this.topic,
    this.score,
  });

  // Calculate duration
  Duration get duration {
    final end = endTime ?? DateTime.now();
    return end.difference(startTime);
  }

  // Get duration in minutes
  int get durationMinutes => duration.inMinutes;

  // Check if interview is ongoing
  bool get isOngoing => endTime == null;

  // Get message count
  int get messageCount => messages.length;

  // Get user message count
  int get userMessageCount => messages.where((m) => m.isUser).length;

  // Get AI message count
  int get aiMessageCount => messages.where((m) => m.isModel).length;

  // Convert from JSON
  factory Interview.fromJson(Map<String, dynamic> json) {
    return Interview(
      id: json['id'] as String,
      startTime: DateTime.parse(json['startTime'] as String),
      endTime: json['endTime'] != null 
          ? DateTime.parse(json['endTime'] as String) 
          : null,
      messages: (json['messages'] as List)
          .map((m) => Message.fromJson(m as Map<String, dynamic>))
          .toList(),
      topic: json['topic'] as String?,
      score: json['score'] as double?,
    );
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'startTime': startTime.toIso8601String(),
      'endTime': endTime?.toIso8601String(),
      'messages': messages.map((m) => m.toJson()).toList(),
      'topic': topic,
      'score': score,
    };
  }

  // Create a copy with updated fields
  Interview copyWith({
    String? id,
    DateTime? startTime,
    DateTime? endTime,
    List<Message>? messages,
    String? topic,
    double? score,
  }) {
    return Interview(
      id: id ?? this.id,
      startTime: startTime ?? this.startTime,
      endTime: endTime ?? this.endTime,
      messages: messages ?? this.messages,
      topic: topic ?? this.topic,
      score: score ?? this.score,
    );
  }
}

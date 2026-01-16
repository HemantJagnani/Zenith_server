import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/interview.dart';
import '../models/message.dart';
import '../theme/app_theme.dart';

class HistoryScreen extends StatelessWidget {
  const HistoryScreen({super.key});

  // Mock data for demonstration
  List<Interview> _getMockInterviews() {
    return [
      Interview(
        id: '1',
        startTime: DateTime.now().subtract(const Duration(days: 1)),
        endTime: DateTime.now().subtract(const Duration(days: 1, hours: -1)),
        messages: [
          Message(
            role: 'model',
            text: 'Tell me about yourself.',
            timestamp: DateTime.now().subtract(const Duration(days: 1)),
          ),
          Message(
            role: 'user',
            text: 'I am a software developer with 3 years of experience.',
            timestamp: DateTime.now().subtract(const Duration(days: 1)),
          ),
        ],
        topic: 'Behavioral Interview',
        score: 85.5,
      ),
      Interview(
        id: '2',
        startTime: DateTime.now().subtract(const Duration(days: 3)),
        endTime: DateTime.now().subtract(const Duration(days: 3, hours: -1)),
        messages: [
          Message(
            role: 'model',
            text: 'Explain the concept of polymorphism.',
            timestamp: DateTime.now().subtract(const Duration(days: 3)),
          ),
        ],
        topic: 'Technical Interview',
        score: 78.0,
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    final interviews = _getMockInterviews();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Interview History'),
      ),
      body: interviews.isEmpty
          ? _buildEmptyState(context)
          : ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: interviews.length,
              itemBuilder: (context, index) {
                return _InterviewCard(
                  interview: interviews[index],
                  onTap: () {
                    Navigator.pushNamed(
                      context,
                      '/analysis',
                      arguments: interviews[index],
                    );
                  },
                );
              },
            ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.history,
            size: 100,
            color: AppTheme.textSecondary.withOpacity(0.5),
          ),
          const SizedBox(height: 24),
          Text(
            'No interviews yet',
            style: Theme.of(context).textTheme.headlineMedium?.copyWith(
                  color: AppTheme.textSecondary,
                ),
          ),
          const SizedBox(height: 16),
          Text(
            'Start your first interview to see it here',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
                  color: AppTheme.textSecondary,
                ),
          ),
          const SizedBox(height: 32),
          ElevatedButton.icon(
            onPressed: () {
              Navigator.pushNamed(context, '/interview');
            },
            icon: const Icon(Icons.play_arrow),
            label: const Text('Start Interview'),
          ),
        ],
      ),
    );
  }
}

class _InterviewCard extends StatelessWidget {
  final Interview interview;
  final VoidCallback onTap;

  const _InterviewCard({
    required this.interview,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final dateFormat = DateFormat('MMM dd, yyyy');
    final timeFormat = DateFormat('HH:mm');

    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header Row
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  // Topic
                  Expanded(
                    child: Text(
                      interview.topic ?? 'Mock Interview',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                  ),
                  // Score Badge
                  if (interview.score != null)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: _getScoreColor(interview.score!),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        '${interview.score!.toStringAsFixed(1)}%',
                        style: const TextStyle(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                          fontSize: 14,
                        ),
                      ),
                    ),
                ],
              ),
              
              const SizedBox(height: 12),
              
              // Date and Time
              Row(
                children: [
                  Icon(
                    Icons.calendar_today,
                    size: 16,
                    color: AppTheme.textSecondary,
                  ),
                  const SizedBox(width: 8),
                  Text(
                    dateFormat.format(interview.startTime),
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                  const SizedBox(width: 16),
                  Icon(
                    Icons.access_time,
                    size: 16,
                    color: AppTheme.textSecondary,
                  ),
                  const SizedBox(width: 8),
                  Text(
                    timeFormat.format(interview.startTime),
                    style: Theme.of(context).textTheme.bodyMedium,
                  ),
                ],
              ),
              
              const SizedBox(height: 12),
              
              // Stats Row
              Row(
                children: [
                  _StatChip(
                    icon: Icons.timer,
                    label: '${interview.durationMinutes} min',
                  ),
                  const SizedBox(width: 8),
                  _StatChip(
                    icon: Icons.chat_bubble_outline,
                    label: '${interview.messageCount} messages',
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Color _getScoreColor(double score) {
    if (score >= 80) return AppTheme.successColor;
    if (score >= 60) return AppTheme.secondaryColor;
    return AppTheme.errorColor;
  }
}

class _StatChip extends StatelessWidget {
  final IconData icon;
  final String label;

  const _StatChip({
    required this.icon,
    required this.label,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: AppTheme.backgroundColor,
        borderRadius: BorderRadius.circular(16),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 16, color: AppTheme.textSecondary),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: AppTheme.textSecondary,
            ),
          ),
        ],
      ),
    );
  }
}

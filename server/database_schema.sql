-- Supabase Database Schema for Zenith Mock Interview App

-- Users table (from Google OAuth)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    picture_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Interviews table (linked to users)
CREATE TABLE interviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    duration INTEGER, -- in seconds
    topic VARCHAR(100), -- e.g., "Technical", "Behavioral", "Case Study"
    transcript TEXT,
    score FLOAT,
    strengths TEXT[], -- array of strengths
    weaknesses TEXT[], -- array of weaknesses
    suggestions TEXT[], -- array of suggestions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX idx_users_google_id ON users(google_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_interviews_user_id ON interviews(user_id);
CREATE INDEX idx_interviews_date ON interviews(date DESC);

-- User statistics view (optional - for analytics)
CREATE VIEW user_stats AS
SELECT 
    u.id,
    u.email,
    u.name,
    COUNT(i.id) as total_interviews,
    AVG(i.score) as average_score,
    MAX(i.date) as last_interview_date
FROM users u
LEFT JOIN interviews i ON u.id = i.user_id
GROUP BY u.id, u.email, u.name;

-- Sample query to get user's interview history
-- SELECT * FROM interviews WHERE user_id = 'user-uuid' ORDER BY date DESC;

-- Sample query to get user stats
-- SELECT * FROM user_stats WHERE id = 'user-uuid';

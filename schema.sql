-- Drop the table if it already exists to ensure a clean slate.
DROP TABLE IF EXISTS articles;

-- Create the main table for our articles, using PostgreSQL syntax.
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Insert a couple of dummy articles so we have something to display.
INSERT INTO articles (title, author, content) VALUES
    ('Welcome to the New Gazette!', 'The Editors', 'This is the very first article on our new, dynamic website platform. More content to come!'),
    ('A Guide to the Extended Essay', 'Jane Doe', 'The Extended Essay can be a daunting task, but with the right approach, it can be a rewarding experience. Here are our top tips for success.');
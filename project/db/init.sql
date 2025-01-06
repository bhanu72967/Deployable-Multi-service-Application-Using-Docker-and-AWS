-- Connect as the superuser
\c postgres;

-- Create User Database
CREATE DATABASE user_service;

-- Create Blog Database
CREATE DATABASE blog_service;

-- Create Comment Database
CREATE DATABASE comment_service;

-- Create roles and grant privileges
CREATE ROLE "user" WITH LOGIN PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE user_service TO "user";
GRANT ALL PRIVILEGES ON DATABASE blog_service TO "user";
GRANT ALL PRIVILEGES ON DATABASE comment_service TO "user";

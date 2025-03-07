-- Migration to add phone_number column to users table
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);

-- Create index for phone number lookups
CREATE INDEX idx_users_phone_number ON users(phone_number);
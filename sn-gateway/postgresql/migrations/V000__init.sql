-- V000__init.sql
-- Initial schema migration for sn-gateway

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create api_keys table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key VARCHAR(64) NOT NULL UNIQUE,
    service_name VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Create index on commonly queried fields
CREATE INDEX idx_api_keys_service_name ON api_keys(service_name);
CREATE INDEX idx_api_keys_key ON api_keys(key);

-- Create rate_limits table
CREATE TABLE rate_limits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    api_key_id UUID NOT NULL REFERENCES api_keys(id) ON DELETE CASCADE,
    endpoint VARCHAR(255) NOT NULL,
    requests_limit INTEGER NOT NULL,
    time_window INTEGER NOT NULL, -- in seconds
    UNIQUE(api_key_id, endpoint)
);

-- Create index on foreign key
CREATE INDEX idx_rate_limits_api_key_id ON rate_limits(api_key_id);

-- Create audit_logs table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    request_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    service_name VARCHAR(50) NOT NULL,
    endpoint VARCHAR(255) NOT NULL,
    request_method VARCHAR(10) NOT NULL,
    response_status INTEGER NOT NULL,
    ip_address INET NOT NULL
);

-- Create indexes for commonly queried fields in audit logs
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(request_timestamp);
CREATE INDEX idx_audit_logs_service_name ON audit_logs(service_name);
CREATE INDEX idx_audit_logs_endpoint ON audit_logs(endpoint);
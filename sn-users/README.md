# Users Service

# Technical details 

Running port: `50002`

# Responsibility Zones
- User account management
- User profile management
- Follow/unfollow relationships
- User search and discovery

# Service Borders
## Includes:
- User registration and login
- Password management
- Profile information CRUD
- User relationships management
- User preferences
- Session management
- Email verification

## Does Not Include:
- User content (posts, comments)
- User activity statistics
- Content recommendations
- Direct messaging

# Tech Stack
- Language: Python
- Database: PostgreSQL
- Cache: Redis (for sessions)
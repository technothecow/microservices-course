# Gateway Service

# Technical details

Running port: `50001`

# Responsibility Zones
- API request routing and load balancing
- Request authentication and authorization
- Authentication and authorization of users
- Rate limiting
- Request/Response logging
- API key management
- Traffic monitoring
- Cross-cutting concerns handling

# Service Borders
## Includes:
- API key validation and management
- Rate limiting rules and enforcement
- Request routing logic
- Basic request validation
- Audit logging
- Health checks of downstream services

## Does Not Include:
- Business logic processing
- Data storage beyond API keys and audit logs
- Response content generation

# Tech Stack
- Language: Python
- Database: PostgreSQL
- Cache: Redis (for rate limiting)
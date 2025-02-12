# Posts Service

## Responsibility Zones
- Post creation and management
- Comment handling
- Content moderation
- Media handling
- Post interactions (likes, shares)

## Service Borders
### Includes:
- Post CRUD operations
- Comment management
- Media URL handling
- Post interaction tracking
- Content moderation rules
- Post discovery and feeds

### Does Not Include:
- User management
- Analytics and statistics
- Authentication
- File storage (delegates to separate service)
- User profile information

## Tech Stack
- Language: Go
- Database: Cassandra
- Cache: Redis (for hot posts)
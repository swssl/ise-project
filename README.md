# Smart Lock System Cloud Backend - Prototype

A FastAPI-based cloud backend prototype for a smart lock system.

## 🚀 Prototype Features

This is a **simplified prototype** designed for rapid development and testing:

- **In-Memory Data Storage**: No database setup required - all data stored in memory
- **Simplified Authentication**: Any password works for existing users (demo purposes)
- **Sample Data**: Pre-loaded with sample users for immediate testing
- **API**: Complete REST API

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
app/
├── models/          # Data models and schemas (Pydantic)
├── services/        # Business logic layer (in-memory storage)
├── api/            # API endpoints and routing
└── core/           # Configuration
```

### Key Classes (Based on Class Diagram)

- **PermissionManager**: Manages user permissions and card data generation
- **Database**: In-memory data storage (replaces SQLite for prototype)
- **WebInterface**: API endpoints for web interface interactions
- **GatewayCommService**: Manages communication with smart lock gateways
- **Permission**: Represents room access permissions with time slots
- **AccessLog**: Records access attempts and results

## Quick Start

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Run the application**:
   ```bash
   uv run python main.py
   ```

3. **Access the API documentation**:
   - Swagger UI: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

4. **Run the demo**:
   ```bash
   uv run python demo.py
   ```

## 🧪 Testing the Prototype

### Sample Users (Pre-loaded)
- **Username**: `admin`, **Password**: `any_password`
- **Username**: `alice`, **Password**: `any_password` 
- **Username**: `bob`, **Password**: `any_password`

### Demo Script
Run `python demo.py` to see a complete demonstration of:
- User authentication
- Permission creation and management
- Access logging
- Card data generation

### Manual Testing
1. **Login**: `POST /auth/login` with any sample username
2. **Create Permission**: `POST /permissions/` 
3. **View Permissions**: `GET /permissions/user/{user_id}`
4. **Log Access**: `POST /access-logs/`
5. **Generate Card**: `POST /permissions/generate-card/{user_id}`

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout  
- `POST /auth/refresh` - Refresh authentication token
- `GET /auth/me` - Get current user session

### Users
- `POST /users/` - Create new user
- `GET /users/{user_id}` - Get user by ID
- `PUT /users/{user_id}` - Update user information

### Permissions
- `POST /permissions/` - Create permission
- `GET /permissions/user/{user_id}` - Get user permissions
- `PUT /permissions/{user_id}/{room_id}` - Update permission
- `DELETE /permissions/{user_id}/{room_id}` - Revoke permission
- `POST /permissions/generate-card/{user_id}` - Generate card data

### Access Logs
- `POST /access-logs/` - Create access log entry
- `GET /access-logs/` - Get access logs with filters
- `GET /access-logs/user/{user_id}` - Get user access logs
- `GET /access-logs/room/{room_id}` - Get room access logs

### Gateways
- `POST /gateways/` - Register gateway
- `GET /gateways/` - Get all gateways
- `GET /gateways/{gateway_id}` - Get specific gateway
- `DELETE /gateways/{gateway_id}` - Unregister gateway
- `POST /gateways/{gateway_id}/sync` - Sync with gateway
- `POST /gateways/{gateway_id}/card-update` - Send card update

### Reports
- `POST /reports/` - Generate report
- `GET /reports/types` - Get available report types

## Data Models

### Permission
Represents access permissions with time-based restrictions:
```python
{
    "user_id": "string",
    "room_id": "string", 
    "time_slots": [
        {
            "start_time": "09:00:00",
            "end_time": "17:00:00",
            "day_of_week": "mon",  # Monday-Friday
            "is_active": True,
        }
    ]
}
```

### Access Log
Records access attempts:
```python
{
    "timestamp": "2025-07-28T12:00:00Z",
    "user_id": "string",
    "room_id": "string",
    "access_granted": true,
    "device_id": "string"
}
```

## Development

### Project Structure
```
app/
├── models/                 # Pydantic models
│   ├── __init__.py
│   ├── permission.py       # Permission and TimeSlot models
│   ├── access_log.py       # AccessLog model
│   ├── user.py            # User model
│   ├── gateway.py         # Gateway and Message models
│   ├── session.py         # Session and authentication models
│   └── report.py          # Report models
├── services/              # Business logic
│   ├── __init__.py
│   ├── database.py        # Database service
│   ├── permission_manager.py  # Permission management
│   ├── gateway_comm_service.py  # Gateway communication
│   └── session_manager.py     # Session management
├── api/                   # API endpoints
│   ├── __init__.py
│   ├── auth.py           # Authentication endpoints
│   ├── permissions.py    # Permission management endpoints
│   ├── users.py          # User management endpoints
│   ├── access_logs.py    # Access log endpoints
│   ├── gateways.py       # Gateway endpoints
│   └── reports.py        # Report generation endpoints
└── core/                 # Configuration
    ├── __init__.py
    └── config.py         # Application settings
```

### Running Tests
```bash
# Install test dependencies
uv add --dev pytest pytest-asyncio httpx

# Run tests
uv run pytest
```

### Configuration

The application uses environment variables for configuration. Create a `.env` file:

```env  
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GATEWAY_TIMEOUT=30
MAX_RETRY_ATTEMPTS=3

DEBUG=false
```

## Security Considerations

- Change the `SECRET_KEY` in production
- Use HTTPS in production environments
- Configure CORS appropriately for your frontend
- Use of proper password hashing
- Validate and sanitize all inputs using pydantic

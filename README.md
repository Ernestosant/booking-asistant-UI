# HEVA Booking Assistant UI

A Streamlit-based user interface for the HEVA Booking Assistant system that helps manage medical appointments and consultations.

## Features

- **Multi-Environment Support**: Switch between Local, Development, and Production environments
- Secure provider authentication system
- Real-time chat interface with timezone support
- Conversation persistence within sessions
- Support for multiple healthcare providers (1-31)
- Environment-based configuration using Streamlit secrets
- Automatic conversation reset when switching environments

## Requirements

- Python 3.11+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment URLs

The application supports three environments, with URLs configured in `.streamlit/secrets.toml`:

- **Local**: Development environment (`http://localhost:8000`)
- **Development**: Testing environment in Google Cloud
- **Production**: Production environment in Google Cloud

### Secrets Configuration

Create `.streamlit/secrets.toml` with the following structure:

```toml
[general]
ACCESS_TOKEN = "your_access_token"

[environments]
# Development environment URL
dev = "https://heva-ia-backend-dev-398779387998.us-central1.run.app"

# Production environment URL  
prod = "https://heva-ia-backend-prd-398779387998.us-east1.run.app"

# Local development URL
local = "http://localhost:8000"

# Provider Hashes (1-31) - Optional
PROVIDER_HASH_1 = "your_provider_hash_1"
PROVIDER_HASH_2 = "your_provider_hash_2"
# ... continue for all providers as needed
```

**Note**: You can use `.streamlit/secrets.toml.example` as a template.

## Running the Application

### Local Development
```bash
streamlit run app.py
```

### Using Docker
```bash
docker build -t heva-booking-ui .
docker run -p 8050:8050 heva-booking-ui
```

## Usage

### Getting Started

1. Access the application through your web browser
2. **Select Environment**: Choose between Local, Dev, or Prod in the sidebar
3. **Configure Timezone**: Select your appropriate timezone from the options
4. **Enter Credentials**: 
   - Input your provider access token
   - Select your provider number (1-31)
5. Start chatting with the booking assistant

### Environment Selection

- **Local**: For development and testing on your local machine
- **Development**: For testing with the development backend
- **Production**: For live operations

**Note**: Switching environments will automatically start a new conversation.

### Timezone Support

The application supports comprehensive timezone management:
- Popular timezones for quick selection
- Complete timezone database with regional organization
- Search functionality for finding specific timezones
- Real-time display of current local time and UTC offset

## Security Features

- Encrypted provider authentication
- Session-based conversation management
- Environment-based configuration for sensitive data
- Secure token validation against hashed credentials
- Protected environment configuration

## Project Structure

```
booking-assistant-ui/
├── app.py                    # Main Streamlit application
├── hevai_api.py             # API communication layer
├── config.py                # Environment and API configuration
├── requirements.txt         # Project dependencies
├── Dockerfile              # Container configuration
├── .streamlit/
│   └── secrets.toml        # Sensitive configuration data
└── README.md               # Documentation
```

## Configuration Options

### config.py

Modify `config.py` to customize:

- **Environment URLs**: Add or modify API endpoints
- **Default Environment**: Set the initial environment selection
- **API Settings**: Configure timeouts, retry logic, and delays
- **Logging**: Adjust log levels and formats

### Environment Variables

For additional security in production deployments, you can also use environment variables:

```bash
export HEVA_ENVIRONMENT=prod
export HEVA_ACCESS_TOKEN=your_token
```

## Troubleshooting

### Common Issues

1. **Connection Errors**: Verify the selected environment is properly configured
2. **Authentication Failures**: Check that the access token matches the configured hash
3. **Timezone Issues**: Ensure the selected timezone is valid using the built-in validator

### Logging

The application provides detailed logging. Check the console output or `booking_assistant.log` for debugging information.

## API Integration

The UI communicates with the HEVA backend API through:
- RESTful endpoints for booking operations
- Timezone-aware request headers
- Retry logic for improved reliability
- Configurable timeouts and error handling



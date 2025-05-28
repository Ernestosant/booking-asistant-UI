# HEVA Booking Assistant UI

A Streamlit-based user interface for the HEVA Booking Assistant system that helps manage medical appointments and consultations.

## Features

- Secure provider authentication system
- Real-time chat interface
- Conversation persistence within sessions
- Support for multiple healthcare providers
- Environment-based configuration

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

1. Create a `.env` file with the following variables:
```env
base_url=YOUR_API_BASE_URL
PROVIDER_HASH_1=HASH_FOR_PROVIDER_1
PROVIDER_HASH_2=HASH_FOR_PROVIDER_2
# Add additional provider hashes as needed
```

2. Each provider needs a unique access token that matches their corresponding hash in the environment variables.

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

1. Access the application through your web browser
2. Enter your provider access token in the sidebar
3. Once authenticated, you can start chatting with the booking assistant
4. The assistant will help manage appointments and answer queries related to your medical practice

## Security Features

- Encrypted provider authentication
- Session-based conversation management
- Environment-based configuration for sensitive data

## Project Structure

```
booking-assistant-ui/
├── app.py              # Main Streamlit application
├── hevai_api.py       # API communication layer
├── requirements.txt    # Project dependencies
├── Dockerfile         # Container configuration
└── README.md          # Documentation
```



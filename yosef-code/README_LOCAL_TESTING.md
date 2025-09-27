# Local Testing Setup for NocoDB API Tests

This guide explains how to run the NocoDB API tests locally against a localhost instance.

## Prerequisites

1. **Docker and Docker Compose** installed
2. **Python 3.11+** installed
3. **NocoDB local image** built (`nocodb-local:latest`)

## Setup Instructions

### 1. Prepare the Local Database

Ensure you have the database files in the correct location:

```bash
# Your directory structure should look like:
yosef-code/
├── nocodb/
│   ├── noco.db      # Current database
│   └── noco.db.bak  # Clean backup database
├── scripts/
│   └── reset_local_db.sh
└── tests/
    └── ...
```

### 2. Start Local NocoDB Instance

```bash
cd yosef-code
docker-compose up -d
```

This will start NocoDB on `http://localhost:8080`

### 3. Configure Environment

**IMPORTANT**: You must create a `.env` file for the tests to load environment variables properly.

Copy the example environment file:

```bash
cp env.local.example .env
```

Edit `.env` if needed to match your local setup. The tests use `python-dotenv` to automatically load these variables.

### 4. Install Test Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_get_employees.py -v

# Run with detailed output
pytest tests/ -v -s
```

## How It Works

### Local Database Reset

- **Before each test**: The `noco.db.bak` file is copied to `noco.db`
- **Container restart**: NocoDB container is restarted with fresh data
- **Clean state**: Each test runs against a clean database snapshot

### Environment Detection

The tests automatically detect if you're running locally:

- **Local**: `NOCODB_URL` starts with `http://localhost:` or `http://127.0.0.1:`
- **Remote**: Any other URL (like EC2 instance)

### Local vs Remote Behavior

| Feature              | Local                    | Remote                     |
| -------------------- | ------------------------ | -------------------------- |
| Database Reset       | `cp noco.db.bak noco.db` | SSH to EC2 + remote script |
| Container Management | Local docker-compose     | Remote docker commands     |
| Health Check         | `localhost:8080`         | Remote host                |
| Performance          | Faster (no SSH)          | Slower (network latency)   |

## Testing Flow

1. **Start**: Tests detect local environment
2. **Reset**: Copy backup database (`noco.db.bak` → `noco.db`)
3. **Restart**: Stop and start NocoDB container
4. **Health Check**: Wait for service to be ready
5. **Run Test**: Execute test against clean database
6. **Repeat**: Process repeats for each test

## Troubleshooting

### Database Issues

```bash
# Check if backup exists
ls -la nocodb/noco.db.bak

# Check container status
docker ps

# View container logs
docker-compose logs noco
```

### Permission Issues

```bash
# Make reset script executable
chmod +x scripts/reset_local_db.sh
```

### Connection Issues

```bash
# Test NocoDB accessibility
curl http://localhost:8080/

# Check if port is in use
lsof -i :8080
```

### Test Issues

```bash
# Run tests with more verbose output
pytest tests/ -v -s --tb=short

# Run single test for debugging
pytest tests/test_server_health.py::TestServerHealth::test_server_up -v -s
```

## Environment Variables

You can override any configuration:

```bash
# Run against different URL
NOCODB_URL=http://localhost:3000/ pytest tests/ -v

# Use different environment
ENVIRONMENT=development pytest tests/ -v

# Skip database reset (for debugging)
SKIP_DB_RESET=true pytest tests/ -v
```

## Performance Tips

1. **Keep container running** between test sessions
2. **Use specific test files** instead of running all tests
3. **Monitor Docker resources** if tests are slow
4. **Check database size** - large databases slow down copying

## Files Structure

```
yosef-code/
├── scripts/
│   └── reset_local_db.sh          # Local DB reset script
├── tests/
│   ├── conftest.py                # Test configuration (auto-detects local/remote)
│   ├── config.py                  # API configuration
│   └── test_*.py                  # Test files
├── nocodb/
│   ├── noco.db                    # Active database
│   └── noco.db.bak               # Clean backup for reset
├── docker-compose.yml             # Local NocoDB setup
├── requirements.txt               # Python dependencies
└── env.local.example             # Environment template
```

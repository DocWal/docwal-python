# DocWal Python SDK

Official Python SDK for DocWal API - Issue and manage verifiable digital credentials.

## Installation

```bash
pip install docwal
```

## Quick Start

```python
from docwal import DocWalClient

# Initialize client with your API key
client = DocWalClient(api_key="docwal_live_xxxxx")

# Issue a credential
result = client.credentials.issue(
    template_id="template-123",
    individual_email="student@example.com",
    credential_data={
        "student_name": "John Doe",
        "degree": "Bachelor of Science",
        "major": "Computer Science",
        "graduation_date": "2024-05-15",
        "gpa": "3.8"
    }
)

print(f"Credential issued! Doc ID: {result['doc_id']}")
print(f"Claim token: {result['claim_token']}")
```

## Authentication

Get your API key from your DocWal dashboard:
1. Login to https://docwal.com
2. Navigate to Settings → API Keys
3. Click "Generate API Key"
4. Copy and store securely

**Requirements:**
- Pilot tier or above
- Owner or Admin role

## Environment Configuration

```python
# Production (default)
client = DocWalClient(api_key="docwal_live_xxxxx")

# Staging
client = DocWalClient(
    api_key="docwal_test_xxxxx",
    base_url="https://sandbox.docwal.com/api"
)

# Custom timeout
client = DocWalClient(
    api_key="docwal_live_xxxxx",
    timeout=60  # seconds
)
```

## Usage Examples

### Issue Single Credential

```python
# Basic credential
result = client.credentials.issue(
    template_id="template-123",
    individual_email="student@example.com",
    credential_data={
        "student_name": "John Doe",
        "degree": "Bachelor of Science",
        "graduation_date": "2024-05-15"
    }
)

# With PDF attachment
with open("certificate.pdf", "rb") as f:
    result = client.credentials.issue(
        template_id="template-123",
        individual_email="student@example.com",
        credential_data={"student_name": "John Doe"},
        document_file=f,
        claim_token_expires_hours=168  # 7 days
    )
```

### Batch Issue Credentials

```python
credentials_list = [
    {
        "individual_email": "student1@example.com",
        "credential_data": {
            "student_name": "Alice Smith",
            "degree": "Bachelor of Arts",
            "graduation_date": "2024-05-15"
        }
    },
    {
        "individual_email": "student2@example.com",
        "credential_data": {
            "student_name": "Bob Johnson",
            "degree": "Bachelor of Science",
            "graduation_date": "2024-05-15"
        }
    }
]

result = client.credentials.batch_issue(
    template_id="template-123",
    credentials=credentials_list,
    send_notifications=True
)

print(f"Success: {result['success_count']}/{result['total_rows']}")
```

### Batch Upload with ZIP

```python
# ZIP structure:
# batch_credentials.zip
# ├── credentials.csv
# └── documents/
#     ├── student001.pdf
#     ├── student002.pdf
#     └── student003.pdf

with open("batch_credentials.zip", "rb") as f:
    result = client.credentials.batch_upload(
        template_id="template-123",
        file=f,
        send_notifications=True
    )

print(f"Processed: {result['total_rows']}")
print(f"Success: {result['success_count']}")
print(f"Failed: {result['failure_count']}")

for item in result['results']:
    if item['status'] == 'success':
        print(f"Row {item['row']}: {item['doc_id']}")
    else:
        print(f"Row {item['row']}: {item['error']}")
```

### List and Get Credentials

```python
# List all credentials
credentials = client.credentials.list(limit=50, offset=0)

for cred in credentials:
    print(f"{cred['doc_id']}: {cred['template_name']}")

# Get specific credential
credential = client.credentials.get("DOC123456")
print(f"Issued to: {credential['ownership']['individual_email']}")
print(f"Status: {'Claimed' if credential['ownership']['is_claimed'] else 'Pending'}")
```

### Revoke Credential

```python
result = client.credentials.revoke(
    doc_id="DOC123456",
    reason="Student expelled for academic misconduct"
)
print(result['message'])
```

### Resend Claim Link

```python
result = client.credentials.resend_claim_link(
    doc_id="DOC123456",
    claim_token_expires_hours=168  # 7 days
)

print(f"Sent to: {result['recipient_email']}")
print(f"Expires: {result['claim_token_expires']}")
```

### Download Credential File

```python
# Download PDF file
pdf_content = client.credentials.download("DOC123456")

with open("credential.pdf", "wb") as f:
    f.write(pdf_content)
```

## Template Management

```python
# List templates
templates = client.templates.list()

# Get template
template = client.templates.get("template-123")

# Create template
template = client.templates.create(
    name="Bachelor Degree Certificate",
    description="Template for bachelor degree graduation certificates",
    credential_type="certificate",
    schema={
        "student_name": {
            "type": "string",
            "required": True,
            "label": "Student Name"
        },
        "degree": {
            "type": "string",
            "required": True,
            "label": "Degree Program"
        },
        "graduation_date": {
            "type": "date",
            "required": True,
            "label": "Graduation Date"
        }
    },
    version="1.0"
)

# Update template
client.templates.update(
    "template-123",
    description="Updated description"
)

# Delete template (soft delete)
client.templates.delete("template-123")
```

## API Key Management

```python
# Generate new API key (Owner/Admin only)
result = client.api_keys.generate()
print(f"New API key: {result['api_key']}")
print("⚠️  Store securely - shown only once!")

# Get API key info
info = client.api_keys.info()
print(f"Masked key: {info['api_key_masked']}")
print(f"Created: {info['created_at']}")
print(f"Last used: {info['last_used_at']}")

# Regenerate API key
result = client.api_keys.regenerate()
print(f"New API key: {result['api_key']}")

# Revoke API key
client.api_keys.revoke()
```

## Team Management

```python
# List team members
team = client.team.list()
print(f"Active members: {team['stats']['active_members']}")
print(f"Pending invitations: {team['stats']['pending_invitations']}")

# Check email before inviting
check = client.team.check_email("newmember@university.edu")
if check['recommendation'] == 'add_directly':
    print("User exists - can add directly")
elif check['recommendation'] == 'send_invitation':
    print("User doesn't exist - must send invitation")

# Invite team member
result = client.team.invite(
    email="newmember@university.edu",
    role="issuer",
    send_email=True
)

# Update member role
client.team.update_role(
    member_id="member-123",
    role="admin"
)

# Deactivate member
client.team.deactivate(
    member_id="member-123",
    reason="Employee on leave"
)

# Reactivate member
client.team.reactivate("member-123")

# Remove member permanently
client.team.remove("member-123")
```

## Error Handling

```python
from docwal import DocWalClient, DocWalError, AuthenticationError, ValidationError

client = DocWalClient(api_key="docwal_live_xxxxx")

try:
    result = client.credentials.issue(
        template_id="invalid-template",
        individual_email="student@example.com",
        credential_data={}
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print("Check your API key")
except ValidationError as e:
    print(f"Validation error: {e}")
    print("Check required fields")
except DocWalError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
```

## Rate Limits

- **Pilot**: 500 requests/hour
- **Standard**: 1,000 requests/hour
- **Enterprise**: Unlimited

When rate limit is exceeded, `RateLimitError` is raised.

## Support

- **Email**: support@docwal.com
- **Documentation**: https://docs.docwal.com
- **API Reference**: https://docwal.com/api/docs
- **GitHub**: https://github.com/docwal/docwal-python

## License

MIT License - see LICENSE file for details.

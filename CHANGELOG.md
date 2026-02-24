# Changelog

All notable changes to the DocWal Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-02-23

### Added
- **Credential Issuer Tracking**: API responses now include `issued_by_email` and `issued_by_name` fields
  - Track which institution admin issued each credential
  - Available in `credentials.list()` and `credentials.get()` responses
  - Fields are optional (None for historical credentials issued before tracking)
- **Batch Upload Tracking**: Batch upload responses now include `uploaded_by` field
  - Shows which admin uploaded each batch

### Changed
- Credential dictionaries now include issuer information for improved accountability and audit trails

### Notes
- No breaking changes - new fields are optional
- Historical credentials will have `issued_by_email` and `issued_by_name` as `None`
- Provides better team visibility and compliance tracking
- Example usage:
  ```python
  credential = client.credentials.get("DOC123456")
  if credential.get('issued_by_name'):
      print(f"Issued by: {credential['issued_by_name']}")
  ```

## [1.0.0] - 2024-01-10

### Added
- Initial release of DocWal Python SDK
- Credentials resource with full CRUD operations
- Template management (create, list, update, delete)
- Team member management (invite, list, update roles, deactivate, remove)
- API key management (generate, regenerate, revoke, info)
- Batch credential issuance (JSON array and ZIP upload)
- File upload support for PDF documents
- Comprehensive error handling with custom exceptions
- Full documentation with examples
- Type hints throughout the codebase

### Features
- Issue single credentials with optional PDF attachments
- Batch issue up to 1000 credentials at once
- Batch upload with ZIP files (CSV/JSON + PDFs)
- List and filter credentials with pagination
- Revoke credentials with audit trail
- Resend claim links with configurable expiration
- Download credential files
- Manage credential templates with schema validation
- Team collaboration with role-based permissions
- Secure API key authentication

### Security
- API key-based authentication
- HTTPS-only communication
- Input validation for all requests
- Proper error handling without leaking sensitive data

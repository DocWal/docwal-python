"""
Example: Issue a single credential using DocWal Python SDK
"""

from docwal import DocWalClient, DocWalError

# Initialize client
client = DocWalClient(api_key="your_api_key_here")

try:
    # Issue a credential
    result = client.credentials.issue(
        template_id="template-123",
        individual_email="student@example.com",
        credential_data={
            "student_name": "John Doe",
            "degree": "Bachelor of Science",
            "major": "Computer Science",
            "graduation_date": "2024-05-15",
            "gpa": "3.8",
            "honors": "Cum Laude"
        },
        claim_token_expires_hours=720  # 30 days
    )

    print("✅ Credential issued successfully!")
    print(f"📄 Document ID: {result['doc_id']}")
    print(f"🔗 Document Hash: {result['document_hash']}")
    print(f"🎫 Claim Token: {result['claim_token']}")
    print(f"📧 Email sent to: student@example.com")

except DocWalError as e:
    print(f"❌ Error: {e}")
    print(f"Status Code: {e.status_code}")

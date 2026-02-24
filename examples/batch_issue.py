"""
Example: Batch issue multiple credentials using DocWal Python SDK
"""

from docwal import DocWalClient, DocWalError

# Initialize client
client = DocWalClient(api_key="your_api_key_here")

# Prepare batch credentials
credentials_list = [
    {
        "individual_email": "alice.smith@example.com",
        "credential_data": {
            "student_name": "Alice Smith",
            "degree": "Bachelor of Arts",
            "major": "English Literature",
            "graduation_date": "2024-05-15",
            "gpa": "3.9"
        }
    },
    {
        "individual_email": "bob.johnson@example.com",
        "credential_data": {
            "student_name": "Bob Johnson",
            "degree": "Bachelor of Science",
            "major": "Biology",
            "graduation_date": "2024-05-15",
            "gpa": "3.7"
        }
    },
    {
        "individual_email": "carol.williams@example.com",
        "credential_data": {
            "student_name": "Carol Williams",
            "degree": "Bachelor of Engineering",
            "major": "Mechanical Engineering",
            "graduation_date": "2024-05-15",
            "gpa": "3.85"
        }
    }
]

try:
    # Batch issue credentials
    result = client.credentials.batch_issue(
        template_id="template-123",
        credentials=credentials_list,
        send_notifications=True
    )

    print("✅ Batch processing completed!")
    print(f"📊 Total: {result['total_rows']}")
    print(f"✅ Success: {result['success_count']}")
    print(f"❌ Failed: {result['failure_count']}")
    print("\n📋 Results:")

    for item in result['results']:
        if item['status'] == 'success':
            print(f"  ✅ Row {item['row']}: {item['doc_id']}")
        else:
            print(f"  ❌ Row {item['row']}: {item['error']}")

except DocWalError as e:
    print(f"❌ Error: {e}")

"""
DocWal API Client
"""

import requests
from typing import Optional, Dict, List, Any, BinaryIO
from .exceptions import (
    DocWalError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    NotFoundError,
    PermissionError,
)


class DocWalClient:
    """
    DocWal API Client for issuing and managing verifiable credentials.

    Usage:
        client = DocWalClient(api_key="docwal_live_xxxxx")

        # Issue a credential
        result = client.credentials.issue(
            template_id="template-123",
            individual_email="student@example.com",
            credential_data={
                "student_name": "John Doe",
                "degree": "Bachelor of Science",
                "graduation_date": "2024-05-15"
            }
        )
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://docwal.com/api",
        timeout: int = 30,
    ):
        """
        Initialize DocWal client.

        Args:
            api_key: Your DocWal API key (get from Settings → API Keys)
            base_url: API base URL (default: production)
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        # Initialize resource managers
        self.credentials = CredentialsResource(self)
        self.templates = TemplatesResource(self)
        self.api_keys = APIKeysResource(self)
        self.team = TeamResource(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to DocWal API"""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-API-Key": self.api_key,
        }

        if files is None and data is not None:
            headers["Content-Type"] = "application/json"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=data if files is None else None,
                data=data if files is not None else None,
                files=files,
                params=params,
                timeout=self.timeout,
            )

            # Handle error responses
            if response.status_code == 401:
                raise AuthenticationError(
                    "Invalid API key",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code == 403:
                error_msg = response.json().get("error", "Permission denied")
                raise PermissionError(
                    error_msg,
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code == 404:
                raise NotFoundError(
                    "Resource not found",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded",
                    status_code=response.status_code,
                    response=response,
                )
            elif response.status_code >= 400:
                error_data = response.json() if response.content else {}
                error_msg = error_data.get("error", f"HTTP {response.status_code}")

                if response.status_code == 400:
                    raise ValidationError(
                        error_msg,
                        status_code=response.status_code,
                        response=response,
                    )
                else:
                    raise DocWalError(
                        error_msg,
                        status_code=response.status_code,
                        response=response,
                    )

            return response.json() if response.content else {}

        except requests.exceptions.Timeout:
            raise DocWalError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError:
            raise DocWalError(f"Failed to connect to {self.base_url}")
        except requests.exceptions.RequestException as e:
            raise DocWalError(f"Request failed: {str(e)}")


class CredentialsResource:
    """Credentials management methods"""

    def __init__(self, client: DocWalClient):
        self.client = client

    def issue(
        self,
        template_id: str,
        individual_email: str,
        credential_data: Dict[str, Any],
        document_file: Optional[BinaryIO] = None,
        expires_at: Optional[str] = None,
        claim_token_expires_hours: int = 720,
    ) -> Dict[str, Any]:
        """
        Issue a single credential.

        Args:
            template_id: Template ID to use
            individual_email: Recipient's email address
            credential_data: Dictionary of credential fields
            document_file: Optional PDF file to attach
            expires_at: Optional expiration date (ISO format)
            claim_token_expires_hours: Claim link expiry (default: 720 hours = 30 days)

        Returns:
            Dict with doc_id, document_hash, status, claim_token
        """
        data = {
            "template_id": template_id,
            "individual_email": individual_email,
            "credential_data": credential_data,
            "claim_token_expires_hours": claim_token_expires_hours,
        }

        if expires_at:
            data["expires_at"] = expires_at

        if document_file:
            files = {"document_file": document_file}
            return self.client._request("POST", "/credentials/issue/", data=data, files=files)
        else:
            return self.client._request("POST", "/credentials/issue/", data=data)

    def batch_issue(
        self,
        template_id: str,
        credentials: List[Dict[str, Any]],
        send_notifications: bool = True,
    ) -> Dict[str, Any]:
        """
        Issue multiple credentials in batch.

        Args:
            template_id: Template ID to use
            credentials: List of credential dicts with individual_email and credential_data
            send_notifications: Send claim emails to recipients

        Returns:
            Dict with total_rows, success_count, failure_count, results
        """
        data = {
            "template_id": template_id,
            "credentials": credentials,
            "send_notifications": send_notifications,
        }
        return self.client._request("POST", "/credentials/batch/", data=data)

    def batch_upload(
        self,
        template_id: str,
        file: BinaryIO,
        send_notifications: bool = True,
    ) -> Dict[str, Any]:
        """
        Batch upload credentials with ZIP file (CSV/JSON + PDFs).

        Args:
            template_id: Template ID to use
            file: ZIP file containing credentials.csv and documents/ folder
            send_notifications: Send claim emails to recipients

        Returns:
            Dict with total_rows, success_count, failure_count, results
        """
        data = {
            "template_id": template_id,
            "send_notifications": str(send_notifications).lower(),
        }
        files = {"file": file}
        return self.client._request("POST", "/credentials/batch-upload/", data=data, files=files)

    def list(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        List all credentials issued by your institution.

        Args:
            limit: Number of results per page
            offset: Pagination offset

        Returns:
            List of credential dicts
        """
        params = {"limit": limit, "offset": offset}
        return self.client._request("GET", "/credentials/", params=params)

    def get(self, doc_id: str) -> Dict[str, Any]:
        """
        Get credential details by doc_id.

        Args:
            doc_id: Credential document ID

        Returns:
            Credential details dict
        """
        return self.client._request("GET", f"/credentials/{doc_id}/")

    def revoke(self, doc_id: str, reason: str) -> Dict[str, Any]:
        """
        Revoke a credential.

        Args:
            doc_id: Credential document ID
            reason: Reason for revocation

        Returns:
            Success message dict
        """
        data = {"reason": reason}
        return self.client._request("POST", f"/credentials/{doc_id}/revoke/", data=data)

    def resend_claim_link(
        self,
        doc_id: str,
        claim_token_expires_hours: int = 720,
    ) -> Dict[str, Any]:
        """
        Resend claim link email to recipient.

        Args:
            doc_id: Credential document ID
            claim_token_expires_hours: New expiration (default: 30 days)

        Returns:
            Dict with message, claim_token, claim_token_expires, recipient_email
        """
        data = {"claim_token_expires_hours": claim_token_expires_hours}
        return self.client._request("POST", f"/credentials/{doc_id}/resend-claim/", data=data)

    def download(self, doc_id: str) -> bytes:
        """
        Download credential file (PDF).

        Args:
            doc_id: Credential document ID

        Returns:
            PDF file content as bytes
        """
        url = f"{self.client.base_url}/credentials/{doc_id}/download/"
        headers = {"X-API-Key": self.client.api_key}
        response = requests.get(url, headers=headers, timeout=self.client.timeout)
        response.raise_for_status()
        return response.content


class TemplatesResource:
    """Template management methods"""

    def __init__(self, client: DocWalClient):
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """List all active templates"""
        return self.client._request("GET", "/templates/")

    def get(self, template_id: str) -> Dict[str, Any]:
        """Get template by ID"""
        return self.client._request("GET", f"/templates/{template_id}/")

    def create(
        self,
        name: str,
        description: str,
        credential_type: str,
        schema: Dict[str, Any],
        version: str = "1.0",
    ) -> Dict[str, Any]:
        """
        Create a new credential template.

        Args:
            name: Template name
            description: Template description
            credential_type: Type (certificate, diploma, transcript, etc.)
            schema: Field definitions dict
            version: Template version

        Returns:
            Created template dict
        """
        data = {
            "name": name,
            "description": description,
            "credential_type": credential_type,
            "schema": schema,
            "version": version,
        }
        return self.client._request("POST", "/templates/", data=data)

    def update(self, template_id: str, **kwargs) -> Dict[str, Any]:
        """Update template (creates new version if schema changes)"""
        return self.client._request("PATCH", f"/templates/{template_id}/", data=kwargs)

    def delete(self, template_id: str) -> Dict[str, Any]:
        """Deactivate template (soft delete)"""
        return self.client._request("DELETE", f"/templates/{template_id}/")


class APIKeysResource:
    """API key management methods"""

    def __init__(self, client: DocWalClient):
        self.client = client

    def generate(self) -> Dict[str, Any]:
        """
        Generate new API key (Owner/Admin only).

        Returns:
            Dict with api_key, created_at, warning
        """
        return self.client._request("POST", "/institutions/api-keys/generate/")

    def info(self) -> Dict[str, Any]:
        """Get API key information (masked)"""
        return self.client._request("GET", "/institutions/api-keys/info/")

    def regenerate(self) -> Dict[str, Any]:
        """
        Regenerate API key (revokes old, creates new).

        Returns:
            Dict with new api_key
        """
        return self.client._request("POST", "/institutions/api-keys/regenerate/")

    def revoke(self) -> Dict[str, Any]:
        """Revoke current API key"""
        return self.client._request("POST", "/institutions/api-keys/revoke/")


class TeamResource:
    """Team management methods"""

    def __init__(self, client: DocWalClient):
        self.client = client

    def list(self) -> Dict[str, Any]:
        """
        List all team members and pending invitations.

        Returns:
            Dict with members, pending_invitations, stats
        """
        return self.client._request("GET", "/institutions/team/")

    def check_email(self, email: str) -> Dict[str, Any]:
        """
        Check if email is valid for invitation.

        Args:
            email: Email address to check

        Returns:
            Dict with validation result and recommendation
        """
        data = {"email": email}
        return self.client._request("POST", "/institutions/team/check-email/", data=data)

    def invite(
        self,
        email: str,
        role: str = "issuer",
        send_email: bool = True,
        add_directly: bool = False,
    ) -> Dict[str, Any]:
        """
        Invite team member.

        Args:
            email: Email address (must use institution domain)
            role: Role (owner, admin, issuer)
            send_email: Send invitation email
            add_directly: Add directly if user exists (skip invitation)

        Returns:
            Dict with invitation or member details
        """
        data = {
            "email": email,
            "role": role,
            "send_email": send_email,
            "add_directly": add_directly,
        }
        return self.client._request("POST", "/institutions/team/invite/", data=data)

    def update_role(self, member_id: str, role: str) -> Dict[str, Any]:
        """Update team member role"""
        data = {"role": role}
        return self.client._request("PATCH", f"/institutions/team/members/{member_id}/role/", data=data)

    def deactivate(self, member_id: str, reason: Optional[str] = None) -> Dict[str, Any]:
        """Deactivate team member (soft delete)"""
        data = {"reason": reason} if reason else {}
        return self.client._request("POST", f"/institutions/team/members/{member_id}/deactivate/", data=data)

    def reactivate(self, member_id: str) -> Dict[str, Any]:
        """Reactivate team member"""
        return self.client._request("POST", f"/institutions/team/members/{member_id}/reactivate/")

    def remove(self, member_id: str) -> Dict[str, Any]:
        """Remove team member (hard delete)"""
        return self.client._request("DELETE", f"/institutions/team/members/{member_id}/remove/")

from google.cloud import secretmanager

def access_secret(project_id, secret_id, version):
    """
    Access a secret- API token, etc- stored in Secret Manager

    Code from https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#secretmanager-access-secret-version-python
    """
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    name = client.secret_version_path(project_id, secret_id, version)

    request=secretmanager.AccessSecretVersionRequest(name=name)

    # Access the secret version
    response = client.access_secret_version(request)

    # Return the secret payload
    payload = response.payload.data.decode('UTF-8')

    return payload

OPENAI_API_KEY = access_secret("lobo-line", "OPENAI_API_KEY", 1)
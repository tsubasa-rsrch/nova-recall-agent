"""
Minimal Bedrock connection test.
Run after setting AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY env vars
(or let it auto-load from tsubasa-daemon/.env).
"""

import os
import json
import boto3
from pathlib import Path


def _load_env():
    env_path = Path.home() / "Documents" / "TsubasaWorkspace" / "tsubasa-daemon" / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


_load_env()


def test_bedrock_nova_lite():
    """Test Nova Lite (cheapest model) with a simple prompt."""
    client = boto3.client(
        "bedrock-runtime",
        region_name="us-east-1",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{
            "role": "user",
            "content": [{"text": "Say 'Nova connection OK' and nothing else."}]
        }],
        inferenceConfig={"maxTokens": 20, "temperature": 0.0},
    )

    text = response["output"]["message"]["content"][0]["text"]
    print(f"✅ Nova Lite response: {text}")
    print(f"✅ Input tokens: {response['usage']['inputTokens']}")
    print(f"✅ Output tokens: {response['usage']['outputTokens']}")
    return True


if __name__ == "__main__":
    print("Testing Bedrock → Nova Lite connection...")
    if not os.environ.get("AWS_ACCESS_KEY_ID"):
        print("❌ AWS_ACCESS_KEY_ID not set. Export your IAM credentials first.")
        print("   export AWS_ACCESS_KEY_ID=AKIAxxxxxxxx")
        print("   export AWS_SECRET_ACCESS_KEY=xxxxxxxxxx")
    else:
        test_bedrock_nova_lite()

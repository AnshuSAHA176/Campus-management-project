

import os

from cloudflare import Cloudflare


client = Cloudflare(
    account_id=os.environ["CLOUDFLARE_ACCOUNT_ID"],
    api_token=os.environ["CLOUDFLARE_API_TOKEN"],
)


def generate_embedding(text: str) -> list[float]:
    response = client.ai.run(
        model_name="@cf/baai/bge-m3",
        text=[text],
    )

    return response["result"]["data"][0]
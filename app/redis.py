import asyncio
import os
from dotenv import load_dotenv

from glide import (
    ClosingError,
    ConnectionError,
    GlideClusterClient,
    GlideClusterClientConfiguration,
    Logger,
    LogLevel,
    NodeAddress,
    RequestError,
    TimeoutError,
    ServerCredentials
)

async def get_conn():

    load_dotenv()

    # Set logger configuration
    Logger.set_logger_config(LogLevel.INFO)

    # Configure the Glide Cluster Client
    credentials = ServerCredentials(username=os.getenv("AWS_REDIS_USER"), password=os.getenv("AWS_REDIS_PASSWORD"))
    addresses = [
        NodeAddress(os.getenv("AWS_REDIS_ENDPOINT"), 6379)
    ]
    config = GlideClusterClientConfiguration(addresses=addresses, credentials=credentials, use_tls=True)
    client = None

    try:
        print("Connecting to Valkey Glide...")

        # Create the client
        client = await GlideClusterClient.create(config)
        print("Connected successfully.")

    except (TimeoutError, RequestError, ConnectionError, ClosingError) as e:
        print(f"An error occurred: {e}")

    return client

async def set_value(data):

    try:
        client = await get_conn()
        # Perform SET operation
        result = await client.set(data["key"], data["value"])
        print(f"Set key 'key' to 'value': {result}")
    
    except Exception as e:
        print(str(e))

    finally:
        if client:
            try:
                await client.close()
                print("Client connection closed.")
            except ClosingError as e:
                print(f"Error closing client: {e}")

async def get_value(data):

    try:
        client = await get_conn()
        # Perform GET operation
        value = await client.get(data)
        print(f"Get response for 'key': {value}")
    
    except Exception as e:
        print(str(e))
        
    finally:
        if client:
            try:
                await client.close()
                print("Client connection closed.")
            except ClosingError as e:
                print(f"Error closing client: {e}")

        return value

async def delete_value(data):

    try:
        client = await get_conn()
        # Perform DELETE operation
        result = await client.delete(data["key"])
    
    except Exception as e:
        print(str(e))

    finally:
        if client:
            try:
                await client.close()
                print("Client connection closed.")
            except ClosingError as e:
                print(f"Error closing client: {e}")

asyncio.run(get_conn())
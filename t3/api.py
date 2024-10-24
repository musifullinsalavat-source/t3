from dotenv import load_dotenv
import os
import supabase
from supabase import create_client, Client

load_dotenv()

key: str = os.getenv('KEY')
url: str = os.getenv('URL')
supabase: Client = create_client(url, key)

# response = (
#     supabase.table("users")
#     .insert({"username": "janedoe123", "email": "janedoe231@example.com"})
#     .execute()
# )

try:
    response = supabase.table("users").select("ja").execute()
except supabase.exceptions.HTTPError as error:
    print(f"Error: {error.status_code} {error.message}")
except Exception as e:
    print(f"Unexpected error: {e}")

print(response)

# if response.raise_when_api_error:
#     print("Error: ", response.error )
# else:
#     print("User added: ", response.data)
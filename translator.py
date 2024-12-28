import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient




AZURE_TENANT_ID=os.getenv("AZURE_TENANT_ID","")
AZURE_CLIENT_ID=os.getenv("AZURE_CLIENT_ID","")
AZURE_SECRET_ID=os.getenv("AZURE_SECRET_ID","")
#KEY_VAULT_URL=env.get("KEY_VAULT_URL","")
KEY_VAULT_URL="https://azureaiproject.vault.azure.net/"

print(f"Tenant ID: {AZURE_TENANT_ID},{AZURE_CLIENT_ID},{AZURE_SECRET_ID}")
#input("enter text")

# Authenticate using DefaultAzureCredential
_credential = ClientSecretCredential(
    tenant_id=AZURE_TENANT_ID,
    client_id=AZURE_CLIENT_ID,
    client_secret=AZURE_SECRET_ID
)

key_client = SecretClient(vault_url=KEY_VAULT_URL, credential=_credential)

key=key_client.get_secret('ai900aikeyvault').value

# set `<your-key>`, `<your-endpoint>`, and  `<region>` variables with the values from the Azure portal
endpoint = "https://api.cognitive.microsofttranslator.com/"
region = "eastus"

credential = TranslatorCredential(key, region)
text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

try:
    source_language = "en"
    target_languages = ["es", "it"]
    input_text_elements = [ InputTextItem(text = "This is a test") ]

    response = text_translator.translate(content = input_text_elements, to = target_languages, from_parameter = source_language)
    translation = response[0] if response else None

    if translation:
        for translated_text in translation.translations:
            print(f"Text was translated to: '{translated_text.to}' and the result is: '{translated_text.text}'.")

except HttpResponseError as exception:
    print(f"Error Code: {exception.error.code}")
    print(f"Message: {exception.error.message}")

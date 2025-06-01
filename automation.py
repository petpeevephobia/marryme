import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
import openai
import ast
import json
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env.local')
load_dotenv(dotenv_path, override=True)
load_dotenv(dotenv_path=".env", override=False)





# GET AUTH VALUES
SCOPES = [
    'https://www.googleapis.com/auth/presentations',
    'https://www.googleapis.com/auth/drive'
]
openai.api_key = os.getenv('OPENAI_API_KEY')

def authenticate_with_service_account():
    with open(os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH"), "r") as f:
        GOOGLE_SERVICE_ACCOUNT = json.load(f)

    creds = service_account.Credentials.from_service_account_info(
        GOOGLE_SERVICE_ACCOUNT,
        scopes=SCOPES
    )
    return creds





# DUPE GOOGLE SLIDES TEMPLATE
def copy_presentation(template_id, new_title, credentials):
    drive_service = build('drive', 'v3', credentials=credentials)
    body = {'name': new_title}
    presentation_copy = drive_service.files().copy(fileId=template_id, body=body).execute()
    return presentation_copy['id']





# GIVE MYSELF ACCESS TO THE DUPED SLIDES
def give_me_access_to_file(file_id, my_email, credentials):
    drive_service = build('drive', 'v3', credentials=credentials)
    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': my_email
    }
    drive_service.permissions().create(
        fileId=file_id,
        body=permission,
        fields='id',
        sendNotificationEmail=True  # Optional: send yourself an email
    ).execute()








# CONVERT CLIENT NOTES INTO JSON
def parse_client_notes(notes):
    print('OpenAI triggered')

    with open("services.txt", "r", encoding="utf-8") as file:
        services = file.read()

        # print(services)
    with open("prompt.txt", "r", encoding="utf-8") as file:
        prompt = f"{file.read()}/n/nUse this guide as a heavy reference to produce for specific keys: {services}. Here are the raw client notes that you must refer to as well: {notes}"

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    raw_output = response.choices[0].message.content
    
    # Remove markdown fences if they still appear
    raw_output = raw_output.strip().strip("```").replace("python", "").strip()
    
    # Safely turn string into dict
    return ast.literal_eval(raw_output)





# ADD DETAILS TO THE SLIDES
def replace_text_in_slides(presentation_id, replacements, credentials):
    """
    Replace text placeholders in a Google Slides presentation.

    Args:
        presentation_id (str): The ID of the Google Slides presentation.
        replacements (dict): A dictionary of placeholder-to-value pairs.
            Example: {"{{client_name}}": "Padi@Bussorah"}
        credentials: Authenticated Google credentials (from service account or OAuth2).
    """
    slides_service = build('slides', 'v1', credentials=credentials)

    requests = []
    for placeholder, value in replacements.items():
        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': placeholder,
                    'matchCase': True
                },
                'replaceText': value
            }
        })

    response = slides_service.presentations().batchUpdate(
        presentationId=presentation_id,
        body={'requests': requests}
    ).execute()

    return response





# ONLY USE NEEDED KEYS FROM result
def extract_keys(full_dict, keys_to_keep):
    return {k: full_dict[k] for k in keys_to_keep if k in full_dict}










if __name__ == '__main__':
    print("👋 Script started")

    TEMPLATE_ID = os.getenv('PRESENTATION_ID')  # Your template Slides ID

    # Get raw client notes
    with open("client_notes.txt", "r", encoding="utf-8") as file:
        client_notes = file.read()

    # Parse into structured result
    print('🤖 Parsing client notes...')
    result = parse_client_notes(notes=client_notes)

    # Keep only what's needed
    needed = ["client_name", "budget", "timeline", "goal", "extras"]
    client_data = extract_keys(result, needed)

    # Load Google credentials to dupe the new slide into my own Drive
    creds = authenticate_with_service_account()

    # Duplicate the Slides template
    print('🔄 Duplicating template...')
    new_presentation_id = copy_presentation(
        template_id=TEMPLATE_ID,
        new_title=f"Proposal for {client_data.get('client_name', 'Client')}",
        credentials=creds
    )

    # Give myself access to the duplicated presentation
    print('🔑 Giving myself access...')
    my_email = os.getenv("MY_EMAIL")
    give_me_access_to_file(new_presentation_id, my_email, creds)

    # Replace text in duplicated presentation
    print('📝 Adding details to slides...')
    replace_text_in_slides(new_presentation_id, {
        f"{{{{{key}}}}}": "\n".join(value) if isinstance(value, list) else str(value)
        for key, value in client_data.items()
    }, creds)

    print(f"✅ Slides created: https://docs.google.com/presentation/d/{new_presentation_id}/edit")
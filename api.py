import requests
import re
from api_key import API_KEY

#upload data for rag
def upload_file(API_KEY, file_path):
    url = 'http://localhost:3000/api/v1/files/'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Accept': 'application/json'
    }
    files = {'file': open(file_path, 'rb')}
    response = requests.post(url, headers=headers, files=files)
    return response.json().get("id", "Error: ID not found")

#adding files to collections
def add_file_to_knowledge(API_KEY, knowledge_id, file_id):
    url = f'http://localhost:3000/api/v1/knowledge/{knowledge_id}/file/add'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {'file_id': file_id}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

#build request with collection id
def pypanther_collectionId(model,API_KEY,message,collection_id):
    API_URL = "http://localhost:3000/api/chat/completions"  

    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
            'files': [{'type': 'collection', 'id': collection_id}]
        }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        raw_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error: No response")
        reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL).strip()
    else:
        reply = f"Error {response.status_code}: {response.text}"
        
    return reply

#build request
def pypanther(model,API_KEY,message):
    API_URL = "http://localhost:3000/api/chat/completions"  

    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
            "model": model,
            "messages": [{"role": "user", "content": message}],
        }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        raw_reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error: No response")
        reply = re.sub(r"<think>.*?</think>", "", raw_reply, flags=re.DOTALL).strip()
    else:
        reply = f"Error {response.status_code}: {response.text}"
        
    return reply

'''
file_id = upload_file(API_KEY,'documents/Handbook-06-2022.pdf')
print(add_file_to_knowledge(API_KEY,knowledge_id,file_id))

file_id2 = upload_file(API_KEY,'documents/faq_cs_graduate.pdf')
print(add_file_to_knowledge(API_KEY,knowledge_id,file_id2))
collection_id = "f802b70c-647c-4273-b7ee-75ee12a404c6"'''

question = "What are tuition and fees?"
answer = pypanther("aics",API_KEY,question)
print(answer)
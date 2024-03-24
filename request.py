import requests

url = 'http://127.0.0.1:8090/aigic'


response = requests.post(url, json={'addr':'1TryMe'})

if response.status_code == 200:
    print('String sent successfully!')
    result = response.json()
    print('Feedback result:', result['content']['output'])
else:
    print('Failed to send string.')

import requests
import random
import string
import bip38


url = 'http://127.0.0.1:8090/aigic'
valid_cnt = 0
invalid_cnt = 0
while True:
    print("###############################################")
    prefix = '1' + ''.join(random.choices(string.ascii_letters.replace('O', '').replace('l', ''), k=5))
    print("Sending prefix: ", prefix)
    response = requests.post(url, json={'addr':prefix})

    if response.status_code == 200:
        print('String sent successfully!')
        result = response.json()
        content = result['content']['output']
        print('Feedback result:', content)

        start_index = content.find('Base Key: ') + len('Base Key: ')
        end_index = content.find('\n', start_index)
        base_key = content[start_index:end_index]
        #print('Base Key:', base_key)

        start_index = content.find('PubAddress: ') + len('PubAddress: ')
        end_index = content.find('\n', start_index)
        pub_address = content[start_index:end_index]
        #print('PubAddress:', pub_address)

        start_index = content.find('Priv (WIF): ') + len('Priv (WIF): ') + 6
        end_index = content.find('\n', start_index)
        priv_address = content[start_index:end_index]
        #print('PrivAddress:', priv_address)

        start_index = content.find('Priv (HEX): ') + len('Priv (HEX): ') + 2
        priv_hex = content[start_index:]
        
        #print('PrivAddress(HEX):', priv_hex)

        if pub_address.startswith(prefix):
            print('Pub Prefix is valid.')

            priv_key_val = bip38.wif_to_private_key(priv_address)
            pub_hex_val = bip38.private_key_to_public_key(priv_key_val)
            pub_address_val = bip38.public_key_to_addresses(pub_hex_val)

            print('Priv + Key -> Pub:', pub_address_val)
            if pub_address_val[:20] == pub_address[:20]:
                print('PubAddress is valid.')
                valid_cnt += 1
            else:
                print('Priv + Key -> Pub is not valid.')
                invalid_cnt += 1
        else:
            print('Pub Prefix is not valid.')
            invalid_cnt += 1
    else:
        print('Failed to send string.')
    
    print('Valid:', valid_cnt, 'Invalid:', invalid_cnt)

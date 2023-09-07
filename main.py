import json, requests
from time import sleep

with open('config.json', 'r') as file:
    config_pipefy = json.load(file)

pipeID = config_pipefy["pipeID"]

phaseID = config_pipefy["phaseID"]

token = config_pipefy["pipefyToken"]

url = "https://api.pipefy.com/graphql"


def create_card(nome, telefone, token, pipeID, phaseID, url):
    headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    payload = {"query": f"""mutation
                {{createCard
                (input: 
                {{pipe_id: "{pipeID}" 
                phase_id: "{phaseID}" 
                fields_attributes: [ 
                {{field_id: "nome_da_empresa", field_value: "{nome}"}}   
                {{field_id: "telefone_do_contato", field_value: "{telefone}"}}   
                ] 
                }}
                )
                {{clientMutationId card {{id title}}
                }}
                }}"""
                }
    sleep(3)
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()["data"]["createCard"]["card"]["id"]

def update_card(token, cardID, url):
        payload = {"query": f"""mutation {{
        updateCardField(input: {{
                card_id: {cardID},
                field_id: "qual_o_meio_de_contato",
                new_value: "Telefone (Mensagem)"
            }})
            {{
            card {{
            fields {{
                value
                field{{
                label
                id
                }}
            }}
            }}
            success
        }}
        }}
        """
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        requests.request("POST", url, json=payload, headers=headers)
        # print(response.text)
        
with open('output.json', 'r') as file:
  data = json.load(file)
  
for card in data:
    nome = card["name"]
    telefone = card["number"]
    cardID = create_card(nome, telefone, token, pipeID, phaseID)
    update_card(token, cardID)

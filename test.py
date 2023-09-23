import api
import pandas as pd


def partes_to_df(grau):
    return pd.DataFrame.from_dict(result.get("%s Grau" % grau).get("partes"))


def mov_to_df(grau):
    return pd.DataFrame.from_dict(result.get("%s Grau" % grau).get("movimentações"))


exemplo = "1129955-58.2023.8.26.0100"
result = api.get_processo_handler(exemplo)

text = f"Informações do processo { result.get('id') }\n\n"
print(text)
# for key, value in result.items():
#     if key != "id":
#         text += f"{key}\n\n"
#         if 'ERROR' in result[key]:
#             text += f"{ result[key] }\n\n"
#         else:
#             for field in value:
#                 text += f"{ field }: { value[field] }\n\n"
dataframe = pd.DataFrame.from_dict(result)
print(dataframe.head(6))

for grau in ["Primeiro", "Segundo"]:
    print(f"\n * {grau} Grau *")

    partes = partes_to_df(grau)
    print(f"\nPartes\n{partes}") if not partes.empty else print("\nPartes: Nenhum registro")

    mov = mov_to_df(grau)
    print(f"\nMovimentações\n{mov}") if not mov.empty else print("\nMovimentações: Nenhum registro\n")
with open(f'{exemplo}.json', 'w', encoding='utf-8') as file:
    dataframe.to_json(file, force_ascii=False)
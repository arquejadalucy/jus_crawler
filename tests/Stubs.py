from app.models import ProcessRequestBody, ProcessRequestInformations

PROCESSO_NAO_ENCONTRADO = "Não existem informações disponíveis para os parâmetros informados."

DOMINIO_TJAL = "www2.tjal.jus.br"
NUMERO_PROCESSO_TEST = "0165801-59.2019.8.06.0001"
NUMERO_PROCESSO_TEST_CODIGO = "0710802-55.2018.8.02.0001"
CODIGO_PROCESSO = "P00006BXP0000"

request_body_json_test = {
  "numero_processo": NUMERO_PROCESSO_TEST
}

def get_url_tjal_segundo_grau(processo_info: ProcessRequestInformations):
    return f"https://{DOMINIO_TJAL}/cposg5/search.do?conversationId=&paginaConsulta=0&cbPesquisa=NUMPROC" \
    f"&numeroDigitoAnoUnificado={processo_info.numeroDigitoAnoUnificado}" \
    f"&foroNumeroUnificado={processo_info.foro}&dePesquisaNuUnificado={processo_info.numero_processo}" \
    f"&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO"

expected_response_body = {
    "id": NUMERO_PROCESSO_TEST,
    "Primeiro Grau": {
        "classe": "Procedimento Comum Cível",
        "area": "Cível",
        "assunto": "Planos de Saúde",
        "data": "30/08/2019",
        "juiz": "ROBERTA PONTE MARQUES MAIA",
        "valor": "R$ 3.000,00",
        "partes": [
            {
                "nome": "Paulo Sergio Quezado de Castro",
                "tipo_de_participacao": "Requerente",
                "advogados": [
                    "Cristiano Porto Linhares Teixeira"
                ]
            },
            {
                "nome": "Amil - Assistência Médica Internacional Ltda",
                "tipo_de_participacao": "Requerido",
                "advogados": [
                    "Antônio de Moraes Dourado Neto"
                ]
            }
        ],
        "movimentações": [
            {
                "data_movimentação": "13/05/2021",
                "descrição_movimentação": "Remetido Recurso Eletrônico ao Tribunal de Justiça"
            },
            {
                "data_movimentação": "13/05/2021",
                "descrição_movimentação": "Certidão emitida"
            },
            {
                "data_movimentação": "12/05/2021",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.21.02047703-2 Tipo da Petição: Contrarrazões Recursais Data: 12/05/2021 12:36"
            },
            {
                "data_movimentação": "19/04/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0131/2021 Data da Publicação: 20/04/2021 Número do Diário: 2592"
            },
            {
                "data_movimentação": "16/04/2021",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0131/2021 Teor do ato: Considerando que, segundo a nova ordem processual instituída pelo CPC/15, a atividade de recebimento de recurso de apelação se tornou meramente administrativa pelo magistrado de grau primevo, conforme art. 1.010, § 3º, recebo a interposição da peça apelatória de fls. Retro. Intime-se, pois, a parte apelada para apresentação facultativa de contrarrazões recursais, em quinze dias, na forma do art. 1.010, § 1º, do CPC/15. Acaso apresentadas, caso se vislumbre insurgência acerca de questões resolvidas ao longo do processo, conceda-se o prazo de que trata o art. 1.009, § 2º, do CPC/15, à parte adversa. Por outro lado, se apresentado recurso adesivo, intime-se a outra parte para contrarrazoar, por quinze dias, na forma do art. 1.010, § 2º, do CPC/15, observando-se, em seguida, a existência ou não de argumentação acerca doutras questões solvidas preteritamente, a fim de cumprir a exigência supraespecificada. Advogados(s): Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "13/05/2021",
                "descrição_movimentação": "Remetido Recurso Eletrônico ao Tribunal de Justiça"
            },
            {
                "data_movimentação": "13/05/2021",
                "descrição_movimentação": "Certidão emitida"
            },
            {
                "data_movimentação": "12/05/2021",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.21.02047703-2 Tipo da Petição: Contrarrazões Recursais Data: 12/05/2021 12:36"
            },
            {
                "data_movimentação": "19/04/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0131/2021 Data da Publicação: 20/04/2021 Número do Diário: 2592"
            },
            {
                "data_movimentação": "16/04/2021",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0131/2021 Teor do ato: Considerando que, segundo a nova ordem processual instituída pelo CPC/15, a atividade de recebimento de recurso de apelação se tornou meramente administrativa pelo magistrado de grau primevo, conforme art. 1.010, § 3º, recebo a interposição da peça apelatória de fls. Retro. Intime-se, pois, a parte apelada para apresentação facultativa de contrarrazões recursais, em quinze dias, na forma do art. 1.010, § 1º, do CPC/15. Acaso apresentadas, caso se vislumbre insurgência acerca de questões resolvidas ao longo do processo, conceda-se o prazo de que trata o art. 1.009, § 2º, do CPC/15, à parte adversa. Por outro lado, se apresentado recurso adesivo, intime-se a outra parte para contrarrazoar, por quinze dias, na forma do art. 1.010, § 2º, do CPC/15, observando-se, em seguida, a existência ou não de argumentação acerca doutras questões solvidas preteritamente, a fim de cumprir a exigência supraespecificada. Advogados(s): Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "13/04/2021",
                "descrição_movimentação": "Outras Decisões Considerando que, segundo a nova ordem processual instituída pelo CPC/15, a atividade de recebimento de recurso de apelação se tornou meramente administrativa pelo magistrado de grau primevo, conforme art. 1.010, § 3º, recebo a interposição da peça apelatória de fls. Retro. Intime-se, pois, a parte apelada para apresentação facultativa de contrarrazões recursais, em quinze dias, na forma do art. 1.010, § 1º, do CPC/15. Acaso apresentadas, caso se vislumbre insurgência acerca de questões resolvidas ao longo do processo, conceda-se o prazo de que trata o art. 1.009, § 2º, do CPC/15, à parte adversa. Por outro lado, se apresentado recurso adesivo, intime-se a outra parte para contrarrazoar, por quinze dias, na forma do art. 1.010, § 2º, do CPC/15, observando-se, em seguida, a existência ou não de argumentação acerca doutras questões solvidas preteritamente, a fim de cumprir a exigência supraespecificada."
            },
            {
                "data_movimentação": "13/04/2021",
                "descrição_movimentação": "Concluso para Despacho"
            },
            {
                "data_movimentação": "08/04/2021",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.21.01981784-4 Tipo da Petição: RECURSO DE APELAÇÃO Data: 08/04/2021 17:39"
            },
            {
                "data_movimentação": "15/03/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0090/2021 Data da Publicação: 16/03/2021 Número do Diário: 2571"
            },
            {
                "data_movimentação": "15/03/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0090/2021 Data da Publicação: 16/03/2021 Número do Diário: 2571"
            },
            {
                "data_movimentação": "12/03/2021",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0090/2021 Teor do ato: Isso posto, rejeito os embargos declaratórios opostos, mantendo a decisão atacada por seus próprios fundamentos, com esteio no art. 1.024 do CPC/15. Intimem-se. Reinicie-se a contagem do prazo recursal e, findo este sem interposição de recurso, à conclusão para sentença. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE), Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "12/03/2021",
                "descrição_movimentação": "Embargos de Declaração Não-acolhidos Isso posto, rejeito os embargos declaratórios opostos, mantendo a decisão atacada por seus próprios fundamentos, com esteio no art. 1.024 do CPC/15. Intimem-se. Reinicie-se a contagem do prazo recursal e, findo este sem interposição de recurso, à conclusão para sentença."
            },
            {
                "data_movimentação": "09/03/2021",
                "descrição_movimentação": "Conclusos"
            },
            {
                "data_movimentação": "09/03/2021",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.21.01923056-8 Tipo da Petição: Embargos de Declaração Cível Data: 09/03/2021 13:13"
            },
            {
                "data_movimentação": "09/03/2021",
                "descrição_movimentação": "Processo entranhado Entranhado o processo 0165801-59.2019.8.06.0001/03 - Classe: Embargos de Declaração Cível em Procedimento Comum Cível - Assunto principal: Planos de Saúde"
            },
            {
                "data_movimentação": "09/03/2021",
                "descrição_movimentação": "Recurso interposto Seq.: 03 - Embargos de Declaração Cível"
            },
            {
                "data_movimentação": "01/03/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0070/2021 Data da Publicação: 02/03/2021 Número do Diário: 2561"
            },
            {
                "data_movimentação": "01/03/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0069/2021 Data da Publicação: 02/03/2021 Número do Diário: 2561"
            },
            {
                "data_movimentação": "01/03/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0068/2021 Data da Publicação: 02/03/2021 Número do Diário: 2561"
            },
            {
                "data_movimentação": "26/02/2021",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0070/2021 Teor do ato: Vistos. Com fundamento no art. 1.023, § 2º, do CPC/15, intime-se o embargado para manifestação facultativa em cinco dias, sob pena de preclusão. Expedientes necessários. Advogados(s): Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "26/02/2021",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0069/2021 Teor do ato: Vistos. Com fundamento no art. 1.023, § 2º, do CPC/15, intime-se o embargado para manifestação facultativa em cinco dias, sob pena de preclusão. Expedientes necessários. Advogados(s): Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "26/02/2021",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0068/2021 Teor do ato: Vistos. Com fundamento no art. 1.023, § 2º, do CPC/15, intime-se o embargado para manifestação facultativa em cinco dias, sob pena de preclusão. Expedientes necessários. Advogados(s): Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "24/02/2021",
                "descrição_movimentação": "Proferido despacho de mero expediente Vistos. Com fundamento no art. 1.023, § 2º, do CPC/15, intime-se o embargado para manifestação facultativa em cinco dias, sob pena de preclusão. Expedientes necessários."
            },
            {
                "data_movimentação": "12/02/2021",
                "descrição_movimentação": "Prazo alterado pelo ajuste na tabela de feriados Prazo referente ao usuário foi alterado para 18/02/2021 devido à alteração da tabela de feriados"
            },
            {
                "data_movimentação": "28/01/2021",
                "descrição_movimentação": "Concluso para Despacho"
            },
            {
                "data_movimentação": "28/01/2021",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.21.01838461-8 Tipo da Petição: Embargos de Declaração Cível Data: 28/01/2021 14:22"
            },
            {
                "data_movimentação": "28/01/2021",
                "descrição_movimentação": "Processo entranhado Entranhado o processo 0165801-59.2019.8.06.0001/02 - Classe: Embargos de Declaração Cível em Procedimento Comum Cível - Assunto principal: Planos de Saúde"
            },
            {
                "data_movimentação": "28/01/2021",
                "descrição_movimentação": "Recurso interposto Seq.: 02 - Embargos de Declaração Cível"
            },
            {
                "data_movimentação": "22/01/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0018/2021 Data da Publicação: 25/01/2021 Número do Diário: 2535"
            },
            {
                "data_movimentação": "22/01/2021",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0018/2021 Data da Publicação: 25/01/2021 Número do Diário: 2535"
            },
            {
                "data_movimentação": "21/01/2021",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0018/2021 Teor do ato: Isso posto, sob esses fundamentos, acolho os embargos de declaração manejados pelo autor para retificar o dispositivo da sentença lançada às fls. 729/735, especificamente no tangente ao medicamento que deve ser fornecido pela requerida, correspondente ao Cosentyx, em substituição ao Stelara. Outrossim, acresço à decisão que o medicamento similar admitido, ante a impossibilidade do fornecimento do Cosentyx, consiste em fármaco de mesma dosagem e de mesmo princípio ativo, conforme receituário médico de profissional dermatologista, fls. 21. Publique-se. Registre-se. Intimem-se. Reinicie-se a contagem do prazo recursal e, findo este sem interposição de recurso, certifique-se e arquive-se. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE), Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "20/01/2021",
                "descrição_movimentação": "Embargos de Declaração Acolhidos Isso posto, sob esses fundamentos, acolho os embargos de declaração manejados pelo autor para retificar o dispositivo da sentença lançada às fls. 729/735, especificamente no tangente ao medicamento que deve ser fornecido pela requerida, correspondente ao Cosentyx, em substituição ao Stelara. Outrossim, acresço à decisão que o medicamento similar admitido, ante a impossibilidade do fornecimento do Cosentyx, consiste em fármaco de mesma dosagem e de mesmo princípio ativo, conforme receituário médico de profissional dermatologista, fls. 21. Publique-se. Registre-se. Intimem-se. Reinicie-se a contagem do prazo recursal e, findo este sem interposição de recurso, certifique-se e arquive-se."
            },
            {
                "data_movimentação": "24/11/2020",
                "descrição_movimentação": "Conclusos"
            },
            {
                "data_movimentação": "24/11/2020",
                "descrição_movimentação": "Certidão emitida"
            },
            {
                "data_movimentação": "05/11/2020",
                "descrição_movimentação": "Certidão emitida"
            },
            {
                "data_movimentação": "03/11/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01535698-1 Tipo da Petição: Petições Intermediárias Diversas Data: 03/11/2020 16:29"
            },
            {
                "data_movimentação": "03/11/2020",
                "descrição_movimentação": "Proferido despacho de mero expediente Vistos. Com fundamento no art. 1.023, § 2º, do CPC/15, intime-se o embargado para manifestação facultativa, em cinco dias, sobre os embargos de declaração de fls. 738/740, sob pena de preclusão. Intime-se."
            },
            {
                "data_movimentação": "23/10/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01519755-7 Tipo da Petição: Petições Intermediárias Diversas Data: 23/10/2020 11:20"
            },
            {
                "data_movimentação": "22/10/2020",
                "descrição_movimentação": "Concluso para Despacho"
            },
            {
                "data_movimentação": "16/10/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01502170-0 Tipo da Petição: Petições Intermediárias Diversas Data: 16/10/2020 09:24"
            },
            {
                "data_movimentação": "16/10/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01502082-7 Tipo da Petição: Embargos de Declaração Cível Data: 16/10/2020 09:17"
            },
            {
                "data_movimentação": "16/10/2020",
                "descrição_movimentação": "Processo entranhado Entranhado o processo 0165801-59.2019.8.06.0001/01 - Classe: Embargos de Declaração Cível em Procedimento Comum Cível - Assunto principal: Planos de Saúde"
            },
            {
                "data_movimentação": "16/10/2020",
                "descrição_movimentação": "Recurso interposto Seq.: 01 - Embargos de Declaração Cível"
            },
            {
                "data_movimentação": "07/10/2020",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0598/2020 Data da Publicação: 07/10/2020 Número do Diário: 2474"
            },
            {
                "data_movimentação": "07/10/2020",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0598/2020 Data da Publicação: 07/10/2020 Número do Diário: 2474"
            },
            {
                "data_movimentação": "03/10/2020",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0598/2020 Teor do ato: Ante o exposto, julgo procedente o pedido inicial para condenar a promovida ao cumprimento da obrigação de fazer consistente no fornecimento de 2 (duas) injeções de Stelara (laboratório Jassen), ou similar da mesma qualidade, periodicamente a cada 3 (três) meses, conforme discriminado à fl. 22, confirmando-se, com isso, a liminar concedida nos autos. Declaro extinto o processo, com julgamento do mérito (artigo 487, I, do CPC). Em razão da sucumbência, condeno a promovida ao pagamento das custas processuais e dos honorários advocatícios devidos ao patrono da autora, que arbitro, por equidade, em R$ 3.000,00 (três mil reais). Publique-se. Registre-se. Intimem-se. Após o trânsito em julgado, certifique-se e arquive-se. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE), Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "30/09/2020",
                "descrição_movimentação": "Julgado procedente o pedido Ante o exposto, julgo procedente o pedido inicial para condenar a promovida ao cumprimento da obrigação de fazer consistente no fornecimento de 2 (duas) injeções de Stelara (laboratório Jassen), ou similar da mesma qualidade, periodicamente a cada 3 (três) meses, conforme discriminado à fl. 22, confirmando-se, com isso, a liminar concedida nos autos. Declaro extinto o processo, com julgamento do mérito (artigo 487, I, do CPC). Em razão da sucumbência, condeno a promovida ao pagamento das custas processuais e dos honorários advocatícios devidos ao patrono da autora, que arbitro, por equidade, em R$ 3.000,00 (três mil reais). Publique-se. Registre-se. Intimem-se. Após o trânsito em julgado, certifique-se e arquive-se."
            },
            {
                "data_movimentação": "17/09/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01450087-6 Tipo da Petição: Petições Intermediárias Diversas Data: 17/09/2020 07:37"
            },
            {
                "data_movimentação": "03/08/2020",
                "descrição_movimentação": "Concluso para Sentença"
            },
            {
                "data_movimentação": "09/07/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01319976-5 Tipo da Petição: Petições Intermediárias Diversas Data: 09/07/2020 18:29"
            },
            {
                "data_movimentação": "03/07/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01307459-8 Tipo da Petição: Petições Intermediárias Diversas Data: 03/07/2020 08:25"
            },
            {
                "data_movimentação": "02/07/2020",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0423/2020 Data da Publicação: 03/07/2020 Número do Diário: 2407"
            },
            {
                "data_movimentação": "01/07/2020",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0423/2020 Teor do ato: Considerando o fim da atividade postulatória com a apresentação da réplica de fls. 583/589, bem como a inexistência de causas obstativas do mérito argumentadas ou ex officio detectadas, determino sejam intimadas as partes para especificarem as provas que pretendem produzir, justificando-as, atentando-se para seus ônus especificados no art. 373 do CPC/15, em quinze dias. Alerto que o silêncio das partes poderá implicar em julgamento antecipado do mérito, na forma do art. 355, I, do CPC/15. Intimem-se. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE), Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "29/06/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01297186-3 Tipo da Petição: Petições Intermediárias Diversas Data: 29/06/2020 13:03"
            },
            {
                "data_movimentação": "22/06/2020",
                "descrição_movimentação": "Outras Decisões Considerando o fim da atividade postulatória com a apresentação da réplica de fls. 583/589, bem como a inexistência de causas obstativas do mérito argumentadas ou ex officio detectadas, determino sejam intimadas as partes para especificarem as provas que pretendem produzir, justificando-as, atentando-se para seus ônus especificados no art. 373 do CPC/15, em quinze dias. Alerto que o silêncio das partes poderá implicar em julgamento antecipado do mérito, na forma do art. 355, I, do CPC/15. Intimem-se."
            },
            {
                "data_movimentação": "19/06/2020",
                "descrição_movimentação": "Concluso para Despacho"
            },
            {
                "data_movimentação": "19/06/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01278449-4 Tipo da Petição: Réplica Data: 19/06/2020 11:10"
            },
            {
                "data_movimentação": "16/06/2020",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0369/2020 Data da Publicação: 17/06/2020 Número do Diário: 2395"
            },
            {
                "data_movimentação": "15/06/2020",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0369/2020 Teor do ato: Vistos em inspeção. Determino que sejam intimadas as partes para especificarem as provas que pretendem produzir, justificando-as, atentando-se para seus ônus especificados no art. 373 do CPC/15, em quinze dias. Alerto que o silêncio das partes poderá implicar em julgamento antecipado do mérito, na forma do art. 355, I, do CPC/15. Intimem-se. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE), Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "01/06/2020",
                "descrição_movimentação": "Outras Decisões Vistos em inspeção. Determino que sejam intimadas as partes para especificarem as provas que pretendem produzir, justificando-as, atentando-se para seus ônus especificados no art. 373 do CPC/15, em quinze dias. Alerto que o silêncio das partes poderá implicar em julgamento antecipado do mérito, na forma do art. 355, I, do CPC/15. Intimem-se."
            },
            {
                "data_movimentação": "25/05/2020",
                "descrição_movimentação": "Concluso para Despacho"
            },
            {
                "data_movimentação": "20/05/2020",
                "descrição_movimentação": "Juntada de Ofício"
            },
            {
                "data_movimentação": "22/04/2020",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0214/2020 Data da Publicação: 23/04/2020 Número do Diário: 2359"
            },
            {
                "data_movimentação": "20/04/2020",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0214/2020 Teor do ato: Manifesta-se a parte autora, em 15 dias, sobre contestação de fls. 172/183 Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE)"
            },
            {
                "data_movimentação": "06/04/2020",
                "descrição_movimentação": "Proferido despacho de mero expediente Manifesta-se a parte autora, em 15 dias, sobre contestação de fls. 172/183"
            },
            {
                "data_movimentação": "31/03/2020",
                "descrição_movimentação": "Concluso para Despacho"
            },
            {
                "data_movimentação": "31/03/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01155364-2 Tipo da Petição: Contestação Data: 31/03/2020 09:30"
            },
            {
                "data_movimentação": "11/03/2020",
                "descrição_movimentação": "Remessa dos Autos a Vara de Origem - Central de Conciliação"
            },
            {
                "data_movimentação": "11/03/2020",
                "descrição_movimentação": "Sessão de Conciliação realizada sem êxito"
            },
            {
                "data_movimentação": "11/03/2020",
                "descrição_movimentação": "Juntada de documento"
            },
            {
                "data_movimentação": "10/03/2020",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.20.01124666-9 Tipo da Petição: Petições Intermediárias Diversas Data: 10/03/2020 12:04"
            },
            {
                "data_movimentação": "12/02/2020",
                "descrição_movimentação": "Certidão emitida"
            },
            {
                "data_movimentação": "12/02/2020",
                "descrição_movimentação": "Expedição de Carta"
            },
            {
                "data_movimentação": "06/02/2020",
                "descrição_movimentação": "Expedição de Ato Ordinatório Conforme disposição expressa na Portaria nº 542/2014, emanada da Diretoria do Fórum Clóvis Beviláqua, cumpram-se os expedientes remanescentes da decisão já proferida nos autos em epígrafe, em especial, para o comparecimento das partes à Audiência de Conciliação na data de 10/03/2020 às 14:00h na sala da COOPERAÇÃO 02, no Centro Judiciário CEJUSC, no Fórum Clóvis Beviláqua. Decisão: \"Conforme disposição expressa na Portaria nº 542/2014, emanada da Diretoria do Fórum Clóvis Beviláqua, designo sessão de Conciliação para a data de 10/03/2020 às 14:00h na sala da Cooperação, no Centro Judiciário. Encaminho os presentes autos à SEJUD respectiva para a confecção dos expedientes necessários.\""
            },
            {
                "data_movimentação": "29/01/2020",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0020/2020 Data da Publicação: 29/01/2020 Número do Diário: 2307"
            },
            {
                "data_movimentação": "27/01/2020",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0020/2020 Teor do ato: Conforme disposição expressa na Portaria nº 542/2014, emanada da Diretoria do Fórum Clóvis Beviláqua, designo sessão de Conciliação para a data de 10/03/2020 às 14:00h na sala da Cooperação, no Centro Judiciário. Encaminho os presentes autos à SEJUD respectiva para a confecção dos expedientes necessários. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE), Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "19/12/2019",
                "descrição_movimentação": "Certidão emitida"
            },
            {
                "data_movimentação": "19/12/2019",
                "descrição_movimentação": "Juntada de documento"
            },
            {
                "data_movimentação": "19/12/2019",
                "descrição_movimentação": "Juntada de documento"
            },
            {
                "data_movimentação": "18/12/2019",
                "descrição_movimentação": "Expedição de Mandado Mandado nº: 001.2019/295544-7 Situação: Cumprido - Ato positivo em 19/12/2019 Local: Oficial de justiça - Jarbas Comin Nunes"
            },
            {
                "data_movimentação": "09/12/2019",
                "descrição_movimentação": "Outras Decisões Vistos. Chamo o feito à ordem para retificar a decisão proferida às fls. 50/55, especificamente a referência ao medicamento a ser fornecido pela requerida, que deve corresponder ao fármaco indicado à fl. 21 (Cosentyx) em vez daquele descrito no receituário que repousa à fl. 26 (Stelara), conforme esclarecido pelo autor às fls. 147/149. Expedientes necessários COM URGÊNCIA."
            },
            {
                "data_movimentação": "15/11/2019",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.19.01676105-5 Tipo da Petição: Petições Intermediárias Diversas Data: 13/11/2019 12:19"
            },
            {
                "data_movimentação": "14/11/2019",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0297/2019 Data da Publicação: 07/10/2019 Número do Diário: 2239"
            },
            {
                "data_movimentação": "14/11/2019",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0297/2019 Data da Publicação: 07/10/2019 Número do Diário: 2239"
            },
            {
                "data_movimentação": "14/11/2019",
                "descrição_movimentação": "Despacho/Decisão disponibilizado no Diário de Justiça Eletrônico Relação :0297/2019 Data da Publicação: 07/10/2019 Número do Diário: 2239"
            },
            {
                "data_movimentação": "04/11/2019",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.19.01655478-5 Tipo da Petição: Petições Intermediárias Diversas Data: 04/11/2019 18:11"
            },
            {
                "data_movimentação": "30/10/2019",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.19.01641995-0 Tipo da Petição: Petições Intermediárias Diversas Data: 29/10/2019 14:59"
            },
            {
                "data_movimentação": "22/10/2019",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.19.01625105-7 Tipo da Petição: Petições Intermediárias Diversas Data: 22/10/2019 09:23"
            },
            {
                "data_movimentação": "04/10/2019",
                "descrição_movimentação": "Expedição de Ato Ordinatório Conforme disposição expressa na Portaria nº 542/2014, emanada da Diretoria do Fórum Clóvis Beviláqua, designo sessão de Conciliação para a data de 10/03/2020 às 14:00h na sala da Cooperação, no Centro Judiciário. Encaminho os presentes autos à SEJUD respectiva para a confecção dos expedientes necessários."
            },
            {
                "data_movimentação": "04/10/2019",
                "descrição_movimentação": "Audiência Designada Conciliação Data: 10/03/2020 Hora 14:00 Local: Cooperação Situacão: Pendente"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Certidão emitida"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Juntada de documento"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Juntada de documento"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Remetidos os Autos para a Central de Conciliação"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0297/2019 Teor do ato: Antes de verificar o atendimento dos requisitos da petição inicial, conforme art. 319 do CPC/15 e demais dispositivos regentes, intime-se o promovente para providenciar o recolhimento das custas judiciais, na forma da tabela anexa à Lei Estadual nº 16.132/16, no prazo de 15 (quinze) dias, sob pena de cancelamento da distribuição, como preconizado no artigo 290 da Novel Lei Adjetiva Civil. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE)"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0297/2019 Teor do ato: Nesse contexto, verifico presentes os pressupostos necessários à concessão da tutela provisória requestada. Ademais, não há que se falar em irreversibilidade da medida antecipatória ora determinada, na forma do art. 300, § 3º, do CPC/15, uma vez que, ainda que eventualmente ao final se apure que a recusa restara contratualmente justificada, abrir-se-á a via de cobrança da operadora em face do promovente, com seus respectivos meios executórios. Com essas breves considerações, presentes os requisitos ensejadores, DEFIRO pedido de tutela provisória de urgência em ordem a determinar que a operadora de plano de saúde demandada, em até cinco dias corridos, adote todas as necessárias providências para fornecer ao promovente o medicamento indicado no receituário acostado à fl. 26, na quantidade e no período nele descrito, sob pena de multa diária no valor de R$ 500,00 (quinhentos reais), com fundamento no art. 301 c/c art. 536, § 1º, do Novo Código de Processo Civil. Destaco que o valor individual e total da multa, além de sua periodicidade, podem ser objeto de revisão, inclusive de ofício, por este magistrado, a fim de que atenda a sua finalidade legal de compelir o cumprimento voluntário da obrigação. Advirto que o descumprimento injustificado deste provimento acarretará no antecipado bloqueio de numerário, via BACENJUD, suficiente à satisfação do autor com as despesas a serem procedidas para a realização do procedimento de forma particular, mediante prévia apresentação de orçamento. Decreto a inversão do ônus da prova, com fulcro no artigo 6º, VIII, do CDC, considerando a hipossuficiência da parte requerente ante o requerido, devendo este, junto com a contestação, apresentar todos os documentos relevantes de que disponha para a análise do mérito, sob pena de preclusão e incidência das consequências das regras de ônus probatórios. No mais, encaminhe-se o feito ao CEJUSC para designação de audiência preliminar de conciliação. Cite-se a parte requerida, com antecedência mínima de 20 (vinte) dias, para comparecer à audiência preliminar designada. Intime-se a requerente do mesmo ato. Advirtam-se ambas as partes de que devem se apresentar à audiência acompanhadas de seus advogados constituídos ou de defensores públicos, em caso de hipossuficiência declarada, bem como que o não comparecimento injustificado do autor ou do réu à audiência de conciliação é considerado ato atentatório à dignidade da justiça e será sancionado com multa de até dois por cento da vantagem econômica pretendida ou do valor da causa, revertida em favor da União ou do Estado, conforme o caso. Resta ciente, ao fim, a requerida de que, caso malograda a solução autocompositiva, detém o prazo de quinze dias para apresentação da contestação, contados a partir da data da audiência preliminar, nos termos do art. 335 do CPC/15. Expedientes necessários, COM URGÊNCIA. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE), Antônio de Moraes Dourado Neto (OAB 23255/PE)"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Encaminhado edital/relação para publicação Relação: 0297/2019 Teor do ato: Considerando que dos autos não consta demonstração de negativa da operadora de plano de saúde acerca do tratamento solicitado na presente demanda (a negativa apresentada refere-se a outra substância), intime-se a parte promovente a fim de que emende a inicial, em quinze dias, sem prejuízo de eventual prorrogação, desde que solicitada dentro do decurso do prazo, acostando documento essencial à sua propositura, consistente na apresentação da negativa formalizada em documento ou, em último caso, ao menos do comprovante de protocolo do pedido administrativo de concessão da terapia, se decorrido in albis prazo razoável para resposta, com fundamento no art. 321 do CPC/15, haja vista a essencial imprescindibilidade de interesse processual, na vertente necessidade de provimento jurisdicional. Advogados(s): Cristiano Porto Linhares Teixeira (OAB 21937/CE)"
            },
            {
                "data_movimentação": "03/10/2019",
                "descrição_movimentação": "Expedição de Mandado Mandado nº: 001.2019/235475-3 Situação: Cumprido - Ato positivo em 03/10/2019 Local: Oficial de justiça - Sangela Rosa Ximenes Silveira"
            },
            {
                "data_movimentação": "02/10/2019",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.19.01582427-4 Tipo da Petição: Petições Intermediárias Diversas Data: 02/10/2019 16:05"
            },
            {
                "data_movimentação": "26/09/2019",
                "descrição_movimentação": "Outras Decisões Nesse contexto, verifico presentes os pressupostos necessários à concessão da tutela provisória requestada. Ademais, não há que se falar em irreversibilidade da medida antecipatória ora determinada, na forma do art. 300, § 3º, do CPC/15, uma vez que, ainda que eventualmente ao final se apure que a recusa restara contratualmente justificada, abrir-se-á a via de cobrança da operadora em face do promovente, com seus respectivos meios executórios. Com essas breves considerações, presentes os requisitos ensejadores, DEFIRO pedido de tutela provisória de urgência em ordem a determinar que a operadora de plano de saúde demandada, em até cinco dias corridos, adote todas as necessárias providências para fornecer ao promovente o medicamento indicado no receituário acostado à fl. 26, na quantidade e no período nele descrito, sob pena de multa diária no valor de R$ 500,00 (quinhentos reais), com fundamento no art. 301 c/c art. 536, § 1º, do Novo Código de Processo Civil. Destaco que o valor individual e total da multa, além de sua periodicidade, podem ser objeto de revisão, inclusive de ofício, por este magistrado, a fim de que atenda a sua finalidade legal de compelir o cumprimento voluntário da obrigação. Advirto que o descumprimento injustificado deste provimento acarretará no antecipado bloqueio de numerário, via BACENJUD, suficiente à satisfação do autor com as despesas a serem procedidas para a realização do procedimento de forma particular, mediante prévia apresentação de orçamento. Decreto a inversão do ônus da prova, com fulcro no artigo 6º, VIII, do CDC, considerando a hipossuficiência da parte requerente ante o requerido, devendo este, junto com a contestação, apresentar todos os documentos relevantes de que disponha para a análise do mérito, sob pena de preclusão e incidência das consequências das regras de ônus probatórios. No mais, encaminhe-se o feito ao CEJUSC para designação de audiência preliminar de conciliação. Cite-se a parte requerida, com antecedência mínima de 20 (vinte) dias, para comparecer à audiência preliminar designada. Intime-se a requerente do mesmo ato. Advirtam-se ambas as partes de que devem se apresentar à audiência acompanhadas de seus advogados constituídos ou de defensores públicos, em caso de hipossuficiência declarada, bem como que o não comparecimento injustificado do autor ou do réu à audiência de conciliação é considerado ato atentatório à dignidade da justiça e será sancionado com multa de até dois por cento da vantagem econômica pretendida ou do valor da causa, revertida em favor da União ou do Estado, conforme o caso. Resta ciente, ao fim, a requerida de que, caso malograda a solução autocompositiva, detém o prazo de quinze dias para apresentação da contestação, contados a partir da data da audiência preliminar, nos termos do art. 335 do CPC/15. Expedientes necessários, COM URGÊNCIA."
            },
            {
                "data_movimentação": "20/09/2019",
                "descrição_movimentação": "Conclusos"
            },
            {
                "data_movimentação": "20/09/2019",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.19.01556850-2 Tipo da Petição: Petições Intermediárias Diversas Data: 20/09/2019 11:07"
            },
            {
                "data_movimentação": "11/09/2019",
                "descrição_movimentação": "Custas Processuais Pagas Custas Iniciais paga em 11/09/2019 através da guia nº 001.1091415-39 no valor de 629,22"
            },
            {
                "data_movimentação": "10/09/2019",
                "descrição_movimentação": "Despacho determinado a emenda da inicial Considerando que dos autos não consta demonstração de negativa da operadora de plano de saúde acerca do tratamento solicitado na presente demanda (a negativa apresentada refere-se a outra substância), intime-se a parte promovente a fim de que emende a inicial, em quinze dias, sem prejuízo de eventual prorrogação, desde que solicitada dentro do decurso do prazo, acostando documento essencial à sua propositura, consistente na apresentação da negativa formalizada em documento ou, em último caso, ao menos do comprovante de protocolo do pedido administrativo de concessão da terapia, se decorrido in albis prazo razoável para resposta, com fundamento no art. 321 do CPC/15, haja vista a essencial imprescindibilidade de interesse processual, na vertente necessidade de provimento jurisdicional.Vencimento: 24/09/2019"
            },
            {
                "data_movimentação": "09/09/2019",
                "descrição_movimentação": "Conclusos"
            },
            {
                "data_movimentação": "06/09/2019",
                "descrição_movimentação": "Juntada de Petição Nº Protocolo: WEB1.19.01527497-5 Tipo da Petição: Pedido de Juntada de Guia de Recolhimento Data: 06/09/2019 14:27"
            },
            {
                "data_movimentação": "05/09/2019",
                "descrição_movimentação": "Custas Processuais Emitidas Guia nº 001.1091415-39 - Custas Iniciais"
            },
            {
                "data_movimentação": "05/09/2019",
                "descrição_movimentação": "Despacho determinado a emenda da inicial Antes de verificar o atendimento dos requisitos da petição inicial, conforme art. 319 do CPC/15 e demais dispositivos regentes, intime-se o promovente para providenciar o recolhimento das custas judiciais, na forma da tabela anexa à Lei Estadual nº 16.132/16, no prazo de 15 (quinze) dias, sob pena de cancelamento da distribuição, como preconizado no artigo 290 da Novel Lei Adjetiva Civil.Vencimento: 19/09/2019"
            },
            {
                "data_movimentação": "30/08/2019",
                "descrição_movimentação": "Conclusos"
            },
            {
                "data_movimentação": "30/08/2019",
                "descrição_movimentação": "Processo Distribuído por Sorteio"
            }
        ]
    },
    "Segundo Grau": {
        "classe": "Apelação Cível",
        "area": "Cível",
        "assunto": "Fornecimento de medicamentos",
        "data": "",
        "juiz": "",
        "valor": "3.000,00",
        "partes": [
            {
                "nome": "Paulo Sérgio Quezado de Castro",
                "tipo_de_participacao": "Apelante:",
                "advogados": [
                    "Cristiano Porto Linhares Teixeira",
                    "Bruna Leite de Matos Sousa"
                ]
            },
            {
                "nome": "AMIL - Assistência Médica Internacional S/A",
                "tipo_de_participacao": "Apelado:",
                "advogados": [
                    "Antônio de Moraes Dourado Neto",
                    "Antônio de Moraes Dourado Neto",
                    "Antônio de Moraes Dourado Neto",
                    "Antônio de Moraes Dourado Neto"
                ]
            }
        ],
        "movimentações": [
            {
                "data_movimentação": "23/05/2023",
                "descrição_movimentação": "Publicado no Diário da Justiça Eletrônico Disponibilizado em 22/05/2023 Tipo de publicação: Despacho Número do Diário Eletrônico: 3080"
            },
            {
                "data_movimentação": "18/05/2023",
                "descrição_movimentação": "Audiência de Conciliação Agendada Considerando a Resolução nº 313/2020 do CNJ e as Portarias nº 01/2020 e 02/2020 do NUPEMEC, designo a audiência conciliatória para o dia 15 de junho de 2023, às 8 horas, a se realizar na modalidade videoconferência. Para acesso à sala virtual, deve-se conectar ao link https://link.tjce.jus.br/723041 ou ao QR Code abaixo, estando este Centro à disposição para quaisquer dúvidas ou solicitações através do e-mail cejusc.2grau@tjce.jus.br ou do whatsApp (85) 3492-9062. Notifiquem-se as partes, através de seus advogados. Expedientes necessários. Fortaleza, 15 de maio de 2023 Dra Ana Paula Feitosa Oliveira Juíza Coordenadora do NUPEMEC/TJCE"
            },
            {
                "data_movimentação": "09/05/2023",
                "descrição_movimentação": "Enviados Autos do Gabinete à Central de Conciliação."
            },
            {
                "data_movimentação": "09/05/2023",
                "descrição_movimentação": "Proferido despacho de mero expediente"
            },
            {
                "data_movimentação": "09/05/2023",
                "descrição_movimentação": "Proferido despacho de mero expediente"
            },
            {
                "data_movimentação": "23/05/2023",
                "descrição_movimentação": "Publicado no Diário da Justiça Eletrônico Disponibilizado em 22/05/2023 Tipo de publicação: Despacho Número do Diário Eletrônico: 3080"
            },
            {
                "data_movimentação": "18/05/2023",
                "descrição_movimentação": "Audiência de Conciliação Agendada Considerando a Resolução nº 313/2020 do CNJ e as Portarias nº 01/2020 e 02/2020 do NUPEMEC, designo a audiência conciliatória para o dia 15 de junho de 2023, às 8 horas, a se realizar na modalidade videoconferência. Para acesso à sala virtual, deve-se conectar ao link https://link.tjce.jus.br/723041 ou ao QR Code abaixo, estando este Centro à disposição para quaisquer dúvidas ou solicitações através do e-mail cejusc.2grau@tjce.jus.br ou do whatsApp (85) 3492-9062. Notifiquem-se as partes, através de seus advogados. Expedientes necessários. Fortaleza, 15 de maio de 2023 Dra Ana Paula Feitosa Oliveira Juíza Coordenadora do NUPEMEC/TJCE"
            },
            {
                "data_movimentação": "09/05/2023",
                "descrição_movimentação": "Enviados Autos do Gabinete à Central de Conciliação."
            },
            {
                "data_movimentação": "09/05/2023",
                "descrição_movimentação": "Proferido despacho de mero expediente"
            },
            {
                "data_movimentação": "09/05/2023",
                "descrição_movimentação": "Proferido despacho de mero expediente"
            },
            {
                "data_movimentação": "02/05/2022",
                "descrição_movimentação": "Expedido Termo de Transferência"
            },
            {
                "data_movimentação": "02/05/2022",
                "descrição_movimentação": "Transferência Magistrado de origem: Vaga - 2 / FRANCISCO EDUARDO TORQUATO SCORSAFAVA PORT 551/22Área de atuação do magistrado (origem): CívelMagistrado de destino: Vaga - 2 / ANDRÉ LUIZ DE SOUZA COSTAÁrea de atuação do magistrado (destino): CívelMotivo: Transferência - Portaria 911/2022"
            },
            {
                "data_movimentação": "25/03/2022",
                "descrição_movimentação": "Expedido Termo de Transferência"
            },
            {
                "data_movimentação": "25/03/2022",
                "descrição_movimentação": "Transferência Magistrado de origem: Vaga - 2 / JOSÉ RICARDO VIDAL PATROCÍNIOÁrea de atuação do magistrado (origem): CívelMagistrado de destino: Vaga - 2 / FRANCISCO EDUARDO TORQUATO SCORSAFAVA PORT 551/22Área de atuação do magistrado (destino): CívelMotivo: Em cumprimento a Portaria 551/2022 - Juiz Convocado"
            },
            {
                "data_movimentação": "25/05/2021",
                "descrição_movimentação": "Publicado no Diário da Justiça Eletrônico Disponibilizado em 24/05/2021 Tipo de publicação: Ata de Distribuição Número do Diário Eletrônico: 2616"
            },
            {
                "data_movimentação": "20/05/2021",
                "descrição_movimentação": "Concluso ao Relator"
            },
            {
                "data_movimentação": "20/05/2021",
                "descrição_movimentação": "Expedido Termo de Autuação/Distribuição/Conclusão"
            },
            {
                "data_movimentação": "20/05/2021",
                "descrição_movimentação": "por prevenção ao Magistrado Motivo: Prevento ao processo 0631506-39.2019.8.06.0000 Órgão Julgador: 66 - 3ª Câmara Direito Privado Relator: 1512 - JOSÉ RICARDO VIDAL PATROCÍNIO"
            },
            {
                "data_movimentação": "20/05/2021",
                "descrição_movimentação": "Processo Autuado Gerência de Distribuição"
            },
            {
                "data_movimentação": "13/05/2021",
                "descrição_movimentação": "Recebidos os autos com Recurso Foro de origem: Fortaleza Vara de origem: 38ª Vara Cível"
            }
        ]
    }
}

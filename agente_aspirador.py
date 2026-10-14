#Bloco 1 — Representação do ambiente e estado inicial
ambiente = { 
    "Entrada": "Suja", 
    "Sala": "Suja", 
    "Cozinha": "Limpa", 
    "Corredor": "Suja", 
    "Quarto_1": "Suja", 
    "Quarto_2": "Limpa", 
    "Casa_de_Banho": "Suja" 
}

localização_agente = "Entrada"
visitados = set()
historico = []

#Bloco 2 — Representação do mapa da habitação como grafo
mapa = { 
    "Entrada": ["Sala"], 
    "Sala": ["Entrada", "Cozinha", "Corredor"], 
    "Cozinha": ["Sala"], 
    "Corredor": ["Sala", "Quarto_1", "Quarto_2", "Casa_de_Banho"], 
    "Quarto_1": ["Corredor"], 
    "Quarto_2": ["Corredor"], 
    "Casa_de_Banho": ["Corredor"] 
}

#Bloco 3 — Função de perceção
def perceber(ambiente, localizacao):
    estado = ambiente[localizacao]
    return   localizacao, estado


#Bloco 4 — Verificação de limpeza completa
def habitacao_totalmente_limpa(ambiente):
 return all(estado == "Limpa" for estado in ambiente.values())

#Bloco 5 — Escolha de uma área vizinha ainda não visitada
def escolher_proxima_area(localizacao, mapa, visitados):
   for vizinho in mapa[localizacao]: 
      if vizinho not in visitados:
         return vizinho
   return None

#Bloco 6 — Procura BFS (Breadth-First Search) para alcançar áreas ainda não visitadas
def encontrar_caminho_para_nao_visitada(inicio, mapa, visitados):
 fila = [[inicio]]
 explorados = {inicio}
 
 while fila:
    caminho = fila.pop(0)
    atual = caminho[-1]

    for vizinho in mapa[atual]:
        if vizinho in explorados:
            continue
        
        novo_caminho = caminho + [vizinho]
        if vizinho not in visitados:
            return novo_caminho
        
        explorados.add(vizinho)
        fila.append(novo_caminho)
 return None

#Bloco 7 — Função de decisão: o “cérebro” do agente

def agente_reativo(percecao, mapa, visitados):
    localizacao, estado = percecao

    if estado == "Suja":
        return ("Aspirar", localizacao)
    
    proxima_area = escolher_proxima_area(localizacao, mapa, visitados)
    if proxima_area is not None:
        return ("Mover", proxima_area)
    
    caminho = encontrar_caminho_para_nao_visitada(localizacao, mapa, visitados)

    if caminho is not None and len(caminho) > 1:
        return ("Mover", caminho[1])
 
    return ("Parar", localizacao)

#Bloco 8 — Execução das ações
def executar_accao(ambiente, localizacao, accao):
 tipo_accao, destino = accao
 if tipo_accao == "Aspirar":
    ambiente[localizacao] = "Limpa"
    
 elif tipo_accao == "Mover":
    localizacao = destino

 return ambiente, localizacao

#Bloco 9 — Ciclo principal: perceber → decidir → agir
passo = 0 
while True:
    passo += 1
    visitados.add(localização_agente)
    percecao = perceber(ambiente, localização_agente)
    accao = agente_reativo(percecao, mapa, visitados)
    
    historico.append({
        "passo": passo,
        "localizacao": localização_agente,
        "percecao": percecao,
        "accao": accao
    })
    
    print(
        f"Passo {passo:02d} | "
        f"Local: {localização_agente:<15} | "
        f"Estado: {percecao[1]:<5} | "
        f"Ação: {accao}"
    )
    
    if accao[0] == "Parar":
        if habitacao_totalmente_limpa(ambiente):
            print("\nRESULTADO: limpeza completa da habitação.")
        else:
            print("\nATENÇÃO: existem áreas que não ficaram limpas.")
        break
        
    ambiente, localização_agente = executar_accao(ambiente, localização_agente, accao)

#Bloco 10 — Resultados, testes e validação da cobertura

print("\nESTADO FINAL DAS DIVISÕES:")
for divisao, estado in ambiente.items():
    print(f"- {divisao}: {estado}")

print("\nÁREAS VISITADAS:")
print(sorted(visitados))

print("\nTODAS AS ÁREAS FORAM VISITADAS?")
print(set(ambiente.keys()) == visitados)

print("\nTODA A HABITAÇÃO ESTÁ LIMPA?")
print(habitacao_totalmente_limpa(ambiente))

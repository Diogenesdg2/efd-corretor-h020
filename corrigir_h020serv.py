import os

def corrigir_h020_faltante(caminho_entrada, caminho_saida=None):
    if not caminho_entrada:
        raise ValueError("Informe o arquivo TXT de entrada.")

    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_entrada}")

    if caminho_saida is None:
        base, ext = os.path.splitext(caminho_entrada)
        caminho_saida = base + "_CORRIGIDO" + ext

    with open(caminho_entrada, "r", encoding="latin-1", errors="ignore") as f:
        linhas = f.readlines()

    linhas_corrigidas = []

    h010_encontrados = 0
    h020_existentes = 0
    h020_inseridos = 0
    h010_invalidos = 0
    
    # Variável para controlar se realmente adicionamos uma linha extra no bloco 9
    # (Adicionamos 1 quando criamos o 9900|H020, e subtraímos 1 se ele já existia lá e o ignoramos)
    net_bloco9 = 0

    for i, linha in enumerate(linhas):
        linha_limpa = linha.rstrip("\r\n")

        # =======================================================
        # 1. TRATAMENTO DO BLOCO 9 (Totalizadores)
        # =======================================================
        
        if linha_limpa.startswith("|9900|H010|"):
            linhas_corrigidas.append(linha_limpa)
            campos_9900 = linha_limpa.split("|")
            if len(campos_9900) >= 4:
                qtd_registros = campos_9900[3]
                # Injeta o totalizador do H020 logo a seguir
                linhas_corrigidas.append(f"|9900|H020|{qtd_registros}|")
                net_bloco9 += 1
            continue

        if linha_limpa.startswith("|9900|H020|"):
            # Ignora a original para não duplicar, logo anulamos a adição acima
            net_bloco9 -= 1
            continue

        if linha_limpa.startswith("|9900|9900|"):
            campos = linha_limpa.split("|")
            if len(campos) >= 4:
                nova_qtd = int(campos[3]) + net_bloco9
                linhas_corrigidas.append(f"|9900|9900|{nova_qtd}|")
            continue
            
        if linha_limpa.startswith("|9990|"):
            campos = linha_limpa.split("|")
            if len(campos) >= 3:
                nova_qtd = int(campos[2]) + net_bloco9
                linhas_corrigidas.append(f"|9990|{nova_qtd}|")
            continue
            
        # =======================================================
        # 2. TRATAMENTO DOS RODAPÉS GERAIS (H990 e 9999)
        # =======================================================
        
        if linha_limpa.startswith("|H990|"):
            campos = linha_limpa.split("|")
            if len(campos) >= 3:
                nova_qtd = int(campos[2]) + h020_inseridos
                linhas_corrigidas.append(f"|H990|{nova_qtd}|")
            continue
            
        if linha_limpa.startswith("|9999|"):
            campos = linha_limpa.split("|")
            if len(campos) >= 3:
                # Soma tudo o que foi inserido no ficheiro inteiro
                nova_qtd = int(campos[2]) + h020_inseridos + net_bloco9
                linhas_corrigidas.append(f"|9999|{nova_qtd}|")
            continue

        # =======================================================
        # 3. ADICIONA A LINHA NORMAL À LISTA
        # =======================================================
        linhas_corrigidas.append(linha_limpa)

        # =======================================================
        # 4. REGRA DE INSERÇÃO DO H020
        # =======================================================
        if not linha_limpa.startswith("|H010|"):
            continue

        h010_encontrados += 1
        proxima_linha = ""

        if i + 1 < len(linhas):
            proxima_linha = linhas[i + 1].strip()

        if proxima_linha.startswith("|H020|"):
            h020_existentes += 1
            continue

        campos = linha_limpa.split("|")

        if len(campos) <= 6:
            h010_invalidos += 1
            continue

        valor_h010 = campos[6].strip()

        if not valor_h010:
            h010_invalidos += 1
            continue

        linha_h020 = f"|H020|060|{valor_h010}|0,00|"
        linhas_corrigidas.append(linha_h020)
        h020_inseridos += 1

    # Gravar o ficheiro
    with open(caminho_saida, "w", encoding="latin-1", newline="") as f:
        for linha in linhas_corrigidas:
            f.write(linha + "\r\n")

    return {
        "arquivo_entrada": caminho_entrada,
        "arquivo_saida": caminho_saida,
        "h010_encontrados": h010_encontrados,
        "h020_existentes": h020_existentes,
        "h020_inseridos": h020_inseridos,
        "h010_invalidos": h010_invalidos,
    }
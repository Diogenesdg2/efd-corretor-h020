# 📄 Corretor SPED/EFD - H020 Faltante

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-2ecc71.svg)
![Status](https://img.shields.io/badge/Status-Concluído-success.svg)

Uma aplicação desktop moderna e leve, desenvolvida em Python, criada especificamente para **automatizar a correção de arquivos do SPED EFD**. O sistema varre o ficheiro TXT original e insere os registos `H020` que foram omitidos pelo ERP, recalculando automaticamente toda a estrutura de blocos para evitar erros no Programa Validador (PVA).

---

## ✨ O que o sistema faz?

Muitos sistemas de gestão (ERPs) geram o ficheiro do SPED EFD omitindo o detalhamento exigido no registo `H020` (Informações complementares do inventário). Este corretor resolve o problema em segundos através das seguintes regras:

1. **Injeção Inteligente:** Para cada linha `|H010|`, verifica se a próxima linha já é um `H020`. Se não for, cria um novo registo `H020` automaticamente.
2. **Extração de Valores:** O valor do `H020` é extraído diretamente da posição 6 do próprio registo `H010`. O padrão de inserção é: `|H020|060|VALOR_TOTAL_DO_H010|0,00|`.
3. **Recálculo de Totalizadores (Bloco 9):** Para que o PVA não acuse erro de estrutura, o sistema atualiza "em andamento" os totalizadores do ficheiro:
   - Replica o `|9900|H010|` gerando o `|9900|H020|`.
   - Soma as inserções nos totalizadores de bloco (`|H990|` e `|9990|`).
   - Soma as inserções no totalizador da tabela geral do Bloco 9 (`|9900|9900|`).
   - Recalcula o total geral do ficheiro de encerramento (`|9999|`).
4. **Segurança de Dados:** O ficheiro original nunca é sobrescrito. É gerada uma cópia `_CORRIGIDO.TXT`.

---

💻 Interface Gráfica
A interface foi construída com CustomTkinter para garantir uma experiência de utilizador agradável, suportando nativamente o modo Claro/Escuro do sistema operativo.

(Adicione aqui uma captura de ecrã do seu sistema a funcionar! Basta arrastar a imagem para o GitHub ao editar este README)

🛠️ Estrutura do Projeto
app.py: Contém toda a lógica da Interface Gráfica (GUI) construída em CustomTkinter, responsável por capturar caminhos de ficheiros e exibir o feedback ao utilizador.

corrigir_h020serv.py: Módulo de serviço isolado contendo a regra de negócio (corrigir_h020_faltante()), processamento em memória e recálculo das matrizes do SPED.

👨‍💻 Autor
Desenvolvido por Diógenes Daniel Gomes

Desenvolvimento de soluções e automações para a área Contábil/Fiscal.


## 🚀 Como executar o projeto

### Pré-requisitos
Certifique-se de que tem o Python instalado (recomendado 3.11 ou superior).

### Instalação
1. Clone o repositório para a sua máquina:
   ```bash
   git clone [https://github.com/Diogenesdg2/efd-corretor-h020.git](https://github.com/Diogenesdg2/efd-corretor-h020.git)
   cd efd-corretor-h020   

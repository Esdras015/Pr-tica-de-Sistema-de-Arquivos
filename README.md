# Prática de Sistema de Arquivos

Implementação de um "mini" simulador de sistema de arquivos para a prática 

Descrição
---------
Este repositório contém uma implementação em Python de um mini-sistema de arquivos que simula a alocação por blocos (First-Fit). O objetivo é demonstrar os conceitos de alocação de espaço, fragmentação interna e externa e operações básicas de gerenciamento de arquivos e diretórios.

Funcionalidades implementadas
-----------------------------
- Criar e excluir diretórios (dois níveis: `raiz` -> diretórios)
- Criar e excluir arquivos dentro de um diretório
- Listar conteúdo de um diretório (mostrando nome, tamanho e blocos alocados)
- Simulação de alocação por blocos (First-Fit) com mapa de blocos visual (`O`=ocupado, `-`=livre)
- Cálculo e exibição de fragmentação interna por arquivo
- Detecção (simples) de fragmentação externa (quando existem múltiplos segmentos livres)

Arquivos principais
-------------------
- `python_arquivos_atividade.py`: implementação do `SistemaArquivos`, classes `Arquivo` e `Diretorio` e interface interativa por linha de comando.
- `demo_run.py`: script de demonstração que executa automaticamente uma sequência de operações para mostrar todas as funcionalidades (criação/exclusão de diretórios e arquivos, mapa de blocos, fragmentação).

Como executar
-------------
1. Certifique-se de ter Python 3 instalado.
2. No diretório do repositório, execute:

```powershell
python .\demo_run.py
```

O script `demo_run.py` imprime no terminal a sequência de operações e os mapas de blocos em vários momentos. Para usar a interface interativa, execute:

```powershell
python .\python_arquivos_atividade.py
```

Observações / Limitações
-----------------------
- A implementação usa dois níveis de diretórios (raiz e subdiretórios). Não permite dois itens com o mesmo nome no mesmo diretório.
- A simulação usa alocação por blocos (First-Fit) e marca blocos como ocupados com `True` internamente.
- A função de fragmentação externa retorna um booleano indicando se existem múltiplos segmentos livres.

Membros
-------
- Rony Elias de Oliveira
- Esdras da Silva Ramos Rodrigues

Créditos
--------
Atividade: Prática de Sistema de Arquivos (20% da 2ª VA) - proposta por Douglas Veras e Silva.

Licença
-------
Este código é fornecido apenas para fins educacionais.

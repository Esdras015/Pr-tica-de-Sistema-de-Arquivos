# ============================
# MINI SISTEMA DE ARQUIVOS
# Alocação: por blocos (First-Fit)
# Fragmentação: Interna e Externa
# Dois níveis: raiz -> diretórios -> arquivos
# ============================

class Arquivo:
    def __init__(self, nome, tamanho, blocos):
        self.nome = nome
        self.tamanho = tamanho
        self.blocos = blocos  # lista de blocos alocados

class Diretorio:
    def __init__(self, nome):
        self.nome = nome
        self.subdiretorios = {}   # dict de Diretorio
        self.arquivos = {}        # dict de Arquivo

class SistemaArquivos:
    def __init__(self, tamanho_bloco, num_blocos):
        self.tamanho_bloco = tamanho_bloco
        self.num_blocos = num_blocos
        self.blocos = [None] * num_blocos  
        self.raiz = Diretorio("raiz")

    # -------------------------------
    # ENCONTRAR DIRETÓRIO (2 níveis)
    # -------------------------------
    def obter_diretorio(self, caminho):
        if caminho == "raiz":
            return self.raiz
        
        partes = caminho.split("/")
        if len(partes) != 2 or partes[0] != "raiz":
            print("❌ Caminho inválido! Use: raiz/nomeDoDiretorio")
            return None
        
        nome_dir = partes[1]
        return self.raiz.subdiretorios.get(nome_dir, None)

    # -------------------------------
    # ALOCAÇÃO REAL FIRST FIT
    # -------------------------------
    def alocar_blocos(self, tamanho):
        blocos_necessarios = (tamanho + self.tamanho_bloco - 1) // self.tamanho_bloco
        blocos_encontrados = []
        
        for i in range(self.num_blocos):
            if self.blocos[i] is None:
                blocos_encontrados.append(i)
                if len(blocos_encontrados) == blocos_necessarios:
                    for b in blocos_encontrados:
                        self.blocos[b] = True
                    return blocos_encontrados
        
        return None  # sem espaço suficiente

    # ---------------------------------------
    # LIBERAÇÃO DE BLOCOS
    # ---------------------------------------
    def liberar_blocos(self, lista_blocos):
        for b in lista_blocos:
            self.blocos[b] = None

    # ---------------------------------------
    # EXIBIR ESTADO DO SISTEMA DE ARQUIVOS
    # ---------------------------------------
    def mostrar_alocacao_blocos(self):
        print("\n=== MAPA DE BLOCOS (O=ocupado, -=livre) ===")
        mapa = "".join(["O" if b else "-" for b in self.blocos])
        print(mapa)
        print("============================================\n")

    # ---------------------------------------
    # FRAGMENTAÇÃO INTERNA
    # ---------------------------------------
    def fragmentacao_interna(self, tamanho):
        resto = tamanho % self.tamanho_bloco
        return 0 if resto == 0 else (self.tamanho_bloco - resto)

    # ---------------------------------------
    # FRAGMENTAÇÃO EXTERNA (REAL)
    # Conta quantos segmentos livres existem
    # ---------------------------------------
    def fragmentacao_externa(self):
        segmentos_livres = 0
        i = 0
        
        while i < self.num_blocos:
            if self.blocos[i] is None:
                segmentos_livres += 1
                while i < self.num_blocos and self.blocos[i] is None:
                    i += 1
            i += 1
        
        return segmentos_livres > 1  # mais de 1 segmento ⇒ fragmentação

    # ---------------------------------------
    # CRIAR DIRETÓRIO
    # ---------------------------------------
    def criar_diretorio(self, nome):
        if nome in self.raiz.subdiretorios or nome in self.raiz.arquivos:
            print("❌ Já existe arquivo ou diretório com esse nome!")
            return
        
        self.raiz.subdiretorios[nome] = Diretorio(nome)
        print(f"📁 Diretório '{nome}' criado!")

    # ---------------------------------------
    # EXCLUIR DIRETÓRIO
    # ---------------------------------------
    def excluir_diretorio(self, nome):
        if nome not in self.raiz.subdiretorios:
            print("❌ Diretório não existe!")
            return
        
        dir_obj = self.raiz.subdiretorios[nome]

        # liberar blocos dos arquivos
        for arq in dir_obj.arquivos.values():
            self.liberar_blocos(arq.blocos)

        del self.raiz.subdiretorios[nome]
        print(f"📁 Diretório '{nome}' excluído!")

    # ---------------------------------------
    # CRIAR ARQUIVO
    # ---------------------------------------
    def criar_arquivo(self, nome_dir, nome_arq, tamanho):
        diretorio = self.obter_diretorio(nome_dir)
        
        if diretorio is None:
            print("❌ Diretório inválido!")
            return
        
        if nome_arq in diretorio.arquivos or nome_arq in diretorio.subdiretorios:
            print("❌ Já existe arquivo ou diretório com esse nome aqui!")
            return
        
        blocos = self.alocar_blocos(tamanho)
        if blocos is None:
            print("❌ Não há espaço suficiente (fragmentação externa pode ser a causa).")
            return
        
        diretorio.arquivos[nome_arq] = Arquivo(nome_arq, tamanho, blocos)
        print(f"📄 Arquivo '{nome_arq}' criado com {len(blocos)} blocos.")
        self.mostrar_alocacao_blocos()

    # ---------------------------------------
    # EXCLUIR ARQUIVO
    # ---------------------------------------
    def excluir_arquivo(self, nome_dir, nome_arq):
        diretorio = self.obter_diretorio(nome_dir)
        
        if diretorio is None or nome_arq not in diretorio.arquivos:
            print("❌ Arquivo não encontrado!")
            return
        
        arq = diretorio.arquivos[nome_arq]
        self.liberar_blocos(arq.blocos)
        del diretorio.arquivos[nome_arq]

        print(f"🗑 Arquivo '{nome_arq}' excluído!")
        self.mostrar_alocacao_blocos()

    # ---------------------------------------
    # LISTAR ARQUIVOS
    # ---------------------------------------
    def listar(self, nome_dir):
        diretorio = self.obter_diretorio(nome_dir)

        if diretorio is None:
            print("❌ Diretório inválido!")
            return
        
        print(f"\n📂 Conteúdo de '{nome_dir}':")

        if diretorio.arquivos:
            print("Arquivos:")
            for arq in diretorio.arquivos.values():
                print(f" - {arq.nome} | {arq.tamanho}B | blocos: {arq.blocos}")
        else:
            print(" - (Sem arquivos)")

        if diretorio.subdiretorios:
            print("\nSubdiretórios:")
            for sd in diretorio.subdiretorios.values():
                print(f" - {sd.nome}")
        else:
            print("\n - (Sem subdiretórios)")

        # Fragmentações
        print("\n🔎 Fragmentação interna dos arquivos:")
        for arq in diretorio.arquivos.values():
            fi = self.fragmentacao_interna(arq.tamanho)
            print(f" - {arq.nome}: {fi} bytes desperdiçados")

        print("\n🔎 Fragmentação externa:", 
              "SIM" if self.fragmentacao_externa() else "NÃO")
        print()


# ====================================================
# MENU DE OPERAÇÕES
# ====================================================
def main():
    print("=== Mini Sistema de Arquivos ===")
    tam = int(input("Tamanho do bloco (em bytes): "))
    nb = int(input("Quantidade de blocos: "))

    sa = SistemaArquivos(tam, nb)

    while True:
        print("""
1. Criar diretório
2. Excluir diretório
3. Criar arquivo
4. Excluir arquivo
5. Listar diretório
6. Mostrar mapa de blocos
0. Sair
""")
        op = input("Escolha: ")

        if op == "1":
            nome = input("Nome do diretório: ")
            sa.criar_diretorio(nome)

        elif op == "2":
            nome = input("Nome do diretório: ")
            sa.excluir_diretorio(nome)

        elif op == "3":
            d = input("Diretório (ex: raiz/docs): ")
            a = input("Nome do arquivo: ")
            t = int(input("Tamanho (bytes): "))
            sa.criar_arquivo(d, a, t)

        elif op == "4":
            d = input("Diretório (ex: raiz/docs): ")
            a = input("Nome do arquivo: ")
            sa.excluir_arquivo(d, a)

        elif op == "5":
            d = input("Diretório (ex: raiz/docs): ")
            sa.listar(d)

        elif op == "6":
            sa.mostrar_alocacao_blocos()

        elif op == "0":
            print("Encerrando...")
            break

        else:
            print("❌ Opção inválida!")


if __name__ == "__main__":
    main()

# Script de demonstração para o Mini Sistema de Arquivos
# Executa uma sequência de operações que cobrem todas as funcionalidades

from python_arquivos_atividade import SistemaArquivos

def separador(titulo):
    print('\n' + '='*10 + ' ' + titulo + ' ' + '='*10)

def main():
    # Configuração: bloco de 64 bytes, 16 blocos (total 1024 bytes)
    sa = SistemaArquivos(tamanho_bloco=64, num_blocos=16)

    separador('Estado inicial')
    sa.mostrar_alocacao_blocos()

    # Criar diretórios
    separador('Criando diretórios')
    sa.criar_diretorio('docs')
    sa.criar_diretorio('images')
    sa.criar_diretorio('bin')
    sa.criar_diretorio('temp')

    # Listar raiz
    separador('Listar raiz (após criação de diretórios)')
    sa.listar('raiz')

    # Criar arquivos variados para testar fragmentação interna
    separador('Criando arquivos em raiz/docs')
    sa.criar_arquivo('raiz/docs', 'report.txt', 100)   # 2 blocos (frag interna)
    sa.criar_arquivo('raiz/docs', 'small.txt', 64)     # 1 bloco (sem frag)
    sa.criar_arquivo('raiz/docs', 'big.pdf', 200)      # 4 blocos

    # Criar arquivos em images
    separador('Criando arquivos em raiz/images')
    sa.criar_arquivo('raiz/images', 'img1.png', 128)   # 2 blocos
    sa.criar_arquivo('raiz/images', 'img2.png', 300)   # 5 blocos

    # Mostrar mapa e listar
    separador('Estado após criação de alguns arquivos')
    sa.mostrar_alocacao_blocos()
    sa.listar('raiz/docs')
    sa.listar('raiz/images')

    # Criar arquivos para encher espaço e forçar fragmentação externa
    separador('Criando arquivos adicionais para preencher blocos')
    sa.criar_arquivo('raiz/bin', 'exe1', 64)
    sa.criar_arquivo('raiz/bin', 'exe2', 64)
    sa.criar_arquivo('raiz/bin', 'exe3', 64)
    sa.criar_arquivo('raiz/bin', 'exe4', 64)
    sa.criar_arquivo('raiz/temp', 'tmp1', 128)

    separador('Mapa após preencher mais arquivos')
    sa.mostrar_alocacao_blocos()

    # Excluir alguns arquivos para criar buracos (fragmentação externa)
    separador('Excluindo arquivos para gerar fragmentação externa')
    sa.excluir_arquivo('raiz/docs', 'small.txt')   # libera 1 bloco no meio
    sa.excluir_arquivo('raiz/bin', 'exe2')
    sa.excluir_arquivo('raiz/images', 'img1.png')

    separador('Mapa após exclusões (fragmentação externa esperada)')
    sa.mostrar_alocacao_blocos()
    print('Fragmentação externa atualmente:', 'SIM' if sa.fragmentacao_externa() else 'NÃO')

    # Tentar criar um arquivo grande para demonstrar falha por fragmentação externa
    separador('Tentativa de criar arquivo grande (pode falhar por fragmentação externa)')
    sa.criar_arquivo('raiz/docs', 'huge.dat', 400)  # exige 7 blocos -> pode falhar

    # Excluir diretório (deverá liberar blocos dos seus arquivos)
    separador('Excluindo diretório raiz/images (libera blocos)')
    sa.excluir_diretorio('images')
    sa.mostrar_alocacao_blocos()

    # Tentar novamente criar o arquivo grande após liberar blocos
    separador('Tentativa de criar arquivo grande novamente (após liberar blocos)')
    sa.criar_arquivo('raiz/docs', 'huge.dat', 400)

    separador('Estado final')
    sa.mostrar_alocacao_blocos()
    sa.listar('raiz')

if __name__ == '__main__':
    main()

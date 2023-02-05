import socket
import couchdb

def conectar():
    """
    Função para conectar ao servidor
    """
    user = 'elias'
    password = 'elias123'
    conn = couchdb.Server(f'http://{user}:{password}@localhost:5984')
    # Não aceita caracteres maiúsculos
    banco = 'pycouchdb'

    if banco in conn:
        db = conn[banco]
        return db
    else:
        try:
            db = conn.create(banco)
            return db
        except socket.gaierror as e:
            print(f'Erro ao conectar ao servidor: {e}')
        except couchdb.http.Unauthorized as f:
            print(f'Sem permissão para acessar o servidor: {f}')
        except ConnectionRefusedError as g:
            print(f'Não foi possível conectar ao servidor: {g}')

# 'couchdb' não necessita de procedimentos específicos para finalizar a conexão, uma vez que o mesmo realiza automaticamente

def listar():
    """
    Função para listar os produtos
    """
    # Definição da conexão
    db = conectar()

    if db:
        if db.info()['doc_count'] > 0:
            print('Listando produtos ...')
            print('---------------------')
            for doc in db:
                print(f"ID: {db[doc]['_id']}")
                print(f"Rev: {db[doc]['_rev']}")
                print(f"Produto: {db[doc]['nome']}")
                print(f"Preço: {db[doc]['preco']}")
                print(f"Estoque: {db[doc]['estoque']}")
                print('---------------------')
        else:
            print("Não existem produtos a serem listados!")
            print('---------------------')
    else:
        print('Não foi possível conectar ao servidor.')
        print('---------------------')

def inserir():
    """
    Função para inserir um produto
    """ 
    # Definição da conexão 
    db = conectar()

    if db:
        print('Inserindo produto ...')
        print('---------------------')
        nome = input("Informe o nome do produto: ")
        preco = float(input("Informe o preço do produto: "))
        estoque = int(input("Informe a quantidade de produtos em estoque: "))

        produto = {'nome': nome, 'preco': preco, 'estoque': estoque}
        
        res = db.save(produto)

        if res:
            print(f'O produto {nome} foi inserido com sucesso')
            print('---------------------')
        else:
            print('Não foi possível inserir o produto.')
            print('---------------------')
    else:
        print(f'Não foi possível conectar ao servidor.')
        print('---------------------')

def atualizar():
    """
    Função para atualizar um produto
    """
    # Definição da conexão
    db = conectar()

    if db:
        print('Atualizando produto ...')
        print('---------------------')

        chave = input('Informe a chave do produto: ')
        
        try:
            doc = db[chave]
            
            nome = input('Informe o nome atualizado do produto: ')
            preco = float(input('Informe o preço atualizado do produto: '))
            estoque = int(input('Informe a quantidade atualizada de produtos em estoque: '))

            doc['nome'] = nome
            doc['preco'] = preco
            doc['estoque'] = estoque
            # Atualiza o documento no banco de dados
            db[doc.id] = doc

            print(f'O produto {nome} foi atualizado com sucesso.')
            print('---------------------')
        except couchdb.http.ResourceNotFound as e:
            print(f'Não foi possível atualizar o produto: {e}')
            print('---------------------')
    else:
        print('Não foi possível conectar ao servidor.')
        print('---------------------')

def deletar():
    """
    Função para deletar um produto
    """  
    # Definição da conexão
    db = conectar()

    if db:
        print('Deletando produtos ...')
        print('---------------------')

        chave = input('Informe a chave do produto: ')

        try:
            db.delete(db[chave])
            print(f'O produto com a chave {chave} foi deletado com sucesso.')
            print('---------------------')
        except couchdb.http.ResourceNotFound as e:
            print(f'Não foi possível deletar o produto: {e}.')
            print('---------------------')
    else:
        print('Não foi possível conectar ao servidor.')
        print('---------------------')

def menu():
    """
    Função para gerar o menu inicial
    """
    # Operações disponíveis no menu ('sair' sempre em última posição)
    operacoesTxt = ['Listar produtos.', 'Inserir produto.', 'Atualizar produto.', 'Deletar produto.', 'Sair.']
    # Extração de nomes das funções correspondentes
    operacoes = [operacao.split()[0].lower() for operacao in operacoesTxt]
    # Formatação de exibição de texto das operações disponíveis no menu
    operacoesTxt = [str(it+1) + ' - ' + operacoesTxt[it] for it in range(0,len(operacoesTxt))]
    
    opcao = 0
    # Loop para seleção de operações no menu pelo usuário
    while(opcao != len(operacoesTxt)):
        #  Prints das operações dispníveis no terminal
        print('=========Gerenciamento de Produtos==============')
        print('Selecione uma opção: ')
        for operacaoTxt in operacoesTxt:
            print(operacaoTxt)
        # Coleta da operação desejada pelo usuário
        opcao = int(input())
        # Chamada das funções desejadas pelo usuário
        if opcao != len(operacoesTxt):
            globals()[operacoes[opcao-1]]()
        # Encerramento do loop 
        elif opcao == len(operacoesTxt):
                print('*** Saindo ***')
        else:
            print('*** Opção inválida ***')
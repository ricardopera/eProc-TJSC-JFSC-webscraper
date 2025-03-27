# eProc TJSC e JFSC Webscraper

Script em Python para extrair dados de processos e fazer downloads de documentos dos autos pelo sistema eProc do Tribunal de Justiça de Santa Catarina (TJSC) e da Justiça Federal de Santa Catarina (JFSC).

## Funcionalidades

- Acesso automatizado ao sistema eProc dos tribunais TJSC e JFSC
- Login automático no sistema com credenciais armazenadas de forma segura
- Leitura de lista de processos de um arquivo de texto
- Busca de processos pelo número
- Download de petições iniciais (arquivos "INIC1" ou "PET1")
- Organização dos documentos baixados em diretório específico

## Requisitos

- Python 3.x
- Google Chrome instalado
- Acesso válido ao sistema eProc (usuário e senha)

## Instalação

1. Clone este repositório para sua máquina local:
   ```
   git clone https://github.com/seu-usuario/eProc-TJSC-JFSC-webscraper.git
   cd eProc-TJSC-JFSC-webscraper
   ```

2. Instale as dependências necessárias:
   ```
   pip install -r requeriments.txt
   ```

3. Crie um arquivo `.env` na pasta raiz do projeto e adicione suas credenciais:
   ```
   USUARIO=seu_usuario
   SENHA=sua_senha
   ```

## Uso

1. Adicione os números dos processos que deseja pesquisar no arquivo `procs.txt`, um por linha.

2. Execute o script:
   ```
   python main.py
   ```

3. Os documentos serão baixados automaticamente na pasta `processos`.

## Configurações

O script possui algumas configurações que podem ser alteradas no arquivo `functions.py`:

- `HEADLESS`: Define se o navegador será executado em modo visível ou oculto
- `DOWNLOADS_DIR`: Diretório onde os documentos serão baixados temporariamente
- `PROCESSOS_DIR`: Diretório onde os documentos serão armazenados permanentemente
- `SHORT_TIMEOUT`, `LONG_TIMEOUT`, `VERY_LONG_TIMEOUT`: Tempos de espera para carregamento de elementos na página

## Observações

- O script funcionará apenas para usuários com acesso válido ao sistema eProc dos tribunais mencionados.
- Os documentos baixados são renomeados para corresponder ao número do processo.
- O projeto verifica se o documento já foi baixado anteriormente para evitar downloads duplicados.

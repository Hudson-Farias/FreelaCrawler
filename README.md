# Projeto Crawler para Plataformas Freelancer

Este projeto consiste em um Crawler em Python 3.11.6 que busca projetos em plataformas de freelancers e os envia para um servidor Discord.

## Dependências

Para executar este projeto, você precisará das seguintes dependências:

- Python 3.11.6
- Bibliotecas Python listadas em `requirements.txt`

## Configuração do Ambiente Virtual com venv

1. Clone o repositório:

```bash
git clone https://github.com/Hudson-Farias/FreelaCrawler.git
cd FreelaCrawler
```

1. Crie e ative um ambiente virtual usando venv:

```bash
python3 -m venv venv
```
No Windows:

```bash
venv\Scripts\activate
```

No macOS e Linux:

```bash
source venv/bin/activate
```

2. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```

Configuração do Python com asdf
Se você estiver utilizando o gerenciador de versões asdf para o Python:

Certifique-se de ter o plugin python instalado:

```bash
asdf plugin-add python
```

Instale o Python 3.11.6 com asdf:

```bash
asdf install python 3.11.6
```

Defina a versão do Python no seu ambiente do projeto:

```bash
asdf local python 3.11.6
```

Executando o Projeto
Certifique-se de ter configurado suas credenciais para as plataformas de freelancers e o token do Discord antes de executar o projeto. Edite os arquivos apropriados para inserir essas informações.

Para rodar o projeto, execute:

```bash
python main.py

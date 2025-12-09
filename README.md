# API
Esse repositório contém um script básico que consome a API do twitter.

O objetivo do script é coletar tweets com as hashtags #carroeletrico, #mobilidade, #Tesla, #BYD...

## Como usar
Para usar, primeiro clone este repositório
```
git clone https://github.com/garipew/webscraping.git
```

Crie um ambiente virtual e ative-o, com
```
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

Instale requirements.txt com
```
pip install -r requirements.txt
```

Adicione a sua KEY em um arquivo .env
```
# .env
API_KEY={my_key}
API_SECRET_KEY={my_secret}
```
E execute o script de geração de token
```
./gen_token.sh
```
Ou, alternativamente, gere seu token manualmente e adicione-o no arquivo .env
```
# .env
BEARER_TOKEN={my_token}
```

Por fim, execute o script com
```
# Windows
python .\scraper.py <query>

# Linux/Mac
python3 ./scraper.py <query>
```

O coletado será armazenado na tabela ***tweets.csv***.

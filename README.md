---
title: PDF to Audio
emoji: 🔊
colorFrom: blue
colorTo: purple
sdk: gradio
app_file: app.py
python_version: "3.12"
---

# PDF to Audio

Aplicativo de linha de comando que extrai o texto de um PDF e gera um arquivo WAV com o Kokoro TTS. O projeto
separa leitura do PDF, sintese de voz, interface de terminal e interface web.

## Requisitos

- Python 3.10, 3.11 ou 3.12. O Kokoro usado pelo projeto ainda nao oferece as
  versoes necessarias para Python 3.13 ou superior.
- `espeak-ng`, necessario pelo Kokoro:
  - macOS: `brew install espeak-ng`
  - Ubuntu/Debian: `sudo apt-get install espeak-ng`

## Instalacao

### Instalar para usar o comando

#### macOS

Instale os requisitos do sistema e o `pipx`:

```bash
brew install python@3.12 espeak-ng pipx
pipx ensurepath
```

#### Linux (Ubuntu/Debian)

Instale Python 3.12, o suporte a ambientes virtuais, `espeak-ng`, `pipx` e Git:

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv espeak-ng pipx git
pipx ensurepath
```

Se sua versao do Ubuntu/Debian nao disponibilizar `python3.12`, instale o
Python 3.12 por uma fonte apropriada para sua distribuicao antes de continuar.

Em distribuicoes Fedora, instale os pacotes equivalentes (`python3.12`,
`espeak-ng`, `pipx` e `git`) com `dnf` antes de executar os comandos do `pipx`.

Depois de instalar os requisitos do seu sistema, abra um novo terminal,
execute `pipx ensurepath` se necessario e instale o app diretamente do GitHub:

```bash
pipx install --python python3.12 \
  "git+https://github.com/LeticiaISilveira/txt_to_audio.git"
```

Depois, o comando fica disponivel de qualquer pasta:

```bash
pdf-to-audio --test-voice
pdf-to-audio "/caminho/para/seu-arquivo.pdf"
```

Para atualizar para a versao mais recente:

```bash
pipx upgrade pdf-to-audio
```

### Instalar para desenvolvimento

Na raiz do projeto, crie o ambiente virtual com Python 3.12 e instale as
dependencias. Para instalar tambem a interface Gradio, use o extra `web`:

```bash
python3.12 -m venv .venv312
source .venv312/bin/activate
python -m pip install -e ".[web]"
```

Use `.venv312` para manter o ambiente isolado. No Windows, crie o ambiente
com `py -3.12 -m venv .venv` e ative-o com `.venv\Scripts\activate`.

## Interface web

Com o ambiente virtual e as dependencias instalados, inicie o Gradio:

```bash
python app.py
```

Abra no navegador o endereco local mostrado no terminal (normalmente
`http://127.0.0.1:7860`). A interface permite enviar um PDF, escolher idioma,
voz e velocidade, ouvir um teste da voz e baixar o audio convertido.

### Publicar e adicionar o link ao GitHub

O README ja inclui a configuracao de um Hugging Face Space Gradio. Para publicar:

1. Crie um Space no [Hugging Face Spaces](https://huggingface.co/new-space) e
   selecione **Gradio** como SDK.
2. Envie os arquivos do projeto para o Space ou conecte o repositorio GitHub.
   O Space usa `app.py` como entrada e instala as bibliotecas de `requirements.txt`.
3. Aguarde a construcao do Space e teste o endereco publico que ele fornecer.
4. No repositorio do GitHub, abra **About → Edit** e cole o endereco do Space no
   campo **Website**.

O primeiro carregamento pode levar algum tempo enquanto o Kokoro baixa os
modelos. Spaces com recursos gratuitos podem ser mais lentos para sintetizar
documentos longos.

## Uso

Converta um PDF para WAV:

```bash
pdf-to-audio ./meu-livro.pdf
```

Por padrao, o audio e salvo ao lado do PDF, com o mesmo nome. Para escolher
outro destino, voz, idioma ou velocidade:

```bash
pdf-to-audio ./meu-livro.pdf \
  --output ./audios/meu-livro.wav \
  --language p \
  --voice pf_dora \
  --speed 1.0
```

Para ouvir uma frase curta e testar uma voz antes de converter um PDF:

```bash
pdf-to-audio --test-voice
```

O comando gera `voice-test.wav` na pasta atual e reproduz o arquivo. Para
testar outra voz ou escolher o destino do WAV:

```bash
pdf-to-audio --test-voice --language p --voice pf_dora --speed 1.0 \
  --output ./teste-de-voz.wav
```

Para vozes em ingles do seu teste, use `--language a`, por exemplo
`pdf-to-audio --test-voice --language a --voice am_eric`. No macOS, o app usa
`afplay`; no Linux, `aplay` ou `paplay`; no Windows, o player WAV do sistema.

O idioma e a voz precisam ser compativeis. Para portugues brasileiro, use
`--language p`, como `pf_dora` ou `pm_alex`. As vozes
`af_heart`, `am_eric`, `am_puck` e `af_nicole` do teste sao vozes em ingles
americano (`--language a`).

Para ver todas as opcoes:

```bash
pdf-to-audio --help
```

O PDF precisa conter texto selecionavel. Arquivos digitalizados como imagem
precisam passar por OCR antes; OCR ainda nao faz parte deste app.

## Estrutura

```text
.
├── examples/
│   └── voice_preview.py       # Gera amostras das vozes em ingles do teste
├── app.py                     # Entrada da interface Gradio
├── src/
│   └── pdf_to_audio/
│       ├── cli.py             # Argumentos e fluxo da aplicacao
│       ├── pdf_reader.py      # Extracao de texto do PDF
│       ├── speech.py          # Geracao e reproducao de WAV
│       └── web.py             # Interface web Gradio
├── tests/
│   ├── test_cli.py
│   ├── test_pdf_reader.py
│   └── test_speech.py
└── pyproject.toml
```

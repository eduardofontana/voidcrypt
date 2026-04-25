# VOIDCRYPT

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="Licenca">
  <img src="https://img.shields.io/badge/Status-Ativo-orange?style=flat-square" alt="Status">
</p>

---

## Aviso

**VOIDCRYPT E UMA FERRAMENTA EDUCACIONAL DE SEGURANCA.**

Este software e fornecido somente para fins de **protecao legitima de privacidade**. Sempre:

- Garanta que voce tem autorizacao legal para criptografar os arquivos em questao
- Guarde backups das suas senhas, pois arquivos criptografados nao podem ser recuperados sem elas
- Teste primeiro com arquivos nao criticos antes de usar com dados importantes

---

## Visao Geral

VoidCrypt e um utilitario CLI de criptografia de arquivos inspirado por ferramentas como VeraCrypt. Ele implementa criptografia moderna para proteger arquivos sensiveis localmente.

### Filosofia Principal

```text
Trave. Oculte. Apague.
```

VoidCrypt oferece criptografia confidencial de arquivos usando criptografia autenticada (AES-256-GCM) com derivacao de chave PBKDF2-HMAC-SHA256 para aumentar a resistencia contra ataques de forca bruta.

---

## Recursos

### Criptografia

- **AES-256-GCM** - Criptografia autenticada padrao da industria
- **PBKDF2-HMAC-SHA256** - Derivacao de chave segura com 600 mil iteracoes
- **Nonce unico por arquivo** - Sem IVs reutilizaveis
- **Aleatoriedade segura** - Usa `os.urandom` para todos os valores criptograficos aleatorios

### Formato de Arquivo

- **Formato binario proprio** - Estrutura organizada para arquivos criptografados
- **Ocultacao opcional do nome do arquivo** - Remove o nome original dos metadados
- **Verificacao de integridade** - A tag de autenticacao impede alteracoes silenciosas

### Interface CLI

- **UI rica no terminal** - Saida colorida com barras de progresso
- **Mascaramento de senha** - Entrada oculta usando `getpass`
- **Mensagens de status** - Retorno claro sobre cada operacao

### Opcoes de Seguranca

- **Nome de saida aleatorio** - Gera nomes de arquivo menos rastreaveis
- **Simulacao de apagamento seguro** - Sobrescreve o arquivo original com dados aleatorios
- **Limite de tentativas** - Opcao de autodestruicao apos tentativas falhas

---

## Instalacao

### Pre-requisitos

```bash
# Python 3.11 ou superior
python --version
```

### Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Inicio Rapido

```bash
# Criptografar um arquivo
python -m voidcrypt.cli.main encrypt documento_secreto.pdf

# Criptografar com nome de arquivo aleatorio
python -m voidcrypt.cli.main encrypt secreto.pdf -r

# Descriptografar um arquivo
python -m voidcrypt.cli.main decrypt documento_secreto.pdf.void

# Ver informacoes do arquivo criptografado
python -m voidcrypt.cli.main info documento_secreto.pdf.void
```

---

## Exemplos de Uso

### Criptografia Basica

```bash
$ python -m voidcrypt.cli.main encrypt segredo.txt
Enter password: ********
Confirm password: ********
OK Encryption complete: segredo.txt.void
```

### Com Opcoes

```bash
# Nome aleatorio e apagamento do original apos criptografar
$ python -m voidcrypt.cli.main encrypt confidencial.pdf -r -s
Enter password: ********
Confirm password: ********
OK Encryption complete: a3f8c2d1e5b6...4a7f.void
```

### Descriptografia

```bash
$ python -m voidcrypt.cli.main decrypt segredo.txt.void
Enter password: ********
OK Decryption complete: segredo.txt
```

### Informacoes do Arquivo

```bash
$ python -m voidcrypt.cli.main info segredo.txt.void

+--------------------------------------+
|       Informacoes do VoidCrypt       |
+--------------------------------------+
| Arquivo        | segredo.txt.void    |
| Tamanho        | 24.50 KB            |
| Versao         | 1                   |
| Nome Original  | segredo.txt         |
| Tam. Original  | 1.02 KB             |
+--------------------------------------+
```

---

## Design Criptografico

### Esquema de Criptografia

| Componente | Valor |
|------------|-------|
| Algoritmo | AES-256-GCM |
| Tamanho da chave | 256 bits (32 bytes) |
| Tamanho do nonce | 96 bits (12 bytes) |
| Tamanho da tag | 128 bits (16 bytes) |
| Modo | Criptografia autenticada |

### Derivacao de Chave

| Parametro | Valor |
|-----------|-------|
| KDF | PBKDF2-HMAC-SHA256 |
| Iteracoes | 600.000 |
| Hash | SHA-256 |
| Tamanho do salt | 256 bits (32 bytes) |

### Por Que Essas Escolhas?

- **AES-GCM**: fornece confidencialidade e integridade em uma unica operacao. A tag de autenticacao garante que adulteracoes sejam detectadas.
- **PBKDF2-HMAC-SHA256**: derivacao de chave amplamente usada, com alto numero de iteracoes para dificultar forca bruta.
- **Nonces unicos**: cada criptografia usa valores aleatorios novos, reduzindo risco de analise por padroes.

---

## Formato do Arquivo

Arquivos criptografados usam um formato binario proprio:

```text
+----------------+----------+------------------------+
| MAGIC HEADER   | 4 bytes  | "VOID"                 |
| VERSION        | 4 bytes  | Versao do formato (1)  |
| SALT           | 32 bytes | Salt do PBKDF2         |
| NONCE          | 12 bytes | Nonce do AES-GCM       |
| TAG            | 16 bytes | Tag de autenticacao    |
| METADATA       | 256 bytes| Metadados JSON         |
| CIPHERTEXT     | N bytes  | Dados criptografados   |
+----------------+----------+------------------------+
```

### Estrutura dos Metadados

```json
{
  "original_size": 1024,
  "original_filename": "secret.txt",
  "timestamp": 1699999999
}
```

---

## Consideracoes de Seguranca

### Pontos Fortes

- Criptografia autenticada evita adulteracoes silenciosas
- PBKDF2-HMAC-SHA256 com 600 mil iteracoes aumenta o custo de ataques de forca bruta
- Salt e nonce novos a cada criptografia
- Valores aleatorios novos para cada arquivo

### Limitacoes

- **Sem recuperacao de senha** - Senha perdida significa dados perdidos
- **Apagamento seguro e limitado** - Recuperacao em nivel de sistema operacional ou armazenamento ainda pode ser possivel
- **Exposicao em memoria** - Senhas podem permanecer temporariamente na memoria do processo

### Boas Praticas

1. **Use senhas fortes** - No minimo 12 caracteres com letras maiusculas, minusculas, numeros e simbolos
2. **Mantenha backups** - Sempre tenha copias dos arquivos importantes
3. **Teste primeiro** - Verifique se criptografia e descriptografia funcionam antes de apagar originais
4. **Nao esqueca as senhas** - Nao existe mecanismo de recuperacao

---

## Estrutura do Projeto

```text
voidcrypt/
|-- core/
|   |-- crypto.py       # Implementacao AES-256-GCM + PBKDF2
|   |-- file_handler.py # I/O de arquivos com progresso
|   |-- format.py       # Formato binario proprio
|   `-- utils.py        # Logs e utilitarios
|-- cli/
|   |-- main.py         # Ponto de entrada da CLI
|   `-- commands.py     # Implementacao dos comandos
|-- config/
|   `-- settings.py     # Configuracoes
|-- tests/
|   `-- test_crypto.py
|-- requirements.txt
|-- run.py
`-- README.md
```

---

## Testes

```bash
# Rodar testes unitarios
python -m pytest tests/

# Ou executar diretamente
python -m voidcrypt.tests.test_crypto
```

Saida esperada:

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 2.451s

OK
```

---

## Dependencias

| Pacote | Finalidade |
|--------|------------|
| cryptography | Criptografia AES-GCM |
| argon2-cffi | Dependencia listada no projeto |
| rich | Interface no terminal |

---

## Licenca

Licenca MIT. Consulte o arquivo LICENSE para mais detalhes.

---

## Aviso Legal

ESTE SOFTWARE E FORNECIDO "COMO ESTA", SEM GARANTIA DE QUALQUER TIPO. USE POR SUA CONTA E RISCO. OS AUTORES NAO SE RESPONSABILIZAM POR DANOS RESULTANTES DO USO DESTE SOFTWARE.

Esta ferramenta e destinada a protecao legitima de privacidade. Sempre cumpra as leis e regulamentacoes aplicaveis na sua jurisdicao.

---

## Creditos

Inspirado por:

- VeraCrypt
- SQLCipher
- Vencedores da Password Hashing Competition

---

<p align="center">
  <sub>Criado para fins educacionais e de protecao legitima de privacidade.</sub>
</p>

# SENTINEL - Modulo 1: verificador de links suspeitos (phishing)
# ATENCAO: este programa NUNCA abre nem acessa o link. Ele le apenas o TEXTO da URL.

# Encurtadores de link mais conhecidos
ENCURTADORES = ["bit.ly", "tinyurl.com", "cutt.ly", "encurtador.com.br", "t.co"]

# Palavras que golpistas usam para assustar ou animar a vitima
PALAVRAS_ISCA = ["login", "verificar", "atualizar", "senha", "premio",
                 "gratis", "bloqueado", "seguranca"]

# Marca conhecida -> dominio oficial dela
MARCAS = {
    "itau": "itau.com.br",
    "bradesco": "bradesco.com.br",
    "nubank": "nubank.com.br",
    "caixa": "caixa.gov.br",
    "correios": "correios.com.br",
    "netflix": "netflix.com",
    "paypal": "paypal.com",
    "mercadolivre": "mercadolivre.com.br",
}


# Pega so a parte do dominio da URL (tira o http:// e corta na primeira barra)
def pegar_dominio(url):
    dominio = url.replace("https://", "")
    dominio = dominio.replace("http://", "")
    dominio = dominio.split("/")[0]
    return dominio


# Verifica se a URL nao usa https
def sem_https(url):
    return not url.startswith("https")


# Verifica se o dominio e um endereco de IP (ex: 192.168.0.1)
def usa_ip(url):
    dominio = pegar_dominio(url)
    pedacos = dominio.split(".")
    if len(pedacos) != 4:
        return False
    for pedaco in pedacos:
        if not pedaco.isdigit():
            return False
    return True


# Verifica se o dominio e um encurtador de link conhecido
def e_encurtador(url):
    dominio = pegar_dominio(url)
    return dominio in ENCURTADORES


# Verifica se existe o caractere @ na URL
def tem_arroba(url):
    return "@" in url


# Verifica se o dominio tem subdominios demais (mais de 3 pontos)
def muitos_subdominios(url):
    dominio = pegar_dominio(url)
    return dominio.count(".") > 3


# Verifica se a URL tem alguma palavra-isca
def tem_palavra_isca(url):
    for palavra in PALAVRAS_ISCA:
        if palavra in url:
            return True
    return False


# Verifica se a URL cita uma marca conhecida sem ser o dominio oficial dela
def imita_marca(url):
    dominio = pegar_dominio(url)
    for marca in MARCAS:
        oficial = MARCAS[marca]
        e_oficial = dominio == oficial or dominio.endswith("." + oficial)
        if marca in url and not e_oficial:
            return True
    return False


# Verifica se a URL e muito longa (mais de 75 caracteres)
def url_muito_longa(url):
    return len(url) > 75


# Roda todas as regras e devolve a pontuacao de risco e a lista de alertas
def analisar(url):
    pontuacao = 0
    alertas = []

    if imita_marca(url):
        pontuacao = pontuacao + 35
        alertas.append("Imita uma marca conhecida, mas o dominio nao e o oficial.")

    if usa_ip(url):
        pontuacao = pontuacao + 25
        alertas.append("Usa numeros de IP no lugar do nome do site: muito usado em golpes.")

    if e_encurtador(url):
        pontuacao = pontuacao + 20
        alertas.append("E um link encurtado: esconde para onde voce vai de verdade.")

    if tem_arroba(url):
        pontuacao = pontuacao + 20
        alertas.append("Tem '@' no endereco: truque para te levar a outro site.")

    if sem_https(url):
        pontuacao = pontuacao + 15
        alertas.append("Nao usa HTTPS: os dados viajam sem protecao.")

    if muitos_subdominios(url):
        pontuacao = pontuacao + 15
        alertas.append("Tem subdominios demais: tenta parecer o site oficial.")

    if tem_palavra_isca(url):
        pontuacao = pontuacao + 10
        alertas.append("Usa palavras de isca (login, premio, senha...) para te apressar.")

    if url_muito_longa(url):
        pontuacao = pontuacao + 5
        alertas.append("Endereco muito longo: dificulta ver o dominio verdadeiro.")

    return pontuacao, alertas


# Transforma a pontuacao no resultado final em palavras
def classificar(pontuacao):
    if pontuacao >= 45:
        return "PERIGOSO"
    if pontuacao >= 20:
        return "SUSPEITO"
    return "SEGURO"


# Mostra o resultado da analise na tela
def mostrar_resultado(url, pontuacao, alertas):
    print("")
    print("=== SENTINEL - ANALISE DE LINK ===")
    print("URL analisada: " + url)
    print("Resultado: " + classificar(pontuacao))
    print("Pontuacao de risco: " + str(pontuacao))
    print("")
    print("Alertas encontrados:")
    if len(alertas) == 0:
        print("- Nenhum alerta encontrado.")
    else:
        for alerta in alertas:
            print("- " + alerta)


if __name__ == "__main__":
    url_digitada = input("Cole a URL para analisar: ")
    url_limpa = url_digitada.strip().lower()
    pontos, lista_de_alertas = analisar(url_limpa)
    mostrar_resultado(url_limpa, pontos, lista_de_alertas)

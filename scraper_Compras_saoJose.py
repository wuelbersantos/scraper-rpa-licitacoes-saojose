import json
import datetime
from selenium.webdriver.common.by import By
from seleniumwire import webdriver
from seleniumwire.utils import decode


class GUI():

    def limparArquivo(self, dado):
        try:
            with open(dado, "r+") as f:
                f.truncate(0)
        except Exception as ex:
            print("erro ao limpar/arquivo ja limpo")
        print("limpei o arquivo " + str(dado))

    def gravarArquivo2(self, info):
        self.limparArquivo("dados.json")
        try:
            json_str = json.dumps(info)
            with open("dados.json", "w") as arquivo:
                arquivo.write(json_str)
            print("gravei  dados.json")
        except Exception as ex:
            print("erro ao gravar dados.json")

    def gravarArquivoNew(self, info, entrada):
        dados = "dados" + entrada + ".json"
        self.limparArquivo(dados)
        try:
            json_str = json.dumps(info)
            with open(dados, "w") as arquivo:
                arquivo.write(json_str)
            print("gravei  dados.json")
        except Exception as ex:
            print("erro ao gravar dados.json")

    def gravarArquivo(self, info):
        try:
            arquivo = open('meu_arquivo.json', 'w')
            arquivo.write(info)
            arquivo.close()
            print("gravei alteracoes meu_arquivo.json")
        except Exception as ex:
            print("erro ao gravar meu_arquivo.json")

    def converterData(self, data):
        data = data.replace('/Date(', '').replace(')/', '')
        unix_time = int(data) / 1000
        date_time = datetime.datetime.fromtimestamp(unix_time)
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    def lerArquivo2(self, conteudo, entrada):
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        json_object = json.loads(conteudo)

        # Loop corrigido para iterar pelos registros reais recebidos no JSON
        for row in range(len(json_object["d"])):
            data = str(json_object["d"][row]["tDtInicial"])
            dataDisputa = str(json_object["d"][row]["tDtFinal"])

            param40 = ""
            aux = json_object["d"][row]["sNmModalidadeTipo"]
            if len(aux) == 0:
                param40 = str(json_object["d"][row]["sNmModalidade"])
            else:
                param40 = str(json_object["d"][row]["sNmModalidadeTipo"])

            orgaoaux = json_object["d"][row]["sNmApelido"]
            if orgaoaux == "":
                orgaoaux = json_object["d"][row]["sNmEmpresa"]
            else:
                orgaoaux = json_object["d"][row]["sNmApelido"]

            json_object["d"][row]["tDtInicial"] = self.converterData(data)
            json_object["d"][row]["tDtFinal"] = self.converterData(dataDisputa)
            json_object["d"][row]["sDsImagem"] = param40

            print(f"############### {row} ##########################")
            print(f"{row} id: {json_object['d'][row]['nCdProcesso']}\n"
                  f" data acolhimento: {json_object['d'][row]['tDtInicial']}\n"
                  f" data Disputa: {json_object['d'][row]['tDtFinal']}\n"
                  f" paran20 Processo : {json_object['d'][row]['sNrProcessoDisplay']}\n"
                  f" Texto : {json_object['d'][row]['sDsObjeto']}\n"
                  f" Situacao : {json_object['d'][row]['sDsSituacao']}\n"
                  f"param40: {param40}\n"
                  f" aux : {json_object['d'][row]['sDsImagem']}\n"
                  f"orgao: {orgaoaux}")

        print("fim processo alteracoes datas orgao e param40")
        self.gravarArquivoNew(json_object, entrada)

    def test_capture_request(self):
        for request in self.driver.requests:
            if request.response:
                if "PesquisarProcessosPorSituacoesAgrupadas" in request.url:
                    response = request.response
                    body = decode(response.body, response.headers.get('content-Encoding', 'identity'))
                    body_cont = body.decode("utf-8")
                    self.a.append(body_cont)

    def esperaId(self):
        validacao = False
        while not validacao:
            try:
                aux = self.driver.find_element(By.ID, "lblMuralTitulo").is_displayed()
                if aux:
                    validacao = True
                    print("validador ok ")
            except Exception:
                print("aguardando")

    def carregandolsita(self):
        validacao = False
        cont = 0
        while not validacao:
            try:
                aux = self.driver.find_element(By.ID, "carregandoLista").is_displayed()
                cont += 1
                if cont >= 200 or aux:
                    validacao = True
                    print("validador ok ")
            except Exception:
                print("aguardando ")

    def qtdlinhas(self):
        lista_qtdlinhas = self.driver.find_elements(By.XPATH,
                                                    "/html/body/form/div[3]/div[4]/div/div[1]/div[3]/div[5]/table/tbody/tr")
        return len(lista_qtdlinhas)

    def loop(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        try:
            self.driver.get("https://egov.paradigmabs.com.br/saojose/Portal/Mural.aspx")
        except Exception:
            print("erro ao abrir navegador")

        self.esperaId()
        self.carregandolsita()
        self.dadosretorno = self.qtdlinhas()

        while self.dadosretorno <= 50:
            self.dadosretorno = self.qtdlinhas()
            self.carregandolsita()
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            print("dados da tela " + str(self.dadosretorno))

        self.test_capture_request()
        self.driver.close()

    def __init__(self):
        self.a = []
        self.b = []
        self.c = []
        self.pagina = []
        self.dadosRetorno = 0
        self.file = ""

        self.loop()

        # Processamento dinâmico e seguro
        for index, conteudo in enumerate(self.a):
            self.lerArquivo2(conteudo, str(index))


a = GUI()

import threading
from threading import Timer, Thread
from subprocess import PIPE, run
from datetime import datetime
from ping3 import ping
from time import sleep

# Variaveis GLOBAIS


# LOCAL
"""
Essas primeiras linhas de variaveis, vão indicar os locais onde os arquivos de configuração e logs iram ficar. 
Como não tenho muito tempo para treinar em casa, onde tenho uma boa infra para a programação, acabo usando o notebook
da empresa para que possar treinar, mas infelizmente alguns sistemas não funciona no note da empresa e preciso testar
outras soluções. Com isso decidi instalar o XAMPP no notebook da empresa e o WAMP64 esta no meu computador de casa. 
Esse locais são essenciais para eu poder fazer a sair por PHP. 

'registro_log_status_LAN_WAN' = Locai que fica na nuvem, para me facilitar na visualização dos arquivos. 
'registro_log_status_PHP_i5 e registro_log_status_PHP_NTB' = São os locais onde fica o arquivo de log para apenas um 
dado por vez. Serve para mostra o status de forma mais 'bonita' para o usuário. 
"""
registro_log_status_LAN_WAN = 'G:/Meu Drive/Estudos/Python/Arquivos de texto/relatorio_internet_v2/'
registro_log_status_PHP_i5 = 'C:/wamp64/www/Meus Projetos/Meus-Projetos-PHP/relatorio_internet_v-txt_v2/'
registro_log_status_PHP_NTB = 'G:/Meu Drive/Estudos/XAMPP/htdocs/_Projetos/relatorio_internet_v-txt_v2/'

# ARQUIVOS
"""
As varias abaixo são responsaveis por criar os arquivos do status do ping. As duas varias disponiveis sempre recebera 
as informações, sem deleto quando um dado entrar. Como eles é possivel lista todos o processo, desde o inicio da criação
do arquivo de log. 
"""
arquivo_log_LAN = '_status_LAN.log'
arquivo_log_WAN = '_status_WAN.log'

# ARQUIVOS CONFIGURAÇÃO
"""
Essas duas variais são responsavel por armazenas as informações de IP e URL que serão usados no ping. Ainda é possivel 
colocar apenas um endereço de LAN e WAN.
"""
arquivo_end_IP4 = '_end_ipv4_1.log'
arquivo_end_URLIP = '_end_url.log'

# Objeto principal
"""
Resolvi criar um objeto mais para poder treinar melhor. Conforma vai passar pelos objetos e atributos vou explicando 
melhor sobre cada um. 
"""


class MonitorPing:
    def __init__(self):
        self.status_ON = 'ATIVO'
        self.status_OFF = 'INATIVO'
        self.data_atual = None
        self.end_LAN = None
        self.end_WAN = None
        self.linha = '___' * 40
        self.linha_error = ' -  - ' * 20

    def hora_certa(self):
        """
        Essa parte é uma das mais importantes, o horario que definira as condições da rede e internet.
        """
        self.data_atual = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')

    def verif_ip_correto_lan(self, valor_end):
        """
        OBS: Todos os endereços de IPV4 possui 4 octetos separados por '.' (ponto). Eu não vou usar endereço WINS para
        imcp na rede. Apenas endereços com os 4 octetos, escritos em decimal.
        Essa função serve para que o endereço de ip seja inserido corretamente, independemente se o host está respondendo
        ou não. Caso o usuário não coloque o endereço correto, no log vai ficar com as informações erradas e na saída
        do php pode ocorrer alguns erros na leitura do arquivo de log.

        Parte_01
        Param_001: os dados inseridos no arquivo de log, serão analisados com o metodo "split", os 4 octetos
        serão separados quando o parametro encontrar um ".", cada octeto é separado e colocar em uma lista. Logo depois
        os dados contidos dentro da lista é separado em cada variável.

        condic_001: essas condições analisam se os valores contidos nas variaveis é verdadeiro.
        O primeiro "if" indentifica se a variavel "valor_end" esta vazia. Caso estaja vazia. retorna FALSO.
        O segundo "elif" vai analisar se o valor que foi digitado é um "www", caso seja verdadeiro, retorna FALSO.
        O terceiro "elif" analisa se o que possui na variavel é números. Caso seja verdade, retorna um VERDADEIRO.
        """
        while True:
            # param_001
            try:
                end_ip_array = valor_end.strip().split('.')
                primeiro_oct = end_ip_array[0]
                segundo_oct = end_ip_array[1]
                terceiro_oct = end_ip_array[2]
                quarto_oct = end_ip_array[3]
            except IndexError:
                return False
            # condic_001
            if len(valor_end) == 0:
                print('Você não digitou nenhum endereço de IP')
                sleep(5)
                return False
            elif primeiro_oct == 'www':
                print('Você não pode adicionar nesse campo um endereço URL.\n'
                      'Digite um endereço de ip no formato indicado (84)')
                sleep(5)
                return False
            elif primeiro_oct in '0123456789':
                print('Você não pode adicionar nesse campo um endereço URL.\n'
                      'Digite um endereço de ip no formato indicado (89)')
                sleep(5)
                return True
            """
            Parte_02
            Essa parte da função é responsavel por analisar se o endereço de IP esta correto. Se possui 4 octetos, se 
            cada octeto possui no "máximo" de 1 a 3 números decimal. 
            for_01: Ele busca pelo "." no endereço que foi inserido pelo usuário. 
            condic_002: Esse condição vai ser responvél por analisar string por string, procurando o ".", conso encontre
            O contador que foi criado vai somar +1. 
            condic_003: Caso a variável "cont" tenha o valor de "3", então vai ser analisado se os endereços de ip, octeto 
            por octeto estão com 1 ou 3 caracteres decimal. Dentro desse condição, vai analisado se o octeto esta correto, 
            caso esteja, a funcção vai retornar um VERDADEIRO.
            """
            cont = 0
            valor_end = str(valor_end)
            # for_01
            for valor_ponto in valor_end:
                # condic_002
                if valor_ponto == '.':
                    cont += 1
            # condic_003
            if cont == 3:
                # condic_004
                if 3 >= len(primeiro_oct) >= 1 and 3 >= len(segundo_oct) >= 1 and 3 >= len(
                        terceiro_oct) >= 1 and 3 >= len(quarto_oct) >= 1:
                    return True
                else:
                    return False
            else:
                return False

    # Funções para LAN
    def verificacao_endIP_LAN(self):
        """
        Essa função permite analisar se o arquivo de configurações, contendo o endereço de ip LAN.
        Caso não seja encontrado, é chamado uma nova funcção para criar o arquivo.
        """
        try:
            verif_IP = open(registro_log_status_LAN_WAN + arquivo_end_IP4, 'r')
            verif_IP.close()
            return True
        except FileNotFoundError:
            return False

    def registrando_end_ip(self):
        """
        Função básica para registrar o endereço de ip LAN.
        Aqui serão solicitados o endereço para o usuário, no próprio texto já mostra como que o endereço deve ser inserido.
        Todos os dados inseridos, passará por uma análise para validar se o endereço esta corrego.
        O arquivo pode conter apenas um endereço de ip LAN. Quando o usuário registra um novo endereço, o arquivo é
        modifica por completo.
        """
        print(self.linha)
        while True:
            entrada_dados = str(input('Entre com o END de ipv4 (x.x.x.x): ')).strip()
            if not self.verif_ip_correto_lan(entrada_dados):
                print()
                print(self.linha_error)
                print('Digite o endereço de IP correto:')
                print(self.linha_error)
                print()
            else:
                try:
                    registrando_endIP = open(registro_log_status_LAN_WAN + arquivo_end_IP4, 'w')
                    try:
                        registrando_endIP.write(f'{entrada_dados}')
                        registrando_endIP.close()
                        print('LAN: Registro realizado com sucesso!')
                        sleep(2)
                        break
                    except FileNotFoundError:
                        print('LAN: Não foi encontrado o arquivo de log (151)')
                    except NameError:
                        print('LAN: Você inseriu dados incorretos (151)')
                except:
                    print('LAN: Ocorreu um erro no arquivo log(151)')

    def verificao_arq_IP_LAN(self):
        """
        Função que verifica o existencia do arquivo de configuração.
        param: É chamada a função "verificacao_endIP_LAN" para analisar o arquivo. Caso returne FALSE.
        É chamado a função para registrar um novo endereço de IP LAN.
        """
        if not self.verificacao_endIP_LAN():
            self.registrando_end_ip()

    def buscando_end_LAN(self):
        """
        Com essa função, é aberto o arquivo que fica o endereço de IP LAN sendo colocado dentro da variável para
        ser usada no momento que o programa estiver em execusão. Quando programa é aberto novamente, é feito outra
        busca.
        """
        try:
            valor_dados_arq = open(registro_log_status_LAN_WAN + arquivo_end_IP4, 'r')
            try:
                self.end_LAN = valor_dados_arq.readline()
                valor_dados_arq.close()
            except IOError:
                print(f'LAN: Não foi possivél encontrar os dados do arquivo {arquivo_end_IP4}')

        except FileNotFoundError:
            print(f'LAN: Arquivo o {arquivo_end_IP4} não foi encontrado! (193)')

    def ping_rede_local(self):
        """
        Essa é a função principal do programa. Com ela vamos realizar o procedimento de ping e como o log sera
        registrado.
        ping_lan_exec: aqui é o coração do programa. Quando o programa esta completamente configurado e o usuário inicia o app
        Quando a função é chamado, a variavel_ip_lan já contem o endereço de IP lan para dar início. A variável "pingdando_end_local"
        vai receber os valores do metodo "run".
        condic_01_lan_true: O "if" vai analisar o metodo "returncode", caso o ping tenha sido respondido, o valor é 0. Se o valor
        for 1, é que o ping não teve resposta do servidor. Quando o valor for igual a 0, então essa condição é VERDADEIRA.

        """
        # variavel_ip_lan
        self.buscando_end_LAN()  # contem o endereço de IP
        try:
            # ping_lan_exec
            pingando_end_local = run('ping ' + self.end_LAN + ' -n 5 -w 1', stdout=PIPE)

            # condic_01_lan_true
            # se o resultado for verdadeiro
            if pingando_end_local.returncode == 0:
                print('')
                print(
                    f'>>> [ {self.data_atual} ] | Status ICMP do endereço de LAN [ {self.end_LAN} ] [ >> {self.status_ON} << ]')
                try:  # Registro realizado na nuvem
                    registrando_status_ON_LAN_txt = open(registro_log_status_LAN_WAN + arquivo_log_LAN, 'a')
                    registrando_status_ON_LAN_txt.write(f'{self.data_atual} - {self.status_ON}\n')
                    registrando_status_ON_LAN_txt.close()
                except TypeError:
                    print(self.linha_error)
                    print('(LAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no arquivo (TXT)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(LAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no arquivo (TXT)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(LAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no arquivo (TXT')
                    print(self.linha_error)

                try:  # Registro realizado no servidor PHP no Mini-i5
                    registrando_status_ON_LAN_PHP_i5 = open(registro_log_status_PHP_i5 + arquivo_log_LAN, 'w')
                    registrando_status_ON_LAN_PHP_i5.write(f'{self.data_atual} - {self.status_ON}')
                    registrando_status_ON_LAN_PHP_i5.close()
                except TypeError:
                    print(self.linha_error)
                    print('(LAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(LAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(LAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (i5)')

                try:  # Registro realizado no servidor PHP notebook dá penso
                    registrando_status_ON_LAN_PHP_NTB = open(registro_log_status_PHP_NTB + arquivo_log_LAN, 'w')
                    registrando_status_ON_LAN_PHP_NTB.write(f'{self.data_atual} - {self.status_ON}')
                    registrando_status_ON_LAN_PHP_NTB.close()
                except TypeError:
                    print(self.linha_error)
                    print('(LAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(LAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(LAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)

            # condic_02_lan_false
            # Se o resultado for FALSO
            else:
                print('')
                print(
                    f'>> {self.data_atual} | Status ICMP do endereço de LAN {self.end_LAN} [ >> {self.status_OFF} << ]')
                try:  # Registro realizado na nuvem
                    registrando_status_OFF_LAN_txt = open(registro_log_status_LAN_WAN + arquivo_log_LAN, 'a')
                    registrando_status_OFF_LAN_txt.write(f'{self.data_atual} - {self.status_OFF}\n')
                    registrando_status_OFF_LAN_txt.close()
                except TypeError:
                    print(self.linha_error)
                    print('(LAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no aqruivo (TXT)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(LAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no arquivo (TXT)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(LAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no arquivo (TXT')
                    print(self.linha_error)

                try:  # Registro realizado no servidor PHP no Mini-i5
                    registrando_status_OFF_LAN_PHP_i5 = open(registro_log_status_PHP_i5 + arquivo_log_LAN, 'w')
                    registrando_status_OFF_LAN_PHP_i5.write(f'{self.data_atual} - {self.status_OFF}')
                    registrando_status_OFF_LAN_PHP_i5.close()
                except TypeError:
                    print(self.linha_error)
                    print('(LAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(LAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(LAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)

                try:  # Registro realizado no servidor PHP notebook dá penso
                    registrando_status_OFF_LAN_PHP_NTB = open(registro_log_status_PHP_NTB + arquivo_log_LAN, 'w')
                    registrando_status_OFF_LAN_PHP_NTB.write(f'{self.data_atual} - {self.status_OFF}')
                    registrando_status_OFF_LAN_PHP_NTB.close()
                except TypeError:
                    print(self.linha_error)
                    print('(LAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(LAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(LAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
        except IOError:
            print('Host de destino LAN inacessível.!\n')

    # Funções para WAN
    def verificando_dados_WAN(self):
        try:
            verif_ip = open(registro_log_status_LAN_WAN + arquivo_end_URLIP, 'r')
            verif_ip.close()
            return True
        except FileNotFoundError:
            return False

    def registrando_end_URRIP(self):
        print(self.linha)
        while True:
            valor_URL = str(input('Digite um URL/IP: '))
            if len(valor_URL) <= 7:
                print('Digite um endereço de ip correto:')
                print(self.linha_error)
            else:
                try:
                    registrando_URL = open(registro_log_status_LAN_WAN + arquivo_end_URLIP, 'w')
                    registrando_URL.write(valor_URL)
                    registrando_URL.close()
                    print('WAN: Registro realizado com sucesso!')
                    sleep(2)
                    break
                except TypeError:
                    print('WAN: Você inseriu um valor errado!')

    def verificando_arq_URL_WAN(self):
        if not self.verificando_dados_WAN():
            self.registrando_end_URRIP()

    def buscando_URL_WAN(self):
        try:
            buscando_URL = open(registro_log_status_LAN_WAN + arquivo_end_URLIP, 'r')
            try:
                self.end_WAN = buscando_URL.readline()
                buscando_URL.close()
            except:
                print('WAN: Não foi encontrados dados no sistema')
        except FileNotFoundError:
            print('WAN: Arquivo no foi enconrado')

    def ping_rede_internet(self):
        """
        Precisa modificar o status, quando link fica online, arquivo off não é modificado e a saida sempre mostra
        que link está inativo
        """
        self.buscando_URL_WAN()
        try:
            pingando_end_internet = run('ping ' + self.end_WAN + ' -n 5 -w 1 ', stdout=PIPE)

            # Quando o ping foi Verdadeiro
            if pingando_end_internet.returncode == 0:
                print('')
                print(
                    f'>>> [ {self.data_atual} ] | Status ICMP do endereço de URL/IP [ {self.end_WAN} ] [ >> {self.status_ON} << ]')
                try:  # Registro realizado na nuvem
                    registrando_status_ON_WAN_txt = open(registro_log_status_LAN_WAN + arquivo_log_WAN, 'a')
                    registrando_status_ON_WAN_txt.write(f'{self.data_atual} - {self.status_ON}\n')
                    registrando_status_ON_WAN_txt.close()
                except TypeError:
                    print(self.linha_error)
                    print('(WAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no arquivo (TXT)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(WAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no arquivo (TXT)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(WAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no arquivo (TXT')
                    print(self.linha_error)

                try:  # Registro realizado no servidor PHP no Mini-i5
                    registrando_status_ON_WAN_PHP_i5 = open(registro_log_status_PHP_i5 + arquivo_log_WAN, 'w')
                    registrando_status_ON_WAN_PHP_i5.write(f'{self.data_atual} - {self.status_ON}')
                    registrando_status_ON_WAN_PHP_i5.close()
                except TypeError:
                    print(self.linha_error)
                    print('(WAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(WAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(WAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)

                try:  # Registro realizado no servidor PHP notebook dá dpenso
                    registrando_status_ON_WAN_PHP_NTB = open(registro_log_status_PHP_NTB + arquivo_log_WAN, 'w')
                    registrando_status_ON_WAN_PHP_NTB.write(f'{self.data_atual} - {self.status_ON}')
                    registrando_status_ON_WAN_PHP_NTB.close()
                except TypeError:
                    print(self.linha_error)
                    print('(WAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(WAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(WAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)

            # Quando o pingo foi FALSO
            else:
                print('')
                print(
                    f'>> {self.data_atual} | Status ICMP do endereço de URL/IP {self.end_WAN} [ >> {self.status_OFF} << ]')
                try:  # Registro realizado na nuvem
                    registrando_status_OFF_WAN_txt = open(registro_log_status_LAN_WAN + arquivo_log_WAN, 'a')
                    registrando_status_OFF_WAN_txt.write(f'{self.data_atual} - {self.status_OFF}\n')
                    registrando_status_OFF_WAN_txt.close()
                except TypeError:
                    print(self.linha_error)
                    print('(WAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no aqruivo (TXT)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(WAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no arquivo (TXT)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(WAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no arquivo (TXT')
                    print(self.linha_error)

                try:  # Registro realizado no servidor PHP no Mini-i5
                    registrando_status_OFF_WAN_PHP_i5 = open(registro_log_status_PHP_i5 + arquivo_log_WAN, 'w')
                    registrando_status_OFF_WAN_PHP_i5.write(f'{self.data_atual} - {self.status_OFF}')
                    registrando_status_OFF_WAN_PHP_i5.close()
                except TypeError:
                    print(self.linha_error)
                    print('(WAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(WAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(WAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (i5)')
                    print(self.linha_error)

                try:  # Registro realizado no servidor PHP notebook dá penso
                    registrando_status_OFF_WAN_PHP_NTB = open(registro_log_status_PHP_NTB + arquivo_log_WAN, 'w')
                    registrando_status_OFF_WAN_PHP_NTB.write(f'{self.data_atual} - {self.status_OFF}')
                    registrando_status_OFF_WAN_PHP_NTB.close()
                except TypeError:
                    print(self.linha_error)
                    print('(WAN (ON)): Dados estão incorretos para serem inseridos no arquivo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except FileNotFoundError:
                    print(self.linha_error)
                    print('(WAN (ON)): O Arquivo/Caminho de log não EXISTE\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
                except IOError:
                    print(self.linha_error)
                    print('(WAN (ON)): Arquivo de log não foi encontrado/não foi possivel reconhece-lo\n'
                          'Não foi possivel registrar no dispositivo (NTB)')
                    print(self.linha_error)
        except:
            print('Host de destino WAN inacessível.!\n')


iniciando_programa = MonitorPing()
iniciando_programa.verificao_arq_IP_LAN()
iniciando_programa.verificando_arq_URL_WAN()

# Busco os endereço de ip/url que já está no sistema. Ajuda ao usuário a identificar os enredeço sem precisar inciar o ping.
iniciando_programa.buscando_end_LAN()
iniciando_programa.buscando_URL_WAN()


# FUNÇÕES EXTERNAS

# F001
def leia_int(valor_opc):
    """
    Apena uma função para analisar se o valor digitado nas opções é um número inteiro.
    """
    while True:
        try:
            return int(input(valor_opc))
        except:
            print('Você escolheu uma opção invalida!')


# F002
def menu_iniciar():
    while True:
        """
        O loop do menu principal, vai interagir com o usuário final. Aqui ele pode escolher se inicia o programa ou configura
        novos enredeços de hosts.
        No inicio o menu mostra os endereços que já esta no sistema. Caso não tenho nenhum endereço, o usuário precisa cadastrar 
        os novos, tanto endereço de LAN como um url ou endereço WAN.
        """
        iniciando_programa.buscando_end_LAN()
        iniciando_programa.buscando_URL_WAN()
        print(iniciando_programa.linha)
        print('Monitorando LAN E WAN'.center(120))
        print(iniciando_programa.linha)

        print()
        print(f'Endereços de LAN e WAN configurados no sistema'.center(120))
        print(f'Endereço LAN: [ {iniciando_programa.end_LAN} ]'.center(120))
        print(f'Endereço WAN: [ {iniciando_programa.end_WAN} ]'.center(120))
        print(f'{" --- ".center(23) * 5}')
        print('''
            [1] Iniciar o programa
            [2] Modificar o endereço LAN
            [3] Modificar o endereço
            [0] Sair do Programa
                    ''')
        print(iniciando_programa.linha)
        resp = leia_int('Escolha uma opção: ')
        if resp == 1:
            continuar = True
            continuar_menu = True

        elif resp == 2:
            iniciando_programa.registrando_end_ip()
            continuar = False
            continuar_menu = False

        elif resp == 3:
            iniciando_programa.registrando_end_URRIP()
            continuar = False
            continuar_menu = False

        elif resp == 0:
            continuar = False
            continuar_menu = True
        else:
            print('Você escolheu uma opção invalida!')
            continuar_menu = False
        print()
        if continuar_menu:
            break
    if continuar:
        iniciando_programa.buscando_end_LAN()
        iniciando_programa.buscando_URL_WAN()
        print('Iniciando o programa!')
        print(iniciando_programa.linha)
        sleep(2)
        print("Endereços para requisição ICMP")
        print(f'[ {iniciando_programa.end_LAN} ] - [ {iniciando_programa.end_WAN} ]')
        print(iniciando_programa.linha)
        while True:
            iniciando_programa.hora_certa()
            comando_LAN = Timer(iniciando_programa.ping_rede_local(), 0)
            comando_WAN = Timer(iniciando_programa.ping_rede_internet(), 0)
            print(iniciando_programa.linha)
    else:
        print('Fechando programa!')
        sleep(2)


# F003
def verif_ip_cadastrados():
    try:

        if len(iniciando_programa.end_LAN) == 0 and len(iniciando_programa.end_WAN) == 0:
            print('Não foi encontrado nenhum endereço de LAN e WAN no registrado\n'
                  'Voce precisa cadastrar ambos no sistema.')
            iniciando_programa.registrando_end_ip()
            iniciando_programa.registrando_end_URRIP()
            return True

        elif len(iniciando_programa.end_LAN) == 0 and len(iniciando_programa.end_WAN) > 1:
            print('Não foi encontrado o enredeço de LAN\n'
                  'É preciso registrar o endereço no sistema')
            iniciando_programa.registrando_end_ip()
            return True

        elif len(iniciando_programa.end_LAN) > 1 and len(iniciando_programa.end_WAN) == 0:
            print('Não foi encontrado o endereço de WAN\n'
                  'É preciso registrar o endereço no sistema')
            iniciando_programa.registrando_end_URRIP()
            return True
        else:
            return True

    except TypeError:
        print('(F003): Arquivos não foram encontrados para verificação')


if verif_ip_cadastrados():
    menu_iniciar()

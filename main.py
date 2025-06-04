import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

class AppMetereologia(QWidget):
    def __init__(self):
        super().__init__() 
        self.cidade = QLabel("Insira o nome da cidade: ", self)
        self.inserir_cidade = QLineEdit(self)
        self.botao = QPushButton("Pesquisar", self)
        self.temperatura = QLabel(self)
        self.representacao_emoji = QLabel(self)
        self.descricao_tempo = QLabel(self)
        self.humidade = QLabel(self)
        self.velocidade_vento = QLabel(self)
        self.direcao_vento = QLabel(self)
        self.precipitacao = QLabel(self)
        self.sensacao_termica = QLabel(self)
        self.qualidade_ar = QLabel(self)
        self.UI()

    def UI(self):
        self.setWindowTitle("Metereologia")
        layout = QVBoxLayout()

        layout.addWidget(self.cidade)
        layout.addWidget(self.inserir_cidade)
        layout.addWidget(self.botao)
        layout.addWidget(self.temperatura)
        layout.addWidget(self.representacao_emoji)
        layout.addWidget(self.descricao_tempo)
        layout.addWidget(self.humidade)
        layout.addWidget(self.velocidade_vento)
        layout.addWidget(self.direcao_vento)
        layout.addWidget(self.precipitacao)
        layout.addWidget(self.sensacao_termica)
        layout.addWidget(self.qualidade_ar)

        self.setLayout(layout)

        self.cidade.setAlignment(Qt.AlignCenter)
        self.inserir_cidade.setAlignment(Qt.AlignCenter)
        self.temperatura.setAlignment(Qt.AlignCenter)
        self.representacao_emoji.setAlignment(Qt.AlignCenter)
        self.descricao_tempo.setAlignment(Qt.AlignCenter)
        self.humidade.setAlignment(Qt.AlignCenter)
        self.velocidade_vento.setAlignment(Qt.AlignCenter)
        self.direcao_vento.setAlignment(Qt.AlignCenter)
        self.precipitacao.setAlignment(Qt.AlignCenter)
        self.sensacao_termica.setAlignment(Qt.AlignCenter)
        self.qualidade_ar.setAlignment(Qt.AlignCenter)

        self.cidade.setObjectName("cidade")
        self.inserir_cidade.setObjectName("cidade_inserir")
        self.botao.setObjectName("botao")
        self.temperatura.setObjectName("temperatura")
        self.representacao_emoji.setObjectName("emoji")
        self.descricao_tempo.setObjectName("descricao")
        self.humidade.setObjectName("humidade")
        self.velocidade_vento.setObjectName("ventoV")
        self.direcao_vento.setObjectName("direcaoV")
        self.precipitacao.setObjectName("precipitacao")
        self.sensacao_termica.setObjectName("termica")
        self.qualidade_ar.setObjectName("qualidade")

        self.setStyleSheet("""
                QWidget {
                    background:  qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255, 183, 77, 255), stop:1 rgba(255, 94, 77, 255));
                }       
                QLabel, QPushButton {
                    font-family: calibri;
                }
                QLabel#cidade {
                    font-size: 40px;
                    font-style: calibri;
                    color:rgb(203, 224, 13);
                    background-color:rgb(98, 33, 110);
                }
                QLineEdit#cidade_inserir {
                    font-size: 40px;
                }
                QPushButton#botao {
                    font-size: 30px;
                    font-weight: bold;
                    margin-top: 20px;
                }
                QLabel#temperatura {
                    font-size: 75px;
                }
                QLabel#emoji {
                    font-size: 100px;
                    font-family: Segoe UI emoji;
                }
                QLabel#descricao {
                    font-size: 50px;
                }
                QLabel#humidade, QLabel#ventoV, QLabel#direcaoV, QLabel#precipitacao, QLabel#termica, QLabel#qualidade {
                    font-size: 40px;
                }
                QLabel#precipitacao, QLabel#qualidade {
                    font-size: 40px;
                    margin-top: 20px;
                }
        """)

        self.botao.clicked.connect(self.get_informacao)

    def get_informacao(self):
        chave_api = "f59cd3ef7c79f2aa8a877510dbeba1e9"
        cidade = self.inserir_cidade.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&lang=pt"

        try:  
            resposta = requests.get(url)
            resposta.raise_for_status()
            data = resposta.json()

            if data["cod"] == 200:

                lat = data["coord"]["lat"]
                lon = data["coord"]["lon"]

            
                url_air_quality = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={chave_api}"
                resposta_air_quality = requests.get(url_air_quality)
                resposta_air_quality.raise_for_status()
                air_quality_data = resposta_air_quality.json()

                self.mostrar_informacao(data, air_quality_data)

        except requests.exceptions.HTTPError as http_error:
           match resposta.status_code:
               case 400:
                   self.mostrar_erros("Pedido negado \nPor favor verifique o nome da cidade")
               case 401:
                   self.mostrar_erros("Não autorizado \nChave da API não é válida")
               case 403:
                   self.mostrar_erros("Proibido \nAcesso negado")
               case 404:
                   self.mostrar_erros("Não encontrado \nCidade não encontrada")
               case 500:
                   self.mostrar_erros("Internal server error \nPor favor tente mais logo")
               case 502:
                   self.mostrar_erros("Bad Gateway \nResposta inválida do servidor")
               case 503:
                   self.mostrar_erros("Serviço indisponível \nServidor está desligado")
               case 504:
                   self.mostrar_erros("Gateway timeout \nSem resposta do servidor")
               case _:
                   self.mostrar_erros(F"Erro de HTTP\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.mostrar_erros("Erro de conexão:\nVerifique a sua conexão à internet")
        except requests.exceptions.Timeout:
            self.mostrar_erros("Erro de timeout\nServidor não consegue solicitar uma resposta")
        except requests.exceptions.TooManyRedirects:
            self.mostrar_erros("Too many Redirects\nErro, vários redirecionamentos")
        except requests.exceptions.RequestException as req_error:
            self.mostrar_erros(f"Request Error:\n{req_error}")

    def mostrar_erros(self, mensagem):
        self.temperatura.setStyleSheet("font-size: 30px;")
        self.temperatura.setText(mensagem)
        self.representacao_emoji.clear()
        self.descricao_tempo.clear()
        self.velocidade_vento.clear()
        self.humidade.clear()
        self.direcao_vento.clear()
        self.precipitacao.clear()
        self.sensacao_termica.clear()
        self.qualidade_ar.clear()
        
        
        
    
    def mostrar_informacao(self, info, air_quality_info):
        self.temperatura.setStyleSheet("font-size: 75px;")
        temperatura_Kelvin = info["main"]["temp"]
        temperatura_Celsius = temperatura_Kelvin - 273.15
        termica_Kelvin = info["main"]["feels_like"]
        termica_Celsius = termica_Kelvin - 273.15
        id_tempo = info["weather"][0]["id"]
        descricao_tempo = info["weather"][0]["description"]
        humidade = info["main"]["humidity"]
        velocidade_vento = info["wind"]["speed"] * 3.6
        direcao_vento = info["wind"]["deg"]
 

        direcao_cardinal = self.direcao_vento_em_cardinal(direcao_vento)

        if "rain" in info:
             precipitacao = info["rain"].get("1h", 0)  # Precipitação na última hora
             self.precipitacao.setText(f"Chuva (precipitação): {precipitacao} mm/h")

        elif "snow" in info:
             precipitacao = info["snow"].get("1h", 0)  # Precipitação na última hora
             self.precipitacao.setText(f"Neve: {precipitacao} mm/h")
        else:
             self.precipitacao.setText("Sem precipitação")
        
        self.temperatura.setText(f"{temperatura_Celsius:.0f}°C")
        self.sensacao_termica.setText(f"Sensação Térmica: {termica_Celsius:.0f}°C")
        self.representacao_emoji.setText(self.emoji(id_tempo))
        self.descricao_tempo.setText(descricao_tempo)
        self.humidade.setText(f"Humidade: {humidade}%")
        self.velocidade_vento.setText(f"Vento: {velocidade_vento:.1f}km/h")
        self.direcao_vento.setText(f"Direção do vento: {direcao_cardinal}")

        aqi = air_quality_info["list"][0]["main"]["aqi"]
        if aqi == 1:
            qualidade_ar = "Boa"
        elif aqi == 2:
            qualidade_ar = "Moderada"
        elif aqi == 3:
         qualidade_ar = "Insalubre"
        elif aqi == 4:
            qualidade_ar = "Muito insalubre"
        else:
            qualidade_ar = "Perigosa"
    
        self.qualidade_ar.setText(f"Qualidade do ar: {qualidade_ar}")


    @staticmethod
    def direcao_vento_em_cardinal(deg):
        if deg >= 0 and deg < 45:
            return "Norte"
        elif deg >= 45 and deg < 90:
            return "Nordeste"
        elif deg >= 90 and deg < 135:
            return "Leste"
        elif deg >= 135 and deg < 180:
            return "Sudeste"
        elif deg >= 180 and deg < 225:
            return "Sul"
        elif deg >= 225 and deg < 270:
            return "Sudoeste"
        elif deg >= 270 and deg < 315:
            return "Oeste"
        elif deg >= 315 and deg < 360:
            return "Noroeste"
        else:
            return "Desconhecido"

    @staticmethod
    def emoji(id_tempo):
        if id_tempo >= 200 and id_tempo <= 232:
            return "⛈️"
        elif id_tempo >= 300 and id_tempo <= 321:
            return "☁"
        elif id_tempo >= 500 and id_tempo <= 531:
            return "🌧"
        elif id_tempo >= 600 and id_tempo <= 622:
            return "🌨"
        elif id_tempo >= 701 and id_tempo <= 741:
            return "🌫"
        elif id_tempo == 762:
            return "🌋"
        elif id_tempo == 771:
            return "💨"
        elif id_tempo == 781:
            return "🌪"
        elif id_tempo == 800:
            return "☀"
        elif id_tempo >= 801 and id_tempo <= 804:
            return "☁☁"
        else:
            return ""
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_metereologia = AppMetereologia()
    app_metereologia.show()
    sys.exit(app.exec_())
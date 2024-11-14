from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import calendar
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco de dados MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # Substitua pelo seu usuário MySQL
        password="mysql2023",     # Substitua pela sua senha MySQL
        database="dbepanouir"  # Certifique-se de que o banco foi criado
    )

# Função para obter as semanas do mês
def get_calendar_data(year, month):
    first_day_of_month = datetime(year, month, 1)
    num_days_in_month = calendar.monthrange(year, month)[1]
    month_name = first_day_of_month.strftime('%B')
    start_weekday = first_day_of_month.weekday()

    weeks = []
    current_week = [None] * start_weekday
    for day in range(1, num_days_in_month + 1):
        current_week.append(day)
        if len(current_week) == 7:
            weeks.append(current_week)
            current_week = []
    if current_week:
        weeks.append(current_week + [None] * (7 - len(current_week)))

    return month_name, weeks, year, month

@app.route('/')
def inicial():
    return render_template('inicial.html')

@app.route('/calendario')
def index():
    today = datetime.today()
    year = int(request.args.get('year', today.year))
    month = int(request.args.get('month', today.month))

    month_name, weeks, year, month = get_calendar_data(year, month)

    return render_template('index.html', month_name=month_name, weeks=weeks,
                           year=year, month=month)

# Função para gerar horários com intervalo de 15 minutos
def gerar_horarios(inicio, fim, intervalo):
    horarios = []
    horario_atual = inicio
    while horario_atual <= fim:
        horarios.append(horario_atual.strftime("%H:%M"))
        horario_atual += timedelta(minutes=intervalo)
    return horarios

@app.route('/dia/<int:year>/<int:month>/<int:day>', methods=['GET', 'POST'])
def dia(year, month, day):
    horarios = gerar_horarios(datetime.strptime("00:00", "%H:%M"), datetime.strptime("23:45", "%H:%M"), 15)

    if request.method == 'POST':
        conn = get_db_connection()
        cursor = conn.cursor()

        for horario in horarios:
            atividade = request.form.get(f"atividade_{horario}")
            status = request.form.get(f"status_{horario}") == "on"

            if atividade:
                # Insere ou atualiza a atividade no banco de dados
                cursor.execute(
                    "REPLACE INTO atividades (ano, mes, dia, horario, atividade, status) VALUES (%s, %s, %s, %s, %s, %s)",
                    (year, month, day, horario, atividade, status)
                )
            else:
                # Remove a atividade se o campo estiver vazio
                cursor.execute(
                    "DELETE FROM atividades WHERE ano = %s AND mes = %s AND dia = %s AND horario = %s",
                    (year, month, day, horario)
                )

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dia', year=year, month=month, day=day))

    # Obter as atividades do banco de dados
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT horario, atividade, status FROM atividades WHERE ano = %s AND mes = %s AND dia = %s", (year, month, day))
    atividades_do_dia = {row['horario']: {'atividade': row['atividade'], 'status': row['status']} for row in cursor.fetchall()}
    cursor.close()
    conn.close()

    return render_template('dia.html', year=year, month=month, day=day,
                           horarios=horarios, atividades=atividades_do_dia)

@app.route('/saude', methods=['GET', 'POST'])
def saude():
    if request.method == 'POST':
        data_nascimento = request.form['data_nascimento']
        peso = float(request.form['peso'])
        altura = float(request.form['altura'])
        sexo = request.form['sexo']
        nivel_atividade = request.form['nivel_atividade']

        # Cálculo das recomendações
        idade = calcular_idade(data_nascimento)
        agua = calcular_agua(peso)
        sono = calcular_sono(idade)
        calorias = calcular_calorias(peso, altura, idade, sexo, nivel_atividade)
        fibras = calcular_fibras(idade, sexo)
        proteinas, carboidratos, gorduras = calcular_macronutrientes(calorias)

        return render_template(
            'saude.html',
            agua=agua, sono=sono, calorias=calorias,
            fibras=fibras, proteinas=proteinas, carboidratos=carboidratos, gorduras=gorduras,
            data_nascimento=data_nascimento, peso=peso, altura=altura, sexo=sexo, nivel_atividade=nivel_atividade
        )
    return render_template('saude.html')

def calcular_idade(data_nascimento):
    hoje = datetime.today()
    nascimento = datetime.strptime(data_nascimento, '%Y-%m-%d')
    idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
    return idade

def calcular_agua(peso):
    return peso * 0.035  # Exemplo: 35 ml por kg

def calcular_sono(idade):
    if idade < 18:
        return "8-10 horas"
    elif 18 <= idade <= 64:
        return "7-9 horas"
    else:
        return "7-8 horas"

def calcular_calorias(peso, altura, idade, sexo, nivel_atividade):
    if sexo == 'M':
        tmb = 10 * peso + 6.25 * altura - 5 * idade + 5
    else:
        tmb = 10 * peso + 6.25 * altura - 5 * idade - 161
    fator_atividade = {'sedentario': 1.2, 'moderado': 1.55, 'ativo': 1.725}.get(nivel_atividade, 1.2)
    return round(tmb * fator_atividade)

def calcular_fibras(idade, sexo):
    if sexo == 'M':
        return 38 if idade < 50 else 30
    else:
        return 25 if idade < 50 else 21

def calcular_macronutrientes(calorias):
    proteinas = round(0.15 * calorias / 4)
    carboidratos = round(0.55 * calorias / 4)
    gorduras = round(0.30 * calorias / 9)
    return proteinas, carboidratos, gorduras

if __name__ == '__main__':
    app.run(debug=True)

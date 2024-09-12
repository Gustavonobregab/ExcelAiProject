import pandas as pd
import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Função para inicializar o modelo da IA com um prompt financeiro
def initialize_model():
    template = """
    Crie um relatório financeiro detalhado, levando em consideração as seguintes diretrizes:

    A análise deve ser baseada em dados financeiros reais da empresa e focar em maximizar o lucro.
    Identifique áreas de custos variáveis, como transporte, eventos e consumo de energia, e proponha sugestões de redução de gastos que sejam realistas e possíveis de implementar.
    Para cada sugestão de redução de custos, mostre o impacto direto no lucro anual, com números claros, estimando o aumento da reserva ou do lucro.
    Inclua recomendações sobre como os recursos economizados podem ser reinvestidos em áreas estratégicas, como marketing ou inovação, destacando o potencial de retorno sobre esse investimento (ROI).
    Apresente as estimativas de impacto percentual no lucro anual e nos resultados financeiros gerais da empresa.
    O foco deve ser em fatos e dados comprovados, garantindo que as decisões sugeridas sejam baseadas em evidências financeiras sólidas.

    Data (JSON format): {financial_data}

    Relatório:
    {{}}
    """
    
    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    return prompt | model

# Função para processar a análise financeira da IA
def process_financial_analysis(financial_data, chain):
    return chain.invoke({"financial_data": financial_data})

# Função para limpar os dados da planilha
def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna()
    return df

# Função para ler a planilha e converter para JSON
def convert_excel_to_json(file_path):
    try:
        df = pd.read_excel(file_path)
        df_clean = clean_data(df)
        json_data = df_clean.to_json(orient="records")
        return json_data
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None


def main():
    
    chain = initialize_model()

    
    excel_file = "Mocks/preenchido.xlsx"
    json_data = convert_excel_to_json(excel_file)

    if json_data:
        print("JSON data converted successfully:")
        result = process_financial_analysis(json_data, chain)
        print("Financial Analysis:")
        print(result)
    else:
        print("Failed to convert Excel to JSON.")

if __name__ == "__main__":
    main()

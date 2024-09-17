import pandas as pd
import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate


def initialize_model():
    template = """
    Crie um relatório financeiro detalhado, levando em consideração as seguintes diretrizes:

    A análise deve ser baseada em dados financeiros reais da empresa e focar em maximizar o lucro.
    Identifique áreas de custos variáveis, como transporte, eventos e consumo de energia, e proponha sugestões de redução de gastos que sejam realistas e possíveis de implementar.
    Para cada sugestão de redução de custos, mostre o impacto direto no lucro anual, com números claros, estimando o aumento da reserva ou do lucro.
    Inclua recomendações sobre como os recursos economizados podem ser reinvestidos em áreas estratégicas, como marketing ou inovação, destacando o potencial de retorno sobre esse investimento (ROI).
    Apresente as estimativas de impacto percentual no lucro anual e nos resultados financeiros gerais da empresa.
    O foco deve ser em fatos e dados comprovados, garantindo que as decisões sugeridas sejam baseadas em evidências financeiras sólidas.

    Data (JSON format): {json_data}

    Relatório:
    {{}}  # Indica onde a resposta será gerada
    """
    
    model = OllamaLLM(model="llama3") 
    prompt = ChatPromptTemplate.from_template(template)  
    return model, prompt 

def process_financial_analysis(json_data, model, prompt):
    prompt_filled = prompt.format(json_data=json_data) 
    result = model.invoke(prompt_filled) 
    return result


def clean_data(df):
    df = df.drop_duplicates() 
    df = df.dropna()  
    return df


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
    model, prompt = initialize_model()  
    
    excel_file = "Mocks/preenchido.xlsx" 
    json_data = convert_excel_to_json(excel_file) 
    if json_data:
        print("JSON data converted successfully:")
        result = process_financial_analysis(json_data, model, prompt) 
        print("Financial Analysis:")
        print(result)  # Exibe o resultado
    else:
        print("Failed to convert Excel to JSON.")

if __name__ == "__main__":
    main()

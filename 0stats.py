import os
import re
import matplotlib.pyplot as plt
from statistics import mean

def main():
    folder = "results"  # Pasta onde estão os ficheiros
    # Dicionário para armazenar os erros para cada número de pontos (de 5 a 20)
    data = {i: [] for i in range(5, 21)}
    
    # Expressão regular para extrair os valores dos ficheiros
    pattern = re.compile(r"Usando (\d+) pontos de configuração: erro médio = ([\d\.]+) cm")
    
    # Processa todos os ficheiros da pasta
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = pattern.search(line)
                    if match:
                        config_points = int(match.group(1))
                        error_value = float(match.group(2))
                        if 5 <= config_points <= 20:
                            data[config_points].append(error_value)
    
    # Calcula a média dos erros para cada configuração
    x_values = list(range(5, 21))
    mean_values = [mean(data[k]) if data[k] else 0 for k in x_values]
    
    # Normalização min-max para eliminar o viés da escala (cm)
    min_val = min(mean_values)
    max_val = max(mean_values)
    normalized_values = [(val - min_val) / (max_val - min_val) for val in mean_values]
    
    # Cria o gráfico de barras com os valores normalizados
    plt.figure(figsize=(10, 6))
    plt.bar(x_values, normalized_values)
    plt.xlabel("Número de pontos de configuração")
    plt.ylabel("Erro normalizado")
    plt.title("Erro normalizado vs Número de pontos de configuração")
    plt.xticks(x_values)
    
    # Salva o gráfico como PNG
    plt.savefig("output_normalized.png")
    print("Gráfico salvo como 'output_normalized.png'.")

if __name__ == "__main__":
    main()

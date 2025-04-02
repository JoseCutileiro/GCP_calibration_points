import os
import re
import matplotlib.pyplot as plt
from statistics import mean

def main():
    folder = "results"  # Pasta onde estão os ficheiros
    # Dicionário para armazenar os erros normalizados de cada configuração, agregados de todos os ficheiros
    aggregated_data = {i: [] for i in range(5, 21)}
    
    # Expressão regular para extrair os valores dos ficheiros
    pattern = re.compile(r"Usando (\d+) pontos de configuração: erro médio = ([\d\.]+) cm")
    
    # Processa cada ficheiro separadamente
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            # Dicionário temporário para armazenar os erros deste ficheiro
            file_data = {}
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    match = pattern.search(line)
                    if match:
                        config_points = int(match.group(1))
                        error_value = float(match.group(2))
                        if 5 <= config_points <= 20:
                            file_data[config_points] = error_value
            # Se houver dados no ficheiro, normaliza-os usando min-max
            if file_data:
                valores = list(file_data.values())
                file_min = min(valores)
                file_max = max(valores)
                # Evita divisão por zero se todos os valores forem iguais
                if file_max == file_min:
                    normalized_file = {k: 0.5 for k in file_data.keys()}
                else:
                    normalized_file = {k: (v - file_min) / (file_max - file_min) for k, v in file_data.items()}
                # Agrega os valores normalizados no dicionário geral
                for config, norm_value in normalized_file.items():
                    aggregated_data[config].append(norm_value)
    
    # Calcula a média dos erros normalizados para cada configuração entre os ficheiros
    x_values = sorted(aggregated_data.keys())
    mean_normalized = [mean(aggregated_data[k]) if aggregated_data[k] else 0 for k in x_values]
    
    # Cria o gráfico de barras com os valores normalizados médios
    plt.figure(figsize=(10, 6))
    plt.bar(x_values, mean_normalized)
    plt.xlabel("Número de pontos de configuração")
    plt.ylabel("Erro normalizado")
    plt.title("Erro normalizado vs Número de pontos de configuração")
    plt.xticks(x_values)
    
    # Salva o gráfico como PNG
    plt.savefig("output_normalized.png")
    print("Gráfico salvo como 'output_normalized.png'.")

if __name__ == "__main__":
    main()

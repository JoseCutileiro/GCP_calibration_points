# TESTE MICHIGAN 
import cv2
import numpy as np
import math

# Listas globais para armazenar os pontos clicados (pixels)
config_points = []
test_points = []

def mouse_callback_config(event, x, y, flags, param):
    global config_points
    if event == cv2.EVENT_LBUTTONDOWN:
        config_points.append((x, y))
        print(f"Ponto Configuração {len(config_points)}: ({x}, {y})")

def mouse_callback_test(event, x, y, flags, param):
    global test_points
    if event == cv2.EVENT_LBUTTONDOWN:
        test_points.append((x, y))
        print(f"Ponto Teste {len(test_points)}: ({x}, {y})")

def parse_latlon(coord_str):
    """
    Converte uma string de coordenada no formato "41.940610°N 85.000736°W"
    para (lat, lon) em graus decimais.
    """
    coord_str = coord_str.strip().upper().replace('°', '')
    parts = coord_str.split()
    lat_str = parts[0]  # Ex: "41.940610N"
    lon_str = parts[1]  # Ex: "85.000736W"
    
    def parse_part(s):
        if s.endswith('N') or s.endswith('E'):
            return float(s[:-1])
        elif s.endswith('S') or s.endswith('W'):
            return -float(s[:-1])
        else:
            return float(s)
    
    lat = parse_part(lat_str)
    lon = parse_part(lon_str)
    return lat, lon

def latlon_to_xy(lat_deg, lon_deg, lat0_deg, lon0_deg):
    """
    Converte (lat, lon) em graus decimais para (X, Y) em metros usando
    uma projeção planar local centrada em (lat0, lon0).
    """
    R = 6371000.0  # Raio médio da Terra em metros
    lat = math.radians(lat_deg)
    lon = math.radians(lon_deg)
    lat0 = math.radians(lat0_deg)
    lon0 = math.radians(lon0_deg)
    X = R * (lon - lon0) * math.cos(lat0)
    Y = R * (lat - lat0)
    return X, Y

def main():
    # 1. Definir as coordenadas de Configuração e Teste (strings)
    config_coords_str = [
        "30.565206°N 104.083595°E",
        "30.565403°N 104.083449°E",
        "30.565391°N 104.083626°E",
        "30.565243°N 104.083402°E",
        "30.565005°N 104.083492°E",
        "30.565513°N 104.083556°E",
        "30.565294°N 104.083816°E",
        "30.565324°N 104.083251°E",
        "30.565461°N 104.083402°E",
        "30.565069°N 104.083711°E",
        "30.565458°N 104.083763°E",
        "30.565160°N 104.083304°E",
        "30.565495°N 104.083471°E",
        "30.565018°N 104.083625°E",
        "30.565415°N 104.083346°E",
        "30.565126°N 104.083803°E",
        "30.565492°N 104.083695°E",
        "30.565086°N 104.083354°E",
        "30.565392°N 104.083834°E",
        "30.565212°N 104.083272°E"
    ]
    test_coords_str = [
        "30.565212°N 104.083272°E",
        "30.565283°N 104.083692°E",
        "30.565282°N 104.083658°E",
        "30.565283°N 104.083629°E",
        "30.565289°N 104.083586°E",
        "30.565301°N 104.083547°E",
        "30.565305°N 104.083518°E",
        "30.565308°N 104.083492°E",
        "30.565305°N 104.083467°E",
        "30.565304°N 104.083445°E",
        "30.565312°N 104.083421°E",
        "30.565314°N 104.083402°E",
        "30.565309°N 104.083380°E",
        "30.565308°N 104.083368°E",
        "30.565318°N 104.083346°E"
    ]
    
    # 2. Converter as strings para (lat, lon)
    config_latlon = [parse_latlon(s) for s in config_coords_str]
    test_latlon   = [parse_latlon(s) for s in test_coords_str]

    # 3. Definir a referência: usamos a primeira coordenada de configuração
    lat0, lon0 = config_latlon[0]

    # 4. Converter para coordenadas locais (X, Y) em metros
    config_world = np.array([latlon_to_xy(lat, lon, lat0, lon0) for (lat, lon) in config_latlon], dtype=np.float32)
    test_world   = np.array([latlon_to_xy(lat, lon, lat0, lon0) for (lat, lon) in test_latlon], dtype=np.float32)

    # 5. Carregar a imagem (substitua "tes.png" pelo caminho da sua imagem)
    image_path = "imgs/CHENGDU.png"
    img = cv2.imread(image_path)
    if img is None:
        print("Erro ao carregar a imagem.")
        return

    # 6. Coletar 20 pontos de configuração (pixels) clicados pelo usuário
    cv2.namedWindow("Configuração: Clique 20 pontos (1 a 20)")
    cv2.setMouseCallback("Configuração: Clique 20 pontos (1 a 20)", mouse_callback_config)
    print("Clique 20 pontos de CONFIGURAÇÃO na imagem (em ordem):")
    while True:
        disp = img.copy()
        for pt in config_points:
            cv2.circle(disp, pt, 3, (0, 0, 255), -1)
        cv2.imshow("Configuração: Clique 20 pontos (1 a 20)", disp)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or len(config_points) >= 20:
            break
    cv2.destroyWindow("Configuração: Clique 20 pontos (1 a 20)")
    if len(config_points) != 20:
        print("Número incorreto de pontos de configuração. Encerrando.")
        return

    # 7. Coletar 15 pontos de teste (pixels) clicados pelo usuário
    cv2.namedWindow("Teste: Clique 15 pontos (T1 a T15)")
    cv2.setMouseCallback("Teste: Clique 15 pontos (T1 a T15)", mouse_callback_test)
    print("Clique 15 pontos de TESTE na imagem (em ordem):")
    while True:
        disp = img.copy()
        for pt in test_points:
            cv2.circle(disp, pt, 3, (255, 0, 0), -1)
        cv2.imshow("Teste: Clique 15 pontos (T1 a T15)", disp)
        key = cv2.waitKey(1) & 0xFF
        if key == 27 or len(test_points) >= 15:
            break
    cv2.destroyWindow("Teste: Clique 15 pontos (T1 a T15)")
    if len(test_points) != 15:
        print("Número incorreto de pontos de teste. Encerrando.")
        return

    # Converter os pontos clicados para arrays NumPy
    config_pixels = np.array(config_points, dtype=np.float32)
    test_pixels   = np.array(test_points, dtype=np.float32)

    # 8. Avaliar a homografia usando diferentes números de pontos de configuração (de 20 até 4)
    print("\nAvaliação da homografia:")
    for n in range(20, 3, -1):
        subset_pixels = config_pixels[:n]
        subset_world  = config_world[:n]
        H, status = cv2.findHomography(subset_pixels, subset_world, cv2.RANSAC, 5.0)
        if H is None:
            print(f"Falha ao calcular homografia com {n} pontos.")
            continue

        # Aplicar a homografia aos pontos de teste
        test_pixels_reshaped = test_pixels.reshape(-1, 1, 2)
        test_pred = cv2.perspectiveTransform(test_pixels_reshaped, H)
        test_pred = test_pred.reshape(-1, 2)

        # Calcular o erro (distância Euclidiana) entre os pontos previstos e os pontos de teste (em metros)
        errors = np.linalg.norm(test_pred - test_world, axis=1)
        mean_error = np.mean(errors)
        mean_error_cm = mean_error * 100.0
        print(f"Usando {n} pontos de configuração: erro médio = {mean_error_cm:.2f} cm")
        
        
    # 9. Avaliar a homografia usando diferentes números de pontos de configuração (de 20 até 4)
    print("\nAvaliação da homografia:")
    for n in range(20, 3, -1):
        subset_pixels = config_pixels[:n]
        subset_world  = config_world[:n]
        H, status = cv2.findHomography(subset_pixels, subset_world, cv2.RANSAC, 5.0)
        if H is None:
            print(f"Falha ao calcular homografia com {n} pontos.")
            continue

        # Aplicar a homografia aos pontos de teste
        test_pixels_reshaped = test_pixels.reshape(-1, 1, 2)
        test_pred = cv2.perspectiveTransform(test_pixels_reshaped, H)
        test_pred = test_pred.reshape(-1, 2)

        # Calcular o erro (distância Euclidiana) entre os pontos previstos e os pontos de teste (em metros)
        errors = np.linalg.norm(test_pred - test_world, axis=1)
        mean_error = np.mean(errors)
        std_error = np.std(errors)
        
        mean_error_cm = mean_error * 100.0
        std_error_cm = std_error * 100.0

        print(f"Usando {n:2d} pontos de configuração: erro médio = {mean_error_cm:.2f} cm | desvio padrão = {std_error_cm:.2f} cm")
        

if __name__ == "__main__":
    main()

import os
import OpenEXR
import Imath
import numpy as np
import matplotlib.pyplot as plt
import sys
def plot_2d_vectors(vectors):
    # 벡터 리스트에서 x와 y 좌표 분리
    x_coords, y_coords = zip(*vectors)
    
    # 그래프 생성
    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, color='blue', label='Points')
    
    # 원점에서 각 점까지 화살표 그리기
    # for x, y in vectors:
    #     plt.arrow(0, 0, x, y, head_width=0.05, head_length=0.1, fc='red', ec='red', alpha=0.5)
    
    # 그래프 설정
    plt.axhline(y=0, color='k', linestyle='--')
    plt.axvline(x=0, color='k', linestyle='--')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('2D Vectors')
    plt.grid(True)
    plt.legend()
    
    # 그래프 표시
    plt.show()


# 디렉토리 경로 설정
directory_path = "./viewmatrices"

vectors = []

if len(sys.argv) > 1:
    print(f"첫 번째 인자: {sys.argv[1]}")
    directory_path = sys.argv[1]
else :
    print("specify directory")
    exit()

# .exr 파일 필터링 및 정렬
exr_files = sorted([f for f in os.listdir(directory_path) if f.endswith(".exr")])

# 파일 처리 루프
for index, exr_file in enumerate(exr_files):
    file_path = os.path.join(directory_path, exr_file)
    print(f"Processing file {index + 1}: {exr_file}")

    # OpenEXR 파일 열기
    exr = OpenEXR.InputFile(file_path)

    # 헤더 정보 가져오기 (예: 해상도)
    header = exr.header()
    data_window = header['dataWindow']
    width = data_window.max.x - data_window.min.x + 1
    height = data_window.max.y - data_window.min.y + 1
    print(f"Resolution: {width}x{height}")

    # 채널 데이터 읽기 (예: R, G, B)
    pixel_type = Imath.PixelType(Imath.PixelType.FLOAT)  # 32-bit float 데이터 타입
    # red_channel = exr.channel('R', pixel_type)
    green_channel = exr.channel('G', pixel_type)
    # blue_channel = exr.channel('B', pixel_type)

    float_array = np.frombuffer(green_channel, dtype=np.float32)

    # 추가 처리 로직 삽입 가능
    print(f"Read channels: G({len(green_channel)} bytes)")
    print("x : %f , y : %f, scale : %f" % (float_array[232], float_array[233], float_array[234]) )

    vector = (float_array[232] *960*0.5, float_array[233] * 540*0.5)
    vectors.append(vector)
    # 파일 닫기
    exr.close()

plot_2d_vectors(vectors)

print("All files processed.")

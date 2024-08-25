import tensorflow as tf

def check_cpu():
    print(f"論理CPU数: {tf.config.experimental.list_physical_devices('CPU')}")

def check_gpu():
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        for gpu in gpus:
            print(f'GPUが利用可能です: {gpu.name}')
    else:
        print('GPUが利用できません')

def main():
    print('CPUをチェックしています...')
    check_cpu()

    print('\nGPUをチェックしています...')
    check_gpu()

if __name__ == '__main__':
    main()

# REQUIRED MODULES (Python 3.8):
#   -'ecdsa' v.0.15
#   -'dnspython' v.1.16.0
#   -'mysql-connector-python' v.8.0.19
from Generators.RandomBrute import multiprocess_brute


def main():
    # Generate random KeyPairs until a 'die' file is created inside project root.
    multiprocess_brute()


if __name__ == '__main__':
    main()

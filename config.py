import argparse
import logging

def get_args():
    parser = argparse.ArgumentParser(description='Image Archiver Service')
    parser.add_argument('-l', action='store_true', dest='lot', help='turn log on/off')
    parser.add_argument('--delay', default=0, type=int, help='delay between response in seconds')
    parser.add_argument('--path', default="photos", help='path to photos dir')
    args = parser.parse_args()
    return args

def get_logger():
        
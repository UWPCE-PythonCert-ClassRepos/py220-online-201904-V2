'''
3. HP Norton's picture search program
'''
import os
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def list_jpg_files(path):
    '''generate list of dirctory and files'''
    output = []
    png_files = []
    for root, dirs, files in os.walk(path):
        dirs.sort()
        files.sort()
        for file in files:
            if '.png' in file:
                #print(root, dirs)
                full_path = os.path.join(root)#, *dirs)
                if full_path not in output:
                    if png_files:
                        output.append(png_files)
                    png_files = []
                    output.append(full_path)
                png_files.append(file)
                #LOGGER.info('files are ', files)
    output.append(png_files)
    #print(output)
    return output

if __name__ == "__main__":
    PATH = '../data/'
    list_jpg_files(PATH)

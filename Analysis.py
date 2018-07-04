import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

input_file = './Test-Data/Odoo-Application/Logs/odoo.log'

def get_timestamp(message):
    print('capture-' + message[5:7] + '-' + message[8:10] + '-' + message[2:4] + '-' + message[11:13] + '-' + message[14:16])
    return 'capture-' + message[5:7] + '-' + message[8:10] + '-' + message[2:4] + '-' + message [11:13] + '-' + message[14:16]

def find_image(line):
    prefix = get_timestamp(line)
    return glob.glob('./screenshots/' + prefix + '*.*')

def show_image(file_path):
    img = mpimg.imread(file_path)
    imgplot = plt.imshow(img)
    plt.show()

key_words = ['message_post', 'name_create']

file_handle = open(input_file, 'r')
file_content = file_handle.readlines()

for line in file_content:
    if line.find(key_words[0]) > 0:
        print('Found ', line)
        found_file_list = find_image(line)
        if len(found_file_list) > 0:      
            show_image(found_file_list[0])
        else:
            print('No evidence (screenshot) found.\n')

file_handle.close()
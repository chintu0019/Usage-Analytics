import os
import pandas as pd
import glob
import sys

participant_list_file = "results/Participants.csv"

participants = pd.read_csv(participant_list_file, header = 0)

last_userID = participants['userID'].iloc[-1]

current_userID = last_userID + 1

try:
    user_dir = sys.argv[1]
    user_name = sys.argv[2]
    print("user directory="+user_dir)
    print("user name="+user_name)
except:
    print('Error: did not pass a valid user directory')

usage_data_file = user_name + "_usage_data.csv"
os.chdir(user_dir)
extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
#combine all files in the list
usage_data = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
usage_data.to_csv(usage_data_file, index=False, encoding='utf-8-sig')
agg_usage_data = pd.read_csv(usage_data_file)
agg_usage_data['userId'] = current_userID
agg_usage_data.to_csv(usage_data_file, index=False, encoding='utf-8-sig')
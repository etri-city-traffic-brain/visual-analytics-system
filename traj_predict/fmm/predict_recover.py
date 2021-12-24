import numpy as np
import pandas as pd
import json
from datetime import datetime
import time

edge_list = []
with open("./graph_ids_sf.txt" ,"r", encoding="utf-8") as txtFile:
# with open("./graph_ids_rome.txt" ,"r", encoding="utf-8") as txtFile:
  edge_string = txtFile.readline()
  
  edge_list = edge_string.split(",")
  
predicted = np.load("./sf_dcrnn_predictions.npz")["prediction"][-1].tolist()
# predicted = np.load("./rome_dcrnn_predictions.npz")["prediction"][-1].tolist()

original_traj_dict = {}
with open("./sf_traj_data_vis.json", "r", encoding="utf-8") as jsonFile:
# with open("./rome_traj_data_vis.json", "r", encoding="utf-8") as jsonFile:
  original_traj_dict = json.load(jsonFile)
  
timestamp_list = list(original_traj_dict.keys())[-len(predicted):]
print(len(timestamp_list), len(predicted))
print(len(edge_list), len(predicted[0]))

traj_dict = {}
for time_index in range(len(predicted)):
  traj_dict[timestamp_list[time_index]] = {}
  for edge_index in range(len(predicted[time_index])):
    traj_dict[timestamp_list[time_index]][edge_list[edge_index]] = int(predicted[time_index][edge_index])
    
with open("./sf_predicted_traj.json", "w", encoding="utf-8") as jsonFile:
# with open("./rome_predicted_traj.json", "w", encoding="utf-8") as jsonFile:
  json.dump(traj_dict, jsonFile, indent="  ")
  
compare_dict = {}
for timestamp in timestamp_list:
  compare_dict[timestamp] = {}
  for edge_id, value in original_traj_dict[timestamp].items():
    if edge_id not in edge_list:
      continue
    
    diff = np.abs(value - traj_dict[timestamp][edge_id])
    compare_dict[timestamp][edge_id] = int(10 - diff)
    print(diff, value, traj_dict[timestamp][edge_id], 10 - diff)
      
with open("./sf_compare_traj.json", "w", encoding="utf-8") as jsonFile:
# with open("./rome_compare_traj.json", "w", encoding="utf-8") as jsonFile:
  json.dump(compare_dict, jsonFile, indent="  ")
import os
import json
from datetime import datetime
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

timestamp_step = 3600

edge_shape = gpd.read_file("./network-new/edges.shp")
node_shape = gpd.read_file("./network-new/nodes.shp")

boundary_point = [(37.795991, -122.423938), (37.772554, -122.419046), (37.794024, -122.391366), (37.795991, -122.423938)]
# boundary_point = [(41.908846, 12.461709), (41.904440, 12.472631), (41.900566, 12.462322), (41.889093, 12.477530), (41.889853, 12.495086), (41.889929, 12.506212), (41.896159, 12.512643), (41.908011, 12.506110), (41.912113, 12.499169)]
polygon = Polygon(boundary_point)

node_connect_dict = {}
traj_dict = {}
exist_way_list = []
way_data_vis = {}

for index in edge_shape.index:
  edge_data = edge_shape.loc[index]
  
  origin_node_id = edge_data["u"]
  destination_node_id = edge_data["v"]

  origin_node_data = node_shape[node_shape["osmid"] == origin_node_id]
  destination_node_data = node_shape[node_shape["osmid"] == destination_node_id]
  
  if Point(origin_node_data["y"].tolist()[0],origin_node_data["x"].tolist()[0]).within(polygon) == False:
    continue
  if Point(destination_node_data["y"].tolist()[0],destination_node_data["x"].tolist()[0]).within(polygon) == False:
    continue

  if destination_node_id not in node_connect_dict.keys():
    node_connect_dict[destination_node_id] = []
  node_connect_dict[destination_node_id].append(edge_data["fid"])
  
  way_data_vis[int(edge_data["fid"])] = []
  for coord in list(edge_data["geometry"].coords):
    way_data_vis[int(edge_data["fid"])].append([float(coord[0]), float(coord[1])])
  
  exist_way_list.append(edge_data["fid"])

with open("./graph_ids_sf.txt", "w", encoding="utf-8") as txtFile:
# with open("./graph_ids_rome.txt", "w", encoding="utf-8") as txtFile:
  data_string = ""
  for way_id in exist_way_list:
    if data_string != "":
      data_string += ","
    data_string += str(way_id)

  txtFile.write(data_string)

with open("./sf_way_data_vis.json", "w", encoding="utf-8") as jsonFile:
# with open("./rome_way_data_vis.json", "w", encoding="utf-8") as jsonFile:
  json.dump(way_data_vis, jsonFile, indent="  ")

print("vaild edge count finish")

adj_data = []
for index in edge_shape.index:
  edge_data = edge_shape.loc[index]
  
  origin_node_id = edge_data["u"]
  
  if origin_node_id in node_connect_dict.keys():
    for target_edge_id in node_connect_dict[origin_node_id]:
      new_data = []
      new_data.append(edge_data["fid"])
      new_data.append(target_edge_id)
      new_data.append(int(edge_data["length"]))

      adj_data.append(new_data)

adj_df = pd.DataFrame(data=adj_data, columns=["from", "to", "cost"])
adj_df.to_csv("./distances_sf.csv", sep=",", na_rep="NaN", index=False)
# adj_df.to_csv("./distances_rome.csv", sep=",", na_rep="NaN", index=False)

print("dcrnn cost calculation finish")

traj_dict = {}
indexes_timestamp = []
indexes = []

path = "./path/"
file_list = os.listdir(path)
file_list_json = [file for file in file_list if file.endswith(".json")]

for file_name in file_list_json:
  traj_data = {}
  with open(path+file_name, "r", encoding="utf-8") as jsonFile:
    traj_data = json.load(jsonFile)
    
  for timestamp, traj_list in traj_data.items():
    for edge_id in traj_list:
      if timestamp not in traj_dict.keys():
        traj_dict[timestamp] = {}
        indexes_timestamp.append(timestamp)
      if edge_id not in traj_dict[timestamp].keys():
        traj_dict[timestamp][edge_id] = 0
      
      traj_dict[timestamp][edge_id] += 1
      
  print(file_name + " finished. (" + str(file_list_json.index(file_name) + 1) + "/" + str(len(file_list_json)) + ")")
  
indexes_timestamp.sort()
for timestamp in indexes_timestamp:
  indexes.append(datetime.fromtimestamp(int(timestamp)))
    
df_data = []
for timestamp in indexes_timestamp[int((len(indexes_timestamp) / 3) * 2):]:
# for timestamp in indexes_timestamp[318:]:
  new_data = []
  if str(timestamp) not in traj_dict.keys():
    for way_id in exist_way_list:
      new_data.append(0)
  else:
    for way_id in exist_way_list:
      if way_id in traj_dict[str(timestamp)].keys():
        new_data.append(traj_dict[str(timestamp)][way_id])
      else:
        new_data.append(0)
  df_data.append(new_data)
  print(str(timestamp) + " finished. (" + str(indexes_timestamp.index(timestamp) + 1) + "/" + str(len(indexes_timestamp)) + ")")

df = pd.DataFrame(data=df_data, columns=exist_way_list, index=indexes[int((len(indexes_timestamp) / 3) * 2):])
# df = pd.DataFrame(data=df_data, columns=exist_way_list, index=indexes[318:])

# modded_df_data = []
# modded_df_data.extend(df_data)
# for repeat in range(100):
#   modded_df_data.extend(df_data)
  
# index_diff = len(modded_df_data) - len(df_data)
# modded_indexes = []
# modded_indexes.extend(indexes[int(len(indexes_timestamp) / 3) * 2:-1])
# for repeat in range(index_diff):
#   result_timestamp = int(indexes_timestamp[-1]) + (3600 * (repeat + 1))
#   modded_indexes.append(datetime.fromtimestamp(int(result_timestamp)))
  
# print(len(modded_df_data), len(modded_indexes))

# df = pd.DataFrame(data=modded_df_data, columns=exist_way_list, index=modded_indexes)
df.to_csv("./dcrnn_df.csv", sep=",", na_rep="NaN")

store = pd.HDFStore('./SanFrancisco.h5')
# store = pd.HDFStore('./Rome.h5')
store.put('d1', df)
store.close()

with open("./sf_traj_data_vis.json", "w", encoding="utf-8") as jsonFile:
# with open("./rome_traj_data_vis.json", "w", encoding="utf-8") as jsonFile:
  json.dump(traj_dict, jsonFile, indent="  ")

print("node count", len(exist_way_list))
print("data length", len(df_data))
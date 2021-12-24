import json
import os
import pandas as pd

timestamp_step = 3600

def WKT_write(point_list, file_name="wkt"):
  wkt = "LineString("
  for index in range(len(point_list)):
    point = point_list[index]
    wkt += str(point[0]) + " " + str(point[1])
    if index != len(point_list) - 1:
      wkt += ","
  wkt += ")"

  with open("./wkt/"+file_name+".txt" ,"w", encoding="utf-8") as f:
    f.write(wkt)

# if not os.path.isfile("./sf_gps_point.csv"):
#   file_list = os.listdir("./SanFrancisco")
#   file_list_json = [file for file in file_list if file.endswith(".json")]

#   vehicle_dict = {}
#   vid_index = 0
#   df = pd.DataFrame(columns=["id", "x", "y", "timestamp"])

#   for file_name in file_list_json:
#     with open("./SanFrancisco/"+file_name, "r", encoding="utf-8") as jsonFile:
#       raw_data = json.load(jsonFile)
#       vid = raw_data[0]
#       if vid not in  vehicle_dict.keys():
#         vid_index += 1
#         vehicle_dict[vid] = vid_index

#       for data in raw_data[1]:
#         new_data = {}
#         new_data["id"] = vehicle_dict[vid]
#         new_data["x"] = data["coordinate"][0]
#         new_data["y"] = data["coordinate"][1]
#         new_data["timestamp"] = data["time"]

#         df = df.append(new_data, ignore_index=True)

#     print(file_name + " finished. (" + str(file_list_json.index(file_name)) + "/" + str(len(file_list_json)) + ")")
        
#   df = df.astype({"id":int, "timestamp":int})
#   df=df.sort_values(by=['id','timestamp'])
#   df.to_csv("./sf_gps_point.csv", sep=";", index=False)
#   with open("./sf_vehicle_dict.json", "w", encoding="utf-8") as jsonFile:
#     json.dump(vehicle_dict, jsonFile)
# else:
df = pd.read_csv("./sf_gps_point.csv", sep=";")
with open("./sf_vehicle_dict.json", "r", encoding="utf-8") as jsonFile:
  vehicle_dict = json.load(jsonFile)

point_overall_data = {}
for vindex in vehicle_dict.values():
  target_df = df[df["id"] == int(vindex)]

  point_dict = {}
  point_list = []
  current_timestamp = 0
  for index, data in target_df.iterrows():
    if current_timestamp == 0:
      current_timestamp = int(data["timestamp"]) - (int(data["timestamp"]) % timestamp_step)
    if current_timestamp + timestamp_step < int(data["timestamp"]):
      WKT_write(point_list, str(vindex)+"_"+str(current_timestamp))
      if str(current_timestamp) not in point_dict:
        point_dict[str(current_timestamp)] = []
      if str(current_timestamp) not in point_overall_data:
        point_overall_data[str(current_timestamp)] = []
        
      point_dict[str(current_timestamp)].extend(point_list)
      new_gps_overall = {}
      new_gps_overall["vid"] = vindex
      new_gps_overall["count"] = len(point_list)
      point_overall_data[str(current_timestamp)].append(new_gps_overall)
      
      current_timestamp = current_timestamp + timestamp_step
      point_list.clear()

    point_list.append([data['x'], data['y']])

  if len(point_list) > 0:
    WKT_write(point_list, str(vindex)+"_"+str(current_timestamp))
    if str(current_timestamp) not in point_dict:
      point_dict[str(current_timestamp)] = []
    if str(current_timestamp) not in point_overall_data:
      point_overall_data[str(current_timestamp)] = []
      
    point_dict[str(current_timestamp)].extend(point_list)
    new_gps_overall = {}
    new_gps_overall["vid"] = vindex
    new_gps_overall["count"] = len(point_list)
    point_overall_data[str(current_timestamp)].append(new_gps_overall)
    
  with open("./vis/gps/gps_data_vis" + str(vindex) + ".json", "w", encoding="utf-8") as jsonFile:
    json.dump(point_dict, jsonFile, indent="  ")
    
  print(str(vindex) + " finished")
  
with open("./gps_data_overall.json", "w", encoding="utf-8") as jsonFile:
  json.dump(point_overall_data, jsonFile, indent="  ")
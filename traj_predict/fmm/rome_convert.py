import pandas as pd
import os
from datetime import datetime
import time
import json

# path = "./rome_tmp/"
# file_list = os.listdir(path)
# file_list_csv = [file for file in file_list if file.endswith(".csv")]

# df = pd.DataFrame()

# for file_name in file_list_csv:
#   tmp_df = pd.read_csv(path+file_name, sep=",")
#   tmp_dict = {"id": [], "timestamp":[], "x": [], "y": []}
#   for index in tmp_df.index:
#     target_row = tmp_df.loc[index].to_dict()
#     timestring = target_row["datetime"][:19]
#     timetuple = datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S").timetuple()
#     timestamp = int(time.mktime(timetuple))
#     tmp_dict["id"].append(target_row["id"])
#     tmp_dict["timestamp"].append(timestamp)
#     tmp_dict["x"].append(target_row["gps_long"])
#     tmp_dict["y"].append(target_row["gps_lat"])
#     # df = df.append(tmp_dict, ignore_index=True)
    
#   mod_df = pd.DataFrame.from_dict(tmp_dict)
#   mod_df = mod_df.astype({"id":int, "timestamp":int})
#   df = pd.concat([df, mod_df])
    
#   print(file_name + " finished. (" + str(file_list_csv.index(file_name)) + "/" + str(len(file_list_csv)) + ")")

# df = df.reset_index()
# df = df.sort_values(by=['id','timestamp'])

df = pd.read_csv("./rome_gps_point.csv", sep=";")

# df = df.drop(columns=["index"])

# print(df)

# df.to_csv("./rome_gps_point.csv", sep=";", index=False)

vehicle_dict = {}
for id in df["id"].unique().tolist():
  vehicle_dict[id] = id

with open("./rome_vehicle_dict.json", "w", encoding="utf-8") as jsonFile:
  json.dump(vehicle_dict, jsonFile, indent="  ")
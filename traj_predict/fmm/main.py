from fmm import FastMapMatch,Network,NetworkGraph,UBODTGenAlgorithm,UBODT,FastMapMatchConfig

### Read network data
network = Network("./network-new/edges.shp","fid","u","v")
print("Nodes {} edges {}".format(network.get_node_count(),network.get_edge_count()))
graph = NetworkGraph(network)

### Precompute an UBODT table

# Can be skipped if you already generated an ubodt file
# ubodt_gen = UBODTGenAlgorithm(network,graph)
# status = ubodt_gen.generate_ubodt("./network-new/ubodt.txt", 0.02, binary=False, use_omp=True)
# print(status)

### Read UBODT

ubodt = UBODT.read_ubodt_csv("./network-new/ubodt.txt")

### Create FMM model
model = FastMapMatch(network,graph,ubodt)
### Define map matching configurations

k = 8
radius = 0.003
gps_error = 0.0005
fmm_config = FastMapMatchConfig(k,radius,gps_error)

### Run map matching for wkt
wkt = ""
with open("./point.txt" ,"r", encoding="utf-8") as f:
  wkt = f.readline()
result = model.match_wkt(wkt,fmm_config)
### Print map matching result
print("Opath ",list(result.opath))
print("Cpath ",list(result.cpath))
print("WKT ",result.mgeom.export_wkt())
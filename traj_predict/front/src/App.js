import React, { useState, useEffect } from 'react';
import DeckGL from '@deck.gl/react';
import {IconLayer, LineLayer} from '@deck.gl/layers';
import {StaticMap} from 'react-map-gl';
import axios from "axios";

import Slider from '@material-ui/core/Slider'

const MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoicGx1bWU3ZWF0IiwiYSI6ImNram14aGE2azA3aW4yd3AweGFtaDZ4N2sifQ.Kuet88B9HRdse4ACOyooDQ';

const INITIAL_VIEW_STATE = {
  longitude: 12.493207,
  latitude: 41.904535,
  zoom: 14,
  pitch: 0,
  bearing: 0
};

const ICON_MAPPING = {
  marker: {x: 0, y: 0, width: 128, height: 128, mask: true}
};

function App({data}) {
  const [way_data, setWay_data] = useState({})
  const [gps_data, setGps_data] = useState([])
  const [aggregate_data, setAggregate_data] = useState([]);
  const [prediction_data, setPrediction_data] = useState([]);
  const [compare_data, setCompare_data] = useState([]);
  const [display_data, setDisplay_data] = useState("agg_radio")
  const [current_time, setCurrenet_time] = useState(0);
  const [max_time, setMax_time] = useState(0);
  const [layers,setLayers] = useState([])

  useEffect(() => {
    loadData();
  },[]);

  useEffect(() => {
    axios.get('./agg.json')
    .then((data)=>{
      const data_list = []
      const time_list = []
      for (let time_val in data.data) {
        time_list.push(time_val)
      }
      time_list.sort()
      console.log(time_list)
      for (let time_val of time_list) {
        const new_time = {}
        new_time["time"] = time_val
        new_time["data"] = []
        for (let way_id in data.data[time_val]) {
          const new_data = {}
          if (way_id in way_data) {
            let coord_list = way_data[way_id]
            for (let i = 0; i < coord_list.length - 1; i++) {
              new_data["id"] = way_id
              new_data["time"] = time_val
              new_data["count"] = data.data[time_val][way_id]
              new_data["from"] = coord_list[i]
              new_data["to"] = coord_list[i+1]
              new_time["data"].push(new_data)
            }
          }
        }
        data_list.push(new_time)
      }
      setMax_time(data_list.length)
      setAggregate_data(data_list)
      console.log(data_list)
      console.log(data_list.length)
    });

    axios.get('./pred.json')
    .then((data)=>{
      const data_list = []
      const time_list = []
      for (let time_val in data.data) {
        time_list.push(time_val)
      }
      time_list.sort()
      console.log(time_list)
      for (let time_val of time_list) {
        const new_time = {}
        new_time["time"] = time_val
        new_time["data"] = []
        for (let way_id in data.data[time_val]) {
          const new_data = {}
          if (way_id in way_data) {
            let coord_list = way_data[way_id]
            for (let i = 0; i < coord_list.length - 1; i++) {
              new_data["id"] = way_id
              new_data["time"] = time_val
              new_data["count"] = data.data[time_val][way_id]
              new_data["from"] = coord_list[i]
              new_data["to"] = coord_list[i+1]
              new_time["data"].push(new_data)
            }
          }
        }
        data_list.push(new_time)
      }
      setPrediction_data(data_list)
    });
  }, [way_data])

  const OnTimeChanged = (event, newValue) => {
    setCurrenet_time(newValue)
  }

  const loadData = () => {
    const way_dict = {}
    const gps_list = []
    axios.get('./way.json')
    .then((data)=>{
      for (let way_id in data.data) {
        way_dict[String(way_id)] = data.data[way_id]
      }  
      setWay_data(way_dict)
    });

    axios.get('./gps.json')
    .then((data)=>{
      for (let timestamp in data.data) {
        const new_time = {}
        new_time["time"] = timestamp
        new_time["data"] = []
        for (let index in data.data[timestamp]) {
          const new_data = {}
          new_data["coord"] = data.data[timestamp][index]
          new_time["data"].push(new_data)
        }
        gps_list.push(new_time)
      }

      console.log(gps_list)
      setGps_data(gps_list)
    });
  }

  useEffect(() => {
    const target_agg_data = []
    if (display_data == "agg_radio") {
      if (aggregate_data.length != 0) {
        target_agg_data.push(...aggregate_data[current_time]["data"])
      }
    }
    else if (display_data == "pred_radio") {
      if (prediction_data.length != 0) {
        target_agg_data.push(...prediction_data[current_time]["data"])
      }
    }
    const target_gps_data = []
    if (gps_data.length != 0) {
      console.log(gps_data[current_time])
      // target_gps_data.push(...gps_data[current_time]["data"])
    }
    console.log(current_time, target_agg_data, target_gps_data)
    setLayers([
      // new IconLayer({
      //   id: 'icon-layer',
      //   data: gps_data,
      //   pickable: true,
      //   // iconAtlas and iconMapping are required
      //   // getIcon: return a string
      //   iconAtlas: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/icon-atlas.png',
      //   iconMapping: ICON_MAPPING,
      //   getIcon: d => 'marker',
      //   sizeScale: 15,
      //   getPosition: d => d.coord,
      //   getSize: d => 2
      // }),
      new LineLayer({
        id: 'line-layer',
        data: target_agg_data,
        pickable: true,
        getWidth: 20,
        getSourcePosition: d => d.from,
        getTargetPosition: d => d.to,
        getColor: d => {
          if (display_data == "agg_radio")
            return [255, (5 - (Math.min(d.count, 5))) * 50, (5 - (Math.min(d.count, 5))) * 50]
          else if (display_data == "pred_radio")
            return [255, (5 - (Math.min(d.count, 5))) * 50, (5 - (Math.min(d.count, 5))) * 50]
        }
        // getColor: d => [255, 0,0]
      }),
      // new LineLayer({
      //   id: 'line-layer',
      //   data: traj_data,
      //   pickable: true,
      //   getWidth: 5,
      //   getSourcePosition: d => d.from,
      //   getTargetPosition: d => d.to,
      //   getColor: d => {
      //     if (d.count == 0) return [255,255,255]
      //     else {
      //       return [255, (100 - (Math.min(d.count * 10, 100))) * 2, (100 - (Math.min(d.count * 10, 100))) * 2]
      //     }
      //   }
      // })
    ])
  }, [current_time, display_data])

  const OnSelectType = (type) => {
    if (type == "agg_radio") {
      setCurrenet_time(current_time + (aggregate_data.length - prediction_data.length))
      setMax_time(aggregate_data.length)
    }
    else if (type == "pred_radio") {
      if (display_data == "agg_radio") {
        if (current_time < aggregate_data.length - prediction_data.length) {
          setCurrenet_time(0)
        }
        else {
          setCurrenet_time(current_time - (aggregate_data.length - prediction_data.length))
        }
      }
      setMax_time(prediction_data.length)
    }
    
    setDisplay_data(type)
  }
  
  return (
    <div>
      <div>
        <DeckGL
          initialViewState={INITIAL_VIEW_STATE}
          controller={true}
          layers={layers}
          style={{"bottom":"0"}}
        >
          <StaticMap mapboxApiAccessToken={MAPBOX_ACCESS_TOKEN} />
        </DeckGL>
      </div>
      <div style={{"position":"relative"}}>
        <div>
          <Slider
            valueLabelDisplay="auto"
            step={1}
            marks
            min={0}
            max={max_time+1}
            value={current_time}
            onChange={OnTimeChanged}
          />
        </div>
        <div>
          <input type="radio" id="agg_radio" checked={display_data == "agg_radio"} onClick={() => {OnSelectType("agg_radio")}}/>
          <input type="radio" id="pred_radio" checked={display_data == "pred_radio"} onClick={() => {OnSelectType("pred_radio")}}/>
        </div>
      </div>
    </div>
  );
}

export default App;

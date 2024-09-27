import Map from './map.js';
import React, { Component } from 'react';
import Button from 'react-bootstrap/Button';

import { createCrimeMarker } from '../crime-marker';

import styled from 'styled-components';

const MapKit = styled.div`
    width: 100%;
    @media all and (min-width: 800px) {
        width: 50%;
    }

    height: calc(100vh - 56px);
    position: absolute;
`

const crimeCategories = {
    "weapon": "severe",
    "assault": "severe",
    "burg": "severe",
    "theft": "severe",
    "dui": "severe",
    "graffiti": "severe",
    "vandalism": "severe",
    "sex": "severe",
    "loitering": "medium",
    "alcohol": "medium",
    "suspicious": "medium",
    "disorderly": "medium",
    "trespassing": "medium",
    "alarm": "info",
    "noise": "info",
    "animal": "info",
    "keep": "info",
    "deceased": "info",
    "towed": "info",
    "citizen": "info",
    "public": "info",
    "found": "info",
    "lost": "info",
    "assist": "info",
    "parking": "info",
    "traffic": "info",
    "welfare": "info",
    "aband": "info",
    "muni": "info",
    "coll": "info", // Collision
    "9": "info",
}

export default class AppleMap extends Component {
    constructor(props) {
        super(props);
        const self = this;
        this.state = {
            markers: [],
            filters: {},
            coloring: null,
            markerColoring: 'none',
            self: self,
        };

        this.map = null;
        this.mapKitDiv = React.createRef();
    }

    componentDidMount() {
        this.initMap();
        this.addMarkers();
    }

    color(coloring) {
        if (coloring == 'type') {
            this.colorMarkersByType();
        } else {
            this.colorMarkersBySeverity();
        }
    }

    render() {
        if (this.state.crimeMarkers) {
            this.state.coloring(this.state.crimeMarkers);
        }
        return <MapKit id="mapKit" ref={this.mapKitDiv}></MapKit>

    }

    colorMarkersBySeverity() {
        const items = this.state.markers;

        const severityToColor = {
            "severe": "#dc3545",
            "medium": "#ffcc00",
            "info": "#007bff",
        };

        items.forEach(item => {
            const {entry, marker} = item;
            const severity = entry.type in crimeCategories ? crimeCategories[entry.type] : "info";
            marker.color = severityToColor[severity];
        });
    }

    assignTypeColors(markerGroups) {
        // Keeps the type and color matched, so it is consistent
        const typeColorMappings = {
            'noise': "#ffcc00"
        };

        let colors = ["#ff3b30", "#ff9500", "#4cd964", "#5ac8fa", "#007aff", "#5856d6", "#ff2d55"];

        var colorIndex = 0;
        let assignColor = entry => {
            const [groupName, group] = entry

            let color;
            if (groupName in typeColorMappings) {
                color = typeColorMappings[groupName];
            } else {
                color = colors[colorIndex];
                colorIndex++;
            }

            group.forEach(item => {
                item.marker.color = color;
            })

            if (colorIndex == colors.length) {
                colorIndex = 0;
            }
        }

        Object.entries(markerGroups).forEach(assignColor);
    }

    colorMarkersByType() {
        const markers = this.state.markers;
        var typeGroups = markers.reduce(function(accumulator, current) {
            const type = current.entry.type.toLowerCase()
            if (current.entry.type in accumulator) {
                accumulator[type].push(current)
            } else {
                accumulator[type] = [current]
            }

            return accumulator;
        }, {});

        this.assignTypeColors(typeGroups);
    }

    addMarkers() {
        let createMarkers = (responseJson) => {
            const crimeMarkers = responseJson.map(createCrimeMarker).filter(i => !!i);
            this.setState({
                'markers': crimeMarkers,
            });

            this.map.addAnnotations(crimeMarkers.map(markers => markers.marker));
        }

        fetch(__API_ROOT__  + '/entries?days=5').then(function(response) {
            return response.json();
        }).then(createMarkers);
    }

    initMap() {
        mapkit.init({
            authorizationCallback: function(done) {
                const xhr = new XMLHttpRequest();
                xhr.open("GET", __API_ROOT__ + "/services/jwt");
                xhr.addEventListener("load", function() {
                    done(this.responseText);
                });
                xhr.send();
            }
        });

        mapkit.addEventListener("error", function(event) {
            switch (event.status) {
            case "Unauthorized":
                console.log("Map token unauthorized", event);
                break;
            }
        });

        var SLO = new mapkit.CoordinateRegion(
            new mapkit.Coordinate(35.2827524, -120.6596156),
            new mapkit.CoordinateSpan(0.167647972, 0.354985255)
        );

        var map = new mapkit.Map(this.mapKitDiv.current);
        map.region = SLO;

        this.map = map;
        return map;
    }
}

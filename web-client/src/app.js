import React from "react";
import './full-page.css';

import Header from './header/header';
import AppleMap from './map/apple-map';
import SideBar from './sidebar/sidebar';

import { grommet, Grommet } from 'grommet'

import './report-info.css';
import './map.css';
import './full-page.css';

import styled from  'styled-components';

const AppContainer = styled.div``
const MapContainer = styled.div``

const crimeMapTheme = grommet

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            'markerColoring': 'severity',
        };

        this.mapRef = React.createRef();
    }

    setMarkerColoring(coloring, e) {
        if (coloring != this.state.markerColoring) {
            this.setState({
                'markerColoring': coloring,
            });

            this.mapRef.current.color(coloring);
        }
    }

    render() {
        return <Grommet theme={crimeMapTheme}>
            <AppContainer>
                <Header color={AppleMap.color} setMarkerColoring={this.setMarkerColoring.bind(this)} />
                <MapContainer>
                    <AppleMap ref={this.mapRef} markerColoring={this.state.markerColoring}/>
                    <SideBar></SideBar>
                </MapContainer>
            </AppContainer>
        </Grommet>
    }
}
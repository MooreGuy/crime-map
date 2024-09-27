import React, { Component } from 'react';
import Navbar from 'react-bootstrap/Navbar';

import Nav from 'react-bootstrap/Nav';
import Button from 'react-bootstrap/Button';
import ToggleButton from 'react-bootstrap/ToggleButton';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';


import styled from 'styled-components';

const StyledBG = styled(ToggleButtonGroup)`
    margin: 0 20px 0 40px;
`

const ColoringButton = styled(Button)`
    &.selected {
        color: #0056b3;
    }
`

const LocationForm = styled.form`
    display: fixed;
`

const LocationDropdown = styled.div`
    color: red;
    width: 20rem;
    height: 50px;
    border: 2px solid #aaa;
    background: white;
    position: absolute;
    /* top: -100px;*/
`
export default class Header extends Component {
    constructor(props) {
        super(props);

        this.state = {
            coloring: 'none'
        }
    }

    setColoring(coloring) {
        this.setState({'coloring': coloring})
        this.props.setMarkerColoring(coloring)
    }


    render() {
        return <Navbar bg="light" expand="sm">
        <Navbar.Brand href="#home">Crime Map</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="mr-auto">
                {/*<Nav.Link href="#home">Home</Nav.Link>*/}

                <StyledBG type="radio" name="options">
                    <ToggleButton value="type" onClick={() => this.setColoring('type')} >Type</ToggleButton>
                    <ToggleButton value="severity" onClick={() => this.setColoring('severity')} >Severity</ToggleButton>
                </StyledBG>
            </Nav>
        </Navbar.Collapse>
        </Navbar>;
    }
}
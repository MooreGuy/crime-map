import React, { Component } from 'react';
import styled from 'styled-components';

import FontAwesome from 'react-fontawesome';

import Button from 'react-bootstrap/Button';
import AlertTypeSelect from './alert-type-select'
import SeverityFilter from './severity-filter';
import LocationFilter from './location-filter';


const Input = styled.input`
    border: none;

    &:focus {
        border-bottom: 1px solid black;
    }

    color: #555;
    background: #f8f9fa;

    margin-bottom: 10px;
    font-size: 24px;
`

const EditControls = styled.div`
    justify-content: flex-end;
    display: flex;

    .saveButton {
        margin: 10px;
    }

`

const StyledAlert = styled.div`
    &.editing {
        /* border-color: blue; */
        /* position: absolute; */
        width: 820px;
        height: 400px;
    }

    transition: height .1s, width .1s linear;
    color: #555;
    margin: 10px 20px 10px 0;
    padding: 20px 20px 0 20px;
    border: 2px solid #eee;
    background: #f8f9fa;
    /* top: -100px;*/
    box-shadow: 2px 2px 4px #eee;

    min-height: 140px;
    width: 400px;

    display: flex;
    flex-direction: column;
    justify-content: space-around;

    p {
        color: #888;
    }

`

export default class Alert extends Component {
    constructor(props) {
        super(props)

        this.state = {
            editing: this.props.new == true,
            saving: false,
            id: this.props.id,
            time: this.props.time,
            name: this.props.name,
            type: this.props.type,
            // TODO: Implement radius management
            radius: 1,
            new: this.props.new,
            location: this.props.location,
        }

        this.onChange = this.onChange.bind(this)
        this.createAlert = this.createAlert.bind(this)
        this.deleteAlert = this.deleteAlert.bind(this)
        this.setEditing = this.setEditing.bind(this)
        this.updateLocation = (location) => {
            this.setState({
                location: location,
            })
        }
    }


    getLocation() {
        let options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0
         };

         return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, options);
         })
    }

    sendWatchRequest(crd) {
        this.setState({
            lat: crd.latitude,
            lng: crd.longitude,
            accuracy: crd.accuracy,
        })

        return fetch(`${__API_ROOT__}/alert`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(this.state),
        })
    }

    // TODO Show error message when failed request.
    createAlert() {
        this.setState({saving: true})
        this.getLocation().then((pos) => {
            const crd = pos.coords;
            return crd
        }).then(this.sendWatchRequest.bind(this)).then(res => res.json())
            .then((data) => {
                if (this.state.new) {
                    this.props.saveHandler(data.id)
                }

                this.setState({
                    id: data.id,
                    saving: false,
                    editing: false,
                    new: false,
                })
        }).catch((err) => {
            console.warn(`ERROR(${err.code}): ${err.message}`);
            this.setState({
                saving: false,
            })

            throw err
        })
    }

    deleteAlert() {
        console.log(this.state.new)
        if (this.state.new) {
            this.props.deleteSelf(this.state.id)
        } else {
            console.log("Delete request")
            fetch(`${__API_ROOT__}/alert/${this.state.id}`, {
                method: 'DELETE',
            }).then(resp => { resp.json() }).then((data) => {
                console.log("Done deleting")
                this.props.deleteSelf(this.state.id)
            })
        }
    }

    setEditing() {
        this.setState({
            'editing': true
        })
    }

    onChange(e) {
        this.setState({
            'name': e.currentTarget.value
        })
    }

    render() {
        let timeEl, descriptionEl
        if (this.props.time) {
           timeEl = <p>spotted around {this.props.time}</p>
           descriptionEl = <p>Event sighted</p>
        } else if (this.props.type == 'alert') {
           descriptionEl = <p>Persistent alert</p>
        } else {
           descriptionEl = <p>Event</p>
        }

        if (this.state.editing) {
            descriptionEl = <div>
                <SeverityFilter/>
                <LocationFilter update={this.updateLocation} value={this.state.location}/>
            </div>
        }


        let saveButton, deleteButton = ""
        if (this.state.editing == true) {
            saveButton = <Button disabled={this.state.saving} className="saveButton"
                onClick={this.state.saving ? null : this.createAlert} variant="primary">Save</Button>
            deleteButton = <Button disabled={this.state.saving}
                onClick={this.state.saving ? null : this.deleteAlert} variant="outline-danger"
                className="saveButton">Delete</Button>
        }

        // TODO: Loading spinner!
        /*<FontAwesome className='super-crazy-colors' name='rocket' size='2x' spin style={{ textShadow: '0 1px 0 rgba(0, 0, 0, 0.1)' }}/>*/
            /*<FontAwesome name='trash' size='10px' style={{ 'align-self': 'flex-end' }} />*/
        return <StyledAlert onClick={this.setEditing.bind(this)} className={this.state.editing ? "editing" : ""}>
            <Input onChange={this.onChange} type="text" value={this.state.name}></Input>
            {descriptionEl}
            {timeEl}


            <EditControls>
                {deleteButton}
                {saveButton}
            </EditControls>
        </StyledAlert>
    }
}
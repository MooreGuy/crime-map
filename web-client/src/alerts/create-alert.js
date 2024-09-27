import React, { Component} from 'react';

import Button from 'react-bootstrap/Button';

import styled from 'styled-components'

const StyledButton = styled(Button)`
    display: inline-block;
`

export default class CreateAlert extends Component {

    render() {
        return <StyledButton onClick={this.props.onSubmit} variant="light">Create Alert</StyledButton>
    }
}
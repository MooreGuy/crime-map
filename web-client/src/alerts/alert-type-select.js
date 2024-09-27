import React from 'react';
import { Select } from 'grommet';

// const AlertTypeSelect = styled.input``
export default function AlertTypeSelect(props) {
    const [value, setValue] = React.useState(props.options[0]);
    return (
        <Select
        options={props.options}
        value={value}
        onChange={({ option }) => setValue(option)}
        />
    );
}


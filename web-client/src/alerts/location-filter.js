import React from 'react';
import { TextInput } from 'grommet'
export default function LocationFilter(props) {
    const [value, setValue] = React.useState(props.value);
    const suggestions = [
        //"Current Location",
        "San Luis Obispo",
    ]

    const save = (event) => {
        props.update(event.target.value);
        return setValue(event.target.value)
    }

    return (
      <TextInput
        placeholder="Choose a location"
        value={value}
        onChange={save}
        suggestions={suggestions}
      />
    );
  }
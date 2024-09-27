import React from 'react';
import { RangeSelector, Box, Stack, Text } from 'grommet';
import styled from 'styled-components'

const StyledStack = styled(Stack)`
    margin: 40px;
`

export default function SeverityFilter(props) {
    const begin = props.begin ? props.begin : 1
    const end = props.end ? props.end : 2
    const [values, setValues] = React.useState([begin, end]);
    return (
        <StyledStack>
            <Box direction="row" justify="between">
            {['Info', 'Medium', 'Severe'].map(value => (
                <Box key={value} pad="small" border={false}>
                <Text style={{ fontFamily: 'monospace' }}>
                    {value}
                </Text>
                </Box>
            ))}
            </Box>
            <RangeSelector
            direction="horizontal"
            invert={false}
            min={0}
            max={2}
            size="full"
            round="small"
            values={values}
            onChange={values => setValues(values)}
            />
        </StyledStack>
    );
}
import React from 'react'
import { Box } from 'grommet'

export default function RecentEvents(props) {
    const events = [
        {
            'id': 123,
            'type': 'Assault',
        }
    ]
    const eventEls = events.map((event) => {
        return <div><h4>{event.type}</h4></div>
    })
    return <Box>
        {eventEls}
    </Box>
}
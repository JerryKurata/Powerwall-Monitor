# PowerWall-Monitor

## Purpose: Implement an application that:
    - On defined intervals poll a Tesla Powerwall gateway to get the current state of information on the Gateway.
    - Logs this information to a database
    - Reads information from the database to provide:
        - report/graphs on past performance
        - extract data for ML Model building, past and predictive

## Workflow
    - Poll gateway
    - For each poll
        - Generate unique polling sequence key (timestamp)
        - call a series of APIs for various status information
        - process the json returned from the API
        - store the json or information derived from the json to a database
    - Reporting/Extract 
        - Extract from database based on criteria
        - Output information desired format
    - Sleep until next polling time

## Architecture
    - Store data in database    
        - flatten json and save data to tables
    - Have a series of objects that can be be populated with information from polls
    - Create objects from database tables 
        - Optionally use Poll ID to gather data for a poll event.

## Database
    - For API return store:
        - Poll ID (timestamp)
        - API called
        - Return json string

    
## Design consideration
    - Speed of polling is more critical than reporting speed

import React from 'react';
import {MDBDataTable} from 'mdbreact';

const EventTable = (rows) => {
  const add_button = (id) => <button className="btn btn-primary" value={id}
                                     onClick={() => console.log(id)}>View</button>

  const buttons = document.getElementsByClassName('table-button');
  const data = {
    columns: [
      {
        label: 'Event ID',
        field: 'event_id',
        sort: 'asc',
        width: 150
      },
      {
        label: 'Chatroom ID',
        field: 'chatroom_id',
        sort: 'asc',
        width: 270
      },
      {
        label: 'Event Name',
        field: 'event_name',
        sort: 'asc',
        width: 200
      },
      {
        label: 'Host Name',
        field: 'host_name',
        sort: 'asc',
        width: 100
      }, {
        label: 'Host Email',
        field: 'host_email',
        sort: 'asc',
        width: 100
      },
      {
        label: 'Location Name',
        field: 'loc_name',
        sort: 'asc',
        width: 150
      },
      {
        label: 'Start Time',
        field: 'start_time',
        sort: 'asc',
        width: 100
      },
      {
        label: 'End Time',
        field: 'end_time',
        sort: 'asc',
        width: 100
      },
      {
        label: 'Description',
        field: 'description',
        sort: false,
        width: 100
      },
      {
        label: 'Details',
        field: 'details',
        sort: false,
        width: 100
      },
    ],
    rows: rows.rows
  };

  return (
    <MDBDataTable
      striped
      bordered
      small
      noBottomColumns
      btn
      data={data}
    />
  );
}

export default EventTable;
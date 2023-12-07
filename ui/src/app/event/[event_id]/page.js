export default function Page({ params }) {
    const eventID = params.event_id;

    return <p>Event ID: {eventID}</p>
}
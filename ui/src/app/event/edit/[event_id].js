import { useRouter } from 'next/router';

export default function Page() {
    const router = useRouter();
    const event_id = router.query.event_id;

    // Testing only.
    return <p>The event id is: {event_id}</p>
};

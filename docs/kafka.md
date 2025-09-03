# Kafka
## Global schema
```json
{
    "event": "", // event type
    "payload": {} // payload
}
```

## Paste Service
### Topics
- paste.events
### Event types
- published
- updated
- created
- deleted

## Notification Service
- worker.**{channel}**
    - telegram
    - email
    - discord


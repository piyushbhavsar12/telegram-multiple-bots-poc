# telegram-multiple-bots-poc
Multiple bot instances using single server
```
uvicorn newapp:app --host 0.0.0.0 --port 8000
```

set ngrok

```
curl --location 'https://api.telegram.org/bot<bot-token>/setWebhook' \
--header 'Content-Type: application/json' \
--data '{"url": "<ngrok-url>/webhook/prayas"}'
```

boom both the bots are working

# telegram-multiple-bots-poc
Multiple bot instances using single server
```
uvicorn newapp:app --host 0.0.0.0 --port 8000
```

set ngrok
in terminal:
```
ngrok 8000
```

copy the link

open the postman and import the curl:
add values on the placeholders

```
curl --location 'https://api.telegram.org/bot<bot-token>/setWebhook' \
--header 'Content-Type: application/json' \
--data '{"url": "<ngrok-url>/webhook/prayas"}'
```

boom both the bots are working

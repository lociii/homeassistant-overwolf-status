# Overwolf Webhook

This custom integration is part of a two-piece system to bridge game events from Overwolf into Home Assistant so that your smart home can react on them.

- Want your lights to flash blue when the blue zone starts moving in PUBG?
- Want your lights to flash red when the bomb is planted in CS:GO?
- Want Alexa to cheer you when you make a kill in Dota 2 or LoL?

This can all be achieved by this integration and the [Overwolf app counterpart](https://TBD).
A list of all possible game events can be found in the [Overwolf documentation](https://overwolf.github.io/api/games/events).

## Setup

1. Install the custom integration `Overwolf Webhook` using the [Home Assistant Community Store](https://hacs.xyz/) ([2022 setup guide](https://www.youtube.com/watch?v=zlaJrepZl2E))
2. Set up the integration `Overwolf Webhook` ([2022 guide on how to install integrations](https://www.youtube.com/watch?v=zKND54iAZ1A&t=940s))
3. Copy the nabu.casa Webhook URL that will be shown during the setup process
4. Install the Overwolf app `Home Assistant Webhook` from the [Overwolf store](https://TBD)
5. Enter the URL copied in step 3 when asked for it by the Overwolf app

Once setup is completed, game events will be sent from Overwolf to your Home Assistant installation. They will there be emitted 1:1 as the custom `overwolf_game_event` [event](https://www.home-assistant.io/docs/configuration/events/) to be processed by your own automations reacting on them.

## Event format

Payload of a kill event for Apex Legends

```yaml
event_type: overwolf_game_event
data:
  game_id: 21566
  event:
    events:
      - name: kill
        data:
          victimName: lociii
origin: REMOTE
time_fired: "YYYY-MM-DDTHH:MM:SS.000000+00:00"
context:
  id: <event_id
  parent_id: null
  user_id: <user_id>
```

The `data` section will contain the actual information from Overwolf where `data.event` is the event content as described in the [Overwolf documentation for Apex Legends](https://overwolf.github.io/api/games/events/apex-legends#kill).

## Automation examples

TBD

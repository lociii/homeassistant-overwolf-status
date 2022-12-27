### Status

Waiting for the Overwolf companion app to be approved and available in the Overwolf store.

### Disclaimer

This project is not endorsed by or affiliated with Overwolf or Home Assistant.

# Overwolf Webhook

This custom integration is part of a two-piece system to forward game events from Overwolf to Home Assistant so that your smart home can react on them.

- Want your lights to flash blue when the blue zone starts moving in PUBG?
- Want your lights to flash red when the bomb is planted in CS:GO?
- Want Alexa to cheer you when you make a kill in Dota 2 or LoL?

This can all be achieved by this integration and the [Overwolf app counterpart](https://TBD).
A list of all possible game events can be found in the [Overwolf documentation](https://overwolf.github.io/api/games/events).

## Setup

1. Install the custom integration `Overwolf Webhook` using the [Home Assistant Community Store](https://hacs.xyz/) ([2022 setup guide](https://www.youtube.com/watch?v=zlaJrepZl2E))
2. Set up the integration `Overwolf Webhook` ([2022 guide on how to install integrations](https://www.youtube.com/watch?v=zKND54iAZ1A&t=940s))
3. Copy the Webhook URL that will be shown during the setup process (based on restrictions on target URLs in the Overwolf app, you can only use hooks.nabu.casa or homeassistant.local URLs)
4. Install the Overwolf app `Home Assistant Game Events` from the [Overwolf store](https://TBD)
5. Enter the URL copied in step 3 when asked for it by the Overwolf app

Once setup is completed, game events will be sent from Overwolf to your Home Assistant installation. They will there be emitted 1:1 as the custom `overwolf_game_event` [event](https://www.home-assistant.io/docs/configuration/events/) to be processed by your own [automations reacting on them](https://www.home-assistant.io/docs/automation/trigger/#event-trigger).

## Event format

Events / info updates will always be sent in the following format

```yaml
event: <string: "event" or "info">,
gameId: <int: game id according to https://overwolf.github.io/api/games/ids>,
gameName: <string: game name according to https://overwolf.github.io/api/games/ids>,
data: <dict: update details>
```

Payload of a [kill event](https://overwolf.github.io/api/games/events/counter-strike-global-offensive#kill-note) for `Counter-Strike: Global Offensive`

```yaml
event: event
gameId: 7764
gameName: "Counter-Strike: Global Offensive"
data:
  events:
    - name: kill
      data:
        totalKills: 5
```

Payload of a [kill count info](https://overwolf.github.io/api/games/events/counter-strike-global-offensive#totalkills-note) for `Counter-Strike: Global Offensive`

```yaml
event: info
gameId: 7764
gameName: "Counter-Strike: Global Offensive"
data:
  player:
    totalKills: 5
```

The `data` section will 1:1 contain the actual information from Overwolf whereas the root contains meta information as described above.  
Whereever Overwolf provided stringified JSON as payload, we will decode it and send it as an actual data structure (e.g. [Rocket League roster info updates](https://overwolf.github.io/api/games/events/rocket-league#roster))

## Automation examples

Automations must be based on the [event trigger](https://www.home-assistant.io/docs/automation/trigger/#event-trigger) listening for `overwolf_game_event` to be received.

Here's an example that will listen to the above mentioned CS:GO kill event and turn a lamp red for one seconds before fading it out again.  
Be aware that the above mentioned data structure is available in a template under the `trigger.event` variable.  
The extension will always send one game event / info update per Home Assistant event.

```yaml
alias: CSGO - Kill
description: ""
trigger:
  - platform: event
    event_type: overwolf_game_event
    event_data:
      data:
        gameId: 7764
    alias: Received an Overwolf CS:GO event
condition:
  - condition: template
    value_template: "{{ trigger.event.data.data.events.0.name == \"kill\" }}"
    alias: Kill event
action:
  - service: light.turn_on
    data:
      rgb_color:
        - 255
        - 0
        - 0
      brightness_pct: 100
    target:
      entity_id: light.example
    alias: Turn light on in red
  - delay:
      hours: 0
      minutes: 0
      seconds: 1
      milliseconds: 0
    alias: Wait a second
  - service: light.turn_off
    data:
      transition: 0.5
    target:
      entity_id: light.example
    alias: Turn light off
mode: single
```

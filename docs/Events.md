#### DuckAppearEvent

```
"emoji_used": `emoji_used` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT '<:official_Duck_01_reversed:439576463436546050>',
```


#### DuckDeathEvents

##### DuckKilledEvent

```python
":skull_crossbones: **{onomatopoeia}**\tYou killed the duck in {time} seconds, you are now at a grand total of {total} ducks (of which {supercanards} "
"were super-ducks) killed on {channel}.     \\_X<   *COUAC*   {exp}"

```
##### DuckFlewAway
```python
_("The duck went away.  ·°'\`'°-.,¸¸.·°'\`"),
_("The duck went to another world.  ·°'\`'°-.,¸¸.·°'\`"),
_("The duck flew over a disproportionately small gap. ·°'\`'°-.,¸¸.·°'\`"),
_("The duck left.  ·°'\`'°-.,¸¸.·°'\`"),
_("The duck left out of boredom.  ·°'\`'°-.,¸¸.·°'\`"),
_("The duck dissipated in space and time.  ·°'\`'°-.,¸¸.·°'\`"),
_("The duck chickened out.  ·°'\`'°-.,¸¸.·°'\`")]
_("The duck didn't have time for this.  ·°'\`'°-.,¸¸.·°'\`"),
_("The duck doesn't want to be sniped.  ·°'\`'°-.,¸¸.·°'\`"),
_("The duck walked up to the lemonade stand.  ·°'\`'°-.,¸¸.·°'\`"),


```

##### DuckFrightenedEvent

```python
_("**FLAPP**\tFrightened by so much noise, the duck fled! CONGRATS! [missed: -1 xp]", language)
```

#### DuckBabyEvents

```python
# spawn
[
    "<:BabyDuck_01:439546718263050241>",
    "<:BabyDuck_02:439551472762355724>", 
    " <:official_BabyDuck_01:439546718527160322>",
    "<a:a_BabyDuck_01:439546761091088385>",
    " <a:a_BabyDuck_02:574299816155414531>"
]

#voice
cri = "**COIN**"

#leave
_("The baby duck left to take a little nap somewhere ·°'\`'°-.,¸¸.·°'\`", language)

#killed
_(":skull_crossbones: **{onomatopoeia}**\tYou killed the baby duck in {time} seconds, and you shouldn't have done this!"
                 " You'll lose some exp, because you shouldn't kill babies"
                 "\_X<   *COUAC*   {exp}", language)

#DuckBabyHuggedEvent
#hugged
_("<:cmd_Hug_01:442695336348221451> **SMACK**\tYou hugged the baby duck, and now it is really happy! [3 exp]\n"
                 "The baby duck left, feeling loved", language)
```

#### NoDuckEvent

```python
There isn't any duck in here
There isn't any duck

_(
"There isn't any duck in here, but the bullet wasn't fired because the infrared detector you added to your weapon is doing its job!",
                                                language))
_(
"Luckily you missed, but what were you aiming at exactly? There isn't any duck in here... [missed: -1 xp] [wild shot: -1 xp]",
                    language)
```

### IAmMentioned

#### AmmoEvent

```python
_("{greet} | Ammo in weapon: {balles_actuelles}/{balles_max} | Magazines left: {chargeurs_actuels}/{chargeurs_max}",
  
            language).format(
            **{"greet": greet, "balles_actuelles": balles, "balles_max": balles_max, "chargeurs_actuels": chargeurs,
               "chargeurs_max": chargeurs_max}))
               
_("** MAGAZINE EMPTY ** | "
  "Ammunition in the weapon: {balles_actuelles} / {balles_max} | "
"Magazines remaining: {chargeurs_actuels} / {chargeurs_max}",
  
language).format(
                **{"balles_actuelles": bullets, "balles_max": level["balles"],
                   "chargeurs_actuels": await get_stat(channel, author, "chargeurs"),
                   "chargeurs_max": level["chargeurs"]}))
```


#### WeaponConfiscatedEvent

```python
You missed the duck &&   [**weapon confiscated**]

_(
"**BANG**\tYou missed the duck... and shot **yourself**! Maybe you should turn your weapon a little before shooting the next time? "
                        "[missed: -1 xp] [hunting accident: -2 xp] [**weapon confiscated**]", language))

_(
"**BANG**\tYou missed the duck... and shot {player}! [missed: -1 xp] [hunting accident: -2 xp] [**weapon confiscated**]",
                        language).format(
                        **{"player": player_killed.mention if await get_pref(channel,
                                                                             "killed_mentions") else player_killed.name}))

_("You don't have a weapon.", language)
```

#### IamWet

#### JammedWeaponEvent

```
Your weapon is jammed
Your weapon just jammed

_("Your weapon is jammed, it must be reloaded to unjam it.", language)
_("Your weapon just jammed, reload it to unjam it.", language)
```




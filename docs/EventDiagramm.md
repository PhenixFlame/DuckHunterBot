```mermaid
graph TD
    Message--Author?-->DuckHuntBot
    DuckHuntBot--DuckSignChekcer-->DuckAppearEvent
    
    DuckHuntBot--Duckkilled-->DuckDeathEvent
    DuckHuntBot--DuckFlewAway-->DuckDeathEvent
    DuckHuntBot--**FLAPP** Frightened-->DuckDeathEvent
    
    DuckHuntBot--MentionMyName-->IamMentioned
    DuckHuntBot--There isn't any duck-->NoDuckEvent
    IamMentioned--X-->AmmoEvent(MAGAZINE EMPTY,)
    IamMentioned--You don't have a weapon-->WeaponConfiscated
    IamMentioned--Your clothes are wet-->IamWet
    IamMentioned--Your weapon is jammed-->JammedWeapon
    IamMentioned--Your weapon just jammed-->JammedWeapon
    IamMentioned--Your weapon is sabotaged-->XXX 
    

```
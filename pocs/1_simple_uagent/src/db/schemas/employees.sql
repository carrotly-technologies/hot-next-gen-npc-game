
NPC {
id
name
description
correlations: Correlation[]
}

Correlations {
    id
    description
    npcId
    opinion
}


Event {
    id
    npcId
    description
}

Building {
    id
    name
    pattern 40x40
}

Send Eventt -> {
    playerId: "123"
    npcId -> NPC1
    description: "Steal items from chest"
}

<character> <description> who is [opinion] to <player>

As a <CharacterName> who is <description> Happened to be <action> by main player
player made <eventDescription>. Genereate 3 choosable options, where one of the options allow to finish


Send Event """

"""

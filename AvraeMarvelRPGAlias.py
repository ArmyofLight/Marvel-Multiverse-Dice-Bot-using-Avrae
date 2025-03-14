# Uncomment the line below when trying to enter this into Avrae
#!servalias marvel embed 
<drac2>
md = vroll('1d6')
d2 = vroll('1d6')
d3 = vroll('1d6')

dice = [md, d2, d3]
diceDisplay = [str(d) for d in dice]  # Capture initial display values

#Default modifiers and counts
abilityMod = 0
damageMod = 0
edgeCount = 0
troubleCount = 0

#Processing arguments
args = &ARGS&
i = 0
while i < len(args):
    arg = args[i]
    if arg.isdigit():
        if abilityMod == 0:
            abilityMod = int(arg)
            i += 1
            if i < len(args) and args[i].isdigit():
                damageMod = int(args[i])
        else:
            i += 1  
    elif arg == 'edge' and i + 1 < len(args) and args[i + 1].isdigit():
        edgeCount = int(args[i + 1])
        i += 2  
    elif arg == 'trouble' and i + 1 < len(args) and args[i + 1].isdigit():
        troubleCount = int(args[i + 1])
        i += 2  
    # else:
    #     i += 1  # Move to next argument

# Handle rerolls for edge and trouble
rerollDescriptions = []
if edgeCount > 0:
    for _ in range(edgeCount):
        min_index = min(range(1, len(dice)), key=lambda i: dice[i].total)  # Exclude Marvel Die if it rolled a 1 initially
        old_roll = dice[min_index]
        new_roll = vroll('1d6')
        dice[min_index] = new_roll if new_roll.total > old_roll.total else old_roll
        diceDisplay[min_index] = f"{old_roll} -> {dice[min_index]}"
        rerollDescriptions.append(f"Edge rerolled Die #{min_index+1}: {old_roll} to {newroll}")
if troubleCount > 0:
    for  in range(troubleCount):
        max_index = max(range(len(dice)), key=lambda i: dice[i].total)
        old_roll = dice[max_index]
        new_roll = vroll('1d6')
        dice[max_index] = new_roll if new_roll.total < old_roll.total else old_roll
        diceDisplay[max_index] = f"{old_roll} -> {dice[max_index]}"
        rerollDescriptions.append(f"Trouble rerolled Die #{max_index+1}: {old_roll} to {new_roll}")

# Adjust Marvel Die for Fantastic Roll
fantasticFlag = False
if md.total == 1:
    md = vroll('6')  # Treat a 1 as a 6 for further calculations
    dice[0] = md
    diceDisplay[0] = f"{md} -> 6! Fantastic!"
    fantasticFlag = True

#Recalculate total after rerolls
total = sum(d.total for d in dice) + abilityMod

title = "Marvel Roll"
if fantasticFlag:
    title = "Fantastic Roll!"
    if dice[0] == 6 and dice[1] == 6 and dice[2] == 6:
        title = "Ultimate Fantastic Roll!"
    # total += 5

#Damage calculation only if damageMod is provided
damageOutput = ""
if damageMod != 0:
    damageTotal = md.total * damageMod + abilityMod
    damageOutput = f"Damage:|Marvel Die: {md.total} * {damageMod} + {abilityMod}\nTotal Damage: {damageTotal}"

#Building the final output
dice_description = "\n".join([f"Marvel Die: {diceDisplay[0]}" if i == 0 else f"Die #{i+1}: {d}" for i, d in enumerate(diceDisplay)])
reroll_description = "\n".join(rerollDescriptions)
finalOutput = f''' -title "{title}" -f "Action Check:|{dice_description}\nAbility Modifier: {abilityMod}\nTotal: {total}" '''
if reroll_description:
    finalOutput += f''' -f "Rerolls:|{reroll_description}" '''
if damageOutput:
    finalOutput += f''' -f "{damageOutput}" '''

return finalOutput
</drac2>
import random

# How many kobolds can your character take in a fight?
# Each kobold is assumed to be in a troop of 4 kobolds that 
# strike automatically once per round.

# Just enter your character's details below!

number_of_kobold_troops = 35
kobolds_hp = 6 * 4 * number_of_kobold_troops

char_name = "Alonzo"
is_paladin = True

char_hp = 115
char_max_hp = 121
char_heal_min = 81
char_heals = 12
defiance = True

char_attacks = [15, 10]
char_damage_dice_num = 1
char_damage_die = 8
char_damage_bonus = 4
char_crit_multiplier = 3

char_damage = lambda: roll_damage(
    char_damage_dice_num, char_damage_die, char_damage_bonus
)
char_crit_damage = lambda: roll_damage(
    char_damage_dice_num * char_crit_multiplier,
    char_damage_die,
    char_damage_bonus * char_crit_multiplier
)
char_crit_min = 17
confirm_bonus = 4

def roll_damage(num, die, bonus):
  roll = 0
  for i in range(num):
    roll += random.randint(1,die)
  return roll + bonus

def attack(ac):
  global kobolds_hp

  attacks = [random.randint(1,20) for i in range(len(char_attacks))]
  for i in range(len(char_attacks)):
    attack = attacks[i]
    bonus = char_attacks[i]
    crit_attack = random.randint(1,20)

    damage = 0
    if attack != 1:
      if attack == 20 or attack+bonus >= ac and attack >= char_crit_min and crit_attack != 1 and crit_attack+bonus+confirm_bonus >= ac:
        damage = char_crit_damage()
        print "Attack %d crits for %d damage!" % (i, damage)
      elif attack+bonus >= ac:
        damage = char_damage()
        print "Attack %d hits!  Did %d damage." % (i, damage)

    troop_hp = kobolds_hp % 24
    troop_hp = 24 if troop_hp == 0 else troop_hp
    kobolds_hp -= min(troop_hp, damage)
    if damage == 0:
      print "Attack %d missed!" % i

    if kobolds_hp <= 0:
      break

turn = 1
while kobolds_hp > 0 and char_hp > 0:
  print "Turn %d" % turn
  print "%s: %d hp" % (char_name, char_hp)
  print "Kobolds: %d hp" % kobolds_hp
  turn += 1
  kobold_damage = roll_damage(4, 3, -4)
  char_hp -= kobold_damage

  print "The kobolds swarm %s for %d damage!" % (char_name, kobold_damage)

  if char_hp <= 0 and char_heals > 0 and defiance and is_paladin:
    heal = roll_damage(7,8,0)
    print "%s nearly falls but is defiantly heals for %d! What a stud!" % (
        char_name, heal
    )
    char_hp = min(char_max_hp, char_hp + heal)
    char_heals -= 1
    defiance = False

  if char_hp < 0:
    break

  min_heals = 1 if defiance else 0
  if char_hp <= char_heal_min and char_heals > min_heals and is_paladin:
    heal = roll_damage(6,8,0)
    print "%s heals for %d hp!" % (char_name, heal)
    char_hp = min(char_max_hp, char_hp + heal)
    char_heals -= 1

  attack(16)

if kobolds_hp <= 0:
  print "%s has defeated the kobolds!" % char_name
else:
  print "%s was overrun..." % char_name

print "%s has %d hp." % (char_name, char_hp)
if is_paladin:
  print "%s has %d lay on hands left." % (char_name, char_heals)

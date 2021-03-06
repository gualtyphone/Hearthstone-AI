from enum import IntEnum


class GameTag(IntEnum):
	"GAME_TAG"

	TURN_START = 8
	TURN_TIMER_SLUSH = 9
	PLAYSTATE = 17
	LAST_AFFECTED_BY = 18
	STEP = 19
	TURN = 20
	FATIGUE = 22
	CURRENT_PLAYER = 23
	FIRST_PLAYER = 24
	RESOURCES_USED = 25
	RESOURCES = 26
	HERO_ENTITY = 27
	MAXHANDSIZE = 28
	STARTHANDSIZE = 29
	PLAYER_ID = 30
	TEAM_ID = 31
	TRIGGER_VISUAL = 32
	RECENTLY_ARRIVED = 33
	PROTECTED = 34
	PROTECTING = 35
	DEFENDING = 36
	PROPOSED_DEFENDER = 37
	ATTACKING = 38
	PROPOSED_ATTACKER = 39
	ATTACHED = 40
	EXHAUSTED = 43
	DAMAGE = 44
	HEALTH = 45
	ATK = 47
	COST = 48
	ZONE = 49
	CONTROLLER = 50
	OWNER = 51
	DEFINITION = 52
	ENTITY_ID = 53
	HISTORY_PROXY = 54
	ELITE = 114
	MAXRESOURCES = 176
	CARD_SET = 183
	DURABILITY = 187
	SILENCED = 188
	WINDFURY = 189
	TAUNT = 190
	STEALTH = 191
	SPELLPOWER = 192
	DIVINE_SHIELD = 194
	CHARGE = 197
	NEXT_STEP = 198
	CLASS = 199
	CARDRACE = 200
	FACTION = 201
	CARDTYPE = 202
	RARITY = 203
	STATE = 204
	SUMMONED = 205
	FREEZE = 208
	ENRAGED = 212
	OVERLOAD = 215
	LOYALTY = 216
	DEATHRATTLE = 217
	BATTLECRY = 218
	SECRET = 219
	COMBO = 220
	CANT_HEAL = 221
	CANT_DAMAGE = 222
	CANT_SET_ASIDE = 223
	CANT_REMOVE_FROM_GAME = 224
	CANT_READY = 225
	CANT_ATTACK = 227
	CANT_DISCARD = 230
	CANT_PLAY = 231
	CANT_DRAW = 232
	CANT_BE_HEALED = 239
	IMMUNE = 240
	CANT_BE_SET_ASIDE = 241
	CANT_BE_REMOVED_FROM_GAME = 242
	CANT_BE_READIED = 243
	CANT_BE_ATTACKED = 245
	CANT_BE_TARGETED = 246
	CANT_BE_DESTROYED = 247
	CANT_BE_SUMMONING_SICK = 253
	FROZEN = 260
	JUST_PLAYED = 261
	LINKED_ENTITY = 262
	ZONE_POSITION = 263
	CANT_BE_FROZEN = 264
	COMBO_ACTIVE = 266
	CARD_TARGET = 267
	NUM_CARDS_PLAYED_THIS_TURN = 269
	CANT_BE_TARGETED_BY_OPPONENTS = 270
	NUM_TURNS_IN_PLAY = 271
	NUM_TURNS_LEFT = 272
	CURRENT_SPELLPOWER = 291
	ARMOR = 292
	MORPH = 293
	IS_MORPHED = 294
	TEMP_RESOURCES = 295
	OVERLOAD_OWED = 296
	NUM_ATTACKS_THIS_TURN = 297
	NEXT_ALLY_BUFF = 302
	MAGNET = 303
	FIRST_CARD_PLAYED_THIS_TURN = 304
	MULLIGAN_STATE = 305
	TAUNT_READY = 306
	STEALTH_READY = 307
	CHARGE_READY = 308
	CANT_BE_TARGETED_BY_SPELLS = 311
	SHOULDEXITCOMBAT = 312
	CREATOR = 313
	CANT_BE_SILENCED = 314
	PARENT_CARD = 316
	NUM_MINIONS_PLAYED_THIS_TURN = 317
	PREDAMAGE = 318
	CANT_BE_TARGETED_BY_HERO_POWERS = 332
	HEALTH_MINIMUM = 337
	TAG_ONE_TURN_EFFECT = 338
	SILENCE = 339
	COUNTER = 340
	ZONES_REVEALED = 348
	ADJACENT_BUFF = 350
	FORCED_PLAY = 352
	LOW_HEALTH_THRESHOLD = 353
	SPELLPOWER_DOUBLE = 356
	HEALING_DOUBLE = 357
	NUM_OPTIONS_PLAYED_THIS_TURN = 358
	TO_BE_DESTROYED = 360
	AURA = 362
	POISONOUS = 363
	HERO_POWER_DOUBLE = 366
	NUM_MINIONS_PLAYER_KILLED_THIS_TURN = 368
	NUM_MINIONS_KILLED_THIS_TURN = 369
	AFFECTED_BY_SPELL_POWER = 370
	EXTRA_DEATHRATTLES = 371
	START_WITH_1_HEALTH = 372
	IMMUNE_WHILE_ATTACKING = 373
	MULTIPLY_HERO_DAMAGE = 374
	MULTIPLY_BUFF_VALUE = 375
	CUSTOM_KEYWORD_EFFECT = 376
	CANT_BE_TARGETED_BY_BATTLECRIES = 379
	HERO_POWER = 380
	DEATHRATTLE_RETURN_ZONE = 382
	STEADY_SHOT_CAN_TARGET = 383
	DISPLAYED_CREATOR = 385
	POWERED_UP = 386
	SPARE_PART = 388
	FORGETFUL = 389
	CAN_SUMMON_MAXPLUSONE_MINION = 390
	OBFUSCATED = 391
	BURNING = 392
	OVERLOAD_LOCKED = 393
	NUM_TIMES_HERO_POWER_USED_THIS_GAME = 394
	CURRENT_HEROPOWER_DAMAGE_BONUS = 395
	HEROPOWER_DAMAGE = 396
	LAST_CARD_PLAYED = 397
	NUM_FRIENDLY_MINIONS_THAT_DIED_THIS_TURN = 398
	NUM_CARDS_DRAWN_THIS_TURN = 399
	INSPIRE = 403
	RECEIVES_DOUBLE_SPELLDAMAGE_BONUS = 404
	HEROPOWER_ADDITIONAL_ACTIVATIONS = 405
	HEROPOWER_ACTIVATIONS_THIS_TURN = 406
	REVEALED = 410
	NUM_FRIENDLY_MINIONS_THAT_DIED_THIS_GAME = 412
	CANNOT_ATTACK_HEROES = 413
	LOCK_AND_LOAD = 414
	DISCOVER = 415
	SHADOWFORM = 416
	NUM_FRIENDLY_MINIONS_THAT_ATTACKED_THIS_TURN = 417
	NUM_RESOURCES_SPENT_THIS_GAME = 418
	CHOOSE_BOTH = 419
	ELECTRIC_CHARGE_LEVEL = 420
	HEAVILY_ARMORED = 421
	DONT_SHOW_IMMUNE = 422
	RITUAL = 424
	PREHEALING = 425
	APPEAR_FUNCTIONALLY_DEAD = 426
	OVERLOAD_THIS_GAME = 427
	SPELLS_COST_HEALTH = 431
	HISTORY_PROXY_NO_BIG_CARD = 432
	PROXY_CTHUN = 434
	TRANSFORMED_FROM_CARD = 435
	CTHUN = 436
	CAST_RANDOM_SPELLS = 437
	SHIFTING = 438
	JADE_GOLEM = 441
	EMBRACE_THE_SHADOW = 442
	CHOOSE_ONE = 443
	EXTRA_ATTACKS_THIS_TURN = 444
	SEEN_CTHUN = 445
	MINION_TYPE_REFERENCE = 447
	UNTOUCHABLE = 448
	CANT_BE_FATIGUED = 456
	AUTOATTACK = 457
	ARMS_DEALING = 458
	PENDING_EVOLUTIONS = 461
	QUEST = 462
	TAG_LAST_KNOWN_COST_IN_HAND = 466
	DEFINING_ENCHANTMENT = 469
	FINISH_ATTACK_SPELL_ON_DAMAGE = 470
	MODULAR_ENTITY_PART_1 = 471
	MODULAR_ENTITY_PART_2 = 472
	MODIFY_DEFINITION_ATTACK = 473
	MODIFY_DEFINITION_HEALTH = 474
	MODIFY_DEFINITION_COST = 475
	MULTIPLE_CLASSES = 476
	ALL_TARGETS_RANDOM = 477
	MULTI_CLASS_GROUP = 480
	CARD_COSTS_HEALTH = 481
	GRIMY_GOONS = 482
	JADE_LOTUS = 483
	KABAL = 484
	ADDITIONAL_PLAY_REQS_1 = 515
	ADDITIONAL_PLAY_REQS_2 = 516
	ELEMENTAL_POWERED_UP = 532
	QUEST_PROGRESS = 534
	QUEST_PROGRESS_TOTAL = 535
	QUEST_CONTRIBUTOR = 541
	ADAPT = 546
	IS_CURRENT_TURN_AN_EXTRA_TURN = 547
	EXTRA_TURNS_TAKEN_THIS_GAME = 548
	TREASURE = 557
	TREASURE_DEFINTIONAL_ATTACK = 558
	TREASURE_DEFINTIONAL_COST = 559
	TREASURE_DEFINTIONAL_HEALTH = 560
	ACTS_LIKE_A_SPELL = 561
	SHIFTING_MINION = 549
	SHIFTING_WEAPON = 550
	DEATH_KNIGHT = 554
	STAMPEDE = 564
	EMPOWERED_TREASURE = 646
	ONE_SIDED_GHOSTLY = 648
	CURRENT_NEGATIVE_SPELLPOWER = 651
	IS_VAMPIRE = 680
	CORRUPTED = 681
	HIDE_HEALTH = 682
	HIDE_ATTACK = 683
	HIDE_COST = 684
	LIFESTEAL = 685
	RECRUIT = 763
	LOOT_CARD_1 = 764
	LOOT_CARD_2 = 765
	LOOT_CARD_3 = 766
	HERO_POWER_DISABLED = 777
	VALEERASHADOW = 779
	OVERRIDECARDNAME = 781
	OVERRIDECARDTEXTBUILDER = 782
	DUNGEON_PASSIVE_BUFF = 783
	HIDDEN_CHOICE = 813
	ZOMBEAST = 823
	HERO_EMOTE_SILENCED = 832
	MINION_IN_HAND_BUFF = 845
	IGNORE_HIDE_STATS_FOR_BIG_CARD = 857
	REAL_TIME_TRANSFORM = 859
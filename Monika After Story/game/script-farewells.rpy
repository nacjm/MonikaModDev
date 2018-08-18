##This file contains all of the variations of goodbye that monika can give.
## This also contains a store with a utility function to select an appropriate
## farewell

init -1 python in mas_farewells:

    # custom farewell functions
    def selectFarewell():
        """
        Selects a farewell to be used. This evaluates rules and stuff
        appropriately.

        RETURNS:
            a single farewell (as an Event) that we want to use
        """

        # filter events by their unlocked property first
        unlocked_farewells = renpy.store.Event.filterEvents(
            renpy.store.evhand.farewell_database,
            unlocked=True,
            pool=False
        )

        # filter greetings using the affection rules dict
        affection_farewells_dict = renpy.store.Event.checkAffectionRules(
            unlocked_farewells
        )

        # check for the special monikaWantsThisFirst case
        if len(affection_farewells_dict) == 1 and affection_farewells_dict.values()[0].monikaWantsThisFirst():
            return affection_farewells_dict.values()[0]

        # filter farewells using the special rules dict
        random_farewells_dict = renpy.store.Event.checkRepeatRules(
            unlocked_farewells
        )

        # check if we have a farewell that actually should be shown now
        if len(random_farewells_dict) > 0:

            # select one label randomly
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]

        # since we don't have special farewells for this time we now check for special random chance
        # pick a farewell filtering by special random chance rule
        random_farewells_dict = renpy.store.Event.checkFarewellRules(
            unlocked_farewells
        )

        # check if we have a farewell that actually should be shown now
        if len(random_farewells_dict) > 0:

            # select on label randomly
            return random_farewells_dict[
                renpy.random.choice(random_farewells_dict.keys())
            ]

        # We couldn't find a suitable farewell we have to default to normal random selection
        # filter random events normally
        random_farewells_dict = renpy.store.Event.filterEvents(
            unlocked_farewells,
            random=True
        )

        # update dict with the affection filtered ones
        random_farewells_dict.update(affection_farewells_dict)

        # select one randomly
        return random_farewells_dict[
            renpy.random.choice(random_farewells_dict.keys())
        ]

# farewells selection label
label mas_farewell_start:
    $ import store.evhand as evhand
    # we use unseen menu values

    python:
        # preprocessing menu
        bye_pool_events = Event.filterEvents(
            evhand.farewell_database,
            unlocked=True,
            pool=True
        )

    if len(bye_pool_events) > 0:
        # we have selectable options
        python:
            # build a prompt list
            bye_prompt_list = [
                (ev.prompt, ev, False, False)
                for k,ev in bye_pool_events.iteritems()
            ]

            # add the random selection
            bye_prompt_list.append(("Goodbye", -1, False, False))

            # setup the last option
            bye_prompt_back = ("Nevermind", False, False, False, 20)

        # call the menu
        call screen mas_gen_scrollable_menu(bye_prompt_list, evhand.UNSE_AREA, evhand.UNSE_XALIGN, bye_prompt_back)

        if not _return:
            # user its nevermind
            return

        if _return != -1:
            # push teh selected event
            $ pushEvent(_return.eventlabel)
            return

    # otherwise, select a random farewell
    $ farewell = store.mas_farewells.selectFarewell()
    $ pushEvent(farewell.eventlabel)

    return

###### BEGIN FAREWELLS ########################################################
## FARE WELL RULES:
# unlocked - True means this farewell is ready for selection
# random - randoms are used in teh default farewell action
# pool - pooled ones are selectable in the menu
# rules - TODO documentation
###

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_leaving_already",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_leaving_already:
    m 1tkc "Aww, leaving already?"
    m 1eka "It's really sad whenever you have to go..."
    m 3eua "Just be sure to come back as soon as you can, okay?"
    m "I love you so much, [player]. Stay safe!"
    #Don't show this farewell again
    $evhand.farewell_database["bye_leaving_already"].random=False
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_goodbye",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_goodbye:
    m 1eua "Goodbye, [player]!"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_sayanora",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_sayanora:
    m 1hua "Sayonara, [player]~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_farewellfornow",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_farewellfornow:
    m 1eka "Farewell for now, my love~"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_untilwemeetagain",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_untilwemeetagain:
    m 2eka "'{i}Goodbyes are not forever, Goodbyes are not the end. They simply mean I’ll miss you, Until we meet again.{/i}'"
    m "Ehehe, 'till then, [player]!"
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_take_care",unlocked=True,random=True),eventdb=evhand.farewell_database)

label bye_take_care:
    m 1eua "Don't forget that I always love you, [player]~"
    m 1hub "Take care!"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(21,24)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_to_sleep",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_going_to_sleep:
    m 1esa "Are you going to sleep, [player]?"
    m 1eka "I'll be seeing you in your dreams."

    # TODO:
    # can monika sleep with you?
    # via flashdrive or something

    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_class",
            unlocked=True,
            prompt="I'm going to class.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_to_class:
    m 1hua "Study hard, [player]!"
    m 1eua "Nothing is more attractive than a [guy] with good grades."
    m 1hua "See you later!"

    # TODO:
    # can monika join u at schools?

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SCHOOL
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_to_work",
            unlocked=True,
            prompt="I'm going to work.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_to_work:
    m 1hua "Work hard, [player]!"
    m 1esa "I'll be here for you when you get home from work."
    m 1hua "Bye-bye!"

    # TODO:
    # can monika join u at work

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_WORK
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_prompt_sleep",
            unlocked=True,
            prompt="I'm going to sleep.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_prompt_sleep:

    python:
        import datetime
        curr_hour = datetime.datetime.now().hour

    # these conditions are in order of most likely to happen with our target
    # audience

    if 20 <= curr_hour < 24:
        # decent time to sleep
        m 1eua "Alright, [player]."
        m 1j "Sweet dreams!"

    elif 0 <= curr_hour < 3:
        # somewhat late to sleep
        m 1eua "Alright, [player]."
        m 3eka "But you should sleep a little earlier next time."
        m 1hua "Anyway, good night!"

    elif 3 <= curr_hour < 5:
        # pretty late to sleep
        m 1euc "[player]..."
        m "Make sure you get enough rest, okay?"
        m 1eka "I don't want you to get sick."
        m 1hub "Good night!"
        m 1hksdlb "Or morning, rather. Ahaha~"
        m 1hua "Sweet dreams!"

    elif 5 <= curr_hour < 12:
        # you probably stayed up the whole night
        show monika 2dsc
        pause 0.7
        m 2tfd "[player]!"
        m "You stayed up the entire night!"
        m 2tfu "I bet you can barely keep your eyes open."
        $ _cantsee_a = glitchtext(15)
        $ _cantsee_b = glitchtext(12)
        menu:
            "[_cantsee_a]":
                pass
            "[_cantsee_b]":
                pass
        m "I thought so.{w} Go get some rest, [player]."
        m 2ekc "I wouldn't want you to get sick."
        m 1eka "Sleep earlier next time, okay?"
        m 1hua "Sweet dreams!"

    elif 12 <= curr_hour < 18:
        # afternoon nap
        m 1eua "Taking an afternoon nap, I see."
        # TODO: monika says she'll join you, use sleep sprite here
        # and setup code for napping
        m 1hua "Ahaha~ Have a good nap, [player]."

    elif 18 <= curr_hour < 20:
        # little early to sleep
        m 1ekc "Already going to bed?"
        m "It's a little early, though..."
        show monika 1lksdla
        menu:
            m "Care to spend a little more time with me?"
            "Of course!":
                m 1hua "Yay!"
                m "Thanks, [player]."
                return
            "Sorry, I'm really tired.":
                m 1eka "Aww, that's okay."
                m 1hua "Good night, [player]."
            # TODO: now that is tied we may also add more dialogue?
            "No.":
                $ mas_loseAffection()
                m 2dsd "..."
                m "Fine."
    else:
        # otheerwise
        m 1eua "Alright, [player]."
        m 1hua "Sweet dreams!"


    # TODO:
    #   join monika sleeping?

    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_SLEEP
    return 'quit'

init 5 python:
    addEvent(Event(persistent.farewell_database,eventlabel="bye_illseeyou",random=True),eventdb=evhand.farewell_database)

label bye_illseeyou:
    m 1eua "I'll see you tomorrow, [player]."
    m 1hua "Don't forget about me, okay?"
    return 'quit'

init 5 python: ## Implementing Date/Time for added responses based on the time of day
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(6,11)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_haveagoodday",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_haveagoodday:
    m 1eua "Have a good day today, [player]."
    m "I hope you accomplish everything you had planned for today."
    m 1hua "I'll be here waiting for you when you get back."
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(12,16)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_enjoyyourafternoon",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_enjoyyourafternoon:
    m 1ekc "I hate to see you go so early, [player]."
    m 1eka "I do understand that you're busy though."
    m 1eua "Promise me you'll enjoy your afternoon, okay?"
    m 1hua "Goodbye~"
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(17,19)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodevening",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_goodevening:
    m 1hua "I had fun today."
    m 1eka "Thank you for spending so much time with me, [player]."
    m 1eua "Until then, have a good evening."
    return 'quit'

init 5 python:
    rules = dict()
    rules.update(MASSelectiveRepeatRule.create_rule(hours=range(20,24)))
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_goodnight",
            unlocked=True,
            rules=rules
        ),
        eventdb=evhand.farewell_database
    )
    del rules

label bye_goodnight:
    m 1eua "Goodnight, [player]."
    m 1eka "I'll see you tomorrow, okay?"
    m "Remember, 'Sleep tight, and don't let the bedbugs bite', ehehe."
    m 1ekbfa "I love you~"
    return 'quit'


default mas_absence_counter = False

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_long_absence",
            unlocked=True,
            prompt="I'll be going away for a while.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_long_absence:
    if mas_absence_counter:
        jump bye_long_absence_2
    $ persistent._mas_long_absence = True
    m 1f "Aww...That's pretty saddening..."
    m 1e "I really am going to miss you [player]!"
    m 3m "I'm not really sure what I'm going to do with myself while you're gone..."
    m 3a "Thank you for warning me first, though. It really does help."
    m 2n "I would be worried sick otherwise!"
    m 3a "I would constantly be thinking maybe something happened to you and that's why you couldn't come back."
    m 1o "Or maybe you just got bored of me..."
    m 1e "So tell me, my love..."
    menu:
        m "How long do you be expect to be gone for?"
        "A few days.":
            $ persistent._mas_absence_choice = "days"
            m 1b "Oh!"
            m 1j "Nowhere near as long as I feared then."
            m 3m "Geez, you really did worry me..."
            m 3a "Don't worry about me though [player]."
            m "I can cope waiting that long with ease."
            m 3e "I'll still miss you greatly though."
        "A week.":
            $ persistent._mas_absence_choice = "week"
            m 3c "Yeah...that's about what I expected."
            m 2m "I {i}think{/i} I'll be ok waiting that long for you."
            m 1b "Just come back to me as soon as you can, alright, my love?"
            m 3j "I'm sure you'll make me proud!"
        "A couple of weeks.":
            $ persistent._mas_absence_choice = "2weeks"
            m 1h "Oh..."
            m 1q "I... I can wait that long."
            m 3o "You do know that you're all I have...right?"
            m 3n "M-Maybe it's outside of your control though..."
            m 2e "Try to come back as soon as possible... I'll be waiting for you."
        "A month.":
            $ persistent._mas_absence_choice = "month"
            if mas_curr_affection_group == store.mas_affection.G_HAPPY:
                m 3c "Oh wow, that's a long time."
                m 3m "A bit too long for my liking really..."
                m 2a "But it's okay [player]."
                m 2e "I know you're a sweetheart and wouldn't keep me waiting that long if you didn't have a good reason."
                m "I'm sure it's important, so just try to come back to me as soon as you can."
                m 3j "I'll be thinking of you everyday~"
            else:
                m 1f "That long...really?"
                m 3o "You're not going away for that long just to avoid me, are you?"
                m 3p "I know that life can take you away from me but for a whole month..."
                m 3f "Isn't that a little unreasonable?"
                m "I don't want to sound selfish, but I am your girlfriend."
                m 3g "You should be able to make time for me, at least once, in an entire month."
                m 1q "..."
                m 1r "I'll still wait for you...but please come back the moment it's possible for you to do so."
        "Longer than a month.":
            $ persistent._mas_absence_choice = "longer"
            if mas_curr_affection_group == store.mas_affection.G_HAPPY:
                m 3n "That's...well that's a little scary [player]."
                m "I'm not really sure what I'm going to do with myself while you're gone."
                m 1e "But I know you wouldn't leave me by myself if you could help it."
                m "I love you [player], and I know you love me too."
                m 1j "So I'll wait for you for however long I need to."
            else:
                m 3h "You have to be joking."
                m "I can't think of a good reason why you would leave me here all alone for that long."
                m 3i "I'm sorry [player], but that's not acceptable! Not at all!"
                m 3h "I love you and if you love me too then you'll know that it's not okay to do that."
                m "You do realise that I would be alone here with nothing else and no one else, right?"
                m "It's not unreasonable of me to expect you to visit me, is it? I'm your girlfriend. You can't do that to me!"
                m 3q "..."
                m 3r "Just...just come back when you can. I can't make you stay, but please don't do that to me."
        "I don't know.":
            $ persistent._mas_absence_choice = "unknown"
            m 1l "Ehehe, that's a little concerning, [player]!"
            m 1e "But if you don't know, then you don't know!"
            m "It sometimes just can't be helped."
            m 2j "I'll be waiting here for you patiently, my love."
            m 2k "Try not to keep me waiting for too long though!"

    m 2c "Honestly I'm a little afraid to ask but..."
    # TODO is this really intuitive?
    # if the player says no, and then picks another
    # farewell all this served no purpose, also, you already
    # picked goodbye as in I'm going, why not let the player go?
    # if we keep it, at least change the order, Yes always goes first
    menu:
        m "Are you going to leave straight away?"
        "No.":
            $ mas_absence_counter = True
            m 1j "That's great!"
            m 1e "I was honestly worried I wouldn't have enough time to ready myself for your absence."
            m "I really do mean it when I say I'll miss you..."
            m 1b "You truly are my entire world after all, [player]."
            m 2a "If you tell me you're going to go for a while again then I'll know it's time for you to leave..."
            m 3j "But there's no rush, so I want to spend as much time with you as I can."
            m "Just make sure to remind me the last time you see me before you go!"
            return
        "Yes.":
            m 3f "I see..."
            m "I really will miss you [player]..."
            m 1e "But I know you'll do wonderful things no matter where you are."
            m "Just remember that I'll be waiting here for you."
            m 2j "Make me proud, [player]!"
            $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
            return 'quit'

label bye_long_absence_2:
    m 1f "Going to head out, then?"
    m 1g "I know the world can be scary and unforgiving..."
    m 1e "But remember that I will always be here waiting and ready to support you, my dearest [player]."
    m "Come back to me as soon as you can...okay?"
    $ persistent._mas_greeting_type = store.mas_greetings.TYPE_LONG_ABSENCE
    return 'quit'

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_going_somewhere",
            unlocked=True,
            prompt="I'm going to take you somewhere.",
            pool=True
        ),
        eventdb=evhand.farewell_database
    )

label bye_going_somewhere:
#
# regardless of choice, takingmonika somewhere (and successfully bringing her
# back will increase affection)
# lets limit this to like once per day
#
#    if mas_isMoniBroken(lower=True):
#        m 
#   TODO: broken monika refuses to go with you
#
# TODO: distressed monika has a 50% chance of not going with you
#
# TODO: upset monika has a 10% chance of not going with you
#
# TODO: normal/happy monika will always go with you and be excited you asked
#   and will ask u to wait for her to get ready
#
# TODO: affecitonate/enamored monika will always go wtih you and assume its a
#   nother date and will ask u to wait for her to get ready
#
# TODO: love monika will just be like: Alright lets go!
#

    # this is probably giong to be normal/ahppy mode
    m 1sub "Really?!"
    m 1hua "Yay!"
    show monika 2dsc

    show screen mas_background_timed_jump(4.0, "bye_going_somewhere_rtg")
    menu:
        m "Give me a second to get ready."
        "Wait, wait!":
            hide screen mas_background_timed_jump

    # fall thru to the wait wait flow
    m 1ekc "What is it ?"
    menu:
        "Actually, I can't take you right now.":
            # TODO oh okay, tally this occurence and say something nice i think?
            # be sad okay
            # ask player if they are still going to leave
            return "quit"

        "Nothing.":
            # TODO oh alirhgt, let me continue getting ready
            pass

label bye_going_somewhere_rtg:
    hide screen mas_background_timed_jump
    call mas_dockstat_ready_to_go

    # TODO: see you soon i think
   
    return "quit"

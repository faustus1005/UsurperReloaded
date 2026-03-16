{$IFNDEF MSDOS}
{$I DEFINES.INC}
{$ENDIF}
{

Copyright 2007 Jakob Dangarden

 This file is part of Usurper.

    Usurper is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Usurper is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Usurper; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
}

unit EdRings;

interface

procedure Reset_Rings;

implementation

uses
  init, obj_ad;

procedure Reset_Rings;
begin
              {typ av objekt :
                               1. head
                               2. body
                               3. arms
                               4. hands
                               5. fingers
                               6. legs
                               7. feets
                               8. waist
                               9. neck
                              10. face
                              11. shield
                              12. mat
                              13. dryck
                              14. vapen }

  {** Ringar **}
  Add_Object('Copper Ring', {name}
    Fingers,   {typ}
    1500,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    15,        {”ka mana}
    1,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    17,        {max level att hittas i dngs}
    'You see nothing special.',
    '',        {normal beskrivning 2}
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Brown Ring', {name}
    Fingers,   {typ}
    15000,     {v„rde i gold}
    25,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Looks like a normal party ring',
    '',        {normal beskrivning 2}
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    'Handy Blackdwarf craftmanship. This ring has magic abilities.',
    '',
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Small Black Ring', {name}
    Fingers,   {typ}
    30000,     {v„rde i gold}
    30,        {”ka/minska hps}
    10,        {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A small and funny looking ring. It has some runes on it.',
    'But you cannot interpret them...',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Dusty Blue Ring', {name}
    Fingers,   {typ}
    150,       {v„rde i gold} -15,       {”ka/minska hps} -5,        {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    True,      {cursed item?}
    10,        {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'The ring has some strange symbols on it : "Axkna Whamna Straghd".',
    'It starts to glow when you touch it...',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    'This ring is a copy of the evil Witchmasters favourite EYE-ring.',
    'It is only useful to some magic users.',
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Silver Ring', {name}
    Fingers,   {typ}
    45000,     {v„rde i gold}
    30,        {”ka/minska hps}
    15,        {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    25,        {”ka wisdom}
    40,        {”ka mana}
    0,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    True,      {cursed item?}
    25,        {min level att hittas i dngs}
    75,        {max level att hittas i dngs}
    'A classic Silver Ring... No visible symbols.',
    '',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    'Magic Users should use this ring.',
    'It is known to disappear when you least expect it.',
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Blue Ring', {name}
    Fingers,   {typ}
    45000,     {v„rde i gold} -10,       {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    5,         {”ka wisdom}
    50,        {”ka mana}
    5,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Measles,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    35,        {min level att hittas i dngs}
    85,        {max level att hittas i dngs}
    '',
    'There is nothing special about this ring.',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    'Magic Users should use this ring.',
    'It is known to disappear when you least expect it.',
    'This ring protects its owner.',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Ring of Life', {name}
    Fingers,   {typ}
    370000,    {v„rde i gold}
    70,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    5,         {”ka wisdom}
    20,        {”ka mana}
    20,        {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Plague,    {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    40,        {min level att hittas i dngs}
    70,        {max level att hittas i dngs}
    '',
    'There is nothing special about this ring.',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    'They say that the Ring of Life can bring misery to its owner.',
    'It is not wise to be evil and wear this ring.',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Grey Ring', {name}
    Fingers,   {typ}
    25,        {v„rde i gold} -5,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    '',
    'There is nothing special about this ring.',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    'This ring is worthless.',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}


  Add_Object('Turtle Ring', {name}
    Fingers,   {typ}
    175000,    {v„rde i gold}
    5,         {”ka/minska hps}
    5,         {”ka stamina}
    5,         {”ka agility}
    5,         {”ka charisma}
    5,         {”ka dexterity}
    5,         {”ka wisdom}
    5,         {”ka mana}
    5,         {”ka armor v„rde}
    5,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    '',
    'The ring makes you happy, just by looking at it.',
    'It has a mystical aura of light.',
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}


  Add_Object('Steel Ring', {name}
    Fingers,    {typ}
    25000,      {v„rde i gold}
    10,         {”ka/minska hps}
    0,          {”ka stamina}
    15,         {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    0,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Smallpox,   {kurerar}
    True,       {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    10,         {min level att hittas i dngs}
    90,         {max level att hittas i dngs}
    'You see nothing special.',
    '',
    '',
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Bronze Ring', {name}
    Fingers,   {typ}
    90000,     {v„rde i gold}
    25,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    15,        {”ka charisma}
    0,         {”ka dexterity}
    15,        {”ka wisdom}
    0,         {”ka mana}
    5,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
    '',
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}


  Add_Object('Gold Ring', {name}
    Fingers,   {typ}
    90000,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    90,        {”ka mana}
    7,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    25,        {min level att hittas i dngs}
    80,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
    '',
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}


  Add_Object('Green Ring', {name}
    Fingers,    {typ}
    10000,      {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    15,         {”ka mana}
    7,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    10,         {min level att hittas i dngs}
    50,         {max level att hittas i dngs}
    'There are strange symbols inscribed on the inside of the ring.',
    '',
    '',
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Moon Ring', {name}
    Fingers,   {typ}
    20000,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    25,        {”ka mana}
    4,         {”ka armor v„rde}
    1,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Blindness, {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
    '',
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Crystal Ring', {name}
    Fingers,   {typ}
    5000,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    2,         {”ka armor v„rde}
    2,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'The ring shines with a soft light.',
    '',
    '',
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

end;

end.

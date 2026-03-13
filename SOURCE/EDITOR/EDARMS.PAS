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

unit EdArms;

interface

procedure Reset_Arms;

implementation

uses
  init, obj_ad;

procedure Reset_Arms;
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

  Add_Object('Grass Straps',   {name}
    Arms,       {typ}
    250,        {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    1,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    True,       {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    1,          {min level att hittas i dngs}
    5,          {max level att hittas i dngs}
    'You see nothing special',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    0,          {”ka strength}
    0,          {”ka defence}
    0);         {strength demanded to use object}

  Add_Object('Wool Straps',   {name}
    Arms,       {typ}
    1000,       {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    2,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    True,       {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    2,          {min level att hittas i dngs}
    7,          {max level att hittas i dngs}
    'You see nothing special',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    0,          {”ka strength}
    0,          {”ka defence}
    0);         {strength demanded to use object}

  Add_Object('Leather Straps',   {name}
    Arms,       {typ}
    2500,       {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    3,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    True,       {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    4,          {min level att hittas i dngs}
    15,         {max level att hittas i dngs}
    'You see nothing special',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    0,          {”ka strength}
    0,          {”ka defence}
    0);         {strength demanded to use object}

  Add_Object('Heavy Leather Straps',   {name}
    Arms,       {typ}
    5500,       {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    4,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    10,         {min level att hittas i dngs}
    25,         {max level att hittas i dngs}
    'You see nothing special',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    0,          {”ka strength}
    0,          {”ka defence}
    0);         {strength demanded to use object}

  Add_Object('Battle Straps',   {name}
    Arms,       {typ}
    25500,      {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    7,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    25,         {min level att hittas i dngs}
    45,         {max level att hittas i dngs}
    'You see nothing special',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    0,          {”ka strength}
    0,          {”ka defence}
    0);         {strength demanded to use object}

  Add_Object('Zulu War Rings',   {name}
    Arms,       {typ}
    50500,      {v„rde i gold}
    35,         {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    10,         {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    55,         {min level att hittas i dngs}
    58,         {max level att hittas i dngs}
    'Golden War Rings of famed Zulu origin.',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    0,          {”ka strength}
    0,          {”ka defence}
    0);         {strength demanded to use object}

  Add_Object('Adder Protection',   {name}
    Arms,       {typ}
    150000,     {v„rde i gold}
    25,         {”ka/minska hps}
    5,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    10,         {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    True,       {finnas i shoppen}
    False,      {kunna hittas i dungeons?}
    False,      {cursed item?}
    55,         {min level att hittas i dngs}
    58,         {max level att hittas i dngs}
    'The Adder is the only thing that can stop UR.',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    10,         {”ka strength}
    10,         {”ka defence}
    0);         {strength demanded to use object}

  Add_Object('Turmoil Bolts',   {name}
    Arms,       {typ}
    750000,     {v„rde i gold}
    65,         {”ka/minska hps}
    20,         {”ka stamina}
    10,         {”ka agility}
    10,         {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    60,         {”ka mana}
    0,          {”ka armor v„rde}
    80,         {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    80,         {min level att hittas i dngs}
    90,         {max level att hittas i dngs}
    'Big and bulky this protection can stop almost anything.',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    20,         {”ka strength}
    20,         {”ka defence}
    50);        {strength demanded to use object}

  Add_Object('Thunder Bolts',   {name}
    Arms,       {typ}
    170000,     {v„rde i gold}
    15,         {”ka/minska hps}
    5,          {”ka stamina}
    10,         {”ka agility}
    10,         {”ka charisma}
    0,          {”ka dexterity}
    0,         {”ka wisdom} -5,        {”ka mana}
    0,          {”ka armor v„rde}
    80,         {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Measles,    {kurerar}
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    70,         {min level att hittas i dngs}
    80,         {max level att hittas i dngs}
    'Enchanted arm protection.',
    '',         {normal beskrivning 2}
    '',         {normal beskrivning 3}
    '',         {normal beskrivning 4}
    '',         {normal beskrivning 5}
    '',         {detaljerad beskrivning 1}
    '',         {detaljerad beskrivning 2}
    '',         {detaljerad beskrivning 3}
    '',         {detaljerad beskrivning 4}
    '',         {detaljerad beskrivning 5}
    5,          {”ka strength}
    15,         {”ka defence}
    30);        {strength demanded to use object}

  {   4: armor_name:='Studded Leather Straps';
      7: armor_name:='Orcish Infantry Straps';
      9: armor_name:='Old and Dirty Straps';
      11: armor_name:='Elven Plate Straps'; }

end;

end.

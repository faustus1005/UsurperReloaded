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

unit EdFood;

interface

procedure Reset_Food;

implementation

uses
  init, obj_ad;

procedure Reset_Food;
begin
 {typ av objekt (ttype) :
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
  14. vapen
  15. around body}

  {** Žtbart **}

  Add_Object('Fried Chicken',   {name}
    Food,      {typ}
    10,        {v„rde i gold}
    15,        {”ka/minska hps}
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
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A delicious chicken!',
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

  Add_Object('Dog Biscuit',   {name}
    Food,      {typ}
    2,         {v„rde i gold}
    5,         {”ka/minska hps}
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
    True,      {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    5,         {min level att hittas i dngs}
    6,         {max level att hittas i dngs}
    'Hmmm... Dog food.',
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

  Add_Object('Criossant',   {name}
    Food,      {typ}
    5,         {v„rde i gold}
    6,         {”ka/minska hps}
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
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Pure Continental Breakfast.',
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

  Add_Object('Lobster',
    Food,      {typ}
    95,        {v„rde i gold}
    15,        {”ka/minska hps}
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
    11,        {min level att hittas i dngs}
    20,        {max level att hittas i dngs}
    'A delicious lobster! Mmmm...',
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

  Add_Object('Hunk of Meat',   {name}
    Food,      {typ}
    20,        {v„rde i gold}
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
    50,        {min level att hittas i dngs}
    55,        {max level att hittas i dngs}
    'Mmmm... looks good enough to eat.',
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

  Add_Object('Pork Chop',   {name}
    Food,      {typ}
    75,        {v„rde i gold}
    15,        {”ka/minska hps}
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
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Fresh Pork!',
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

  Add_Object('Pomegranate',   {name}
    Food,      {typ}
    1,         {v„rde i gold} -25,       {”ka/minska hps}
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
    'An Apple is it ?',
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

  Add_Object('Dead Rat',   {name}
    Food,      {typ}
    5,         {v„rde i gold}
    5,         {”ka/minska hps}
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
    'Yieck! A big black rat! Are you gonna eat this?',
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

  Add_Object('IceCream',   {name}
    Food,      {typ}
    10,        {v„rde i gold} -5,        {”ka/minska hps}
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
    True,      {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    15,        {min level att hittas i dngs}
    30,        {max level att hittas i dngs}
    'A cold piece of ice. Can this be IceCream?!',
    '',        {normal beskrivning 2}
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Bread',   {name}
    Food,               {typ}
    100,                {v„rde i gold}
    50,                 {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    0,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    True,               {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'A bread. Nothing more, nothing less.',
    'It looks very tasty...',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',
    '',
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Apple',   {name}
    Food,               {typ}
    3,                  {v„rde i gold}
    3,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    0,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    True,               {finnas i shoppen}
    True,               {kunna hittas i dungeons?}
    False,              {cursed item?}
    38,                 {min level att hittas i dngs}
    88,                 {max level att hittas i dngs}
    'A green apple.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',
    '',
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

end;

end.

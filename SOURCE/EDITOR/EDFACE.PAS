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

unit EdFace;

interface


procedure Reset_Face;

implementation

uses
  init, obj_ad;

procedure Reset_Face;
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
  14. vapen}


  {* Ansikts prylar * }

  Add_Object('Usher Protection', {name}
    Face,      {typ}
    2500,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    2,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    15,        {max level att hittas i dngs}
    'Standard infantry mode.',
    '',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    2,         {”ka strength}
    2,         {”ka defence}
    1);        {strength demanded to use object}

  Add_Object('Veil',
    Face,      {typ}
    9400,      {v„rde i gold}
    15,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    5,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    1,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Measles,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    5,         {”ka strength}
    0,         {”ka defence}
    1);        {strength demanded to use object}

  Add_Object('Snake Mask', {name}
    Face,      {typ}
    250,       {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    15,        {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    1,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    15,        {max level att hittas i dngs}
    'Can scare a few enemies.',
    '',
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

  Add_Object('Wopas Face', {name}
    Face,      {typ}
    150,       {v„rde i gold}
    0,         {”ka/minska hps}
    10,        {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    1,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    15,        {max level att hittas i dngs}
    '',
    '',
    '',
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

  Add_Object('Death Mask', {name}
    Face,       {typ}
    5000,       {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    5,          {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    True,       {finnas i shoppen}
    False,      {kunna hittas i dungeons?}
    False,      {cursed item?}
    1,          {min level att hittas i dngs}
    99,         {max level att hittas i dngs}
    'It is black with yellow stripes.',
    '',
    '',               {normal beskrivning 3}
    '',               {normal beskrivning 4}
    '',               {normal beskrivning 5}
    '',               {detaljerad beskrivning 1}
    '',               {detaljerad beskrivning 2}
    '',               {detaljerad beskrivning 3}
    '',               {detaljerad beskrivning 4}
    '',               {detaljerad beskrivning 5}
    0,                {”ka strength}
    0,                {”ka defence}
    0);               {strength demanded to use object}

  Add_Object('Crape', {name}
    Face,             {typ}
    2500,             {v„rde i gold}
    10,               {”ka/minska hps}
    0,                {”ka stamina}
    0,                {”ka agility}
    0,                {”ka charisma}
    0,                {”ka dexterity}
    0,                {”ka wisdom}
    0,                {”ka mana}
    0,                {”ka armor v„rde}
    0,                {”ka attack v„rde}
    '',               {„gd av?}
    False,            {bara EN i spelet}
    Nothing,          {kurerar}
    True,             {finnas i shoppen}
    True,             {kunna hittas i dungeons?}
    False,            {cursed item?}
    25,               {min level att hittas i dngs}
    35,               {max level att hittas i dngs}
    'A Funeral must.',
    '',
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

  Add_Object('Senior Scare', {name}
    Face,      {typ}
    750,       {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    15,        {”ka wisdom}
    15,        {”ka mana}
    2,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
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

  Add_Object('Black Mask', {name}
    Face,      {typ}
    10000,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    7,         {”ka armor v„rde}
    7,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
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

     { 1: armor_name:='Grass Mask';
      2: armor_name:='Wool Mask';
      3: armor_name:='Leather Mask';
      4: armor_name:='Iron Mask';
      5: armor_name:='Turtle Mask';
      6: armor_name:='Steel Mask';
      7: armor_name:='Golden Priest Mask';
      8: armor_name:='Old Mask';
      9: armor_name:='Mask of the Titans';
      10: armor_name:='Tiger Mask';
      11: armor_name:='Lion Mask';
      12: armor_name:='Druid Sacrifical Mask';
      13: armor_name:='Mask of the Undead';
      14: armor_name:='Black Death Mask';
      15: armor_name:='Great Demon Mask';}

end;

end.

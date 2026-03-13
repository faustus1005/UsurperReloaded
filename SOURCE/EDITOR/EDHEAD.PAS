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

unit EdHead;

interface

procedure Reset_Head;

implementation

uses
  init, obj_ad;

procedure Reset_Head;
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


  {** Hj„lmar, och annat man har p† huvudet **}

  Add_Object('Grass Helmet', {name}
    Head,      {typ}
    100,       {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
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
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    10,        {max level att hittas i dngs}
    'The helmet doesn' + chr(39) + 't look like that it can protect',
    'from very much damage.',
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

  Add_Object('Old Crown', {name}
    Head,      {typ}
    150,       {v„rde i gold} -1,         {”ka/minska hps}
    0,         {”ka stamina}
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
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A dusty old crown. Looks like a medieval type of crown.',
    '',
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

  Add_Object('Black Crown', {name}
    Head,       {typ}
    5000,       {v„rde i gold}
    15,         {”ka/minska hps}
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
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    1,          {min level att hittas i dngs}
    99,         {max level att hittas i dngs}
    'You see nothing special.',
    '',
    '',                  {normal beskrivning 3}
    '',                  {normal beskrivning 4}
    '',                  {normal beskrivning 5}
    '',                  {detaljerad beskrivning 1}
    '',                  {detaljerad beskrivning 2}
    '',                  {detaljerad beskrivning 3}
    '',                  {detaljerad beskrivning 4}
    '',                  {detaljerad beskrivning 5}
    0,                   {”ka strength}
    0,                   {”ka defence}
    0);                  {strength demanded to use object}

  Add_Object('Flat Cap', {name}
    Head,                {typ}
    2500,                {v„rde i gold}
    0,                   {”ka/minska hps}
    0,                   {”ka stamina}
    0,                   {”ka agility}
    0,                   {”ka charisma}
    0,                   {”ka dexterity}
    0,                   {”ka wisdom}
    0,                   {”ka mana}
    2,                   {”ka armor v„rde}
    0,                   {”ka attack v„rde}
    '',                  {„gd av?}
    False,               {bara EN i spelet}
    Nothing,             {kurerar}
    True,                {finnas i shoppen}
    False,               {kunna hittas i dungeons?}
    False,               {cursed item?}
    1,                   {min level att hittas i dngs}
    99,                  {max level att hittas i dngs}
    'A grey dull cap. Used by peasants.',
    '',
    '',                  {normal beskrivning 3}
    '',                  {normal beskrivning 4}
    '',                  {normal beskrivning 5}
    '',                  {detaljerad beskrivning 1}
    '',                  {detaljerad beskrivning 2}
    '',                  {detaljerad beskrivning 3}
    '',                  {detaljerad beskrivning 4}
    '',                  {detaljerad beskrivning 5}
    0,                   {”ka strength}
    0,                   {”ka defence}
    0);                  {strength demanded to use object}

  Add_Object('Evil Cap', {name}
    Head,                {typ}
    7500,                {v„rde i gold}
    15,                  {”ka/minska hps}
    0,                   {”ka stamina}
    0,                   {”ka agility}
    0,                   {”ka charisma}
    0,                   {”ka dexterity}
    0,                   {”ka wisdom}
    0,                   {”ka mana}
    4,                   {”ka armor v„rde}
    0,                   {”ka attack v„rde}
    '',                  {„gd av?}
    False,               {bara EN i spelet}
    Smallpox,            {kurerar}
    True,                {finnas i shoppen}
    False,               {kunna hittas i dungeons?}
    False,               {cursed item?}
    1,                   {min level att hittas i dngs}
    99,                  {max level att hittas i dngs}
    'A Bathing Cap.',
    '',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    10,        {”ka strength}
    10,        {”ka defence}
    10);       {strength demanded to use object}

  Add_Object('Snake Helmet', {name}
    Head,      {typ}
    75,        {v„rde i gold}
    0,         {”ka/minska hps}
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
    30,        {max level att hittas i dngs}
    '',
    '',
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    1,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}

  Add_Object('Green Beret', {name}
    Head,      {typ}
    7000,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    4,         {”ka armor v„rde}
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

  Add_Object('Death Helmet', {name}
    Head,      {typ}
    17000,     {v„rde i gold}
    15,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    15,        {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    7,         {”ka armor v„rde}
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

  Add_Object('Orc Helmet', {name}
    Head,      {typ}
    10000,     {v„rde i gold}
    10,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    25,        {”ka mana}
    4,         {”ka armor v„rde}
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

  Add_Object('Troll Helmet', {name}
    Head,      {typ}
    7000,      {v„rde i gold}
    0,         {”ka/minska hps}
    15,        {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    35,        {”ka mana}
    3,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    '',
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

  Add_Object('Turmoil Helmet', {name}
    Head,      {typ}
    10,        {v„rde i gold} -5,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde} -5,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    True,      {cursed item?}
    20,        {min level att hittas i dngs}
    50,        {max level att hittas i dngs}
    '',
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

  Add_Object('Skull-Cap', {name}
    Head,      {typ}
    700,       {v„rde i gold}
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
    25,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
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

  Add_Object('Woolly Hat', {name}
    Head,       {typ}
    1700,       {v„rde i gold}
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
    False,      {kunna hittas i dungeons?}
    False,      {cursed item?}
    1,          {min level att hittas i dngs}
    99,         {max level att hittas i dngs}
    'The woolly is purple and quite ugly.',
    'However, a perfect choice during cold winterdays.',
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

  Add_Object('Deerstalker', {name}
    Head,       {typ}
    190000,     {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    30,         {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    False,      {finnas i shoppen}
    True,       {kunna hittas i dungeons?}
    False,      {cursed item?}
    80,         {min level att hittas i dngs}
    99,         {max level att hittas i dngs}
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

  Add_Object('Hymer Defence', {name}
    Head,      {typ}
    5800,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    3,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    7,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Measles,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    '',
    '',
    '',          {normal beskrivning 3}
    '',          {normal beskrivning 4}
    '',          {normal beskrivning 5}
    '',          {detaljerad beskrivning 1}
    '',          {detaljerad beskrivning 2}
    '',          {detaljerad beskrivning 3}
    '',          {detaljerad beskrivning 4}
    '',          {detaljerad beskrivning 5}
    0,           {”ka strength}
    0,           {”ka defence}
    0);          {strength demanded to use object}

  Add_Object('Crystal Crown', {name}
    Head,        {typ}
    15000,       {v„rde i gold}
    0,           {”ka/minska hps}
    0,           {”ka stamina}
    0,           {”ka agility}
    0,           {”ka charisma}
    0,           {”ka dexterity}
    0,           {”ka wisdom}
    50,          {”ka mana}
    3,           {”ka armor v„rde}
    0,           {”ka attack v„rde}
    '',          {„gd av?}
    False,       {bara EN i spelet}
    Nothing,     {kurerar}
    False,       {finnas i shoppen}
    True,        {kunna hittas i dungeons?}
    False,       {cursed item?}
    20,          {min level att hittas i dngs}
    70,          {max level att hittas i dngs}
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


  Add_Object('Stone Crown', {name}
    Head,      {typ}
    5,         {v„rde i gold} -15,       {”ka/minska hps} -5,        {”ka stamina} -5,
    {”ka agility} -5,        {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana} -4,        {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Big and ugly Crown. It is extremely heavy!',
    '',
    '',                  {normal beskrivning 3}
    '',                  {normal beskrivning 4}
    '',                  {normal beskrivning 5}
    '',                  {detaljerad beskrivning 1}
    '',                  {detaljerad beskrivning 2}
    '',                  {detaljerad beskrivning 3}
    '',                  {detaljerad beskrivning 4}
    '',                  {detaljerad beskrivning 5}
    0,                   {”ka strength}
    0,                   {”ka defence}
    0);                  {strength demanded to use object}

  Add_Object('Wool Cap', {name}
    Head,                {typ}
    150,                 {v„rde i gold}
    0,                   {”ka/minska hps}
    0,                   {”ka stamina}
    0,                   {”ka agility}
    0,                   {”ka charisma}
    0,                   {”ka dexterity}
    0,                   {”ka wisdom}
    0,                   {”ka mana}
    1,                   {”ka armor v„rde}
    0,                   {”ka attack v„rde}
    '',                  {„gd av?}
    False,               {bara EN i spelet}
    Nothing,             {kurerar}
    True,                {finnas i shoppen}
    False,               {kunna hittas i dungeons?}
    False,               {cursed item?}
    1,                   {min level att hittas i dngs}
    99,                  {max level att hittas i dngs}
    'A standard Wool Cap.',
    'Used by shepherds and peasants. Warm and cosy.',
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

  Add_Object('Straw Hat', {name}
    Head,      {typ}
    250,       {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    1,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
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
    'A rugged Straw. Nice to have when going fishing.',
    'Also often used for romantic escapades. Good charm effect.',
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

  Add_Object('Leather Helmet', {name}
    Head,       {typ}
    1000,       {v„rde i gold}
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
    'The most popular light weight helmet right now.',
    'Rangers are especially fond of it, because of its color',
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


  Add_Object('Stone Helmet', {name}
    Head,       {typ}
    2500,       {v„rde i gold}
    0,         {”ka/minska hps} -2,        {”ka stamina}
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
    1,          {min level att hittas i dngs}
    99,         {max level att hittas i dngs}
    'The helmet is grey and rugged. It looks heavy and robust.',
    'As there are no openings for the mouth or nose, you could',
    'expect it to get very warm during a fight.',
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


  Add_Object('Brass Helmet', {name}
    Head,      {typ}
    3750,      {v„rde i gold}
    5,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    8,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'This helmet is an excellent proof of blackdwarf craftmanship.',
    'It has no edges where a weapon can cause damage. It is',
    'completely smooth and glossy.',
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


  Add_Object('Iron Helmet', {name}
    Head,      {typ}
    5500,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    12,        {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Standard Paladin equipment. Often used by young',
    'knights at jousting tournaments.',
    'The helmet is round and bulky, with a little feather on top.',
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


  Add_Object('Silver Helmet', {name}
    Head,      {typ}
    10500,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    10,        {”ka mana}
    15,        {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'With this shiny masterpiece on your head you can',
    'call attention to yourself. By some, seen as',
    'more of a "show for your girlfriend thing", rather than',
    'a useful armor.',
    'The helmet has beautiful ornaments, and at the lower right',
    'side you can see sacral insignias.',
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}


  Add_Object('Bowler', {name}
    Head,              {typ}
    550,               {v„rde i gold}
    0,                 {”ka/minska hps}
    0,                 {”ka stamina}
    10,                {”ka agility}
    0,                 {”ka charisma}
    0,                 {”ka dexterity}
    0,                 {”ka wisdom}
    0,                 {”ka mana}
    1,                 {”ka armor v„rde}
    0,                 {”ka attack v„rde}
    '',                {„gd av?}
    False,             {bara EN i spelet}
    Nothing,           {kurerar}
    True,              {finnas i shoppen}
    False,             {kunna hittas i dungeons?}
    False,             {cursed item?}
    1,                 {min level att hittas i dngs}
    99,                {max level att hittas i dngs}
    'Your standard black bowler. With this on you can walk the',
    'streets like a gentleman. It is doubtful however, if it can',
    'stop an axe or something more vicious.',
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


  Add_Object('Bronze Helmet', {name}
    Head,       {typ}
    17900,      {v„rde i gold}
    0,          {”ka/minska hps}
    0,          {”ka stamina}
    0,          {”ka agility}
    0,          {”ka charisma}
    0,          {”ka dexterity}
    0,          {”ka wisdom}
    0,          {”ka mana}
    20,         {”ka armor v„rde}
    0,          {”ka attack v„rde}
    '',         {„gd av?}
    False,      {bara EN i spelet}
    Nothing,    {kurerar}
    True,       {finnas i shoppen}
    False,      {kunna hittas i dungeons?}
    False,      {cursed item?}
    1,          {min level att hittas i dngs}
    99,         {max level att hittas i dngs}
    'Also called "The Dragon Slayer". This is the first in the',
    'series of Bronze Deluxe Wares from Gato Blacksmith.',
    'When it arrived 50 years ago it was state of the art in',
    'the bronze market. It has been outdated but its still popular.',
    'It has two dragons inscribed on the front. Scary sight for foes.',
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    0,         {”ka strength}
    0,         {”ka defence}
    0);        {strength demanded to use object}


  Add_Object('The Destroyer', {name}
    Head,      {typ}
    4500,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    40,        {”ka mana}
    1,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Grim and beautiful.',
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


  Add_Object('Top Hat', {name}
    Head,               {typ}
    7500,               {v„rde i gold}
    5,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    5,                  {”ka dexterity}
    15,                 {”ka wisdom}
    15,                 {”ka mana}
    5,                  {”ka armor v„rde}
    0,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    True,               {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'Classic "Gandalf" model. It is blue with a yellow border',
    'at the brim.',
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


  Add_Object('Black Hood', {name}
    Head,      {typ}
    2000,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    7,         {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Classic "Hangman" model. It is black with two holes for',
    'the eyes. Primarily used by smalltime criminals and other',
    'lowlives.',
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


  Add_Object('Madmans Cap', {name}
    Head,      {typ}
    6700,      {v„rde i gold}
    20,        {”ka/minska hps} -5,        {”ka stamina}
    0,         {”ka agility}
    10,        {”ka charisma}
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
    '',
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


  Add_Object('White Helmet', {name}
    Head,      {typ}
    25000,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    30,        {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'This is the Heavy Combat Model.',
    'It is glimmering so strange that it could be enchanted',
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


  Add_Object('Glass Helmet', {name}
    Head,      {typ}
    36800,     {v„rde i gold} -5,        {”ka/minska hps} -2,        {”ka stamina}
    0,         {”ka agility}
    8,         {”ka charisma}
    8,         {”ka dexterity}
    28,        {”ka wisdom}
    50,        {”ka mana}
    28,        {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'The helmet is completely transparent!',
    'It is thick and robust, with a special chin protector.',
    'The glass glows when you touch it...',
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

  Add_Object('Laurel Wreath', {name}
    Head,      {typ}
    120000,    {v„rde i gold}
    100,       {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    35,        {”ka armor v„rde}
    0,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Blindness, {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    70,        {min level att hittas i dngs}
    75,        {max level att hittas i dngs}
    'It looks rather uncomfortable.',
    '',
    '',
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

end;









end.

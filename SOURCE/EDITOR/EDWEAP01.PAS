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

unit EdWeap01;

interface


procedure Reset_Monster_Weapons;

implementation

uses
  Init, Obj_Ad, edweap;

procedure Reset_Monster_Weapons;
begin

  {resetar globala counter,m1,m2 - f”r att statbaren skall kunna jobba}
  {statbar m†ste „ven veta totala antalet filer/poster}

  { ** Monster Vapen START ** }

  Add_Object('Staff',   {name}
    Weapon,    {typ}
    50,        {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    1,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'An oak staff.',
    '',        {normal beskrivning 2}
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

  Add_Object('Old Staff',   {name}
    Weapon,    {typ}
    75,        {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    2,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    2,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'An old oak staff.',
    '',        {normal beskrivning 2}
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

  Add_Object('Stone Hammer',   {name}
    Weapon,    {typ}
    750,       {v„rde i gold}
    5,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    1,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A heavy hammer.',
    '',        {normal beskrivning 2}
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

  Add_Object('White Blade',   {name}
    Weapon,    {typ}
    990,       {v„rde i gold}
    0,         {”ka/minska hps}
    10,        {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    2,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Plague,    {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A sharp blade.',
    '',        {normal beskrivning 2}
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

  Add_Object('Dirty Razor',   {name}
    Weapon,    {typ}
    1500,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    5,         {”ka mana}
    0,         {”ka armor v„rde}
    3,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'Wouldn' + chr(39) + 't recommend having a shave with this.',
    '',        {normal beskrivning 2}
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


  Add_Object('Black Blade',   {name}
    Weapon,    {typ}
    2000,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    2,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A thin black blade....',
    '',        {normal beskrivning 2}
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


  Add_Object('Huge Club',   {name}
    Weapon,    {typ}
    7500,      {v„rde i gold} -5,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    12,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    True,      {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'You see nothing special.',
    '',        {normal beskrivning 2}
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

  Add_Object('Dwarven Battle Hammer',   {name}
    Weapon,    {typ}
    27000,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    35,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A very fine weapon indeed.',
    '',        {normal beskrivning 2}
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

  Add_Object('Black Sword',   {name}
    Weapon,    {typ}
    47000,     {v„rde i gold} -15,       {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom} -15,       {”ka mana}
    0,         {”ka armor v„rde}
    45,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'An evil and scary looking sword. You can almost',
    'smell blood on it...',
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

  Add_Object('White Sword',   {name}
    Weapon,    {typ}
    57000,     {v„rde i gold}
    15,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    15,        {”ka mana}
    0,         {”ka armor v„rde}
    40,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A very fine elvish sword.',
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

  Add_Object('White Dagger',   {name}
    Weapon,    {typ}
    37000,     {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    25,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A very fine elvish dagger.',
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

  Add_Object('Black Axe',   {name}
    Weapon,    {typ}
    77000,     {v„rde i gold}
    25,        {”ka/minska hps}
    15,        {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    55,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'A very fine dwarven axe.',
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

  Add_Object('Red Pole',   {name}
    Weapon,    {typ}
    7000,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    75,        {”ka mana}
    0,         {”ka armor v„rde}
    20,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'This pole has a strange aura around it.',
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

  Add_Object('White Pole',   {name}
    Weapon,    {typ}
    140000,    {v„rde i gold}
    45,        {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    50,        {”ka mana}
    0,         {”ka armor v„rde}
    40,        {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    99,        {max level att hittas i dngs}
    'You see nothing special.',
    '',
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Hammer',  {name}
    Weapon,             {typ}
    1000,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    3,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'A big hammer.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Sharp Blade',   {name}
    Weapon,             {typ}
    750,                {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    4,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'A backstabbing tool.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Green Knife',   {name}
    Weapon,             {typ}
    3000,               {v„rde i gold}
    15,                 {”ka/minska hps}
    15,                 {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,         {”ka mana} -3,        {”ka armor v„rde}
    5,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'The "Gnoll Cutter" model. Long and with a thin blade.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Old Staff',   {name}
    Weapon,             {typ}
    50,        {v„rde i gold} -5,        {”ka/minska hps} -5,        {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    2,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    True,               {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('War Hammer',   {name}
    Weapon,             {typ}
    4000,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    15,                 {”ka mana}
    0,                  {”ka armor v„rde}
    5,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'A very heavy Battle Tool. You need strength to use this!',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Pole',    {name}
    Weapon,             {typ}
    450,                {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    2,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Crossbow',   {name}
    Weapon,             {typ}
    2500,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    6,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'Standard Orcish infantry model.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('ShortSword',   {name}
    Weapon,             {typ}
    1500,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    10,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Turtle Spear',  {name}
    Weapon,             {typ}
    6000,               {v„rde i gold}
    25,                 {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,         {”ka wisdom} -40,       {”ka mana}
    0,                  {”ka armor v„rde}
    15,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'The spear is is green with strange inscriptions on it.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Jumbo Sword',   {name}
    Weapon,             {typ}
    35000,              {v„rde i gold}
    50,                 {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,         {”ka charisma} -25,       {”ka dexterity}
    0,         {”ka wisdom} -25,       {”ka mana}
    0,                  {”ka armor v„rde}
    25,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Rapier',  {name}
    Weapon,             {typ}
    6750,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    7,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'A short rapier.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Supreme Staff',   {name}
    Weapon,             {typ}
    7000000,            {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    300,                {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'This is the largest Staff you have ever seen.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Razor',   {name}
    Weapon,             {typ}
    150,                {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    3,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    True,               {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'British Steel...',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('LongSword',   {name}
    Weapon,             {typ}
    5000,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    15,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Opal Club',   {name}
    Weapon,             {typ}
    85000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,         {”ka agility} -35,       {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    25,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'A very heavy item.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Sling',   {name}
    Weapon,             {typ}
    900,                {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    2,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Wood Axe',  {name}
    Weapon,             {typ}
    1900,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    5,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'Go and chop some wood.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Black Axe',  {name}
    Weapon,             {typ}
    19000,              {v„rde i gold}
    5,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    50,                 {”ka mana}
    0,                  {”ka armor v„rde}
    25,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'This item may be cursed.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Animated Axe',  {name}
    Weapon,             {typ}
    29000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    30,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'Wow! A flying Axe!',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Animated Sword',  {name}
    Weapon,             {typ}
    59000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    40,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'Wow! A flying Sword!',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Silver Dagger',  {name}
    Weapon,             {typ}
    190000,             {v„rde i gold}
    10,                 {”ka/minska hps}
    20,                 {”ka stamina}
    0,                  {”ka agility}
    50,                 {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    100,                {”ka mana}
    0,                  {”ka armor v„rde}
    90,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'A long elvish model. Looks enchanted somehow.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Long Cane',  {name}
    Weapon,             {typ}
    1900,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    3,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Jungle Knife',  {name}
    Weapon,             {typ}
    500,                {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,         {”ka mana} -3,        {”ka armor v„rde}
    0,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    True,               {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Stone Club',  {name}
    Weapon,             {typ}
    5000,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    7,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Halberd', {name}
    Weapon,             {typ}
    8900,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    15,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Ruin Axe', {name}
    Weapon,             {typ}
    19000,              {v„rde i gold}
    15,                 {”ka/minska hps}
    15,                 {”ka stamina}
    15,                 {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    18,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Snake Dagger', {name}
    Weapon,             {typ}
    180000,             {v„rde i gold}
    25,                 {”ka/minska hps}
    25,                 {”ka stamina}
    25,                 {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,         {”ka wisdom} -100,      {”ka mana}
    0,                  {”ka armor v„rde}
    58,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Cobra Dagger', {name}
    Weapon,             {typ}
    280000,             {v„rde i gold}
    100,                {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,         {”ka wisdom} -25,       {”ka mana}
    0,                  {”ka armor v„rde}
    18,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Focus Sword', {name}
    Weapon,             {typ}
    380000,             {v„rde i gold}
    15,                 {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    88,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Sting Axe', {name}
    Weapon,             {typ}
    12000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    20,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Golden Axe', {name}
    Weapon,             {typ}
    1200000,            {v„rde i gold}
    0,                  {”ka/minska hps}
    40,                 {”ka stamina}
    40,                 {”ka agility}
    40,                 {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    100,                {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Storm Sword', {name}
    Weapon,             {typ}
    2200000,            {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    200,                {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Flying Dagger', {name}
    Weapon,             {typ}
    2200,      {v„rde i gold} -5,        {”ka/minska hps}
    0,                  {”ka stamina}
    0,         {”ka agility} -15,       {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    40,                 {”ka mana}
    0,                  {”ka armor v„rde}
    2,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Divine Lance', {name}
    Weapon,             {typ}
    35000,              {v„rde i gold}
    15,                 {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    12,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Blood Axe', {name}
    Weapon,             {typ}
    15000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    25,                 {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    8,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Plague,             {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Twin Sword', {name}
    Weapon,             {typ}
    75000,              {v„rde i gold}
    45,                 {”ka/minska hps}
    0,         {”ka stamina} -5,        {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    15,                 {”ka mana}
    0,                  {”ka armor v„rde}
    26,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Great Staff', {name}
    Weapon,             {typ}
    85000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    15,                 {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    25,                 {”ka mana}
    0,                  {”ka armor v„rde}
    28,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Black Dagger', {name}
    Weapon,             {typ}
    185000,             {v„rde i gold}
    35,                 {”ka/minska hps}
    15,                 {”ka stamina}
    15,                 {”ka agility}
    15,                 {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    35,        {”ka mana} -5,        {”ka armor v„rde}
    35,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Black Sword', {name}
    Weapon,             {typ}
    140000,             {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    10,                 {”ka armor v„rde}
    25,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Black Pole', {name}
    Weapon,             {typ}
    35000,              {v„rde i gold}
    0,         {”ka/minska hps} -5,        {”ka stamina}
    25,                 {”ka agility}
    0,         {”ka charisma} -15,       {”ka dexterity}
    0,                  {”ka wisdom}
    35,                 {”ka mana}
    0,                  {”ka armor v„rde}
    15,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Green Sword', {name}
    Weapon,             {typ}
    25000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    39,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Storm Axe', {name}
    Weapon,             {typ}
    225000,             {v„rde i gold}
    0,                  {”ka/minska hps}
    50,                 {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    27,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Plague,             {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Divine Axe', {name}
    Weapon,             {typ}
    255000,             {v„rde i gold}
    50,                 {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    20,                 {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    15,                 {”ka mana}
    1,                  {”ka armor v„rde}
    30,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Divine Dagger', {name}
    Weapon,             {typ}
    15000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,         {”ka mana} -5,        {”ka armor v„rde}
    2,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    True,               {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Blood Sword', {name}
    Weapon,             {typ}
    375000,             {v„rde i gold}
    25,                 {”ka/minska hps}
    25,                 {”ka stamina}
    25,                 {”ka agility}
    25,                 {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    32,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Neo Spear', {name}
    Weapon,             {typ}
    250,                {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    15,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Double Sword', {name}
    Weapon,             {typ}
    350000,             {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    40,                 {”ka dexterity}
    15,                 {”ka wisdom}
    45,                 {”ka mana}
    0,                  {”ka armor v„rde}
    25,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Double Axe', {name}
    Weapon,             {typ}
    50000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    29,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Double Dagger', {name}
    Weapon,             {typ}
    75000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    24,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Solar Sword', {name}
    Weapon,             {typ}
    95000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    15,                 {”ka dexterity}
    15,                 {”ka wisdom}
    15,                 {”ka mana}
    0,                  {”ka armor v„rde}
    14,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Green Spade', {name}
    Weapon,             {typ}
    60000,              {v„rde i gold}
    0,                  {”ka/minska hps}
    0,                  {”ka stamina}
    0,                  {”ka agility}
    0,                  {”ka charisma}
    0,                  {”ka dexterity}
    0,                  {”ka wisdom}
    0,                  {”ka mana}
    0,                  {”ka armor v„rde}
    10,                 {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    True,               {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Black Longsword', {name}
    Weapon,             {typ}
    6000,               {v„rde i gold}
    0,                  {”ka/minska hps}
    0,         {”ka stamina} -3,        {”ka agility} -3,        {”ka charisma} -3,
    {”ka dexterity} -3,        {”ka wisdom} -15,       {”ka mana} -5,        {”ka armor v„rde}
    3,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    True,               {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Angel Lance', {name}
    Weapon,             {typ}
    35000,              {v„rde i gold}
    3,                  {”ka/minska hps}
    3,                  {”ka stamina}
    3,                  {”ka agility}
    3,                  {”ka charisma}
    3,                  {”ka dexterity}
    3,                  {”ka wisdom}
    3,                  {”ka mana}
    3,                  {”ka armor v„rde}
    3,                  {”ka attack v„rde}
    '',                 {„gd av?}
    False,              {bara EN i spelet}
    Nothing,            {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'You see nothing special.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}

  Add_Object('Ground Divider', {name}
    Weapon,             {typ}
    5000,               {v„rde i gold}
    10,                 {”ka/minska hps}
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
    All,                {kurerar}
    False,              {finnas i shoppen}
    False,              {kunna hittas i dungeons?}
    False,              {cursed item?}
    1,                  {min level att hittas i dngs}
    99,                 {max level att hittas i dngs}
    'The Divider is black and mysterious.',
    '',                 {normal beskrivning 2}
    '',                 {normal beskrivning 3}
    '',                 {normal beskrivning 4}
    '',                 {normal beskrivning 5}
    '',                 {detaljerad beskrivning 1}
    '',                 {detaljerad beskrivning 2}
    '',                 {detaljerad beskrivning 3}
    '',                 {detaljerad beskrivning 4}
    '',                 {detaljerad beskrivning 5}
    0,                  {”ka strength}
    0,                  {”ka defence}
    0);                 {strength demanded to use object}


  Reset_Weapons;

end;

end.

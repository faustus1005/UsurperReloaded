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

unit EdWeap3;

interface

uses
  init, Obj_Ad;

procedure Reset_weapons3;

implementation

procedure Reset_weapons3;
begin

  Add_Object('Black Axe',   {name}
    Weapon,    {typ}
    93000000,  {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    180,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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
    25);       {strength needed to use object}

  Add_Object('Horse-Whip',   {name}
    Weapon,    {typ}
    2500,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    3,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    1,         {min level att hittas i dngs}
    5,         {max level att hittas i dngs}
    'Now you only need a Horse...',
    '',        {normal beskrivning 2}
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    2,         {”ka strength}
    0,         {”ka defence}
    3);        {strength demanded to use object}

  Add_Object('Bayonet',   {name}
    Weapon,    {typ}
    1500,      {v„rde i gold}
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
    True,      {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    14,        {min level att hittas i dngs}
    17,        {max level att hittas i dngs}
    'A sharp bayonet it is...',
    '',        {normal beskrivning 2}
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    4,         {”ka strength}
    0,         {”ka defence}
    4);        {strength demanded to use object}

  Add_Object('Hay-Fork',   {name}
    Weapon,    {typ}
    500,       {v„rde i gold}
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
    Plague,    {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    2,         {min level att hittas i dngs}
    7,         {max level att hittas i dngs}
    'Now you only need a Horse...',
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
    2);        {strength demanded to use object}

  Add_Object('Meat Hook',   {name}
    Weapon,    {typ}
    5000,      {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    5,         {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    False,     {finnas i shoppen}
    True,      {kunna hittas i dungeons?}
    False,     {cursed item?}
    3,         {min level att hittas i dngs}
    5,         {max level att hittas i dngs}
    'A grim looking hook it is...',
    '',        {normal beskrivning 2}
    '',        {normal beskrivning 3}
    '',        {normal beskrivning 4}
    '',        {normal beskrivning 5}
    '',        {detaljerad beskrivning 1}
    '',        {detaljerad beskrivning 2}
    '',        {detaljerad beskrivning 3}
    '',        {detaljerad beskrivning 4}
    '',        {detaljerad beskrivning 5}
    3,         {”ka strength}
    3,         {”ka defence}
    5);        {strength demanded to use object}


  Add_Object('Red Axe',   {name}
    Weapon,    {typ}
    95000000,  {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    181,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Paladins Hammer',   {name}
    Weapon,    {typ}
    100000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    182,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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


  Add_Object('Supreme Dagger',   {name}
    Weapon,    {typ}
    120000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    183,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Club of Life',   {name}
    Weapon,    {typ}
    130000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    184,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Last Dragons Claw',   {name}
    Weapon,    {typ}
    150000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    185,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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


  Add_Object('Hammer of Satan',   {name}
    Weapon,            {typ}
    200000000,         {v„rde i gold}
    0,                 {”ka/minska hps}
    0,                 {”ka stamina}
    0,                 {”ka agility}
    0,                 {”ka charisma}
    0,                 {”ka dexterity}
    0,                 {”ka wisdom}
    0,                 {”ka mana}
    0,                 {”ka armor v„rde}
    186,               {”ka attack v„rde}
    '',                {„gd av?}
    False,             {bara EN i spelet}
    Nothing,           {kurerar}
    True,              {finnas i shoppen}
    False,             {kunna hittas i dungeons?}
    False,             {cursed item?}
    1,                 {min level att hittas i dngs}
    99,                {max level att hittas i dngs}
    'You see nothing special.',
    '',                {normal beskrivning 2}
    '',                {normal beskrivning 3}
    '',                {normal beskrivning 4}
    '',                {normal beskrivning 5}
    '',                {detaljerad beskrivning 1}
    '',                {detaljerad beskrivning 2}
    '',                {detaljerad beskrivning 3}
    '',                {detaljerad beskrivning 4}
    '',                {detaljerad beskrivning 5}
    0,                 {”ka strength}
    0,                 {”ka defence}
    0);                {strength demanded to use object}

  Add_Object('Scalpel',   {name}
    Weapon,            {typ}
    2000,              {v„rde i gold}
    0,                 {”ka/minska hps}
    0,                 {”ka stamina}
    0,                 {”ka agility}
    0,                 {”ka charisma}
    0,                 {”ka dexterity}
    0,                 {”ka wisdom}
    0,                 {”ka mana}
    0,                 {”ka armor v„rde}
    4,                 {”ka attack v„rde}
    '',                {„gd av?}
    False,             {bara EN i spelet}
    blindness,         {kurerar}
    True,              {finnas i shoppen}
    False,             {kunna hittas i dungeons?}
    False,             {cursed item?}
    1,                 {min level att hittas i dngs}
    99,                {max level att hittas i dngs}
    'The standard surgeon tool. Looks very sharp indeed ...',
    '',                {normal beskrivning 2}
    '',                {normal beskrivning 3}
    '',                {normal beskrivning 4}
    '',                {normal beskrivning 5}
    '',                {detaljerad beskrivning 1}
    '',                {detaljerad beskrivning 2}
    '',                {detaljerad beskrivning 3}
    '',                {detaljerad beskrivning 4}
    '',                {detaljerad beskrivning 5}
    0,                 {”ka strength}
    0,                 {”ka defence}
    0);                {strength demanded to use object}

  Add_Object('Whip',   {name}
    Weapon,            {typ}
    4000,              {v„rde i gold}
    0,                 {”ka/minska hps}
    0,                 {”ka stamina}
    0,                 {”ka agility}
    0,                 {”ka charisma}
    0,                 {”ka dexterity}
    0,                 {”ka wisdom}
    0,                 {”ka mana}
    0,                 {”ka armor v„rde}
    5,                 {”ka attack v„rde}
    '',                {„gd av?}
    False,             {bara EN i spelet}
    Nothing,           {kurerar}
    True,              {finnas i shoppen}
    False,             {kunna hittas i dungeons?}
    False,             {cursed item?}
    1,                 {min level att hittas i dngs}
    99,                {max level att hittas i dngs}
    'The whip is long and black. It looks as if it could',
    'do some interesting damage...',
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

  Add_Object('Neptunus Hammer',   {name}
    Weapon,    {typ}
    230000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    187,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Blade of Destiny',   {name}
    Weapon,    {typ}
    250000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    188,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Horn of the Future',   {name}
    Weapon,    {typ}
    300000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    189,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Indras Pole',   {name}
    Weapon,    {typ}
    350000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    190,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Enforcer',   {name}
    Weapon,    {typ}
    400000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    191,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Eruptor',   {name}
    Weapon,    {typ}
    450000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    192,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Warbanger',   {name}
    Weapon,    {typ}
    500000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    193,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Sword of Sauron',   {name}
    Weapon,    {typ}
    550000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    194,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Spear of Sun',   {name}
    Weapon,    {typ}
    600000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    195,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Crystal Sword',   {name}
    Weapon,    {typ}
    650000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    230,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Orion Sword',   {name}
    Weapon,    {typ}
    675000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    270,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Beholders Staff',   {name}
    Weapon,    {typ}
    700000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    300,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Decryptor',   {name}
    Weapon,    {typ}
    750000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    325,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Boltor',   {name}
    Weapon,    {typ}
    800000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    350,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('Dark Supreme',   {name}
    Weapon,    {typ}
    850000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    375,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

  Add_Object('*Last Blade*',   {name}
    Weapon,    {typ}
    900000000, {v„rde i gold}
    0,         {”ka/minska hps}
    0,         {”ka stamina}
    0,         {”ka agility}
    0,         {”ka charisma}
    0,         {”ka dexterity}
    0,         {”ka wisdom}
    0,         {”ka mana}
    0,         {”ka armor v„rde}
    400,       {”ka attack v„rde}
    '',        {„gd av?}
    False,     {bara EN i spelet}
    Nothing,   {kurerar}
    True,      {finnas i shoppen}
    False,     {kunna hittas i dungeons?}
    False,     {cursed item?}
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

end;

end.

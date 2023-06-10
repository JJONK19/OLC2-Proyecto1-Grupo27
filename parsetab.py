
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftCOMAleftORleftANDrightNOTleftIGUALACIONDISTINTOleftMENORQMAYORQMAYORIGMENORIGleftMASMENOSleftMULDIVMODleftPARENIPARENDleftPOTrightUNARIOAND CADENA COMA CORD CORI DECIMAL DISTINTO DIV DOSPTS ENTERO ID IGUAL IGUALACION LLAVED LLAVEI MAS MAYORIG MAYORQ MENORIG MENORQ MENOS MOD MUL NOT OR PAREND PARENI POT PT PTCOMA RANY RBOOLEAN RCONCAT RCONSOLE RELSE REXPONENTIAL RFALSE RFIXED RIF RINTERFACE RLC RLET RLOG RNULL RNUMBER RSPLIT RSTRING RTRUE RTSTRING RUC\n            inicio : sentencias\n        \n            sentencias : sentencias sentencia \n                      | sentencia\n        \n            sentencia : print PTCOMA\n                        | expresion PTCOMA\n                        | declaraciones PTCOMA\n                        | if PTCOMA\n        \n            if : RIF PARENI expresion PAREND LLAVEI sentencias LLAVED elseif RELSE LLAVEI sentencias LLAVED\n                | RIF PARENI expresion PAREND LLAVEI sentencias LLAVED RELSE LLAVEI sentencias LLAVED\n                | RIF PARENI expresion PAREND LLAVEI sentencias LLAVED elseif\n                | RIF PARENI expresion PAREND LLAVEI sentencias LLAVED\n                \n        \n            elseif : elseif RELSE RIF PARENI expresion PAREND LLAVEI sentencias LLAVED \n                | RELSE RIF PARENI expresion PAREND LLAVEI sentencias LLAVED\n        \n            declaraciones : RLET ID DOSPTS tipo IGUAL expresion \n                    | RLET ID \n        \n            declaraciones : RLET ID IGUAL expresion \n        \n            declaraciones : RLET ID DOSPTS tipo \n        \n            declaraciones : RINTERFACE ID LLAVEI atributos LLAVED\n        \n            atributos : atributos atributo\n                    | atributo\n        \n            atributo : ID DOSPTS tipo PTCOMA \n        \n            tipo : RSTRING\n        \n            tipo : RANY\n        \n            tipo : RNUMBER\n        \n            tipo : RBOOLEAN\n        \n            print : RCONSOLE PT RLOG PARENI listaExpresiones PAREND\n        \n            listaExpresiones : listaExpresiones COMA expresion  \n                            | expresion \n        \n            expresion : expresion MAS expresion\n        \n            expresion : expresion MENOS expresion\n        \n            expresion : expresion MUL expresion\n        \n            expresion : expresion DIV expresion\n        \n            expresion : expresion MOD expresion\n        \n            expresion : expresion POT expresion\n        \n            expresion : NOT expresion\n        \n            expresion : expresion IGUALACION expresion\n        \n            expresion : expresion DISTINTO expresion\n        \n            expresion : expresion MAYORQ expresion\n        \n            expresion : expresion MENORQ expresion\n        \n            expresion : expresion MAYORIG expresion\n        \n            expresion : expresion MENORIG expresion\n        \n            expresion : expresion OR expresion\n        \n            expresion : expresion AND expresion\n        \n            expresion : MENOS expresion %prec UNARIO\n        \n            expresion : PARENI expresion PAREND\n        \n            expresion : RTRUE\n                     | RFALSE\n        \n            expresion : RNULL\n        \n            expresion : ENTERO\n                    | DECIMAL\n        \n            expresion : CADENA\n        \n            expresion : nativa\n        \n            expresion : CORI listaExpresiones CORD\n        \n            nativa : tofixed\n                    | toexponential\n                    | tostring\n                    | tolowercase\n                    | touppercase\n                    | split\n                    | concat\n        \n            tofixed : expresion PT RFIXED PARENI expresion PAREND \n        \n            toexponential : expresion PT REXPONENTIAL PARENI expresion PAREND \n        \n            tostring : expresion PT RTSTRING PARENI PAREND \n        \n            tolowercase : expresion PT RLC PARENI PAREND \n        \n            touppercase : expresion PT RUC PARENI PAREND \n        \n            split : expresion PT RSPLIT PARENI expresion PAREND \n        \n            concat : expresion PT RCONCAT PARENI listaExpresiones PAREND\n        '
    
_lr_action_items = {'RCONSOLE':([0,2,3,30,31,32,48,49,119,127,134,136,138,140,147,148,149,150,],[8,8,-3,-2,-4,-5,-6,-7,8,8,8,8,8,8,8,8,8,8,]),'NOT':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[11,11,-3,11,11,11,11,-2,-4,-5,11,11,11,11,11,11,11,11,11,11,11,11,11,11,-6,-7,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,]),'MENOS':([0,2,3,5,9,10,11,12,13,14,15,16,17,18,19,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,51,52,53,55,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,83,85,87,88,89,93,94,95,96,102,107,108,109,110,111,112,115,119,120,121,122,123,125,127,134,136,137,138,139,140,141,143,147,148,149,150,],[10,10,-3,34,10,10,10,-46,-47,-48,-49,-50,-51,-52,10,-54,-55,-56,-57,-58,-59,-60,-2,-4,-5,10,10,10,10,10,10,10,10,10,10,10,10,10,10,-6,-7,34,-44,34,34,10,-29,-30,-31,-32,-33,-34,34,34,34,34,34,34,34,34,-45,-53,10,10,34,10,10,10,10,10,34,34,34,34,-63,-64,-65,34,10,10,-61,-62,-66,-67,34,10,10,10,10,10,10,10,34,34,10,10,10,10,]),'PARENI':([0,2,3,9,10,11,19,22,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,73,74,75,76,77,78,79,80,83,85,88,89,93,94,95,115,119,127,133,134,135,136,137,138,139,140,147,148,149,150,],[9,9,-3,9,9,9,9,58,-2,-4,-5,9,9,9,9,9,9,9,9,9,9,9,9,9,9,-6,-7,9,88,89,90,91,92,93,94,95,9,9,9,9,9,9,9,9,9,9,137,9,139,9,9,9,9,9,9,9,9,9,]),'RTRUE':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[12,12,-3,12,12,12,12,-2,-4,-5,12,12,12,12,12,12,12,12,12,12,12,12,12,12,-6,-7,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,]),'RFALSE':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[13,13,-3,13,13,13,13,-2,-4,-5,13,13,13,13,13,13,13,13,13,13,13,13,13,13,-6,-7,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,]),'RNULL':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[14,14,-3,14,14,14,14,-2,-4,-5,14,14,14,14,14,14,14,14,14,14,14,14,14,14,-6,-7,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'ENTERO':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[15,15,-3,15,15,15,15,-2,-4,-5,15,15,15,15,15,15,15,15,15,15,15,15,15,15,-6,-7,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,]),'DECIMAL':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[16,16,-3,16,16,16,16,-2,-4,-5,16,16,16,16,16,16,16,16,16,16,16,16,16,16,-6,-7,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,]),'CADENA':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[17,17,-3,17,17,17,17,-2,-4,-5,17,17,17,17,17,17,17,17,17,17,17,17,17,17,-6,-7,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'CORI':([0,2,3,9,10,11,19,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,48,49,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[19,19,-3,19,19,19,19,-2,-4,-5,19,19,19,19,19,19,19,19,19,19,19,19,19,19,-6,-7,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'RLET':([0,2,3,30,31,32,48,49,119,127,134,136,138,140,147,148,149,150,],[20,20,-3,-2,-4,-5,-6,-7,20,20,20,20,20,20,20,20,20,20,]),'RINTERFACE':([0,2,3,30,31,32,48,49,119,127,134,136,138,140,147,148,149,150,],[21,21,-3,-2,-4,-5,-6,-7,21,21,21,21,21,21,21,21,21,21,]),'RIF':([0,2,3,30,31,32,48,49,119,127,131,132,134,136,138,140,147,148,149,150,],[22,22,-3,-2,-4,-5,-6,-7,22,22,133,135,22,22,22,22,22,22,22,22,]),'$end':([1,2,3,30,31,32,48,49,],[0,-1,-3,-2,-4,-5,-6,-7,]),'LLAVED':([3,30,31,32,48,49,104,105,118,127,128,138,140,149,150,],[-3,-2,-4,-5,-6,-7,117,-20,-19,129,-21,142,144,151,152,]),'PTCOMA':([4,5,6,7,12,13,14,15,16,17,18,23,24,25,26,27,28,29,52,53,56,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,97,98,99,100,101,102,109,110,111,117,120,121,122,123,124,125,126,129,130,142,144,151,152,],[31,32,48,49,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,-44,-35,-15,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,-42,-43,-45,-53,-17,-22,-23,-24,-25,-16,-63,-64,-65,-18,-61,-62,-66,-67,-26,-14,128,-11,-10,-9,-8,-13,-12,]),'MAS':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[33,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,33,-44,33,33,-29,-30,-31,-32,-33,-34,33,33,33,33,33,33,33,33,-45,-53,33,33,33,33,33,-63,-64,-65,33,-61,-62,-66,-67,33,33,33,]),'MUL':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[35,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,35,-44,35,35,35,35,-31,-32,-33,-34,35,35,35,35,35,35,35,35,-45,-53,35,35,35,35,35,-63,-64,-65,35,-61,-62,-66,-67,35,35,35,]),'DIV':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[36,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,36,-44,36,36,36,36,-31,-32,-33,-34,36,36,36,36,36,36,36,36,-45,-53,36,36,36,36,36,-63,-64,-65,36,-61,-62,-66,-67,36,36,36,]),'MOD':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[37,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,37,-44,37,37,37,37,-31,-32,-33,-34,37,37,37,37,37,37,37,37,-45,-53,37,37,37,37,37,-63,-64,-65,37,-61,-62,-66,-67,37,37,37,]),'POT':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[38,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,38,-44,38,38,38,38,38,38,38,-34,38,38,38,38,38,38,38,38,-45,-53,38,38,38,38,38,-63,-64,-65,38,-61,-62,-66,-67,38,38,38,]),'IGUALACION':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[39,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,39,-44,39,39,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,39,39,-45,-53,39,39,39,39,39,-63,-64,-65,39,-61,-62,-66,-67,39,39,39,]),'DISTINTO':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[40,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,40,-44,40,40,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,40,40,-45,-53,40,40,40,40,40,-63,-64,-65,40,-61,-62,-66,-67,40,40,40,]),'MAYORQ':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[41,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,41,-44,41,41,-29,-30,-31,-32,-33,-34,41,41,-38,-39,-40,-41,41,41,-45,-53,41,41,41,41,41,-63,-64,-65,41,-61,-62,-66,-67,41,41,41,]),'MENORQ':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[42,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,42,-44,42,42,-29,-30,-31,-32,-33,-34,42,42,-38,-39,-40,-41,42,42,-45,-53,42,42,42,42,42,-63,-64,-65,42,-61,-62,-66,-67,42,42,42,]),'MAYORIG':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[43,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,43,-44,43,43,-29,-30,-31,-32,-33,-34,43,43,-38,-39,-40,-41,43,43,-45,-53,43,43,43,43,43,-63,-64,-65,43,-61,-62,-66,-67,43,43,43,]),'MENORIG':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[44,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,44,-44,44,44,-29,-30,-31,-32,-33,-34,44,44,-38,-39,-40,-41,44,44,-45,-53,44,44,44,44,44,-63,-64,-65,44,-61,-62,-66,-67,44,44,44,]),'OR':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[45,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,45,-44,-35,45,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,-42,-43,-45,-53,45,45,45,45,45,-63,-64,-65,45,-61,-62,-66,-67,45,45,45,]),'AND':([5,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[46,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,46,-44,-35,46,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,46,-43,-45,-53,46,46,46,46,46,-63,-64,-65,46,-61,-62,-66,-67,46,46,46,]),'PT':([5,8,12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,96,102,107,108,109,110,111,112,120,121,122,123,125,141,143,],[47,50,-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,47,-44,-35,47,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,-42,-43,-45,-53,47,47,47,47,47,-63,-64,-65,47,-61,-62,-66,-67,47,47,47,]),'PAREND':([12,13,14,15,16,17,18,23,24,25,26,27,28,29,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,87,90,91,92,96,107,108,109,110,111,112,113,114,120,121,122,123,141,143,],[-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,81,-44,-35,-28,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,-42,-43,-45,-53,106,109,110,111,-27,120,121,-63,-64,-65,122,123,124,-61,-62,-66,-67,145,146,]),'CORD':([12,13,14,15,16,17,18,23,24,25,26,27,28,29,52,53,54,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,96,109,110,111,120,121,122,123,],[-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,-44,-35,82,-28,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,-42,-43,-45,-53,-27,-63,-64,-65,-61,-62,-66,-67,]),'COMA':([12,13,14,15,16,17,18,23,24,25,26,27,28,29,52,53,54,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,81,82,96,109,110,111,113,114,120,121,122,123,],[-46,-47,-48,-49,-50,-51,-52,-54,-55,-56,-57,-58,-59,-60,-44,-35,83,-28,-29,-30,-31,-32,-33,-34,-36,-37,-38,-39,-40,-41,-42,-43,-45,-53,-27,-63,-64,-65,83,83,-61,-62,-66,-67,]),'ID':([20,21,86,104,105,118,128,],[56,57,103,103,-20,-19,-21,]),'RFIXED':([47,],[73,]),'REXPONENTIAL':([47,],[74,]),'RTSTRING':([47,],[75,]),'RLC':([47,],[76,]),'RUC':([47,],[77,]),'RSPLIT':([47,],[78,]),'RCONCAT':([47,],[79,]),'RLOG':([50,],[80,]),'DOSPTS':([56,103,],[84,116,]),'IGUAL':([56,97,98,99,100,101,],[85,115,-22,-23,-24,-25,]),'LLAVEI':([57,106,131,132,145,146,],[86,119,134,136,147,148,]),'RSTRING':([84,116,],[98,98,]),'RANY':([84,116,],[99,99,]),'RNUMBER':([84,116,],[100,100,]),'RBOOLEAN':([84,116,],[101,101,]),'RELSE':([129,130,151,152,],[131,132,-13,-12,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'inicio':([0,],[1,]),'sentencias':([0,119,134,136,147,148,],[2,127,138,140,149,150,]),'sentencia':([0,2,119,127,134,136,138,140,147,148,149,150,],[3,30,3,30,3,3,30,30,3,3,30,30,]),'print':([0,2,119,127,134,136,138,140,147,148,149,150,],[4,4,4,4,4,4,4,4,4,4,4,4,]),'expresion':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[5,5,51,52,53,55,59,60,61,62,63,64,65,66,67,68,69,70,71,72,87,96,102,107,108,112,55,55,125,5,5,5,5,141,5,143,5,5,5,5,5,]),'declaraciones':([0,2,119,127,134,136,138,140,147,148,149,150,],[6,6,6,6,6,6,6,6,6,6,6,6,]),'if':([0,2,119,127,134,136,138,140,147,148,149,150,],[7,7,7,7,7,7,7,7,7,7,7,7,]),'nativa':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'tofixed':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'toexponential':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,24,]),'tostring':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,]),'tolowercase':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,26,]),'touppercase':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,27,]),'split':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,28,]),'concat':([0,2,9,10,11,19,33,34,35,36,37,38,39,40,41,42,43,44,45,46,58,83,85,88,89,93,94,95,115,119,127,134,136,137,138,139,140,147,148,149,150,],[29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,29,]),'listaExpresiones':([19,94,95,],[54,113,114,]),'tipo':([84,116,],[97,126,]),'atributos':([86,],[104,]),'atributo':([86,104,],[105,118,]),'elseif':([129,],[130,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> inicio","S'",1,None,None,None),
  ('inicio -> sentencias','inicio',1,'p_INICIO','Analizador.py',233),
  ('sentencias -> sentencias sentencia','sentencias',2,'p_SENTENCIAS','Analizador.py',241),
  ('sentencias -> sentencia','sentencias',1,'p_SENTENCIAS','Analizador.py',242),
  ('sentencia -> print PTCOMA','sentencia',2,'p_SENTENCIAS_1','Analizador.py',253),
  ('sentencia -> expresion PTCOMA','sentencia',2,'p_SENTENCIAS_1','Analizador.py',254),
  ('sentencia -> declaraciones PTCOMA','sentencia',2,'p_SENTENCIAS_1','Analizador.py',255),
  ('sentencia -> if PTCOMA','sentencia',2,'p_SENTENCIAS_1','Analizador.py',256),
  ('if -> RIF PARENI expresion PAREND LLAVEI sentencias LLAVED elseif RELSE LLAVEI sentencias LLAVED','if',12,'p_IF','Analizador.py',263),
  ('if -> RIF PARENI expresion PAREND LLAVEI sentencias LLAVED RELSE LLAVEI sentencias LLAVED','if',11,'p_IF','Analizador.py',264),
  ('if -> RIF PARENI expresion PAREND LLAVEI sentencias LLAVED elseif','if',8,'p_IF','Analizador.py',265),
  ('if -> RIF PARENI expresion PAREND LLAVEI sentencias LLAVED','if',7,'p_IF','Analizador.py',266),
  ('elseif -> elseif RELSE RIF PARENI expresion PAREND LLAVEI sentencias LLAVED','elseif',9,'p_IF_ELSE','Analizador.py',287),
  ('elseif -> RELSE RIF PARENI expresion PAREND LLAVEI sentencias LLAVED','elseif',8,'p_IF_ELSE','Analizador.py',288),
  ('declaraciones -> RLET ID DOSPTS tipo IGUAL expresion','declaraciones',6,'p_DECLARACION_PRIMITIVA1','Analizador.py',302),
  ('declaraciones -> RLET ID','declaraciones',2,'p_DECLARACION_PRIMITIVA1','Analizador.py',303),
  ('declaraciones -> RLET ID IGUAL expresion','declaraciones',4,'p_DECLARACION_PRIMITIVA2','Analizador.py',314),
  ('declaraciones -> RLET ID DOSPTS tipo','declaraciones',4,'p_DECLARACION_PRIMITIVA3','Analizador.py',320),
  ('declaraciones -> RINTERFACE ID LLAVEI atributos LLAVED','declaraciones',5,'p_DECLARACION_INTERFACE','Analizador.py',326),
  ('atributos -> atributos atributo','atributos',2,'p_DECLARACION_INTERFACE_ATRIBUTOS','Analizador.py',332),
  ('atributos -> atributo','atributos',1,'p_DECLARACION_INTERFACE_ATRIBUTOS','Analizador.py',333),
  ('atributo -> ID DOSPTS tipo PTCOMA','atributo',4,'p_DECLARACION_INTERFACE_ATRIBUTO','Analizador.py',343),
  ('tipo -> RSTRING','tipo',1,'p_TIPO_STRING','Analizador.py',350),
  ('tipo -> RANY','tipo',1,'p_TIPO_ANY','Analizador.py',357),
  ('tipo -> RNUMBER','tipo',1,'p_TIPO_NUMBER','Analizador.py',364),
  ('tipo -> RBOOLEAN','tipo',1,'p_TIPO_BOOLEAN','Analizador.py',371),
  ('print -> RCONSOLE PT RLOG PARENI listaExpresiones PAREND','print',6,'p_PRINT_SIMPLE','Analizador.py',379),
  ('listaExpresiones -> listaExpresiones COMA expresion','listaExpresiones',3,'p_LISTA_EXPRESIONES','Analizador.py',386),
  ('listaExpresiones -> expresion','listaExpresiones',1,'p_LISTA_EXPRESIONES','Analizador.py',387),
  ('expresion -> expresion MAS expresion','expresion',3,'p_EXPRESION_SUMA','Analizador.py',398),
  ('expresion -> expresion MENOS expresion','expresion',3,'p_EXPRESION_RESTA','Analizador.py',405),
  ('expresion -> expresion MUL expresion','expresion',3,'p_EXPRESION_MULTIPLICACION','Analizador.py',412),
  ('expresion -> expresion DIV expresion','expresion',3,'p_EXPRESION_DIVISION','Analizador.py',419),
  ('expresion -> expresion MOD expresion','expresion',3,'p_EXPRESION_MOD','Analizador.py',425),
  ('expresion -> expresion POT expresion','expresion',3,'p_EXPRESION_POTENCIA','Analizador.py',431),
  ('expresion -> NOT expresion','expresion',2,'p_EXPRESION_NOT','Analizador.py',438),
  ('expresion -> expresion IGUALACION expresion','expresion',3,'p_EXPRESION_IGUALACION','Analizador.py',444),
  ('expresion -> expresion DISTINTO expresion','expresion',3,'p_EXPRESION_DISTINTO','Analizador.py',450),
  ('expresion -> expresion MAYORQ expresion','expresion',3,'p_EXPRESION_MAYORQ','Analizador.py',456),
  ('expresion -> expresion MENORQ expresion','expresion',3,'p_EXPRESION_MENORQ','Analizador.py',463),
  ('expresion -> expresion MAYORIG expresion','expresion',3,'p_EXPRESION_MAYORIG','Analizador.py',469),
  ('expresion -> expresion MENORIG expresion','expresion',3,'p_EXPRESION_MENORIG','Analizador.py',476),
  ('expresion -> expresion OR expresion','expresion',3,'p_EXPRESION_OR','Analizador.py',483),
  ('expresion -> expresion AND expresion','expresion',3,'p_EXPRESION_AND','Analizador.py',489),
  ('expresion -> MENOS expresion','expresion',2,'p_EXPRESION_UNARIO','Analizador.py',495),
  ('expresion -> PARENI expresion PAREND','expresion',3,'p_EXPRESION_PARENTESIS','Analizador.py',502),
  ('expresion -> RTRUE','expresion',1,'p_EXPRESION_BOOLEAN','Analizador.py',508),
  ('expresion -> RFALSE','expresion',1,'p_EXPRESION_BOOLEAN','Analizador.py',509),
  ('expresion -> RNULL','expresion',1,'p_EXPRESION_NULL','Analizador.py',515),
  ('expresion -> ENTERO','expresion',1,'p_EXPRESION_NUMBER','Analizador.py',521),
  ('expresion -> DECIMAL','expresion',1,'p_EXPRESION_NUMBER','Analizador.py',522),
  ('expresion -> CADENA','expresion',1,'p_EXPRESION_CADENA','Analizador.py',528),
  ('expresion -> nativa','expresion',1,'p_EXPRESION_NATIVAS','Analizador.py',534),
  ('expresion -> CORI listaExpresiones CORD','expresion',3,'p_EXPRESION_ARRAY','Analizador.py',540),
  ('nativa -> tofixed','nativa',1,'p_NATIVA','Analizador.py',547),
  ('nativa -> toexponential','nativa',1,'p_NATIVA','Analizador.py',548),
  ('nativa -> tostring','nativa',1,'p_NATIVA','Analizador.py',549),
  ('nativa -> tolowercase','nativa',1,'p_NATIVA','Analizador.py',550),
  ('nativa -> touppercase','nativa',1,'p_NATIVA','Analizador.py',551),
  ('nativa -> split','nativa',1,'p_NATIVA','Analizador.py',552),
  ('nativa -> concat','nativa',1,'p_NATIVA','Analizador.py',553),
  ('tofixed -> expresion PT RFIXED PARENI expresion PAREND','tofixed',6,'p_NATIVA_TOFIXED','Analizador.py',559),
  ('toexponential -> expresion PT REXPONENTIAL PARENI expresion PAREND','toexponential',6,'p_NATIVA_TOEXPONENTIAL','Analizador.py',565),
  ('tostring -> expresion PT RTSTRING PARENI PAREND','tostring',5,'p_NATIVA_TOSTRING','Analizador.py',571),
  ('tolowercase -> expresion PT RLC PARENI PAREND','tolowercase',5,'p_NATIVA_TOLOWERCASE','Analizador.py',577),
  ('touppercase -> expresion PT RUC PARENI PAREND','touppercase',5,'p_NATIVA_TOUPPERCASE','Analizador.py',583),
  ('split -> expresion PT RSPLIT PARENI expresion PAREND','split',6,'p_NATIVA_SPLIT','Analizador.py',589),
  ('concat -> expresion PT RCONCAT PARENI listaExpresiones PAREND','concat',6,'p_NATIVA_CONCAT','Analizador.py',595),
]

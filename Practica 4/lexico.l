%{
    #include<stdio.h>
%}

%%
(^\/\/.*?$|\/\*.*?\*\/)		            { printf("<comentario>"); }
"do"|"while"|"for"                      {printf("<ciclo>");}
"int"|"char"|"float"|"void"|"double"    {printf("<tipo de dato>");}
"if"|"else"|"switch"|"case"|"default"   {printf("<estructura_de_control>");}
"break"|"continue"|"goto"               {printf("<sentencia_de_control>");}
"static"|"auto"|"extern"|"register"    {printf("<clase_de_almacenamiento>");}
[+-]?[0-9]+                             {printf("<entero>");}
[+-]?([0-9]*[.])?[0-9]+                 {printf("<decimal>");}
([a-zA-Z_][a-zA-Z0-9_]*)                {printf("<identificador>");}
[a-zA-Z_]?\"(\\.|[^\\"])*\"             {printf("<cadena>");}
"const"			{ printf("<constante>"); }
"enum"			{ printf("<tipo de dato>"); }
"return"		{ printf("<sentencia>"); }
"short"			{ printf("<rango_de_valor>"); }
"long"			{ printf("<rango_de_valor>"); }
"signed"		{ printf("<rango_de_valor>"); }
"sizeof"		{ printf("<operador_compilacion>"); }
"struct"		{ printf("<estructura_de_datos>"); }
"typedef"		{ printf("<palabra_reservada>"); }
"union"			{ printf("<estructura_de_datos>"); }
"unsigned"		{ printf("<rango_de_valor>"); }
"volatile"		{ printf("<variable_volatil>"); }
"..."			{ printf("<delimitador>"); }
">>="			{ printf("<operador_asignacion>"); }
"<<="			{ printf("<operador_asignacion>"); }
"+="			{ printf("<operador_asignacion>"); }
"-="			{ printf("<operador_asignacion>"); }
"*="			{ printf("<operador_asignacion>"); }
"/="			{ printf("<operador_asignacion>"); }
"%="			{ printf("<operador_asignacion>"); }
"&="			{ printf("<operador_asignacion>"); }
"^="			{ printf("<operador_asignacion>"); }
"|="			{ printf("<operador_asignacion>"); }
">>"			{ printf("<operador_desplazamiento>"); }
"<<"			{ printf("<operador_desplazamiento>"); }
"++"			{ printf("<operador_unario_incremento_decremento>"); }
"--"			{ printf("<operador_unario_incremento_decremento>"); }
"->"			{ printf("<operador_acceso_instancia>"); }
"&&"			{ printf("<operador_relacional>"); }
"||"			{ printf("<operador_relacional>"); }
"<="			{ printf("<operador_relacional>"); }
">="			{ printf("<operador_relacional>"); }
"=="			{ printf("<operador_relacional>"); }
"!="			{ printf("<operador_relacional>"); }
";"			    { printf("<delimitador>"); }
"#"			    { printf("<delimitador>"); }
"{"		        { printf("<delimitador>"); }
"}"		        { printf("<delimitador>"); }
","			    { printf("<delimitador>"); }
":"			    { printf("<delimitador>"); }
"="			    { printf("<asignacion>"); }
"("			    { printf("<delimitador>"); }
")"			    { printf("<delimitador>"); }
"["		        { printf("<delimitador>"); }
"]"		        { printf("<delimitador>"); }
"."			    { printf("<operador_acceso_instancia"); }
"&"			    { printf("<operadores_bit_a_bit>"); }
"!"			    { printf("<operador_negacion_complemento>"); }
"~"			    { printf("<operador_negacion_complemento>"); }
"-"			    { printf("<operador_aditivo>"); }
"+"			    { printf("<operador_aditivo>"); }
"*"			    { printf("<operadores_multiplicacion>"); }
"/"			    { printf("<operadores_multiplicacion>"); }
"%"			    { printf("<operadores_multiplicacion>"); }
"<"			    { printf("<operador_relacional>"); }
">"			    { printf("<operador_relacional>"); }
"^"			    { printf("<operadores_bit_a_bit>"); }
"|"			    { printf("<operadores_bit_a_bit>"); }
"?"			    { printf("?"); }
" "             { printf(" ");}
.               { printf("No reconocido");}
%%
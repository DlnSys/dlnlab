# Protocole de communication

Les trames envoyées par le bloc RSA à l'accélérateur modulaire suivent la forme suivante.

| senderId | receiverId | opcode | operand1(opt) | operand2(opt) |

Les trames envoyées par l'accélérateur au bloc RSA suivent la forme suivante.

| senderId | receiverId | operand1 |

Avec : 
- senderId : 1 octet codant l'Id du bloc expéditeur
- receiverId : 1 octet codant l'Id du bloc destinataire
- opcode (optionnel) : 1 octet codant l'opération (voir ci-après)
- operand1 : un certain nombre d'octets représentant le premier opérande 
- operand2 : un certain nombre d'octets représentant le second opérande

# Description des opérations

## Chargement du module N
Demande le chargement du module N dans l'accélérateur hardware.
- opcode : 0x11
- operand1 : 2 octets représentant la taille t de N en bits
- operand2 : t octets représentant la valeur de N

## Addition modulaire
Demande l'addition modulaire de deux opérandes de taille t.
La taille t est inférée par l'accélérateur grâce à sa connaissance de N.
- opcode : 0x22
- operand1 : t octets représentant la valeur du premier opérande
- operand2 : t octets représentant la valeur du second opérande

## Soustraction modulaire
Demande la soustraction modulaire de deux opérandes de taille t.
La taille t est inférée par l'accélérateur grâce à sa connaissance de N.
- opcode : 0x33
- operand1 : t octets représentant la valeur du premier opérande
- operand2 : t octets représentant la valeur du second opérande

## Inversion modulaire
Demande l'inversion modulaire d'un opérande de taille t. Si l'élément n'a pas d'inverse, retourne 0.
La taille t est inférée par l'accélérateur grâce à sa connaissance de N.
- opcode : 0x44
- operand1 : t octets représentant la valeur à inverser
- operand2 : non présent

## Multiplication modulaire
Demande la multiplication modulaire de deux opérandes de taille t.
La taille t est inférée par l'accélérateur grâce à sa connaissance de N.
- opcode : 0x55
- operand1 : t octets représentant la valeur du premier opérande
- operand2 : t octets représentant la valeur du second opérande

## Mise au carré modulaire
Demande la mise au carré modulaire d'un opérande de taille t.
La taille t est inférée par l'accélérateur grâce à sa connaissance de N.
- opcode : 0x66
- operand1 : t octets représentant la valeur à mettre au carré
- operand2 : non présent

## Demande de réponse
Demande de la réponse suite à une demande d'opération.
- opcode : 0x77
- operand1 : non présent
- operand2 : non présent

La réponse de taille t suit le format de trames décrit au début de ce document.

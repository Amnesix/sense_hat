# sense_hat
Quelques développement autour de la carte sense_hat.

## serpent.py
Jeu de type serpent. Appuyer sur le bouton du joystick pour démarrer une
nouvelle partie. La partie démarre réellement en choisissant une direction,
toujours avec le joystick.
Attention, le serpent accélère non par à chaque nourriture avalée, mais en
permanence. Le but est donc de perdre le moins de temps possible.

Pour éviter de rendre le tout injouable, la longueur du serpent est limitée à 20
pixels et le timer ne descend pas en dessous de 1/10s.

Prochaine version  ? Utilisation de l'accéléromètre pour diriger le serpent qui
se déplacera toujours vers le bas...

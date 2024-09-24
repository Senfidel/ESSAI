#1. Initialiser le dépôt Git local (si ce n'est pas déjà fait) : 
#Si votre projet n'a pas encore été initialisé avec Git, commencez par créer un dépôt Git dans votre répertoire de travail :

git init


Cela crée un dépôt Git local dans votre répertoire.

2. Vérifier que tous les fichiers sont suivis par Git :
Pour que Git prenne en compte tous vos fichiers et dossiers, vous devez les ajouter à l'index (staging area). Utilisez la commande suivante :

git add .

Le . signifie "tout ajouter", ce qui inclut tous les fichiers et dossiers de votre espace de travail.
Si vous avez des fichiers que vous souhaitez exclure, vous pouvez les mentionner dans un fichier .gitignore.
3. Faire un commit des fichiers ajoutés :
Une fois que tous les fichiers sont ajoutés à l'index, vous devez créer un commit pour enregistrer ces changements dans l'historique Git local. Utilisez cette commande :

git commit -m "Ajout initial de tous les fichiers"


e -m permet d'ajouter un message de commit directement (ici, "Ajout initial de tous les fichiers"). Ce message est une description des modifications.
4. Ajouter le dépôt distant (GitHub) :
Si vous n'avez pas encore associé votre dépôt local à un dépôt distant sur GitHub, vous devez le faire. Utilisez cette commande pour ajouter l'URL de votre dépôt GitHub (assurez-vous de remplacer https://github.com/username/repository.git par l'URL réelle de votre dépôt GitHub) :

git remote add origin https://github.com/username/repository.git


origin est le nom que vous donnez au dépôt distant (vous pouvez utiliser un autre nom, mais origin est la convention la plus courante).
5. Pousser tous les fichiers vers GitHub :
Maintenant, vous pouvez pousser tous les fichiers de votre espace de travail local vers GitHub. Utilisez cette commande pour envoyer vos changements à la branche main du dépôt GitHub :


git push -u origin main

-u permet de définir la branche main sur le dépôt distant comme la branche par défaut pour les futurs push.
Si vous utilisez une autre branche par défaut (par exemple master), remplacez main par le nom de la branche correspondante.
6. Authentification (si nécessaire) :
Si vous n'êtes pas connecté à GitHub via Git sur votre terminal, Git vous demandera vos informations de connexion. Entrez votre nom d'utilisateur GitHub et votre token d'accès personnel (si vous avez activé l'authentification par token sur GitHub, ce qui est le cas pour la plupart des utilisateurs modernes à cause de la dépréciation des mots de passe pour l'accès HTTPS).



Résumé des commandes :
Initialiser un dépôt Git (si nécessaire) : git init
Ajouter tous les fichiers et dossiers à l'index : git add .
Créer un commit : git commit -m "Ajout initial de tous les fichiers"
Ajouter le dépôt distant GitHub : git remote add origin https://github.com/username/repository.git
Pousser tous les fichiers vers GitHub : git push -u origin main
Cela poussera tous les dossiers et fichiers de votre espace de travail local vers votre dépôt GitHub.

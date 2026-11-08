# Livraison des films sur Google Drive

L'action `.github/workflows/drive-upload.yml` réassemble les films poussés en morceaux sur la branche
`video-transfer` et les envoie sur Drive. Elle lit quatre secrets du dépôt.

## 1. Créer les secrets (une fois)

1. Google Cloud Console → nouveau projet → « API et services » → activer **Google Drive API**.
2. « Écran de consentement OAuth » : type Externe, ajoutez votre adresse comme utilisateur test.
   (En mode Test, le jeton de rafraîchissement dure 7 jours : assez pour la livraison.)
3. « Identifiants » → Créer → ID client OAuth → type **Application de bureau** (ou « Application Web » avec
   l'URI de redirection `https://developers.google.com/oauthplayground`). Notez l'ID et le secret client.
4. https://developers.google.com/oauthplayground → roue dentée → cochez « Use your own OAuth credentials »,
   collez l'ID et le secret → étape 1 : saisissez le périmètre `https://www.googleapis.com/auth/drive.file`
   → « Authorize APIs » → étape 2 : « Exchange authorization code for tokens » → copiez le **Refresh token**.
5. GitHub → knoel99/milady-2027 → Settings → Secrets and variables → Actions → New repository secret :
   - `GDRIVE_CLIENT_ID`
   - `GDRIVE_CLIENT_SECRET`
   - `GDRIVE_REFRESH_TOKEN`
   - `GDRIVE_FOLDER_ID` (facultatif : l'identifiant à la fin de l'URL du dossier Drive voulu)

Le périmètre `drive.file` ne donne accès qu'aux fichiers créés par cette application, pas au reste du Drive.

## 2. Lancer l'envoi

Actions → **drive-upload** → Run workflow (branche `video-transfer`). Le journal affiche l'identifiant Drive
de chaque film. Ensuite, supprimez la branche `video-transfer` (elle ne sert qu'au transport) et, si vous le
souhaitez, révoquez l'accès dans https://myaccount.google.com/permissions.

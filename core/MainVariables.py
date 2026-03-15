from django.conf import settings

HostURL, localhost = "https://innocaptcha.midoghanam.site", "http://127.0.0.1:8000"

BaseURL = localhost if getattr(settings, "DevMode", False) else HostURL

OAuth = {
  "GitHub": {
    "AppID": 1294780,
    "PrivateKey": "SHA256:CbQyqVXiuPzDGDnLPEvXdc6MpWa4yd3aM/GuIRmak80=",
    "ClientID": "Iv23liIiuqtJ1SLlWVWH",
    "ClientSecret": "bd1597ac086e2199ee11b9a8cf0134a0b948caad",
    "urls": {
      "auth": "https://github.com/login/oauth/authorize",
      "token": "https://github.com/login/oauth/access_token",
      "userinfo": "https://api.github.com/user",
    },
    "scops": {
      "login": "read:user user:email",
      "signup": "read:user user:email",
      "add_account": "read:user user:email user:follow user write:discussion read:discussion admin:org read:org admin:public_key write:public_key read:public_key admin:gpg_key write:gpg_key read:gpg_key repo repo:status repo_deployment public_repo repo:invite security_events gist notifications workflow codespace write:packages read:packages delete:packages admin:repo_hook delete_repo",
    },
  },
  "Google": {
    "ClientID": "490611769339-biodtr18p7atublgi40pgti5qm29fr2s.apps.googleusercontent.com",
    "ProjectID": "gen-lang-client-0896922511",
    "ClientSecret": "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",
    "urls": {
      "auth": "https://accounts.google.com/o/oauth2/auth",
      "token": "https://oauth2.googleapis.com/token",
      "userinfo": 'https://www.googleapis.com/oauth2/v3/userinfo',
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    },
    "scops": {
      "login": "openid email profile",
      "signup": "openid email profile",
      "add_account": "openid email profile https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/drive https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/drive.metadata https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.readonly https://www.googleapis.com/auth/contacts https://www.googleapis.com/auth/contacts.readonly https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.modify https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/youtube https://www.googleapis.com/auth/youtube.readonly https://www.googleapis.com/auth/photoslibrary.readonly https://www.googleapis.com/auth/photoslibrary.appendonly https://www.googleapis.com/auth/tasks",
    },
  },
}


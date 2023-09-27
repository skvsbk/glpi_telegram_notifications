# Notification of GLPI v.9.5.12 events via telegram bot
### 1. GLPI 
Make an additional *telegramid* field for Users. Enter the telegram chat_id for each user in this field.
Make notification to email by PHP. Email server has procmail for sorting letters, see below. 

### 2. Linux server
Install *postfix* on the Linux server. Add user *glpibot*. In the glpibot home directory, create a *.procmailrc* file with the following content:

```
PATH=$PATH:/usr/bin:/usr/local/bin:/usr/local/news/bin
MAILDIR=/var/spool/mail
LOGFILE=$MAILDIR/from
LOCKFILE=$HOME/.lockmail

:0
* ^Subject:.*Undelivered
/dev/null

:0
* To:.*glpibot@
{
SUBJECT=`formail -x Subject:`

:0
| $HOME/notify_bot.sh      "$SUBJECT"
}
```



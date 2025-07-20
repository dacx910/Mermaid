<h1 align="center">
  Mermaid
  <br>
  <img width="256" height="256" alt="small_mermaid_logo" src="https://github.com/user-attachments/assets/91b4ced8-74f5-4b0b-8bd8-81a066864933" />
  <br>
</h1>
<p align="center"><i>A supplemental Discord bot for moderation, monitoring, and securing servers</i></p>
<p>There are many (much better) Discord bots that can do moderation, but this is one that I've tailored to my specific use-cases and preferences.
<br><br>
It was primarily spawned from a desire for multi-level word blacklists, which are, essentially, a multi-level word blacklist checks for multiple separate tokens inside a message before it flags it as spam.
<br><br>
As an example, the "FreeMacbook" campaign uses the phrase "strictly first come first serve" very frequently in its spam messages, but I don't want to ban everyone from using this phrase. Instead, Mermaid will check for both this phrase and the words "dm" or "text", which may have its share of false-positives but it's significantly better than banning the phrase, "first come first serve".
</p>
<h1>Post-Installation & Maintenance Notes</h1>
<p>
After installation, there's really only one command you need to run, which is `/set_mod_channel`. This will change the channel the bot sends its alerts in, and is also where you should be executing any other commands. Other than that, there's not much to be aware of except a few permissions restrictions on certain commands and actions.
<br><br>
The `/audit_server` and `/audit_user` commands are not inherently dangerous (they pull from publicly available information), but because I don't think regular users should *need* to use them, they both require the "View Audit Log" permission.
<br><br>
The `/set_mod_channel` command requires Administrator.
<br><br>
Automated detections frequently create actions, including "Ban", "Kick", "Audit User", and "False Positive". Ban and Kick require their respective permissions, but Audit User and False Positive don't require any permissions. This is because automated detections only appear in the set mod channel, and as such, users without some degree of moderation authority should not be able to see the contents of this channel. These actions are also not inherently dangerous, so in the case that an unprivileged user ends up interacting with these actions, the overall impact is minimal.
</p>

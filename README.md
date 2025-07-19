# Mermaid

> A supplemental Discord bot for moderation, monitoring, and securing servers

There are many (much better) Discord bots that can do moderation, but this is one that I've tailored to my specific use-cases and preferences.

It was primarily spawned from a desire for multi-level word blacklists. Essentially, a multi-level word blacklist checks for multiple separate tokens inside a message before it flags it as spam. As an example, the "FreeMacbook" campaign uses the phrase "strictly first come first serve" very frequently in its spam messages, but I don't want to ban everyone from using this phrase. Instead, Mermaid will check for both this phrase and the words "dm" or "text", which may have its share of false-positives but it's significantly better than banning the phrase, "first come first server".

# Post-Installation & Maintenance Notes

After installation, there's really only one command you need to run, which is `/set_mod_channel`. This will change the channel the bot sends its alerts in, and is also where you should be executing any other commands.





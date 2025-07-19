# Plan of Action

Defending against these bots will be rolled out in a multi-phase plan and each phase will build on top of the previous phases to create a comprehensive system.

## Phase 0 - Analysis

This phase will be effectively perpetual throughout all development of this Discord bot. Phase 0 focuses on a set of questions:

- What do the solicitation messages have in common?

- What do the scam user accounts have in common?

- Where are these bots coming from?

- What data can we collect from users before they enter the server?

Data will be collected both manually and automatically. Scam messages and users can be screened manually and day-to-day observations can be observed. Automatically, the Discord bot will track invites across the server and detect which invite link a user uses when they join the server. To prevent over-collection, only invites with >7 days duration will be tracked.

All known-scam message content and user data including: user id, username, account creation date, badges, and linked accounts will be indexed.

Data collection prior to server entry is subject to future research. 

## Phase 1 - Message Blocking

In this phase, the bot will target a heuristics-based message filtering approach, automatically detecting suspicious strings inside the message content and flagging and deleting it.

## Phase 2 - User-based Heuristics

In this phase, the bot will look at user data outlined in Phase 0 to determine whether a user is suspicious, it will flag these users but not ban them until a moderator has cleared the issue or a message matching Phase 1's detections is detected.

## Phase 3 - Pre-entry and Isolation

In this phase, the bot will automatically detect users prior to server entry and deny entry accordingly. **In the event** that it is not possible to prevent user entry to a server, then users who have matched Phase 1 & 2 detection will be added to a database shared across servers to immediately ban users on this blacklist.

## Phase 4 - Server Policy Change

It is likely that in development several key weaknesses in server policy will be identified and remediation required. Because this is the most intrusive step, it is last in the line of priorities.

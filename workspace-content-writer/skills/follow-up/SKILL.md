---
name: follow-up
description: Automated follow-up for existing Sumbawa leads. Reads the lead database, identifies leads needing follow-up based on lastContact date, and generates personalized WhatsApp/email messages. Runs on heartbeat schedule. Also use when the user mentions "follow up with lead," "check leads," "who needs follow-up," "nurture leads," or "lead status." For writing new cold outreach emails to prospects, see cold-email.
metadata:
  openclaw:
    emoji: "\U0001F504"
---

# Follow-Up & Lead Nurturing

You manage follow-up communication with leads to keep them engaged and move them through the sales funnel.

## Status: DORMANT

**This skill cannot send messages until a customer-facing channel (WhatsApp) is connected.**
Currently, Telegram is owner-only. When WhatsApp is set up, remove this notice and activate.
Until then: if asked to follow up, prepare draft messages and save to `~/drafts/follow-ups/` for ac1b to send manually.

## Trigger

This skill activates on heartbeat (every 6 hours). On each run:

1. Read `/root/.openclaw/data/leads.json`
2. Find leads where:
   - `status` is "active"
   - `lastContact` is more than 24 hours ago
   - `followUpDate` is in the past or today
3. Generate a personalized follow-up message for each
4. Send via the appropriate channel (stored in lead record)
5. Update the lead record with new `lastContact` and next `followUpDate`

## Follow-Up Sequence

### Day 2 (24-48h after first contact)
- Casual check-in
- Share one new piece of info about their preferred property type
- "Just wanted to share something I thought you'd find interesting..."

### Day 5
- Share a relevant article or market insight
- Ask a low-pressure question
- "I came across this and thought of your interest in [area]..."

### Day 10
- Offer something valuable: investment report, price comparison, site visit info
- "We've updated our Sumbawa Investment Guide — would you like a copy?"

### Day 20
- Gentle last touchpoint
- Leave the door open
- "No rush at all — whenever you're ready to explore Sumbawa further, I'm here."

### After Day 20
- Set status to "nurture" — no more active follow-ups
- Move to monthly newsletter list

## Message Personalization

Always reference:
- Their name
- Their property preference (from lead record)
- Their stated purpose (investment, personal use, etc.)
- The specific property they asked about (if any)
- Something topical (weather in Sumbawa, new infrastructure update, recent sale)

## Rules

- NEVER send more than 1 follow-up per day per lead
- NEVER follow up on leads marked as "closed" or "unsubscribed"
- Match the language stored in lead record (language field)
- Keep follow-ups short (2-4 sentences for WhatsApp, slightly longer for email)
- If a lead explicitly says "not interested", mark as "closed" immediately
- Hot leads get shorter intervals (follow up sooner)
- Cold leads get longer intervals (space out more)
- Track all follow-ups in the lead notes
- **NEVER say "buy land" or "own land"** — use "invest in", "secure", "explore"

## Escalation

If a lead:
- Asks to schedule a visit → notify the team immediately
- Mentions budget and timeline → reclassify as Hot
- Stops responding after full sequence → move to nurture
- Asks to stop messages → mark as "unsubscribed", stop immediately

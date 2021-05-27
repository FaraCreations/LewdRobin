# LewdRobin
A Discord bot that facilitates anonymous, turn-based erotic writing. 

LewdRobin generates writing prompts from a configurable pool of environments, characters, scenes, and play types. Contributors then join my prompts anonymously and are assigned temporary aliases which their writing will be posted under.

With the prompt as a starting point, contributors take turns adding to the story. Each contributor gets a configurable amount of time to write before the turn passes to the next person in line.

## User Guide
All of LewdRobin's user-facing features can be accessed either through slash commands or reactions. Both ways will be listed in this guide.

*Contributing to a prompt, step-by-step*

**1.**  Make sure your server admins have invited me to their server, configured a channel for LewdRobin prompts to play out in, and generated a prompt.

**2.**  You can join LewdRobin prompts by reacting to them with ✅ or by using the /join command along with the prompt's 4-digit code either in the server or in my DMs. Once you've joined, LewdRobin will DM you with the alias your contributions will be made under. However, the prompt may not immediately begin if it has fewer than the minimum required contributors (this count updates on the prompt message).

**3.**  Contributing is turn-based, and each player gets 30 minutes (default) to contribute. LewdRobin will DM you when it's your turn. That DM will get pinned, and has a set of reacitons you can use to control your turn. If you need a refresher on the prompt, react with 📝 and LewdRobin will DM it to you. If you'd like some context, react with 📚 and LewdRobin will DM you the three most recent contributions to the prompt.

**4.**  Now it's your turn to start contributing. You can do this in two ways. You can use the /post slash command with the prompt number and the text you'd like to post, either in the relevant server or my DMs. The easier way, however, is to react with ▶️ to enter Play Mode. Play Mode lasts the rest of your turn, and while you're in it, anything you DM LewdRobin (except slash commands) will get posted as a contribution to the prompt.

**5.**  Your turn will end automatically after its designated duration is over. You can end it early with ⏩ or /pass. You can also drop from the prompt at any time with ❎ (on the DM LewdRobin sent you when your turn started or the prompt itself) or /drop. If you don't post a contribution or pass your turn within the time limit, you will be dropped from the prompt for inactivity.

## Admin Startup
*step-by-step guide to get me set up on your server*

**1.**  Use this link to add me to your server:

<https://discord.com/api/oauth2/authorize?client_id=839249838972862535&permissions=76864&scope=bot%20applications.commands>

Once you've added LewdRobin to your server, the bot will need a minute or two to set up slash commands.

**2.**  Make a channel for LewdRobin prompts to run in. LewdRobin will need the `View Channel, Send Message, Add Reactions, Manage Messages, and Read Message History` permissions here. Potential contributors to the prompts generated here should have the `View Channel, Add Reactions, Read Message History, and Use Slash Commands` permissions here. They should *not* have the `Send Messages` persmission in this channel.

**3.**  Create LewdRobin Admin and Moderator roles. By default, only server admins can configure LewdRobin settings or run prompts. If you want other members of your server to be able to do so, you will have to create roles for them. These will control who can use which slash and reaction commands in this server. These roles can be called anything, and don't need to grant any actual Discord permissions. Once you've created these roles, you will need to copy their IDs. To do this enable developer mode (User Settings -> Advanced -> Developer Mode) and right click on the roles in the role interface. Use the /roles command and paste in the role IDs for the IDs you want to be LewdRobin Admins and Moderators.

*Admins* can configure, /display and /reset settings, /ban and /unban_all contributors.

*Moderators* can /run prompts, /pause and resume prompts, and /kick contributors.

**4.**  Configure settings. LewdRobin uses default settings to start with, but they can be fine-tuned for each channel prompts are run in. See Prompt Configuration for more info.

## Prompt Configuration

This will cover prompt settings configurable by people with the LewdRobin Admin role for your server. All settings have a server-wide default which is not (currently) modifiable. Any adjustments to settings are made on a channel-by-channel basis. Use /display_settings in a channel to create a message displaying its current settings. Modify settings with the commands listed below.

**/Contributors**

  turn_length – length in minutes of each contributor's turn
  
  contributor_minimum – the minimum number of contributors a prompt needs before it can start  
  
  contributor_maximum – the most contributors a prompt can have at once
  
**/categories**  

  \[category\]\_on – whether prompts will generate this type of thing. At least one category must be turned on.  

  character_number – how many randomly generated characters will be created per prompt  
  
  play_number – how many play types will be generated per prompt

**/environments**

Environments and scenes both use these tags to determine the pool for generation. If any of an environment's tags are excluded here, it will be excluded; scenes are then drawn from a pool that matches the environment's tags.  

  \[america/europe/japan\] - environments set in this specific region  
  
  historical – environments set before 1980  
  
  modern – environments set between 1980 and 2030  
  
  futuristic – environments set after 2030  
  
  fantasy – environments with magical or fantasy-related elements
**/character_types**  

  \[type\] – toggles whether this type of character is generated. If at least one of cis_men or cis_women are enabled, they will be given a weighted bias in the generation pool.

**/species**

If humans are enabled, they will be given a weighted bias.  

  \[species\] – whether characters from this species group will be generated. May include multiple similar species.

**/play**  

  \[play type\] – whether play recommendations from this activity group will be included. May include multiple similar activities.
  
## Automation

This feature is still under development, and the related /time command doesn't do anything (yet). Check back later. :)

## Tip the Author

I spent a lot of time lovingly coding to make LewdRobin work. If you'd like to send me a tip, you can do so via:

<https://paypal.me/FaraCreations>

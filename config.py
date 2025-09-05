import os

# Bot Configuration
BOT_TOKEN =  os.getenv("BOT_TOKEN", "your_bot_token_here")

# Authorized Users
OWNER_IDS = [
    1328026158683390025
]

DEV_IDS = [
    1328026158683390025
]

ADMIN_IDS = [
    
]

# Default bot prefix
DEFAULT_PREFIX = "&"

# Discord default grey color
EMBED_COLOR = 0x2f3136

# Database file
DATABASE_FILE = "database/bot.db"

# Support Server Configuration
SUPPORT_SERVER_LINK = "https://discord.gg/VmvwknN2Jp"
SUPPORT_SERVER_ID = 0  

# Role IDs for automatic badge assignment (from support server)
ADMIN_ROLE_ID = 0  
MOD_ROLE_ID = 0  
STAFF_ROLE_ID = 0  
PARTNER_ROLE_ID = 0  
BUG_HUNTER_ROLE_ID = 0  
EARLY_SUPPORT_ROLE_ID = 0  
PREMIUM_USER_ROLE_ID = 0  

MANUAL_WEBHOOKS = {
    "server_join": "https://discord.com/api/webhooks/1413206141839736945/-iPEv9TtpuAw0SXB3VGw2NAC9ziWbE-oOwzpyOVGkCWTjWXTmrQIvrUvr8WzkvhZ6DQB",
    "server_leave": "https://discord.com/api/webhooks/1413206409864151060/ww4sWHKGp0UgPhUSzJBpncmCYgi9VcTBMPJa-Gu3sNfg1e-kupjTTHNLcUyMTEfe21Ia",
    "command_executed": "https://discord.com/api/webhooks/1413206673723756614/e6y13tAenv7XvIgjGO5y-Xf8GK6Caxp4vkVegvhZ0wryg-ROkdjlIIKlb_EUg13u8Ddc",
    "error": "https://discord.com/api/webhooks/1413206472036323428/cvfo2nlQhQLF7XZb2RYzO2WcPXn_HIsgqgLa3P5Y8WggCJbkfdnolmoWWWDPbz7InEV4",
    "ratelimit": "https://discord.com/api/webhooks/1413206535047217222/5e2sYGptby_KntZVrU7wehZG2dooUqOK4biYi0eT01_62ekSnJR7Bvim3xNOMSG0-P7p"
}

DIRECT_MESSAGE_CHANNELS = {
    "premium_activated": 1412407575810543727,
    "backup": 1412407691531518065           }

# Custom Emoji Variables
class emoji:
    check = "<a:Check:1341859939211149334>"
    cross = "<a:Cross:1341860595615666257>"  
    error = "<:error:1411359275263066212>" # yellow exclamation 
    alert = "<:alert:1411253727548936313>"
    loading= "<a:loading:1341871375811477504>"
    warn = "<:warn:1411359623889289228>" # red exclamation 
    add = "<:add:1411359302614126774>"
    remove = "<:remove:1411359210306011156>"
    setting = "<:setting:1411359256858591443>"
    arrowright = "<:arrowright:1411359237036179590>"
    arrowleft = "<:arrowleft:1411359340039897279>"
    doublearrowright = "<:doublearrowright:1411359346746720348>"
    doublearrowleft = "<:doublearrowleft:1411359421531029595>"
    boost = "<:boost:1411359245277991052>"
    search = "<:search:1411253700353200158>"
    download = "<:download:1341868818837934171>"
    greet = "<:greet:1411359295953698829>"
    kick = "<:kick:1411385018022101167>"
    ban = "<:ban:1411384144734322729> "
    mic = "<:mic1:1411384099565862953>"
    micmuted = "<:micmuted:1411384035783082057>"
    attachment = "<:attachment:1411384157233348709>"
    channel = "<:channel:1411384119333490720> "
    link = "<:link1:1411384210245160985>"
    ruby = "<:ruby:1411384171649171477>"
    hidden = "<:hidden:1411359225891786852>"
    unhidden = "<:unhidden:1411382680137896047>"
    lock = ""
    unlock = "<:unlock1:1411382989308432425>"
    trash = "<:trash:1411385302962143363>"
    timer = "<:timer1:1411359263187800076>"
    user = "<:user:1411382870282342443>"
    mod = "<:moderation:1341855253712207976>"
    edit = "<:edit:1411720312533418056>"
    server = "<:server:1411731977274392808>"
    key = "<:key1:1411743230139174992>"
    role = "<:role:1412136161182482432>"
    category = "<:category:1341854317270925323>"
    msgd = "<:messagedisabled:1412452152692965376>"
    np = "<:np:1413070049677152257>"
    antinuke = "<:antinuke:1341856469821296857>"
    enable = "<:disable_no:1341860245219315854><:enable_yes:1341860100452651030>"
    disable = "<:disable_yes:1341860221902917662><:enable_no:1341860375770960014>"
    automod = "<:automod:1341855582050844673>"
    customrole = "<:customrole:1341855680985825280>"
    cmd = "<:commands:1413222847173886082>"
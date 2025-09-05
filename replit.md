# Discord Bot Project

## Overview
This project is a multi-purpose Discord bot developed with Python and the discord.py library. It offers a range of features including interactive embed building, automated welcome/leave messages, vanity role management, activity-based role assignment, comprehensive ignore system, badge management, logging system, and utility commands. The bot is designed with a modular, cog-based architecture to ensure easy extensibility and maintainability, focusing on providing a robust and flexible solution for Discord server management. The project aims to provide an all-in-one solution for server administration and engagement.

## Recent Changes

### September 3, 2025
- **Removed bot immunity from antinuke**: Bots now require whitelisting for any actions, no automatic immunity
- **Added antinuke command alias**: "an" can now be used as shorthand for "antinuke" commands  
- **Reordered help panel categories**: Antinuke, Automod, Moderation, Utility, Welcomer, Autoresponder, Embed Builder, Autorole, Vanityrole, Activityroles, Voicemaster, Ignore
- **Added comprehensive media system**: Media channel restrictions with bypass functionality
  - Media channel management: add, remove, show, reset commands
  - Media bypass system: user/role-based bypass with management commands
  - Automatic message filtering: deletes non-media messages in configured channels
- **Fixed bot mention prefix display**: Now shows actual server prefix instead of bot mention
- **Removed voicemaster dropdown**: Cleaned up unnecessary dropdown menu, kept button-only interface
- **Verified logging system**: Confirmed all logging webhooks and command execution logging working properly
- **Added advanced automod system**: Comprehensive automoderation with interactive setup panels
  - Antispam protection with configurable limits, timeframes, and punishments
  - Antilink protection with domain allow/disallow lists and Discord invite blocking
  - Interactive button-based setup for all automod features
  - Comprehensive whitelist system for users, roles, and channels
  - Database-backed settings with full customization options
  - Placeholder implementations for antibadwords, antizalgo, and anticaps (coming soon)

### September 2, 2025
- **Fixed ignore system**: Added proper database tables and command checking logic
- **Enhanced badge system**: Multiple badge selection and proper ordering with role-based assignment
- **Improved profile command**: Specific badge ordering and removed support server requirement
- **Added webhook logging**: Comprehensive logging for server joins/leaves, commands, errors, and premium
- **Added backup command**: Database backup with automatic file sending to designated channels
- **Enhanced bot mention support**: Bot mention works as alternative prefix with invalid command responses

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Core Framework
- **Language**: Python 3.x
- **Primary Library**: discord.py with commands extension
- **Architecture Pattern**: Cog-based modular design
- **Database**: SQLite with aiosqlite for async operations
- **Configuration**: Environment variable-based with fallback defaults

### Bot Structure
- **Main Entry Point**: `main.py` for initialization and cog loading.
- **Configuration Management**: Centralized settings and authorization levels.
- **Database Layer**: SQLite operations with defined table schemas for various features.
- **Helper Utilities**: Common functions, decorators, and permission checks.
- **Variable System**: Dynamic text/embed variable parsing and replacement.

### Authorization System
A three-tier permission structure comprising Owner, Developer, and Admin levels, alongside a "No-Prefix Users" system for specific command execution without prefixes.

### Database Schema
Core tables: `guild_settings`, `saved_embeds`, `welcomer_settings`, `vanityrole_settings`, `activityroles_settings`, `no_prefix_users`, `warnings`, `warn_punishments`, `autoresponders`, `voicemaster_settings`, `premium_guilds`, `automod_antispam`, `automod_antilink`, `automod_antibadwords`, `automod_antizalgo`, `automod_anticaps`, `automod_whitelist`, `automod_strikes`, `media_channels`, `media_bypass`.

### Feature Modules (Cogs)
- **Embed Builder**: Interactive creation, editing, and saving of embed templates with dynamic content.
- **Welcomer System**: Automated welcome/leave messages with custom embeds and variable parsing.
- **Vanity Role Management**: Automatic role assignment based on vanity URL usage.
- **Activity Roles**: Dynamic role assignment based on Discord activities (gaming, streaming, etc.).
- **Utility Commands**: Server prefix customization, variable references, and general admin tools.
- **Owner Tools**: Bot administration and maintenance commands, including no-prefix user management.
- **Help System**: Dynamic, paginated help generation with category descriptions, command counts, and navigation controls.
- **Moderation System**: Comprehensive tools for muting, banning, kicking, role management, and a customizable warning system with punishment thresholds.
- **Voice Channel Management**: Commands for individual and bulk voice actions (mute, deafen, kick, ban), and advanced temporary voice channel management via Voicemaster.
- **No-Prefix System**: Time-based access for executing commands without a prefix, with expiry tracking.
- **Autoresponder System**: Custom auto-responses based on message content, supporting auto-messages and auto-reactions with various match modes and embed integration.
- **Voicemaster System**: Manages temporary voice channels with multiple setup variants (Standard, Duo, Trio, Squad), control panels, and advanced features like locking, hiding, limiting, renaming, inviting, banning, and claiming ownership.
- **Autorole System**: Configurable automatic role assignment with support for multiple roles per category and a clear setup/clear process.
- **Premium System**: Guild-based premium access management with expiry tracking and owner commands for administration.
- **Bot Mention Response System**: Provides interactive statistics and team information when the bot is mentioned.
- **Command Positioning System**: Ensures logical ordering of commands in the help menu across all cogs for improved navigation.
- **Advanced Automod System**: Comprehensive automoderation with antispam, antilink protection, and advanced configuration options. Features interactive setup panels, domain management, whitelist system, and customizable punishments with strike tracking.

### UI Components
Utilizes Discord UI components such as interactive views, modal forms for input, button controls for quick actions, and embed previews for real-time visualization.

## External Dependencies

### Core Dependencies
- **discord.py**: Primary Discord API wrapper.
- **aiosqlite**: Asynchronous SQLite database operations.
- **asyncio**: For asynchronous programming.

### Discord API Integration
- Requires specific bot permissions (manage roles, send messages, embed links).
- Utilizes message content, member, and presence intents.
- Designed to support hybrid commands (traditional and application commands).

### Database
- **SQLite**: Local file-based database storage (`database/bot.db`).
- Self-contained, without external database dependencies.
- Database schema designed for future migrations and updates.

### Environment Variables
- **BOT_TOKEN**: Discord bot token for authentication.
- All sensitive data managed through environment variables.
- Supports separate configurations for development and production environments.